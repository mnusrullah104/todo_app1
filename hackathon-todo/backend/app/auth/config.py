"""
Better Auth integration for Python backend.

This module handles integration with Better Auth from the frontend,
validating JWT tokens issued by Better Auth.
"""
import os
from typing import Optional
from uuid import UUID
import httpx
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from jose import JWTError, jwt
import asyncio

# Better Auth Configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "")
BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:8888")

security = HTTPBearer()


class BetterAuthPayload:
    """Decoded Better Auth JWT token payload"""

    def __init__(self, sub: str, exp: int, iat: int, **kwargs):
        self.sub = sub  # User ID
        self.exp = exp  # Expiration timestamp
        self.iat = iat  # Issued at timestamp
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def user_id(self) -> UUID:
        """Get user ID as UUID"""
        return UUID(self.sub)

    def is_expired(self) -> bool:
        """Check if token is expired"""
        return datetime.utcnow().timestamp() > self.exp


async def validate_better_auth_session(headers: dict) -> dict:
    """
    Validate Better Auth session by calling the Better Auth service.

    Args:
        headers: Request headers containing the authorization token

    Returns:
        Session data from Better Auth service

    Raises:
        HTTPException: If session is missing, invalid, or expired
    """
    try:
        # Get authorization header
        auth_header = headers.get("authorization") or headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header[7:]  # Remove "Bearer " prefix

        # Call Better Auth service to validate session
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{BETTER_AUTH_URL}/api/get-session",
                headers={"Authorization": f"Bearer {token}"}
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session",
                headers={"WWW-Authenticate": "Bearer"},
            )

        session_data = response.json()
        return session_data

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to validate session with Better Auth service",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Session validation error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_id(request: Request) -> UUID:
    """
    FastAPI dependency to extract and validate user ID by calling Better Auth service.

    Args:
        request: HTTP request containing the authorization header

    Returns:
        User ID (UUID)

    Raises:
        HTTPException: If session is missing, invalid, or expired
    """
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate session with Better Auth service to get user ID
    session_data = await validate_better_auth_session(dict(request.headers))

    # Extract user ID from session data
    user_id_str = session_data.get("user", {}).get("id")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session data: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UUID(user_id_str)