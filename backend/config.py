from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database (Supabase PostgreSQL)
    # Get the connection string from: https://supabase.com -> Project Settings -> Database
    # Use Connection Pooling with Session mode for FastAPI
    DATABASE_URL: str = "postgresql://postgres:[password]@[project-id].pooler.supabase.com:6543/postgres"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
