
from pathlib import Path
from typing import Annotated
import httpx
import io

import redis
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pypdf import PdfReader
from sqlalchemy.orm import Session

from .ai import analyze_cv, embed
from .config import settings
from .db import Base, engine, get_db
from .matching import calculate_match
from .models import Candidate, Job, Match
from .schemas import (
    CandidateCreate,
    CandidateOut,
    JobCreate,
    JobOut,
    MatchOut,
    MatchRequest,
    SearchRequest,
)
from .seed import seed_jobs


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="JobMatch AI / MatchTN",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

origins = [
    x.strip()
    for x in settings.cors_origins.split(",")
    if x.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REDIS
# ============================================================

redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True
)


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup():

    Base.metadata.create_all(bind=engine)

    db = next(get_db())

    try:
        seed_jobs(db)
    finally:
        db.close()


# ============================================================
# RATE LIMITING
# ============================================================

@app.middleware("http")
async def rate_limit(request, call_next):

    if not request.url.path.startswith("/api/"):
        return await call_next(request)

    try:

        key = (
            f"rate:"
            f"{request.client.host if request.client else 'unknown'}"
        )

        count = redis_client.incr(key)

        if count == 1:
            redis_client.expire(
                key,
                60
            )

        if count > settings.rate_limit_per_minute:

            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

    except HTTPException:
        raise

    except Exception:
        # Keep local development available
        # if Redis is temporarily unavailable.
        pass

    return await call_next(request)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/healthz")
def healthz():

    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
        "llm_provider": settings.llm_provider,
    }


# ============================================================
# READINESS CHECK
# ============================================================

@app.get("/readyz")
def readyz(
    db: Session = Depends(get_db)
):

    db.execute(
        __import__("sqlalchemy").text("SELECT 1")
    )

    return {
        "status": "ready"
    }


# ============================================================
# API KEY AUTHENTICATION
# ============================================================

def require_api_key(
    x_api_key: Annotated[str | None, Header()] = None
):

    if x_api_key != settings.app_api_key:

        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )


# ============================================================
# CANDIDATES
# ============================================================

@app.post(
    "/api/v1/candidates",
    response_model=CandidateOut,
    dependencies=[Depends(require_api_key)]
)
def create_candidate(
    payload: CandidateCreate,
    db: Session = Depends(get_db)
):

    candidate = Candidate(
        **payload.model_dump()
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


@app.get(
    "/api/v1/candidates",
    response_model=list[CandidateOut],
    dependencies=[Depends(require_api_key)]
)
def list_candidates(
    db: Session = Depends(get_db)
):

    return (
        db.query(Candidate)
        .order_by(Candidate.id.desc())
        .all()
    )


# ============================================================
# UPLOAD CV
#
# Public endpoint for portfolio frontend.
# No API key required.
# ============================================================

@app.post(
    "/api/v1/candidates/upload-cv",
    response_model=CandidateOut
)
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # Validate file extension
    # --------------------------------------------------------

    if (
        not file.filename
        or not file.filename.lower().endswith(".pdf")
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF CV files are supported."
        )

    # --------------------------------------------------------
    # Read file
    # --------------------------------------------------------

    content = await file.read()

    # --------------------------------------------------------
    # Validate size
    # --------------------------------------------------------

    if len(content) > 8 * 1024 * 1024:

        raise HTTPException(
            status_code=413,
            detail="CV must be smaller than 8 MB."
        )

    # --------------------------------------------------------
    # Extract PDF text
    # --------------------------------------------------------

    try:

        reader = PdfReader(
            io.BytesIO(content)
        )

        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        ).strip()

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=f"Unable to read PDF: {exc}"
        ) from exc

    if not text:

        raise HTTPException(
            status_code=400,
            detail="No readable text found in the PDF."
        )

    # --------------------------------------------------------
    # Analyze CV
    # --------------------------------------------------------

    try:

        profile = analyze_cv(text)

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"CV analysis failed: {exc}"
        ) from exc

    # --------------------------------------------------------
    # Candidate identity
    # --------------------------------------------------------

    name = (
        profile.get("name")
        or Path(file.filename).stem
    )

    email = (
        f"cv-"
        f"{abs(hash(file.filename + text[:100]))}"
        f"@local.jobmatch"
    )

    # --------------------------------------------------------
    # Avoid duplicate demo uploads
    # --------------------------------------------------------

    existing = (
        db.query(Candidate)
        .filter(Candidate.email == email)
        .first()
    )

    if existing:

        candidate = existing

        candidate.name = name

        candidate.title = profile.get(
            "title",
            ""
        )

        candidate.location = profile.get(
            "location",
            ""
        )

        candidate.skills = profile.get(
            "skills",
            []
        )

        candidate.experience_years = float(
            profile.get(
                "experience_years"
            ) or 0
        )

        candidate.education = profile.get(
            "education",
            ""
        )

        candidate.languages = profile.get(
            "languages",
            []
        )

        candidate.preferred_countries = profile.get(
            "preferred_countries",
            []
        )

        candidate.cv_filename = file.filename

        candidate.cv_text = text

    else:

        candidate = Candidate(

            name=name,

            email=email,

            title=profile.get(
                "title",
                ""
            ),

            location=profile.get(
                "location",
                ""
            ),

            skills=profile.get(
                "skills",
                []
            ),

            experience_years=float(
                profile.get(
                    "experience_years"
                ) or 0
            ),

            education=profile.get(
                "education",
                ""
            ),

            languages=profile.get(
                "languages",
                []
            ),

            preferred_countries=profile.get(
                "preferred_countries",
                []
            ),

            remote_preference=True,

            cv_filename=file.filename,

            cv_text=text,
        )

        db.add(candidate)

    # --------------------------------------------------------
    # Generate embedding
    # --------------------------------------------------------

    candidate.embedding = embed(
        " ".join(candidate.skills)
        + " "
        + candidate.cv_text
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    db.commit()
    db.refresh(candidate)

    return candidate


# ============================================================
# JOBS
# ============================================================

@app.post(
    "/api/v1/jobs",
    response_model=JobOut,
    dependencies=[Depends(require_api_key)]
)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db)
):

    job = Job(
        **payload.model_dump()
    )

    job.embedding = embed(
        " ".join(job.skills)
        + " "
        + job.description
    )

    db.add(job)

    db.commit()

    db.refresh(job)

    return job


@app.get(
    "/api/v1/jobs",
    response_model=list[JobOut],
    dependencies=[Depends(require_api_key)]
)
def list_jobs(
    db: Session = Depends(get_db)
):

    return (
        db.query(Job)
        .order_by(Job.id.desc())
        .all()
    )


# ============================================================
# CREATE MATCH
# ============================================================

@app.post(
    "/api/v1/matches",
    response_model=MatchOut,
    dependencies=[Depends(require_api_key)]
)
def create_match(
    payload: MatchRequest,
    db: Session = Depends(get_db)
):

    candidate = db.get(
        Candidate,
        payload.candidate_id
    )

    job = db.get(
        Job,
        payload.job_id
    )

    if not candidate or not job:

        raise HTTPException(
            status_code=404,
            detail="Candidate or job not found"
        )

    try:

        (
            score,
            keyword,
            semantic,
            experience,
            location,
            missing,
            explanation,
        ) = calculate_match(
            candidate,
            job
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Matching failed: {exc}"
        ) from exc

    match = Match(

        candidate_id=candidate.id,

        job_id=job.id,

        score=score,

        keyword_score=keyword,

        semantic_score=semantic,

        experience_score=experience,

        location_score=location,

        missing_skills=missing,

        explanation=explanation,
    )

    db.add(match)

    db.commit()

    db.refresh(match)

    return match


# ============================================================
# EXTRACT SKILLS FROM JOB
# ============================================================

def extract_job_skills(
    text: str
) -> list[str]:

    lower = text.lower()

    skill_catalog = [

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

        "machine learning",
        "devops",
        "devsecops",
        "cloud",

        "rest api",
    ]

    return [
        skill
        for skill in skill_catalog
        if skill in lower
    ]


# ============================================================
# ADZUNA SEARCH
# ============================================================

async def fetch_adzuna_jobs(
    candidate,
    payload
):

    # --------------------------------------------------------
    # Check Adzuna credentials
    # --------------------------------------------------------

    if (
        not settings.adzuna_app_id
        or not settings.adzuna_app_key
    ):

        raise HTTPException(
            status_code=500,
            detail="Adzuna API credentials are not configured."
        )

    # --------------------------------------------------------
    # Search query
    # --------------------------------------------------------

    what = (
        candidate.title
        or "software developer"
    )

    # --------------------------------------------------------
    # Supported Adzuna countries
    # --------------------------------------------------------

    country_map = {
        "france": "fr",
        "switzerland": "ch",
        "germany": "de",
        "canada": "ca",
        "united kingdom": "gb",
        "uk": "gb",
    }

    # --------------------------------------------------------
    # Requested countries
    # --------------------------------------------------------

    requested_countries = (
        payload.countries
        or candidate.preferred_countries
    )

    if not requested_countries:

        requested_countries = [
            "france"
        ]

    results = []

    # --------------------------------------------------------
    # Adzuna requests
    # --------------------------------------------------------

    async with httpx.AsyncClient(
        timeout=20.0
    ) as client:

        for country in requested_countries:

            country_name = country.strip()

            country_lower = country_name.lower()

            # ------------------------------------------------
            # Tunisia is currently skipped because
            # Adzuna /jobs/tn returns 404.
            # ------------------------------------------------

            if country_lower == "tunisia":

                continue

            # ------------------------------------------------
            # Remote uses France endpoint
            # ------------------------------------------------

            if country_lower == "remote":

                country_code = "fr"

            else:

                country_code = country_map.get(
                    country_lower
                )

            # ------------------------------------------------
            # Unsupported country
            # ------------------------------------------------

            if not country_code:

                print(
                    f"Adzuna country not supported: "
                    f"{country_name}"
                )

                continue

            # ------------------------------------------------
            # Request parameters
            # ------------------------------------------------

            params = {

                "app_id":
                    settings.adzuna_app_id,

                "app_key":
                    settings.adzuna_app_key,

                "results_per_page":
                    min(payload.limit, 30),

                "what":
                    what,

                "content-type":
                    "application/json",

            }

            # ------------------------------------------------
            # Location
            # ------------------------------------------------

            if country_lower != "remote":

                params["where"] = country_name

            # ------------------------------------------------
            # Remote search
            # ------------------------------------------------

            if (
                payload.remote_only
                or country_lower == "remote"
            ):

                params["what"] = (
                    f"{what} remote"
                )

            # ------------------------------------------------
            # Adzuna URL
            # ------------------------------------------------

            url = (
                "https://api.adzuna.com/v1/api/jobs/"
                f"{country_code}/search/1"
            )

            # ------------------------------------------------
            # API request
            # ------------------------------------------------

            try:

                response = await client.get(
                    url,
                    params=params
                )

                response.raise_for_status()

                data = response.json()

                # --------------------------------------------
                # Keep requested country
                # --------------------------------------------

                for item in data.get(
                    "results",
                    []
                ):

                    item["_country"] = (
                        country_name
                    )

                results.extend(
                    data.get(
                        "results",
                        []
                    )
                )

            # ------------------------------------------------
            # Do not stop the complete search if one country
            # fails.
            # ------------------------------------------------

            except httpx.HTTPError as exc:

                print(
                    f"Adzuna unavailable for "
                    f"{country_name}: {exc}"
                )

                continue

    return {

        "count": len(results),

        "results": results,

    }


# ============================================================
# SEARCH + MATCHING
#
# Public endpoint for portfolio frontend.
# No API key required.
# ============================================================

@app.post(
    "/api/v1/search",
    response_model=list[MatchOut]
)
async def search_opportunities(
    payload: SearchRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Find candidate
    # --------------------------------------------------------

    candidate = db.get(
        Candidate,
        payload.candidate_id
    )

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    # --------------------------------------------------------
    # Search Adzuna
    # --------------------------------------------------------

    data = await fetch_adzuna_jobs(
        candidate,
        payload
    )

    results = []

    # --------------------------------------------------------
    # Convert Adzuna jobs to our Job model
    # --------------------------------------------------------

    for item in data.get(
        "results",
        []
    ):

        company = item.get(
            "company",
            {}
        )

        location = item.get(
            "location",
            {}
        )

        job_title = (
            item.get("title")
            or "Unknown position"
        )

        company_name = (
            company.get(
                "display_name",
                "Unknown company"
            )
        )

        location_name = (
            location.get(
                "display_name",
                ""
            )
        )

        description = (
            item.get(
                "description",
                ""
            )
        )

        job_url = (
            item.get(
                "redirect_url",
                ""
            )
        )

        # ----------------------------------------------------
        # Avoid duplicate Adzuna jobs
        # ----------------------------------------------------

        existing_job = (

            db.query(Job)

            .filter(
                Job.url == job_url
            )

            .first()

        )

        if existing_job:

            job = existing_job

        else:

            job = Job(

                title=job_title,

                company=company_name,

                location=location_name,

                country=item.get(
                    "_country",
                    ""
                ),

                description=description,

                skills=extract_job_skills(
                    f"{job_title} {description}"
                ),

                min_experience_years=0,

                remote=False,

                employment_type="Full-time",

                salary_min=item.get(
                    "salary_min"
                ),

                salary_max=item.get(
                    "salary_max"
                ),

                currency="EUR",

                url=job_url,

                source="adzuna",
            )

            # ------------------------------------------------
            # Generate job embedding
            # ------------------------------------------------

            job.embedding = embed(
                f"{job.title} "
                f"{job.description}"
            )

            db.add(job)

            db.flush()

        # ----------------------------------------------------
        # Calculate candidate/job match
        # ----------------------------------------------------

        (
            score,
            keyword,
            semantic,
            experience,
            location_score,
            missing,
            explanation,
        ) = calculate_match(
            candidate,
            job
        )

        # ----------------------------------------------------
        # Create Match
        # ----------------------------------------------------

        match = Match(

            candidate_id=candidate.id,

            job_id=job.id,

            score=score,

            keyword_score=keyword,

            semantic_score=semantic,

            experience_score=experience,

            location_score=location_score,

            missing_skills=missing,

            explanation=explanation,

        )

        db.add(match)

        db.flush()

        results.append(match)

    # --------------------------------------------------------
    # Commit
    # --------------------------------------------------------

    db.commit()

    # --------------------------------------------------------
    # Return best matches first
    # --------------------------------------------------------

    return sorted(
        results,
        key=lambda x: x.score,
        reverse=True
    )


# ============================================================
# GET CANDIDATE
# ============================================================

@app.get(
    "/api/v1/candidates/{candidate_id}",
    response_model=CandidateOut,
    dependencies=[Depends(require_api_key)]
)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    candidate = db.get(
        Candidate,
        candidate_id
    )

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate


# ============================================================
# GET JOB
#
# Public because the portfolio frontend requests job details
# after the public search endpoint.
# ============================================================

@app.get(
    "/api/v1/jobs/{job_id}",
    response_model=JobOut
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.get(
        Job,
        job_id
    )

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


# ============================================================
# GET CANDIDATE MATCHES
# ============================================================

@app.get(
    "/api/v1/matches/candidate/{candidate_id}",
    response_model=list[MatchOut],
    dependencies=[Depends(require_api_key)]
)
def candidate_matches(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(Match)
        .filter(
            Match.candidate_id == candidate_id
        )
        .order_by(
            Match.score.desc()
        )
        .all()
    )


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
def root():

    return FileResponse(
        "static/index.html"
    )
