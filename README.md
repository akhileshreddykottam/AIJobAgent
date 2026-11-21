# AI Job Search Agent

This Streamlit app ranks the illustrative sample jobs in `jobs.py` by matching your skills only against job skills and your interests only against job interests. Cross-category matches do not contribute to scores or appear in results. Choose a catalog location, then select skills available at that location; the interests dropdown is limited to jobs at that location that share at least one selected skill. Each result explains matched skills, matched interests, and missing skills, followed by an optional Gemini-generated analysis.

The catalog is for demonstration only; it is not a source of current or verified job vacancies. Newly added sample employers are fictional.

## Job catalog

The catalog is a Python list, not a live database. To add an illustrative listing, append a dictionary to `jobs` in `jobs.py` with a `title`, `company`, `location`, a nonempty `skills` list, and a nonempty `interests` list. Keep the terms concise so users can search for them as comma-separated entries. Use fictional employers and do not present sample records as real openings.

Choose a location and at least one skill before searching; selecting interests is optional. The location, skills, and interests are catalog-backed dropdown selections, and changing a location or skill clears any now-unavailable dependent choices. A job's unique skill and interest terms form the score denominator; only exact same-category matches count. Duplicate terms are counted once, and a term shared by both job categories receives credit only when directly selected in its corresponding user category.

## Setup

Install the app dependencies in your project environment:

```powershell
pip install streamlit google-genai
```

Set the `GEMINI_API_KEY` environment variable before starting the app. In PyCharm, open **Run → Edit Configurations**, choose the configuration that runs Streamlit, and add `GEMINI_API_KEY` with your key under **Environment variables**. Restart the app after changing the value; a running Streamlit process does not receive environment changes made afterward.

To run from a PowerShell terminal instead, set the key before launching Streamlit:

```powershell
$env:GEMINI_API_KEY = "your-api-key"
streamlit run app.py
```

The model defaults to `gemini-3.5-flash-lite`. To select another model, set `GEMINI_MODEL` in the run configuration or shell before launching the app. If AI analysis fails, the app provides a safe diagnostic for missing configuration, API-key access, model availability, quota, or network errors without displaying provider error details; local job matches remain visible.

AI analysis is optional: local job matching still works if the API key is missing or Gemini is temporarily unavailable.

## Credential safety

Never commit API keys to source control. A key was previously embedded in the project source; revoke or rotate that exposed credential in the provider console, then configure a new key through `GEMINI_API_KEY`. The app has no hard-coded fallback key.

## Tests

Run the unit and Streamlit interaction tests with:

```powershell
python -m unittest discover -s tests
```