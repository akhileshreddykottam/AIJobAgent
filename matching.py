def _normalize_skills(skills):
    normalized = []
    seen = set()

    for skill in skills:
        if not isinstance(skill, str):
            continue

        skill = skill.strip().casefold()
        if skill and skill not in seen:
            normalized.append(skill)
            seen.add(skill)

    return normalized


def matched_skills(user_skills, job_skills):
    user_skill_set = set(_normalize_skills(user_skills))
    return [
        skill
        for skill in _normalize_skills(job_skills)
        if skill in user_skill_set
    ]


def missing_skills(user_skills, job_skills):
    user_skill_set = set(_normalize_skills(user_skills))
    return [
        skill
        for skill in _normalize_skills(job_skills)
        if skill not in user_skill_set
    ]


def match_breakdown(user_skills, job_skills, user_interests=(), job_interests=()):
    normalized_user_skills = _normalize_skills(user_skills)
    normalized_job_skills = _normalize_skills(job_skills)
    normalized_user_interests = _normalize_skills(user_interests)
    normalized_job_interests = _normalize_skills(job_interests)

    user_skill_set = set(normalized_user_skills)
    job_skill_set = set(normalized_job_skills)
    user_interest_set = set(normalized_user_interests)
    job_interest_set = set(normalized_job_interests)

    job_terms = _normalize_skills(normalized_job_skills + normalized_job_interests)
    matched_terms = {
        term
        for term in job_terms
        if (term in job_skill_set and term in user_skill_set)
        or (term in job_interest_set and term in user_interest_set)
    }

    score = round(len(matched_terms) / len(job_terms) * 100) if job_terms else 0

    return {
        "score": score,
        "matched_skills": [skill for skill in normalized_job_skills if skill in user_skill_set],
        "matched_interests": [
            interest
            for interest in normalized_job_interests
            if interest in user_interest_set
        ],
        "missing_skills": missing_skills(normalized_user_skills, normalized_job_skills),
    }


def calculate_match(user_skills, job_skills, user_interests=(), job_interests=()):
    return match_breakdown(
        user_skills,
        job_skills,
        user_interests,
        job_interests,
    )["score"]
