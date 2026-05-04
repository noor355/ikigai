from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

# Create database engine with enhanced connection resilience
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Ping connection before using (prevents stale connections)
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,  # Recycle connections every 1 hour to prevent timeout
    connect_args={
        "connect_timeout": 10,
        "application_name": "ikigai_app",
    }
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
