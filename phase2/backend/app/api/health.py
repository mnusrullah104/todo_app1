"""
Health check endpoint for monitoring application and database status.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session

router = APIRouter()


@router.get("/health")
async def health_check(session: Session = Depends(get_session)):
    """
    Health check endpoint.

    Returns:
        - status: "healthy" if database connection is working
        - database: "connected" or "disconnected"

    Status Codes:
        - 200: Service is healthy
        - 503: Service is unhealthy (database connection failed)
    """
    try:
        # Test database connection with simple query
        session.exec(select(1)).first()
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database temporarily unavailable. Please retry in 30 seconds.",
            headers={"Retry-After": "30"}
        )
