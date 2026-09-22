from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(160), default="")
    location: Mapped[str] = mapped_column(String(160), default="")
    skills: Mapped[list] = mapped_column(JSON, default=list)
    experience_years: Mapped[float] = mapped_column(Float, default=0)
    education: Mapped[str] = mapped_column(Text, default="")
    languages: Mapped[list] = mapped_column(JSON, default=list)
    preferred_countries: Mapped[list] = mapped_column(JSON, default=list)
    remote_preference: Mapped[bool] = mapped_column(Boolean, default=True)
    cv_filename: Mapped[str] = mapped_column(String(255), default="")
    cv_text: Mapped[str] = mapped_column(Text, default="")
    embedding: Mapped[list | None] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    company: Mapped[str] = mapped_column(String(200))
    location: Mapped[str] = mapped_column(String(200), default="")
    country: Mapped[str] = mapped_column(String(100), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    skills: Mapped[list] = mapped_column(JSON, default=list)
    min_experience_years: Mapped[float] = mapped_column(Float, default=0)
    remote: Mapped[bool] = mapped_column(Boolean, default=False)
    employment_type: Mapped[str] = mapped_column(String(80), default="Full-time")
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="EUR")
    url: Mapped[str] = mapped_column(String(1000), default="")
    source: Mapped[str] = mapped_column(String(100), default="demo")
    embedding: Mapped[list | None] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(Integer, index=True)
    job_id: Mapped[int] = mapped_column(Integer, index=True)
    score: Mapped[float] = mapped_column(Float)
    keyword_score: Mapped[float] = mapped_column(Float)
    semantic_score: Mapped[float] = mapped_column(Float)
    experience_score: Mapped[float] = mapped_column(Float)
    location_score: Mapped[float] = mapped_column(Float)
    missing_skills: Mapped[list] = mapped_column(JSON, default=list)
    explanation: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
