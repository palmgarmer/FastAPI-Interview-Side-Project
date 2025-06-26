from fastapi import FastAPI
from app.db import create_tables
from app.routers import candidates, interviews, feedback

# Create FastAPI app instance
app = FastAPI(
    title="Candidate Management API",
    description="API for managing candidates, interviews, and feedback",
    version="1.0.0"
)

# Include routers
app.include_router(candidates.router)
app.include_router(interviews.router)
app.include_router(feedback.router)

# Startup event - runs when app starts
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    from app.models import candidate, interview, feedback
    
    # Create database tables
    await create_tables()

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
