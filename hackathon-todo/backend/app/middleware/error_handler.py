"""
Error handler middleware for consistent error responses.

This module provides standardized exception handlers for various error types
to ensure consistent error responses across the application.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
import logging
from typing import Union

from app.core.exceptions import TodoAppException

# Set up logging
logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: TodoAppException) -> JSONResponse:
    """
    Handle custom application exceptions.

    Args:
        request: The HTTP request that caused the exception
        exc: The TodoAppException instance

    Returns:
        JSONResponse with standardized error format
    """
    error_response = {
        "error": {
            "code": exc.code,
            "message": exc.detail,
            "request_id": getattr(request.state, "request_id", "unknown"),
        }
    }

    # Log the error with context
    logger.error(
        f"App exception: {exc.code} - {exc.detail}",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "url": str(request.url),
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle request validation errors.

    Args:
        request: The HTTP request that caused the exception
        exc: The RequestValidationError instance

    Returns:
        JSONResponse with standardized validation error format
    """
    # Format validation errors
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error['loc']),
            "message": error['msg'],
            "type": error['type'],
        })

    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": errors,
            "request_id": getattr(request.state, "request_id", "unknown"),
        }
    }

    # Log the validation error
    logger.warning(
        f"Validation error: {len(errors)} validation errors",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "url": str(request.url),
            "method": request.method,
            "errors": [e["message"] for e in errors],
        },
    )

    return JSONResponse(
        status_code=422,  # Unprocessable Entity
        content=error_response,
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    Handle database-related errors.

    Args:
        request: The HTTP request that caused the exception
        exc: The SQLAlchemyError instance

    Returns:
        JSONResponse with standardized database error format
    """
    error_response = {
        "error": {
            "code": "DATABASE_ERROR",
            "message": "Database operation failed",
            "request_id": getattr(request.state, "request_id", "unknown"),
        }
    }

    # Log the database error
    logger.error(
        f"Database error: {str(exc)}",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "url": str(request.url),
            "method": request.method,
            "exception_type": type(exc).__name__,
        },
    )

    return JSONResponse(
        status_code=500,
        content=error_response,
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected errors.

    Args:
        request: The HTTP request that caused the exception
        exc: The generic Exception instance

    Returns:
        JSONResponse with standardized error format
    """
    error_response = {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
            "request_id": getattr(request.state, "request_id", "unknown"),
        }
    }

    # Log the full traceback for debugging
    logger.error(
        f"Unexpected error: {str(exc)}",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "url": str(request.url),
            "method": request.method,
            "traceback": traceback.format_exc(),
        },
    )

    return JSONResponse(
        status_code=500,
        content=error_response,
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions.

    Args:
        request: The HTTP request that caused the exception
        exc: The StarletteHTTPException instance

    Returns:
        JSONResponse with standardized error format
    """
    error_response = {
        "error": {
            "code": f"HTTP_{exc.status_code}",
            "message": exc.detail,
            "request_id": getattr(request.state, "request_id", "unknown"),
        }
    }

    # Log the HTTP error
    logger.warning(
        f"HTTP error: {exc.status_code} - {exc.detail}",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "url": str(request.url),
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
        headers=exc.headers,
    )