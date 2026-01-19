"""
FastAPI application setup for CoverageSummarizer Web UI.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Create FastAPI app
app = FastAPI(
    title="CoverageSummarizer API",
    description="Summaries with guaranteed coverage and auditability",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup paths
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Include routes
from src.api import routes
app.include_router(routes.router)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("🚀 CoverageSummarizer Web UI started")
    print(f"📁 Static files: {STATIC_DIR}")
    print(f"📄 Templates: {TEMPLATES_DIR}")
    print("✅ Ready to process documents with guaranteed coverage!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    from src.api.progress_tracker import get_progress_tracker
    tracker = get_progress_tracker()
    cleaned = tracker.cleanup_old_sessions()
    print(f"🧹 Cleaned up {cleaned} old sessions")
    print("👋 CoverageSummarizer Web UI shutting down")
