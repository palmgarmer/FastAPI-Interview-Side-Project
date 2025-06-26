from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_tables
from app.routers import candidates, interviews, feedback


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup: Create database tables
    from app.models import candidate, interview, feedback
    await create_tables()
    yield
    # Shutdown: cleanup if needed


# Create FastAPI app instance
app = FastAPI(
    title="Candidate Management API",
    description="API for managing candidates, interviews, and feedback",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(candidates.router)
app.include_router(interviews.router)
app.include_router(feedback.router)

# Basic health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Candidate Management API is running"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Candidate Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
