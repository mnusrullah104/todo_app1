"""
User model for Better Auth integration.

This model represents the user data structure compatible with Better Auth.
Note: Better Auth manages its own user accounts in its database, but we maintain
a reference for tasks and other related data in our application database.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class User(SQLModel, table=True):
    """
    User reference model for application-specific data.

    Fields:
        id: Unique user identifier (UUID) - matches Better Auth user ID
        email: User's email address (unique)
        email_verified: Whether email has been verified
        name: Optional display name
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False, max_length=255)
    email_verified: bool = Field(default=False)
    name: Optional[str] = Field(default=None, max_length=255)
    # Remove password_hash as this is managed by Better Auth
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "email_verified": False,
                "name": "John Doe",
                "created_at": "2026-01-02T10:00:00Z",
                "updated_at": "2026-01-02T10:00:00Z",
            }
        }