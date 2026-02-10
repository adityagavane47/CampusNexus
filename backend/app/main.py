"""
CampusNexus - FastAPI Main Application
Decentralized LinkedIn & Marketplace for VIT Pune Students
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth, feed, escrow, marketplace, ai, oauth, notifications

settings = get_settings()

app = FastAPI(
    title="CampusNexus API",
    description=f"Decentralized Campus Ecosystem for {settings.college_name} on Algorand",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Middleware (Required for OAuth)
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.jwt_secret_key,
    https_only=False  # Set to True in production with HTTPS
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(oauth.router, prefix="/api/oauth", tags=["OAuth"])
app.include_router(feed.router, prefix="/api/feed", tags=["Project Feed"])
app.include_router(escrow.router, prefix="/api/escrow", tags=["Escrow"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI & Automation"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "app": "CampusNexus",
        "college": settings.college_name,
        "network": settings.algorand_network,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "algorand_network": settings.algorand_network,
        "algorand_node": settings.algorand_algod_address,
    }
