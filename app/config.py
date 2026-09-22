from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "jobmatch-ai"
    environment: str = "local"
    app_api_key: str = "change-me-local-api-key"
    port: int = 8000
    rate_limit_per_minute: int = 60

    database_url: str = "postgresql+psycopg://jobmatch:jobmatch@postgres:5432/jobmatch"
    redis_url: str = "redis://redis:6379/0"

    adzuna_app_id: str = ""
    adzuna_app_key: str = ""

    llm_provider: str = "mock"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_base_url: str = "https://api.openai.com/v1"

    cors_origins: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()