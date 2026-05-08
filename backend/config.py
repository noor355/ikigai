from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database (Supabase PostgreSQL)
    DATABASE_URL: str = "postgresql://postgres.vlocrlpvodgwgriqqpsj:ikigaiproject123@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Ikigai Career Guidance API"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    # ML Settings
    MODEL_PATH: str = "ml_engine/models/"

    # Gemini API
    GEMINI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
