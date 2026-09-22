# 🚀 JobMatch AI / MatchTN

> **AI-Powered Career Matching Platform**
> Analyze your CV, discover relevant job opportunities, and understand why each position matches your profile.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql\&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis\&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker\&logoColor=white)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws\&logoColor=white)](https://aws.amazon.com/ec2/)

---

## 📌 Overview

**JobMatch AI / MatchTN** is a full-stack AI-powered recruitment platform designed to help candidates find job opportunities that match their skills, experience, education, and career preferences.

The platform analyzes a candidate's CV, extracts structured profile information, searches external job opportunities, calculates compatibility scores, identifies missing skills, and provides an explanation for each recommendation.

### Core workflow

```text
                 ┌─────────────────┐
                 │   Candidate CV  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   CV Analysis   │
                 │  AI / Heuristic │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Candidate Profile│
                 │ Skills / Exp.   │
                 │ Education / Geo │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   Job Search    │
                 │     Adzuna      │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Matching Engine │
                 │ Score + Skills  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Recommended Jobs│
                 └─────────────────┘
```

---

# ✨ Features

## 📄 CV Analysis

Upload a CV and automatically extract:

* Candidate name
* Professional title
* Skills
* Experience
* Education
* Languages
* Location
* Preferred countries
* Career-related information

The platform supports two analysis modes:

* **Mock / heuristic mode** — no paid AI API required
* **OpenAI mode** — AI-powered extraction and explanations

---

## 🔎 Job Search

The application searches job opportunities using the **Adzuna Jobs API**.

Supported markets include:

* 🇫🇷 France
* 🇨🇭 Switzerland
* 🇩🇪 Germany
* 🇨🇦 Canada
* 🇬🇧 United Kingdom
* 🌍 Remote opportunities

The platform can search multiple target countries based on the candidate profile.

---

## 🤖 AI Matching

Each job is evaluated against the candidate profile.

The matching engine considers factors such as:

* Skills
* Job title
* Experience
* Location
* Candidate preferences
* Required technologies

Example:

```text
Job: Full Stack Developer

Compatibility: 87%

Matching skills:
✓ Java
✓ Spring Boot
✓ JavaScript
✓ SQL
✓ Git

Missing skills:
• Kubernetes
• AWS
```

---

## 📊 Compatibility Score

Each recommendation receives a compatibility score that helps the candidate understand how closely the position matches their profile.

The platform also provides an explanation instead of displaying only a numerical score.

---

## 🎯 Skill Gap Analysis

JobMatch AI identifies missing or less-represented skills.

Example:

```text
Your profile:
Java ✓
Spring Boot ✓
Angular ✓
Docker ✓

Job requirements:
Java ✓
Spring Boot ✓
Angular ✓
Docker ✓
Kubernetes ✗
Terraform ✗
```

This can help candidates identify skills to develop for their target positions.

---

# 🏗️ Architecture

```text
                         INTERNET
                            │
                            ▼
                    ┌───────────────┐
                    │    AWS EC2    │
                    │    Ubuntu     │
                    └───────┬───────┘
                            │
                         HTTP :80
                            │
                            ▼
                  ┌───────────────────┐
                  │   Docker Compose  │
                  └─────────┬─────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │   FastAPI   │   │ PostgreSQL  │   │    Redis    │
   │    :8000    │   │    :5432    │   │    :6379    │
   └──────┬──────┘   └─────────────┘   └─────────────┘
          │
          ├──────────────► Adzuna API
          │
          └──────────────► OpenAI API (optional)
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL
* pgvector
* Redis

## Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI
* Netflix-inspired dark interface

## AI

* OpenAI API — optional
* Embeddings
* CV information extraction
* Match explanation
* Heuristic fallback

## Job Data

* Adzuna API

## DevOps

* Docker
* Docker Compose
* AWS EC2
* Linux / Ubuntu
* Git / GitHub

## Future Infrastructure

* Kubernetes
* Amazon EKS
* Terraform
* GitHub Actions / GitLab CI/CD
* Prometheus
* Grafana

---

# 📁 Project Structure

```text
jobmatch-ai/
│
├── app/
│   ├── ai.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── ...
│
├── static/
│   └── index.html
│
├── docker/
│   └── postgres/
│       └── init.sql
│
├── docs/
│   └── ...
│
├── k8s/
│   └── ...
│
├── terraform/
│   └── ...
│
├── .github/
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🚀 Run Locally

## 1. Clone the repository

```bash
git clone https://github.com/azizbh799-alt/jobmatch-ai.git
cd jobmatch-ai
```

## 2. Create the environment file

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure your environment variables:

```env
APP_NAME=jobmatch-ai
ENVIRONMENT=local

APP_API_KEY=change-me-local-api-key

DATABASE_URL=postgresql+psycopg://jobmatch:jobmatch@postgres:5432/jobmatch
REDIS_URL=redis://redis:6379/0

ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key

LLM_PROVIDER=mock

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

CORS_ORIGINS=http://localhost:8000
```

> Never commit `.env` or API keys to GitHub.

---

# 🐳 Run with Docker Compose

Build the application:

```bash
docker compose build
```

Start the services:

```bash
docker compose up -d
```

Check the containers:

```bash
docker compose ps
```

Expected services:

```text
api
postgres
redis
```

Check API health:

```bash
curl http://localhost:8000/readyz
```

Expected:

```json
{
  "status": "ready"
}
```

---

# 🌐 Web Interface

When running locally:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

OpenAPI specification:

```text
http://localhost:8000/openapi.json
```

---

# ☁️ AWS EC2 Deployment

JobMatch AI can be deployed on an Ubuntu EC2 instance using Docker Compose.

## EC2 Architecture

```text
                    Internet
                       │
                       │ HTTP :80
                       ▼
              ┌─────────────────┐
              │   AWS EC2       │
              │   Ubuntu        │
              │ 98.91.26.198    │
              └────────┬────────┘
                       │
                       ▼
                Docker Compose
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
          FastAPI   PostgreSQL   Redis
```

## EC2 Security Group

Recommended inbound rules:

| Protocol | Port | Source      |
| -------- | ---: | ----------- |
| SSH      |   22 | My IP only  |
| HTTP     |   80 | `0.0.0.0/0` |
| HTTPS    |  443 | `0.0.0.0/0` |

PostgreSQL and Redis should **not** be exposed to the public Internet.

---

## Deploy on EC2

Connect to the server:

```bash
ssh -i jobmatch-ai-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Clone the repository:

```bash
git clone https://github.com/azizbh799-alt/jobmatch-ai.git
cd jobmatch-ai
```

Create the environment:

```bash
nano .env
```

Configure the required variables.

Then start the application:

```bash
docker compose up -d --build
```

Check:

```bash
docker compose ps
```

Test:

```bash
curl http://localhost/readyz
```

---

# 🌍 Public Web Access

For public HTTP access, the API container is mapped from port `8000` to port `80`:

```yaml
api:
  build: .
  env_file:
    - .env
  ports:
    - "80:8000"
```

After changing the configuration:

```bash
docker compose down
docker compose up -d --build
```

The application is then accessible through:

```text
http://YOUR_EC2_PUBLIC_IP
```

Example:

```text
http://98.91.26.198
```

---

# 🔐 HTTPS Roadmap

The current EC2 deployment uses HTTP for the initial deployment.

For production, HTTPS should be enabled using:

```text
Internet
    │
    ▼
HTTPS :443
    │
    ▼
Nginx / Reverse Proxy
    │
    ▼
FastAPI :8000
```

Recommended production components:

* Nginx
* Let's Encrypt
* Certbot
* HTTPS
* Domain name
* HTTP → HTTPS redirect

Example final architecture:

```text
                    Internet
                       │
                    HTTPS :443
                       │
                       ▼
                 ┌───────────┐
                 │   Nginx   │
                 │ TLS/HTTPS │
                 └─────┬─────┘
                       │
                    :8000
                       │
                       ▼
                  ┌─────────┐
                  │ FastAPI │
                  └────┬────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
         PostgreSQL           Redis
```

---

# 🔌 API Endpoints

## Health

```http
GET /healthz
```

Returns application health information.

---

## Readiness

```http
GET /readyz
```

Example:

```json
{
  "status": "ready"
}
```

---

## Upload CV

```http
POST /api/v1/candidates/upload-cv
```

Uploads and analyzes a candidate CV.

---

## Search Jobs

```http
POST /api/v1/search
```

Searches and matches jobs according to the candidate profile.

---

## Get Job

```http
GET /api/v1/jobs/{job_id}
```

Returns detailed information about a selected job.

---

# 🤖 AI Modes

## Mock Mode

Recommended for development and demonstrations without API costs:

```env
LLM_PROVIDER=mock
```

The application uses deterministic local embeddings and heuristic CV analysis.

Advantages:

* No OpenAI cost
* No external AI dependency
* Works offline for AI processing
* Good for development and demos

---

## OpenAI Mode

To enable OpenAI:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key
```

The application can then use OpenAI for:

* CV extraction
* Embeddings
* Job matching
* Match explanations

> Never expose your OpenAI API key in GitHub, screenshots, videos, frontend JavaScript, or Docker logs.

---

# 🧪 Testing

Check Python syntax:

```bash
python -m py_compile app/ai.py
```

```bash
python -m py_compile app/main.py
```

Check containers:

```bash
docker compose ps
```

View API logs:

```bash
docker compose logs --tail=100 api
```

Follow API logs:

```bash
docker compose logs -f api
```

---

# 🐞 Troubleshooting

## Application doesn't open

Check:

```bash
docker compose ps
```

Then:

```bash
curl http://localhost/readyz
```

Check port 80:

```bash
sudo ss -tulpn | grep :80
```

Check AWS Security Group:

```text
HTTP 80 → 0.0.0.0/0
```

---

## API container is restarting

Check:

```bash
docker compose logs --tail=100 api
```

---

## PostgreSQL is unhealthy

Check:

```bash
docker compose logs postgres
```

---

## Redis is unhealthy

Check:

```bash
docker compose logs redis
```

---

## Check environment variables

Do not print secret values publicly.

For debugging, check only variable names:

```bash
docker compose config
```

Avoid sharing output containing:

```text
ADZUNA_APP_KEY
OPENAI_API_KEY
APP_API_KEY
```

---

# 🔒 Security

Security considerations implemented or planned:

* Environment variables for secrets
* `.env` excluded from Git
* API authentication key
* Rate limiting
* CORS configuration
* Docker isolation
* AWS Security Groups
* Private PostgreSQL/Redis access
* HTTPS roadmap
* Secret management roadmap

Production improvements:

* AWS Secrets Manager
* HTTPS
* Nginx reverse proxy
* IAM least privilege
* CloudWatch
* WAF
* Network isolation
* Database backups
* CI/CD security scanning

---

# 📈 DevOps Roadmap

The project is designed to evolve from a Docker Compose deployment into a cloud-native platform.

### Phase 1 — Application

* FastAPI
* PostgreSQL
* Redis
* JavaScript frontend
* Adzuna API
* AI matching

### Phase 2 — Containerization

* Docker
* Docker Compose
* Health checks
* Environment configuration

### Phase 3 — AWS

* EC2
* Security Groups
* HTTPS
* Nginx
* CloudWatch

### Phase 4 — Infrastructure as Code

* Terraform
* VPC
* Subnets
* IAM
* EC2
* Load Balancer

### Phase 5 — Kubernetes

* Kubernetes
* Amazon EKS
* Deployments
* Services
* ConfigMaps
* Secrets
* Ingress

### Phase 6 — DevSecOps

* GitHub/GitLab CI/CD
* SonarQube
* Trivy
* Container security
* Automated testing
* Security gates

### Phase 7 — Observability

* Prometheus
* Grafana
* Application metrics
* Infrastructure monitoring
* Alerting

---

# 📊 Future Architecture

```text
                           GitHub
                              │
                              ▼
                       CI/CD Pipeline
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
             SonarQube      Trivy       Tests
                │             │             │
                └─────────────┼─────────────┘
                              │
                              ▼
                         Docker Image
                              │
                              ▼
                         AWS ECR
                              │
                              ▼
                          Amazon EKS
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
            FastAPI        Redis        PostgreSQL
               │
               ├──────────────► Adzuna
               │
               └──────────────► OpenAI
                              │
                              ▼
                    Prometheus + Grafana
```

---

# 📸 Demo

The application provides a modern dark interface inspired by streaming platforms while maintaining an original JobMatch AI identity.

Main workflow:

```text
Upload CV
    ↓
AI Profile Analysis
    ↓
Select Target Markets
    ↓
Search Jobs
    ↓
Calculate Compatibility
    ↓
Analyze Skill Gaps
    ↓
Review Recommendations
```

---

# 📦 Requirements

For local development:

* Python 3.11+
* Docker
* Docker Compose
* Git

For AWS deployment:

* AWS account
* EC2 instance
* Ubuntu
* Security Group
* Docker
* Git

Optional:

* Adzuna API credentials
* OpenAI API credentials
* Domain name
* AWS Route 53

---

# 👨‍💻 Author

**Mohamed Aziz Becheikh**

Full Stack Developer | Cloud & DevSecOps Enthusiast

Skills and technologies:

* Python
* FastAPI
* Java / Spring Boot
* Angular
* JavaScript
* Docker
* Kubernetes
* AWS
* Terraform
* Ansible
* Git/GitHub
* CI/CD
* PostgreSQL
* Redis
* DevSecOps
* AI / LLM

---

# 🔗 Repository

GitHub:

https://github.com/azizbh799-alt/jobmatch-ai

---

# 📄 License

This project is intended for educational, portfolio, and demonstration purposes.

© 2026 Mohamed Aziz Becheikh
