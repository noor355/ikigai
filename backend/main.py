from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import engine, Base
import routes_auth
import routes_profile
import routes_daily
import routes_recommendations

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered career recommendation system based on Ikigai framework",
    version="1.0.0"
)

# Add CORS middleware - explicitly set origins
cors_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes_auth.router)
app.include_router(routes_profile.router)
app.include_router(routes_daily.router)
app.include_router(routes_recommendations.router)


@app.get("/")
def home():
    """Root endpoint"""
    return {
        "message": "Ikigai Career Guidance API",
        "api_version": "v1",
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/v1/auth",
            "profile": "/api/v1/profile",
            "daily_entries": "/api/v1/daily-entries",
            "recommendations": "/api/v1/recommendations"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
