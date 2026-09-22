import hashlib
import math
from typing import Any

from openai import OpenAI

from .config import settings


def _mock_embedding(text: str, dimensions: int = 1536) -> list[float]:
    # Deterministic, dependency-free development embedding.
    values = []
    seed = text.lower().encode("utf-8")

    for i in range(dimensions):
        digest = hashlib.sha256(
            seed + i.to_bytes(4, "little")
        ).digest()

        values.append(
            (int.from_bytes(digest[:4], "little") / 2**32) * 2 - 1
        )

    norm = math.sqrt(sum(v * v for v in values)) or 1

    return [v / norm for v in values]


def embed(text: str) -> list[float]:
    """
    Generate an embedding for the given text.

    In mock mode, a deterministic local embedding is generated.
    In OpenAI mode, OpenAI embeddings are used.
    """

    if settings.llm_provider.lower() != "openai":
        return _mock_embedding(text)

    if not settings.openai_api_key:
        raise RuntimeError(
            "LLM_PROVIDER=openai but OPENAI_API_KEY is empty."
        )

    client = OpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )

    response = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=text[:12000],
    )

    return response.data[0].embedding


def analyze_cv(text: str) -> dict[str, Any]:
    """
    Analyze a CV and return a structured candidate profile.

    Mock mode:
        Uses heuristic_cv_analysis().

    OpenAI mode:
        Uses an LLM to extract structured CV information.
    """

    if settings.llm_provider.lower() != "openai":
        return heuristic_cv_analysis(text)

    if not settings.openai_api_key:
        raise RuntimeError(
            "LLM_PROVIDER=openai but OPENAI_API_KEY is empty."
        )

    client = OpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )

    prompt = f"""
Extract a candidate profile from this CV.

Return ONLY valid JSON with these keys:
name,
title,
location,
skills,
experience_years,
education,
languages,
preferred_countries.

Rules:
- skills and languages must be arrays.
- preferred_countries must be an array.
- experience_years must be a number.
- Do not invent information.
- If information is unknown, use an empty string, empty array, or 0.
- Detect the candidate's actual professional title.
- The candidate may work in IT, finance, accounting, marketing,
  human resources, engineering, management, healthcare, or another field.

CV:
{text[:16000]}
"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract structured CV data accurately. "
                    "Always identify the actual professional domain "
                    "and job title from the CV."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    import json

    return json.loads(
        response.choices[0].message.content
    )


def explain_match(
    candidate: Any,
    job: Any,
    score: float,
    missing: list[str],
) -> str:
    """
    Explain why a candidate matches a job.
    """

    if settings.llm_provider.lower() != "openai":
        if missing:
            return (
                f"Overall compatibility is {score:.0f}%. "
                "The profile matches several required skills, "
                f"but is missing: {', '.join(missing)}."
            )

        return (
            f"Overall compatibility is {score:.0f}%. "
            "The candidate's skills and experience align well "
            "with this opportunity."
        )

    if not settings.openai_api_key:
        return (
            f"Compatibility is {score:.0f}%. "
            f"Missing skills: {', '.join(missing) or 'none'}."
        )

    client = OpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )

    prompt = f"""
Explain this job match in 3 concise sentences.

Candidate skills:
{candidate.skills}

Candidate experience:
{candidate.experience_years}

Job title:
{job.title}

Job skills:
{job.skills}

Job location:
{job.location}, {job.country}

Score:
{score:.0f}%

Missing skills:
{missing}
"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You explain candidate-job compatibility "
                    "objectively."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content.strip()


def heuristic_cv_analysis(text: str) -> dict[str, Any]:
    """
    Local CV parser used when LLM_PROVIDER=mock.

    This parser supports multiple professional domains,
    not only IT.
    """

    import re

    lower = text.lower()

    # =========================================================
    # Skills
    # =========================================================

    skill_catalog = [
        # -------------------------
        # IT
        # -------------------------
        "python",
        "fastapi",
        "django",
        "java",
        "spring boot",
        "javascript",
        "typescript",
        "angular",
        "react",
        "node.js",
        "php",
        "c#",
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "docker",
        "kubernetes",
        "terraform",
        "aws",
        "azure",
        "gcp",
        "linux",
        "ansible",
        "jenkins",
        "gitlab",
        "github actions",
        "git",
        "redis",
        "prometheus",
        "grafana",
        "openai",
        "machine learning",
        "devops",
        "devsecops",
        "cloud",
        "rest api",

        # -------------------------
        # Accounting / Finance
        # -------------------------
        "comptabilité",
        "comptable",
        "accounting",
        "accountant",
        "audit",
        "auditing",
        "fiscalité",
        "fiscalite",
        "taxation",
        "finance",
        "financial analysis",
        "financial reporting",
        "ifrs",
        "gaap",
        "tva",
        "vat",
        "excel",
        "microsoft excel",
        "sage",
        "sap",
        "oracle financials",
        "quickbooks",
        "budgeting",
        "financial management",
        "cost accounting",
        "management accounting",

        # -------------------------
        # Business
        # -------------------------
        "business analysis",
        "business analyst",
        "business management",
        "project management",
        "project manager",

        # -------------------------
        # Human Resources
        # -------------------------
        "human resources",
        "ressources humaines",
        "recruitment",
        "recrutement",
        "talent acquisition",
        "payroll",
        "paie",

        # -------------------------
        # Marketing
        # -------------------------
        "marketing",
        "digital marketing",
        "communication",
        "social media",
        "seo",
        "sem",

        # -------------------------
        # Engineering
        # -------------------------
        "engineering",
        "mechanical engineering",
        "electrical engineering",
        "civil engineering",
        "industrial engineering",
    ]

    skills = [
        skill
        for skill in skill_catalog
        if skill in lower
    ]

    # Remove duplicate skills while preserving order
    skills = list(dict.fromkeys(skills))

    # =========================================================
    # Job Title
    # =========================================================

    title = ""

    title_candidates = [
        # -------------------------
        # Accounting / Finance
        # -------------------------
        "expert-comptable",
        "expert comptable",
        "senior accountant",
        "financial accountant",
        "accounting manager",
        "finance manager",
        "financial auditor",
        "internal auditor",
        "management accountant",
        "accountant",
        "comptable",

        # -------------------------
        # IT
        # -------------------------
        "cloud / full stack developer",
        "cloud engineer",
        "devops engineer",
        "devsecops engineer",
        "full stack developer",
        "full-stack developer",
        "software engineer",
        "software developer",
        "backend developer",
        "frontend developer",
        "web developer",
        "data engineer",
        "data scientist",
        "machine learning engineer",
        "cybersecurity engineer",
        "security engineer",
        "network engineer",
        "system administrator",
        "systems administrator",
        "developer",

        # -------------------------
        # Business
        # -------------------------
        "business analyst",
        "business manager",
        "financial analyst",
        "project manager",
        "product manager",

        # -------------------------
        # Human Resources
        # -------------------------
        "human resources manager",
        "hr manager",
        "human resources specialist",
        "hr specialist",
        "recruiter",
        "talent acquisition specialist",

        # -------------------------
        # Marketing
        # -------------------------
        "marketing manager",
        "digital marketing manager",
        "marketing specialist",
        "marketing coordinator",

        # -------------------------
        # Engineering
        # -------------------------
        "civil engineer",
        "mechanical engineer",
        "electrical engineer",
        "industrial engineer",
        "software engineer",
        "engineer",
    ]

    # Longer titles first
    title_candidates = sorted(
        title_candidates,
        key=len,
        reverse=True,
    )

    for candidate in title_candidates:
        if candidate in lower:
            title = candidate.title()
            break

    # Fallback only if no title was detected
    if not title:
        title = "IT Candidate"

    # =========================================================
    # Location
    # =========================================================

    location = ""

    locations = [
        "tunisia",
        "tunisie",
        "tunis",
        "nabeul",
        "sousse",
        "sfax",
        "monastir",
        "france",
        "paris",
        "switzerland",
        "suisse",
        "germany",
        "allemagne",
        "canada",
        "uae",
        "united arab emirates",
        "dubai",
    ]

    # Longer locations first
    locations = sorted(
        locations,
        key=len,
        reverse=True,
    )

    for loc in locations:
        if re.search(
            r"\b" + re.escape(loc) + r"\b",
            lower,
        ):
            location = loc.title()
            break

    location_map = {
        "Tunisie": "Tunisia",
        "Tunis": "Tunis, Tunisia",
        "Nabeul": "Nabeul, Tunisia",
        "Sousse": "Sousse, Tunisia",
        "Sfax": "Sfax, Tunisia",
        "Suisse": "Switzerland",
        "Allemagne": "Germany",
        "Uae": "United Arab Emirates",
    }

    location = location_map.get(
        location,
        location,
    )

    # =========================================================
    # Languages
    # =========================================================

    language_map = {
        "arabic": "Arabic",
        "arabe": "Arabic",
        "french": "French",
        "français": "French",
        "francais": "French",
        "english": "English",
        "anglais": "English",
        "german": "German",
        "allemand": "German",
        "spanish": "Spanish",
        "espagnol": "Spanish",
        "italian": "Italian",
        "italien": "Italian",
    }

    languages = []

    for keyword, language in language_map.items():
        if re.search(
            r"\b" + re.escape(keyword) + r"\b",
            lower,
        ):
            if language not in languages:
                languages.append(language)

    # =========================================================
    # Experience
    # =========================================================

    experience_years = 0

    experience_patterns = [
        # "5 years of experience"
        r"(\d+(?:[.,]\d+)?)\s*\+?\s*"
        r"(?:years?|ans?)\s+"
        r"(?:of\s+)?"
        r"(?:experience|expérience)",

        # "experience: 5 years"
        r"(?:experience|expérience)"
        r"\s*[:\-]?\s*"
        r"(\d+(?:[.,]\d+)?)\s*\+?\s*"
        r"(?:years?|ans?)",
    ]

    for pattern in experience_patterns:
        match = re.search(
            pattern,
            lower,
        )

        if match:
            experience_years = float(
                match.group(1).replace(",", ".")
            )
            break

    # =========================================================
    # Education
    # =========================================================

    education = ""

    education_keywords = [
        "master",
        "mastère",
        "mastere",
        "mba",
        "bachelor",
        "licence",
        "engineering",
        "engineer",
        "cycle ingénieur",
        "cycle d'ingénieur",
        "computer science",
        "computer engineering",
        "informatique",
        "technologies de l'informatique",
        "accounting",
        "comptabilité",
        "finance",
        "business administration",
        "management",
    ]

    for keyword in education_keywords:
        if keyword in lower:
            education = keyword.title()
            break

    # =========================================================
    # Preferred Countries
    # =========================================================

    preferred_countries = []

    country_map = {
        "france": "fr",
        "switzerland": "ch",
        "suisse": "ch",
        "germany": "de",
        "allemagne": "de",
        "canada": "ca",
        "united kingdom": "gb",
        "uk": "gb",
        "uae": "ae",
        "united arab emirates": "ae",
        "dubai": "ae",
    }

    for keyword, country in country_map.items():
        if re.search(
            r"\b" + re.escape(keyword) + r"\b",
            lower,
        ):
            if country not in preferred_countries:
                preferred_countries.append(country)

    # =========================================================
    # Result
    # =========================================================

    return {
        "name": "",
        "title": title,
        "location": location,
        "skills": skills,
        "experience_years": experience_years,
        "education": education,
        "languages": languages,
        "preferred_countries": preferred_countries,
    }