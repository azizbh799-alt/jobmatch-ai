from pydantic import BaseModel, EmailStr, Field


class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    title: str = ""
    location: str = ""
    skills: list[str] = Field(default_factory=list)
    experience_years: float = 0
    education: str = ""
    languages: list[str] = Field(default_factory=list)
    preferred_countries: list[str] = Field(default_factory=list)
    remote_preference: bool = True


class CandidateOut(CandidateCreate):
    id: int
    cv_filename: str = ""


class JobCreate(BaseModel):
    title: str
    company: str
    location: str = ""
    country: str = ""
    description: str = ""
    skills: list[str] = Field(default_factory=list)
    min_experience_years: float = 0
    remote: bool = False
    employment_type: str = "Full-time"
    salary_min: int | None = None
    salary_max: int | None = None
    currency: str = "EUR"
    url: str = ""
    source: str = "demo"


class JobOut(JobCreate):
    id: int


class MatchRequest(BaseModel):
    candidate_id: int
    job_id: int


class MatchOut(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    score: float
    keyword_score: float
    semantic_score: float
    experience_score: float
    location_score: float
    missing_skills: list[str]
    explanation: str


class SearchRequest(BaseModel):
    candidate_id: int
    countries: list[str] = Field(default_factory=list)
    remote_only: bool = False
    limit: int = 10
