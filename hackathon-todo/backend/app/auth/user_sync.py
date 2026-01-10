"""
User synchronization between Better Auth and application database.

This module handles the synchronization of user data between Better Auth
and the application's user records.
"""
from sqlmodel import Session
from uuid import UUID
import httpx
from fastapi import HTTPException, status
from typing import Optional

from app.models.user import User


def get_or_create_app_user_from_better_auth(session: Session, user_payload) -> User:
    """
    Get or create an application user record based on Better Auth user data.

    Args:
        session: Database session
        user_payload: Better Auth user payload (could be BetterAuthPayload or dict-like)

    Returns:
        User record from the application database
    """
    # Handle both the old BetterAuthPayload and new dict-like payload
    if hasattr(user_payload, 'sub'):
        # It's an object with attributes (like BetterAuthPayload)
        user_id = UUID(user_payload.sub)
        email = getattr(user_payload, 'email', '')
        name = getattr(user_payload, 'name', None)
        email_verified = getattr(user_payload, 'emailVerified', False)
    else:
        # It's a dict-like object
        user_id_str = getattr(user_payload, 'sub', None) or user_payload.get('id')
        if not user_id_str:
            raise ValueError("User payload must contain user ID")
        user_id = UUID(user_id_str)

        email = getattr(user_payload, 'email', user_payload.get('email', ''))
        name = getattr(user_payload, 'name', user_payload.get('name', None))
        email_verified = getattr(user_payload, 'emailVerified', user_payload.get('emailVerified', False))

    # Try to find existing user by ID
    existing_user = session.get(User, user_id)

    if existing_user:
        # Update user data if needed
        existing_user.email = email
        existing_user.name = name
        existing_user.email_verified = email_verified
        from datetime import datetime
        existing_user.updated_at = datetime.utcnow()  # Update timestamp
        session.add(existing_user)
        session.commit()
        session.refresh(existing_user)
        return existing_user
    else:
        # Create new user record
        from datetime import datetime
        new_user = User(
            id=user_id,
            email=email,
            name=name,
            email_verified=email_verified,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user