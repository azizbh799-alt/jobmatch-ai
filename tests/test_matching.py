from types import SimpleNamespace

from app.matching import experience_score, keyword_score, location_score


def test_keyword_score():
    candidate = SimpleNamespace(skills=["Python", "Docker", "AWS"])
    job = SimpleNamespace(skills=["Python", "Docker", "Kubernetes"])
    score, missing = keyword_score(candidate, job)
    assert score > 50
    assert "kubernetes" in missing


def test_experience_score():
    candidate = SimpleNamespace(experience_years=2)
    job = SimpleNamespace(min_experience_years=1)
    assert experience_score(candidate, job) == 100


def test_remote_location():
    candidate = SimpleNamespace(
        remote_preference=True,
        preferred_countries=[],
        location="Tunisia",
    )
    job = SimpleNamespace(remote=True, country="France", location="Paris")
    assert location_score(candidate, job) == 100
