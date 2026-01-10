"""
Health check API endpoints for monitoring and uptime tracking.
"""
from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify the application is running properly.

    Returns:
        Dict[str, Any]: Health status with timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "todo-api",
        "version": "1.0.0"
    }