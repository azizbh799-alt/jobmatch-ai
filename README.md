# 🚀 JobMatch AI — MatchTN

> **AI-Powered Career Matching Platform**
> Analyze your CV, discover relevant job opportunities, identify skill gaps, and understand why each position matches your profile.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql\&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker\&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript\&logoColor=black)
![API](https://img.shields.io/badge/API-REST-02569B)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

**JobMatch AI / MatchTN** is an intelligent job-matching platform designed to connect candidates with relevant career opportunities.

The platform analyzes a candidate's CV and extracts key information such as:

* 🧑‍💻 Skills
* 💼 Professional experience
* 🎓 Education
* 📍 Location
* 🌍 Preferred countries
* 🗣️ Languages
* 🎯 Career preferences

It then searches for job opportunities through external job APIs and calculates a **candidate–job compatibility score**.

The platform also provides:

* Skill-gap detection
* Job matching
* Match explanations
* Personalized recommendations
* External job search
* REST API
* CV analysis
* Redis caching
* PostgreSQL persistence
* Dockerized infrastructure
* LLM/OpenAI integration with local fallback

---

# 🎯 Main Features

## 📄 1. AI CV Analysis

Upload a CV and automatically extract structured candidate information.

Example:

```text
CV
 │
 ▼
CV Parser
 │
 ├── Skills
 ├── Experience
 ├── Education
 ├── Location
 ├── Languages
 └── Preferred Countries
```

The application can operate using:

* LLM/OpenAI-based analysis
* Local heuristic analysis
* Deterministic mock embeddings for local development

This allows the platform to continue working even when an external LLM service is unavailable.

---

## 🔎 2. Intelligent Job Search

Job opportunities can be retrieved from external job providers such as **Adzuna**.

Supported international markets include:

* 🇫🇷 France
* 🇨🇭 Switzerland
* 🇩🇪 Germany
* 🇨🇦 Canada
* 🇬🇧 United Kingdom

The application can also process remote-job searches.

---

## 🤝 3. Candidate–Job Matching

Each job is evaluated against the candidate profile.

The matching engine considers factors such as:

```text
Skills
Experience
Education
Location
Languages
Job Title
Career Preferences
```

Example:

```text
Candidate
   │
   ├── Python
   ├── FastAPI
   ├── Docker
   ├── AWS
   └── PostgreSQL
          │
          ▼
      Matching Engine
          │
          ▼
   ┌─────────────────┐
   │ Compatibility   │
   │     87%         │
   └─────────────────┘
```

---

## 🧩 4. Skill Gap Detection

The platform identifies technologies and skills required by a job that are missing from the candidate profile.

Example:

```text
Candidate Skills
----------------
Python
FastAPI
Docker
PostgreSQL

Job Requirements
----------------
Python
FastAPI
Docker
Kubernetes
Terraform

Missing Skills
--------------
Kubernetes
Terraform
```

This gives candidates a clear indication of what they should learn to improve their employability.

---

## 🧠 5. AI Match Explanation

Instead of providing only a score, the application explains **why** a job matches the candidate.

Example:

```text
Match Score: 87%

Why this job matches:
✓ Strong Python experience
✓ FastAPI experience
✓ Docker knowledge
✓ PostgreSQL experience

Skills to improve:
• Kubernetes
• Terraform
```

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      Candidate      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Web Frontend    │
                         │ HTML / CSS / JS     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      REST API       │
                         └───────┬─────┬───────┘
                                 │     │
                    ┌────────────┘     └────────────┐
                    ▼                               ▼
          ┌─────────────────┐              ┌─────────────────┐
          │   CV Analyzer   │              │ Matching Engine │
          │                 │              │                 │
          │ LLM / Heuristic │              │ Score + Gaps    │
          └────────┬────────┘              └────────┬────────┘
                   │                                │
                   └──────────────┬─────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │   PostgreSQL    │
                         │     Database    │
                         └─────────────────┘
                                  ▲
                                  │
                         ┌─────────────────┐
                         │      Redis      │
                         │      Cache      │
                         └─────────────────┘

                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Job APIs      │
                         │     Adzuna      │
                         └─────────────────┘
```

---

# 🛠️ Technology Stack

## Backend

| Technology | Purpose                    |
| ---------- | -------------------------- |
| Python     | Main programming language  |
| FastAPI    | REST API framework         |
| Pydantic   | Data validation & settings |
| SQLAlchemy | Database ORM               |
| PostgreSQL | Persistent data storage    |
| Redis      | Caching                    |
| Uvicorn    | ASGI server                |

## AI / Matching

| Technology             | Purpose                    |
| ---------------------- | -------------------------- |
| OpenAI / LLM           | CV analysis & explanations |
| Local heuristic engine | Fallback CV analysis       |
| Embeddings             | Semantic similarity        |
| Matching engine        | Candidate-job scoring      |
| Skill-gap engine       | Missing skill detection    |

## Frontend

| Technology | Purpose               |
| ---------- | --------------------- |
| HTML5      | Application structure |
| CSS3       | Responsive UI         |
| JavaScript | Frontend logic        |
| Fetch API  | Backend communication |

## DevOps

| Technology     | Purpose                  |
| -------------- | ------------------------ |
| Docker         | Containerization         |
| Docker Compose | Local orchestration      |
| Git            | Version control          |
| GitHub         | Source code hosting      |
| Kubernetes     | Deployment configuration |
| Terraform      | Infrastructure as Code   |

---

# 📂 Project Structure

```text
JobMatch-AI-MatchTN/
│
├── app/
│   ├── ai.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── ...
│
├── docker/
│   └── postgres/
│       └── init.sql
│
├── docs/
│   └── architecture.md
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secret.example.yaml
│
├── static/
│   └── index.html
│
├── terraform/
│   └── README.md
│
├── tests/
│   └── test_matching.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/azizbh799-alt/jobmatch-ai.git
cd jobmatch-ai
```

---

## 2. Configure environment variables

Create a `.env` file:

```bash
cp .env.example .env
```

Configure the required variables:

```env
APP_API_KEY=your-local-api-key

DATABASE_URL=postgresql+psycopg://jobmatch:jobmatch@postgres:5432/jobmatch

REDIS_URL=redis://redis:6379/0

ADZUNA_APP_ID=your-adzuna-app-id
ADZUNA_APP_KEY=your-adzuna-app-key

LLM_PROVIDER=mock

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

> ⚠️ Never commit your `.env` file or API keys to GitHub.

---

# 🐳 Run with Docker

Build the containers:

```bash
docker compose build
```

Start the application:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

Expected services:

```text
jobmatch-api
jobmatch-postgres
jobmatch-redis
```

---

# 🌐 Access the Application

### Web Application

```text
http://localhost:8000
```

### Swagger API Documentation

```text
http://localhost:8000/docs
```

### OpenAPI Specification

```text
http://localhost:8000/openapi.json
```

### Health Check

```text
http://localhost:8000/readyz
```

Expected response:

```json
{
  "status": "ready"
}
```

---

# 🔌 API Endpoints

## CV Upload

```http
POST /api/v1/candidates/upload-cv
```

Uploads and analyzes a candidate CV.

---

## Job Search

```http
POST /api/v1/search
```

Searches and matches available jobs against the candidate profile.

---

## Job Details

```http
GET /api/v1/jobs/{job_id}
```

Returns detailed information about a specific job.

---

# 🧪 Testing

Run the test suite:

```bash
docker compose exec api pytest
```

Or locally:

```bash
pytest
```

Example:

```text
tests/
└── test_matching.py
```

---

# 🔐 Security

The project includes several security-oriented practices:

* Environment variables for secrets
* `.env` excluded from Git
* API authentication
* Rate limiting
* Input validation with Pydantic
* Docker isolation
* Separation between application and database
* Example secrets instead of real credentials
* External API credentials stored outside source code

For production deployment, additional controls should be implemented, including:

* HTTPS/TLS
* Secret management
* Strong authentication
* Database encryption
* Network policies
* Container image scanning
* Centralized logging
* Monitoring and alerting

---

# 🚀 DevOps & Deployment

The project is designed to evolve from local Docker Compose development toward cloud-native deployment.

Current infrastructure components include:

```text
GitHub
   │
   ▼
CI/CD
   │
   ▼
Docker Image
   │
   ▼
Kubernetes
   │
   ├── API Deployment
   ├── Service
   ├── ConfigMap
   └── Secrets
```

Infrastructure-as-Code configuration is also included through Terraform.

---

# 📊 Monitoring Roadmap

The platform can be extended with:

```text
Prometheus
     │
     ▼
Application Metrics
     │
     ▼
Grafana
```

Potential metrics:

* API response time
* Request count
* Error rate
* Job search latency
* CV processing time
* Matching latency
* Redis cache hit ratio
* Database performance

---

# 🔄 CI/CD

The repository contains a GitHub Actions workflow.

Example pipeline:

```text
Developer
    │
    ▼
Git Push
    │
    ▼
GitHub Actions
    │
    ├── Install dependencies
    ├── Run tests
    ├── Validate application
    └── Build Docker image
            │
            ▼
        Deployment
```

---

# 💡 Future Improvements

Planned improvements include:

* [ ] Advanced semantic job matching
* [ ] Improved CV parsing
* [ ] Multilingual CV support
* [ ] Candidate authentication
* [ ] Saved jobs
* [ ] Job alerts
* [ ] Personalized learning recommendations
* [ ] Kubernetes production deployment
* [ ] AWS deployment
* [ ] Terraform infrastructure
* [ ] Prometheus + Grafana monitoring
* [ ] Advanced security scanning
* [ ] CI/CD deployment pipeline
* [ ] Vector database integration
* [ ] Advanced recommendation engine

---

# 🎓 Learning Objectives

This project demonstrates practical experience in:

### Backend Development

* REST API development
* FastAPI
* Database design
* Authentication
* API integration
* Data validation

### AI Engineering

* LLM integration
* Prompt-based extraction
* Embeddings
* Semantic matching
* Recommendation systems
* AI fallback strategies

### Cloud & DevOps

* Docker
* Docker Compose
* Kubernetes
* Terraform
* CI/CD
* Cloud deployment
* Monitoring

### Software Engineering

* Modular architecture
* Environment-based configuration
* Automated testing
* API documentation
* Version control
* Containerization

---

# 📸 Application

The platform provides a modern dashboard where users can:

1. Upload their CV
2. Analyze their profile
3. Select target markets
4. Search for opportunities
5. View compatibility scores
6. Analyze missing skills
7. Read AI-generated explanations

---

# 👨‍💻 Author

**Mohamed Aziz Becheikh**

Full Stack Developer | Cloud & DevSecOps Enthusiast

📍 Tunisia

### Technologies

```text
Python • FastAPI • Java • Spring Boot • Angular
Docker • Kubernetes • AWS • Terraform • Ansible
PostgreSQL • Redis • Git • CI/CD
AI • LLM • DevSecOps
```

---

# ⭐ Project Highlights

> **From CV → AI Analysis → Job Search → Matching → Skill Gap → Career Recommendation**

JobMatch AI combines **Full Stack development, Artificial Intelligence, Cloud technologies, and DevOps practices** into a single end-to-end project.

If you find this project useful, consider giving the repository a ⭐.

---

## 📄 License

This project is licensed under the MIT License.
