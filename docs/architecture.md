# Architecture

## Local

Browser -> FastAPI -> PostgreSQL/pgvector + Redis

CV:
Browser -> upload-cv -> pypdf -> CV profile -> embedding

Matching:
Candidate embedding + job embedding -> semantic score
Candidate/job skills -> keyword score
Experience -> experience score
Country/remote -> location score
All components -> final match score

## International jobs

The included jobs are demo records only. Production ingestion should use legally permitted APIs, feeds, partner sources, or user-provided imports. Store source, source_id, URL and publication date.

## Production

Browser -> CDN/ALB -> EKS -> FastAPI
                         -> RDS PostgreSQL/pgvector
                         -> ElastiCache Redis
                         -> S3 CV storage
                         -> Secrets Manager
                         -> OpenAI
