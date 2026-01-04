"""
Authentication request/response schemas.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID
from datetime import datetime
from app.core.sanitization import sanitize_string, sanitize_email


class RegisterRequest(BaseModel):
    """User registration request"""

    email: EmailStr = Field(..., description="Valid email address (RFC 5322)")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    name: str | None = Field(None, max_length=255, description="Optional display name")

    @field_validator('email', mode='before')
    @classmethod
    def sanitize_email_field(cls, v: str) -> str:
        """Sanitize and normalize email."""
        sanitized = sanitize_email(v)
        if not sanitized:
            raise ValueError("Invalid email address")
        return sanitized

    @field_validator('name')
    @classmethod
    def sanitize_name(cls, v: str | None) -> str | None:
        """Sanitize name to prevent XSS attacks."""
        if v is None:
            return None
        return sanitize_string(v, max_length=255)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "name": "John Doe",
            }
        }


class LoginRequest(BaseModel):
    """User login request"""

    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }


class UserResponse(BaseModel):
    """User data in API responses"""

    id: UUID
    email: str
    email_verified: bool
    name: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
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


class AuthResponse(BaseModel):
    """Authentication response with user and token"""

    user: UserResponse
    token: str = Field(..., description="JWT access token")

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "email_verified": False,
                    "name": "John Doe",
                    "created_at": "2026-01-02T10:00:00Z",
                    "updated_at": "2026-01-02T10:00:00Z",
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }
