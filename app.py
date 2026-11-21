import html
from concurrent.futures import ThreadPoolExecutor

import streamlit as st
import httpx
from google.genai.errors import APIError

from jobs import jobs, job_locations
from matching import match_breakdown
from ai_helper import generate_response


def _unique_terms(terms):
    unique_terms = {}
    for term in terms:
        if not isinstance(term, str):
            continue

        term = term.strip()
        if term:
            unique_terms.setdefault(term.casefold(), term)

    return sorted(unique_terms.values(), key=str.casefold)


CUSTOM_CSS = """
<style>
.block-container { max-width: 900px; padding-top: 2rem; }
.hero {
    background: linear-gradient(135deg, #0f2a4a 0%, #1d4f7c 100%);
    border-radius: 12px; padding: 22px 32px; margin-bottom: 1.5rem; color: #ffffff;
}
.hero h1 { margin: 0; padding: 0; line-height: 1.2; font-size: 1.9rem; font-weight: 700; color: #ffffff; }
.hero p { margin: 4px 0 0; color: #cbd9ea; }
.chip {
    display: inline-block; padding: 2px 11px; margin: 2px 6px 2px 0;
    border-radius: 6px; font-size: .82rem; font-weight: 500; border: 1px solid transparent;
}
.chip-ok { background: rgba(22,163,74,.12); color: #15803d; border-color: rgba(22,163,74,.35); }
.chip-interest { background: rgba(37,99,235,.12); color: #1d4ed8; border-color: rgba(37,99,235,.35); }
.chip-miss { background: rgba(220,38,38,.10); color: #b91c1c; border-color: rgba(220,38,38,.30); }
.chip-none { background: rgba(100,116,139,.12); color: #64748b; border-color: rgba(100,116,139,.25); }
[data-testid="stBaseButton-primary"] {
    background: #0f2a4a; color: #ffffff; border: 1px solid #0f2a4a;
    border-radius: 8px; font-weight: 600; padding: .6rem 1rem;
    transition: background .15s ease, box-shadow .15s ease;
}
[data-testid="stBaseButton-primary"]:hover {
    background: #1d4f7c; border-color: #1d4f7c; color: #ffffff;
    box-shadow: 0 2px 8px rgba(15,42,74,.25);
}
[data-testid="stBaseButton-primary"]:focus:not(:active) { color: #ffffff; border-color: #1d4f7c; }
[data-testid="stBaseButton-primary"]:active { background: #0b1f38; color: #ffffff; }
[data-baseweb="tag"] { background: #e2e8f0 !important; border-radius: 6px !important; }
[data-baseweb="tag"] span { color: #1e293b !important; }
.job-meta { color: #64748b; margin: 0 0 .5rem; }
.score { font-size: 2rem; font-weight: 700; text-align: right; line-height: 1; }
.score small { display: block; font-size: .75rem; font-weight: 400; color: #64748b; }
</style>
"""


def _chips(terms, css_class):
    if not terms:
        return '<span class="chip chip-none">None</span>'

    return "".join(
        f'<span class="chip {css_class}">{html.escape(term)}</span>'
        for term in terms
    )


def print_job_result(job, breakdown):
    score = breakdown["score"]
    score_color = "#15803d" if score >= 70 else "#b45309" if score >= 40 else "#b91c1c"
    title_col, score_col = st.columns([4, 1])
    with title_col:
        st.markdown(f"### {html.escape(job['title'])}")
        st.markdown(
            f'<p class="job-meta">🏢 {html.escape(str(job.get("company", "Not specified")))}'
            f' &nbsp;·&nbsp; 📍 {html.escape(", ".join(job_locations(job)) or "Not specified")}</p>',
            unsafe_allow_html=True,
        )
    with score_col:
        st.markdown(
            f'<div class="score" style="color:{score_color}">{score}%'
            f"<small>Match Score</small></div>",
            unsafe_allow_html=True,
        )
    st.progress(score / 100)

    st.markdown(
        f"✅ **Matched Skills** &nbsp; {_chips(breakdown['matched_skills'], 'chip-ok')}",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"💡 **Matched Interests** &nbsp; {_chips(breakdown['matched_interests'], 'chip-interest')}",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"⚠️ **Missing Skills** &nbsp; {_chips(breakdown['missing_skills'], 'chip-miss')}",
        unsafe_allow_html=True,
    )


def get_ai_analysis(job, breakdown, interests):
    prompt = f"""
Student matching skills:
{', '.join(breakdown['matched_skills']) or 'None'}

Student interests matching job interests:
{', '.join(breakdown['matched_interests']) or 'None'}

Match skills only to required skills, and interests only to job interests.

Missing required skills:
{', '.join(breakdown['missing_skills']) or 'None'}

Student interests:
{', '.join(interests) or 'None'}

Job title:
{job['title']}

Required skills:
{', '.join(job['skills'])}

Job interests:
{', '.join(job.get('interests', [])) or 'None'}

Respond in exactly two lines:

Why Match:
<one short sentence explaining why this job is a good match>

Learn:
<a comma-separated list of the most important missing skills to improve chances of getting the job>

Keep the response concise.
"""

    return generate_response(prompt)


def _ai_error_message(error):
    if isinstance(error, RuntimeError):
        detail = (
            "GEMINI_API_KEY is not set. Add it to the PyCharm run configuration "
            "environment variables, then restart the app."
        )
    elif isinstance(error, APIError):
        if error.code in (401, 403):
            detail = "Gemini rejected the API key or it lacks permission. Check the key and its API access."
        elif error.code == 404:
            detail = "Gemini could not find the configured model. Check GEMINI_MODEL and model access."
        elif error.code == 429:
            detail = "The Gemini quota or rate limit was reached. Check the project quota and try again later."
        elif error.code is not None and error.code >= 500:
            detail = "The Gemini service is temporarily unavailable. Try again later."
        else:
            detail = "Gemini rejected the request. Check the model setting and API key permissions."
    elif isinstance(error, httpx.HTTPError):
        detail = "A network error prevented a connection to Gemini. Check your connection and try again."
    else:
        detail = "An unexpected error occurred. Verify your Gemini settings and try again."

    return f"AI analysis is unavailable: {detail} Local job results are still shown."


st.set_page_config(page_title="AI Job Search Agent", page_icon="💼", layout="centered")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.markdown(
    '<div class="hero"><h1>💼 AI Job Search Agent</h1>'
    "<p>Pick your location, skills and interests to find your best-matching jobs.</p></div>",
    unsafe_allow_html=True,
)
st.caption("Illustrative sample data only — these are not current or verified job vacancies.")

def _collapse_search_form():
    if st.session_state.get("location_selection") and st.session_state.get("skill_selection"):
        st.session_state["search_form_collapsed"] = True


with st.expander(
    "🔎 Search filters",
    expanded=not st.session_state.get("search_form_collapsed", False),
):
    name_col, location_col = st.columns(2)
    with name_col:
        name = st.text_input("What's your name?", placeholder="e.g. Sam") or ""
    locations = _unique_terms(
        location for job in jobs for location in job_locations(job)
    )
    with location_col:
        selected_location = st.selectbox(
            "Location",
            locations,
            index=None,
            placeholder="Select a location",
            key="location_selection",
        )
    location_jobs = [job for job in jobs if selected_location in job_locations(job)]

    skill_options = _unique_terms(
        skill
        for job in location_jobs
        for skill in job.get("skills", [])
    )
    st.session_state["skill_selection"] = [
        skill
        for skill in st.session_state.get("skill_selection", [])
        if skill in skill_options
    ]
    selected_skills = st.multiselect(
        "Skills",
        skill_options,
        key="skill_selection",
        disabled=selected_location is None or not skill_options,
    )

    selected_skill_keys = {skill.casefold() for skill in selected_skills}
    interest_options = _unique_terms(
        interest
        for job in location_jobs
        if selected_skill_keys.intersection(
            skill.casefold()
            for skill in job.get("skills", [])
            if isinstance(skill, str)
        )
        for interest in job.get("interests", [])
    )
    st.session_state["interest_selection"] = [
        interest
        for interest in st.session_state.get("interest_selection", [])
        if interest in interest_options
    ]
    selected_interests = st.multiselect(
        "Interests",
        interest_options,
        key="interest_selection",
        disabled=not selected_skills or not interest_options,
    )

    search_clicked = st.button(
        "🔍 Find Matching Jobs",
        type="primary",
        use_container_width=True,
        on_click=_collapse_search_form,
    )

if search_clicked:
    if selected_location is None:
        st.warning("Please select a location to find matching jobs.")
    elif not selected_skills:
        st.warning("Please select at least one skill to find matching jobs.")
    else:
        st.success(f"Hello {name.strip()}!" if name.strip() else "Hello!")
        results = []

        for job in location_jobs:
            breakdown = match_breakdown(
                selected_skills,
                job["skills"],
                selected_interests,
                job.get("interests", []),
            )
            if breakdown["score"] == 0:
                continue

            results.append({
                "job": job,
                "score": breakdown["score"],
                "breakdown": breakdown,
            })

        results.sort(key=lambda result: result["score"], reverse=True)

        if not results:
            st.info("No matching jobs found. Try changing your skills or location.")
        else:
            top_results = results[:3]

            def _analyze(result):
                try:
                    return get_ai_analysis(
                        result["job"],
                        result["breakdown"],
                        selected_interests,
                    ), None
                except Exception as error:
                    return None, error

            with st.spinner("Analyzing matches with AI..."):
                with ThreadPoolExecutor(max_workers=len(top_results)) as executor:
                    analyses = list(executor.map(_analyze, top_results))

            st.subheader(f"Top {len(top_results)} matches")
            for result, (analysis, error) in zip(top_results, analyses):
                job = result["job"]
                with st.container(border=True):
                    print_job_result(job, result["breakdown"])

                    st.markdown("**🤖 AI Analysis**")
                    if error is not None:
                        st.warning(_ai_error_message(error))
                    else:
                        st.info(analysis or "AI analysis did not return a response.")
