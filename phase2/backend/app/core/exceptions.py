"""
Custom application exceptions with standardized error codes.
"""
from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class TodoAppException(HTTPException):
    """Base exception for all application errors."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.code = code
        self.message = message
        self.field = field
        self.details = details
        super().__init__(status_code=status_code, detail=message)


# Authentication Exceptions
class UnauthorizedException(TodoAppException):
    """User is not authenticated."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            message=message,
        )


class InvalidCredentialsException(TodoAppException):
    """Invalid username or password."""

    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_CREDENTIALS",
            message=message,
        )


class ForbiddenException(TodoAppException):
    """User does not have permission to access this resource."""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message,
        )


class TokenExpiredException(TodoAppException):
    """JWT token has expired."""

    def __init__(self, message: str = "Authentication token has expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="TOKEN_EXPIRED",
            message=message,
        )


# Resource Exceptions
class ResourceNotFoundException(TodoAppException):
    """Requested resource was not found."""

    def __init__(
        self,
        resource_type: str = "Resource",
        resource_id: Optional[str] = None,
    ):
        message = f"{resource_type} not found"
        if resource_id:
            message = f"{resource_type} with ID '{resource_id}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="RESOURCE_NOT_FOUND",
            message=message,
        )


class ResourceAlreadyExistsException(TodoAppException):
    """Resource already exists (e.g., duplicate email)."""

    def __init__(
        self,
        resource_type: str = "Resource",
        field: Optional[str] = None,
        value: Optional[str] = None,
    ):
        message = f"{resource_type} already exists"
        if field and value:
            message = f"{resource_type} with {field} '{value}' already exists"
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="RESOURCE_ALREADY_EXISTS",
            message=message,
            field=field,
        )


# Validation Exceptions
class ValidationException(TodoAppException):
    """Request validation failed."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            message=message,
            field=field,
            details=details,
        )


# Database Exceptions
class DatabaseException(TodoAppException):
    """Database operation failed."""

    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="DATABASE_ERROR",
            message=message,
        )


# Rate Limiting
class RateLimitExceededException(TodoAppException):
    """Rate limit exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded. Please try again later.",
        retry_after: Optional[int] = None,
    ):
        details = {"retry_after": retry_after} if retry_after else None
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="RATE_LIMIT_EXCEEDED",
            message=message,
            details=details,
        )
