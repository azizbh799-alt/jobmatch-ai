import math
import re

from .ai import embed, explain_match


def normalize(values):
    return {re.sub(r"[^a-z0-9+#.]+", " ", str(v).lower()).strip() for v in values}


def keyword_score(candidate, job) -> tuple[float, list[str]]:
    candidate_skills = normalize(candidate.skills)
    job_skills = normalize(job.skills)
    if not job_skills:
        return 100.0, []
    matched = candidate_skills & job_skills
    missing = sorted(job_skills - candidate_skills)
    return (len(matched) / len(job_skills)) * 100, missing


def cosine(a, b):
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if not na or not nb:
        return 0.0
    return max(0.0, min(100.0, ((dot / (na * nb)) + 1) * 50))


def experience_score(candidate, job):
    required = float(job.min_experience_years or 0)
    actual = float(candidate.experience_years or 0)
    if required <= 0:
        return 100.0
    return min(100.0, (actual / required) * 100)


def location_score(candidate, job):
    if job.remote and candidate.remote_preference:
        return 100.0
    preferred = normalize(candidate.preferred_countries)
    country = str(job.country or "").lower()
    if preferred and country and country in preferred:
        return 100.0
    if str(candidate.location or "").lower() in str(job.location or "").lower():
        return 80.0
    return 35.0


def calculate_match(candidate, job):
    keyword, missing = keyword_score(candidate, job)

    candidate_text = " ".join(candidate.skills) + " " + candidate.cv_text
    job_text = " ".join(job.skills) + " " + job.description
    semantic = cosine(embed(candidate_text), embed(job_text))

    experience = experience_score(candidate, job)
    location = location_score(candidate, job)

    score = (
        keyword * 0.40
        + semantic * 0.35
        + experience * 0.15
        + location * 0.10
    )

    explanation = explain_match(candidate, job, score, missing)
    return score, keyword, semantic, experience, location, missing, explanation
