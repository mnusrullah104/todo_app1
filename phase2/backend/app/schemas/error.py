"""
Standardized error response schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ErrorDetail(BaseModel):
    """Detailed error information."""

    code: str = Field(
        ...,
        description="Machine-readable error code",
        examples=["VALIDATION_ERROR", "RESOURCE_NOT_FOUND", "UNAUTHORIZED"]
    )
    message: str = Field(
        ...,
        description="Human-readable error message",
        examples=["Email already registered", "Invalid credentials"]
    )
    field: Optional[str] = Field(
        None,
        description="Field name for validation errors",
        examples=["email", "password"]
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional error context"
    )


class ErrorResponse(BaseModel):
    """Standardized error response format."""

    success: bool = Field(
        False,
        description="Always false for error responses"
    )
    error: ErrorDetail = Field(
        ...,
        description="Error details"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error occurrence timestamp (UTC)"
    )
    request_id: Optional[str] = Field(
        None,
        description="Request ID for error tracking"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Email address is already registered",
                    "field": "email"
                },
                "timestamp": "2026-01-03T10:30:00Z",
                "request_id": "req_abc123"
            }
        }
