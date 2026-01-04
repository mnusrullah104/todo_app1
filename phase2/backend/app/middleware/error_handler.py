"""
Global error handling middleware with standardized error responses.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import TodoAppException
from app.schemas.error import ErrorResponse, ErrorDetail
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


def get_request_id(request: Request) -> str:
    """Get or generate request ID for tracking."""
    return request.headers.get("X-Request-ID", f"req_{uuid.uuid4().hex[:12]}")


def log_error_with_context(request: Request, exc: Exception, request_id: str):
    """Log error with full request context."""
    logger.error(
        f"[{request_id}] Error processing request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        },
        exc_info=True,
    )


async def app_exception_handler(request: Request, exc: TodoAppException):
    """
    Handle custom application exceptions with standardized format.
    """
    request_id = get_request_id(request)

    log_error_with_context(request, exc, request_id)

    error_response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code=exc.code,
            message=exc.message,
            field=exc.field,
            details=exc.details,
        ),
        timestamp=datetime.utcnow(),
        request_id=request_id,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(mode='json', exclude_none=True),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors (422 Unprocessable Entity).
    """
    request_id = get_request_id(request)

    log_error_with_context(request, exc, request_id)

    # Extract first validation error for cleaner message
    errors = exc.errors()
    first_error = errors[0] if errors else {}
    field = ".".join(str(loc) for loc in first_error.get("loc", [])[1:])  # Skip 'body'
    message = first_error.get("msg", "Validation error")

    error_response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message=message,
            field=field if field else None,
            details={"errors": errors} if len(errors) > 1 else None,
        ),
        timestamp=datetime.utcnow(),
        request_id=request_id,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(mode='json', exclude_none=True),
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle database errors (503 Service Unavailable).
    """
    request_id = get_request_id(request)

    log_error_with_context(request, exc, request_id)

    error_response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code="DATABASE_ERROR",
            message="Database temporarily unavailable. Please retry in 30 seconds.",
        ),
        timestamp=datetime.utcnow(),
        request_id=request_id,
    )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=error_response.model_dump(mode='json', exclude_none=True),
        headers={"Retry-After": "30"},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected errors (500 Internal Server Error).
    Log details but return generic message to client.
    """
    request_id = get_request_id(request)

    log_error_with_context(request, exc, request_id)

    error_response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please try again later.",
        ),
        timestamp=datetime.utcnow(),
        request_id=request_id,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(mode='json', exclude_none=True),
    )
