"""
API routes for the LYRAIOS system.
"""

from fastapi import APIRouter

from app.api.routes.tools import router as tools_router
from app.api.routes.health import router as health_router

# Create main router
router = APIRouter()

# Include sub-routers
router.include_router(tools_router, prefix="/tools", tags=["tools"])
router.include_router(health_router, prefix="/health", tags=["health"])
