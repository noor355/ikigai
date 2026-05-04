from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import engine, Base
import uvicorn

print("Starting backend initialization...")

# Create database tables on startup
try:
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created/verified")
except Exception as e:
    print(f"[WARNING] Warning creating database tables: {str(e)}")

print("Importing routes...")
try:
    import routes_auth
    print("[OK] routes_auth imported")
    import routes_profile
    print("[OK] routes_profile imported")
    import routes_daily
    print("[OK] routes_daily imported")
    print("[LOADING] Initializing recommendation engine with NLP models...")
    import routes_recommendations
    print("[OK] routes_recommendations imported (NLP models loaded!)")
    import routes_chat_new
    print("[OK] routes_chat_new imported")
except Exception as e:
    print(f"[ERROR] Error importing routes: {str(e)}")
    import traceback
    traceback.print_exc()

print("Initializing FastAPI app...")

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered career recommendation system based on Ikigai framework",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

print("Including routers...")
try:
    app.include_router(routes_auth.router)
    app.include_router(routes_profile.router)
    app.include_router(routes_daily.router)
    app.include_router(routes_recommendations.router)
    app.include_router(routes_chat_new.router)
    print("[OK] All routers included")
except Exception as e:
    print(f"[ERROR] Error including routers: {str(e)}")
    import traceback
    traceback.print_exc()


@app.get("/")
def home():
    """Root endpoint"""
    return {
        "message": "Ikigai Career Guidance API",
        "api_version": "v1",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting Uvicorn server on http://0.0.0.0:8000")
    print("First startup will load NLP models (~2-3 minutes)")
    print("Once loaded, everything is ready for demo!")
    print("="*60 + "\n")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
