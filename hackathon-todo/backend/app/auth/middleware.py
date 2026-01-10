"""
Better Auth middleware for validating requests in FastAPI.

This module provides middleware and dependencies for validating
Better Auth sessions via API calls to the Better Auth service.
"""
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from uuid import UUID
import os
from typing import Optional

from app.database import get_session
from sqlmodel import Session

from app.auth.user_sync import get_or_create_app_user_from_better_auth

# Security scheme for Swagger UI
security = HTTPBearer()


# Define the dependency function directly at module level
async def get_current_user_id_from_request(request: Request) -> UUID:
    """Dependency function for getting current user ID."""
    from app.auth.config import get_current_user_id
    return await get_current_user_id(request)


# Create the dependency object at module level
require_auth_dependency = Depends(get_current_user_id_from_request)


async def require_same_user_dependency(request: Request, requested_user_id: UUID) -> UUID:
    """Dependency function for requiring same user."""
    from app.auth.config import get_current_user_id
    current_user_id = await get_current_user_id(request)

    if current_user_id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in session does not match requested user_id",
        )
    return current_user_id


async def require_auth_with_sync(request: Request, session: Session = Depends(get_session)) -> UUID:
    """Dependency function for requiring auth with sync."""
    from app.auth.config import get_current_user_id, validate_better_auth_session
    from app.auth.user_sync import get_or_create_app_user_from_better_auth

    # Validate session with Better Auth service to get user ID
    current_user_id = await get_current_user_id(request)

    # Now that we have a valid session, sync user with application database
    session_data = await validate_better_auth_session(dict(request.headers))

    # Create a simplified payload with essential user info
    class SimpleUserPayload:
        def __init__(self, user_data):
            self.sub = user_data.get("id", str(current_user_id))
            self.email = user_data.get("email", "")
            self.name = user_data.get("name", "")
            self.emailVerified = user_data.get("emailVerified", False)

    user_payload = SimpleUserPayload(session_data.get("user", {}))

    # Sync user with application database
    app_user = get_or_create_app_user_from_better_auth(session, user_payload)

    return app_user.id


# Create dependency object at module level
require_auth_with_sync_dependency = Depends(require_auth_with_sync)


def require_same_user(requested_user_id: UUID):
    """Returns a dependency for ensuring the authenticated user matches the requested user."""
    async def dependency(request: Request) -> UUID:
        return await require_same_user_dependency(request, requested_user_id)

    return Depends(dependency)