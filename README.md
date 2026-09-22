# JobMatch AI / MatchTN

AI-powered SaaS platform for analyzing an IT CV and matching it with Tunisia + international job opportunities.

## Main workflow

1. Upload a CV PDF.
2. Extract CV text.
3. Build a candidate profile.
4. Choose target countries / remote preference.
5. Search the local demo job catalog.
6. Generate embeddings.
7. Hybrid matching: keyword + semantic similarity + experience + location/remote.
8. Return ranked opportunities with missing skills and explanation.
9. Open the original job URL.

## Stack

- FastAPI
- PostgreSQL + pgvector
- Redis
- OpenAI (optional)
- pypdf
- Docker Compose
- Kubernetes manifests
- Terraform starter
- GitHub Actions
- Ruff, Bandit, Gitleaks, Trivy

## Run locally

Copy `.env.example` to `.env`.

For development without OpenAI credits, keep:

```env
LLM_PROVIDER=mock
```

Then:

```powershell
docker compose up -d --build
docker compose ps
```

Open:

- http://localhost:8000
- http://localhost:8000/docs
- http://localhost:8000/healthz

The UI lets you upload a CV and search matching jobs.

## OpenAI mode

OpenAI is optional. If you have API credits:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
```

Never commit `.env`.

## API key

The API uses `X-API-Key` for `/api/v1/*`.

Default local value:

```text
change-me-local-api-key
```

The frontend reads this value from a field so it can call the API.

## Demo jobs

The database is seeded automatically with international demo opportunities for:

- France
- Switzerland
- Germany
- Canada
- UAE
- Remote
- Tunisia

They are clearly marked as demo data. Replace them with legally permitted job APIs/feeds or your own imported data before production.

## Production roadmap

- Managed PostgreSQL/RDS + pgvector
- ElastiCache/Redis
- S3 for CV storage
- EKS + Ingress/TLS
- Secrets Manager
- Background workers
- Alembic migrations
- Real job APIs/feeds
- OAuth/JWT
- Observability
- Backups
