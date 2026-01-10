"""
Custom exceptions for the Todo application.

This module defines custom exception classes for the application
with consistent error codes and messages.
"""
from typing import Optional
from fastapi import HTTPException, status


class TodoAppException(HTTPException):
    """
    Base exception class for application-specific errors.

    All custom application exceptions should inherit from this class.
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
        code: str = "APP_ERROR",
        headers: Optional[dict] = None
    ):
        """
        Initialize the exception.

        Args:
            status_code: HTTP status code
            detail: Human-readable error message
            code: Machine-readable error code
            headers: Optional headers to include in response
        """
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code = code
        self.detail = detail
        self.status_code = status_code
        self.headers = headers or {}


class AuthenticationError(TodoAppException):
    """
    Exception raised for authentication-related errors.
    """

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            code="AUTHENTICATION_ERROR",
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationError(TodoAppException):
    """
    Exception raised for authorization-related errors.
    """

    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            code="AUTHORIZATION_ERROR"
        )


class ValidationError(TodoAppException):
    """
    Exception raised for validation-related errors.
    """

    def __init__(self, detail: str = "Validation failed"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            code="VALIDATION_ERROR"
        )


class NotFoundError(TodoAppException):
    """
    Exception raised when a requested resource is not found.
    """

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            code="NOT_FOUND_ERROR"
        )


class ConflictError(TodoAppException):
    """
    Exception raised when there's a conflict (e.g., duplicate resource).
    """

    def __init__(self, detail: str = "Conflict detected"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            code="CONFLICT_ERROR"
        )


class DatabaseError(TodoAppException):
    """
    Exception raised for database-related errors.
    """

    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            code="DATABASE_ERROR"
        )


class TaskNotFoundError(NotFoundError):
    """
    Exception raised when a requested task is not found.
    """

    def __init__(self, task_id: str):
        super().__init__(detail=f"Task with ID {task_id} not found")


class UserTaskMismatchError(AuthorizationError):
    """
    Exception raised when a user tries to access another user's task.
    """

    def __init__(self):
        super().__init__(detail="User ID in session does not match requested user_id")


class TaskValidationError(ValidationError):
    """
    Exception raised for task-specific validation errors.
    """

    def __init__(self, detail: str = "Task validation failed"):
        super().__init__(detail=detail)


class UserNotFoundError(NotFoundError):
    """
    Exception raised when a requested user is not found.
    """

    def __init__(self, user_id: str):
        super().__init__(detail=f"User with ID {user_id} not found")