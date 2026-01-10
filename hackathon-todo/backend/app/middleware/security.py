"""
Security middleware for FastAPI application.

This module provides security-related middleware for the application,
including security headers and other protective measures.
"""
from fastapi import Request, Response
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import secrets
import string


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Add security headers to the response.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            Response with security headers added
        """
        # Generate a unique request ID for tracking
        request_id = "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(16)
        )
        request.state.request_id = request_id

        # Call the next middleware/handler
        response = await call_next(request)

        # Add security headers to the response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        # Content Security Policy - restricts sources for various content types
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' http://localhost:* https://api.better-auth.com; "
            "frame-ancestors 'none'; "
            "object-src 'none'; "
            "base-uri 'self';"
        )

        # Cache control for sensitive data
        if request.url.path.startswith("/api/") and "auth" not in request.url.path:
            # Don't cache authenticated API responses by default
            response.headers.setdefault("Cache-Control", "no-store")

        return response