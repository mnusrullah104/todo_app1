"""
Rate limiting middleware using in-memory storage.

For production, consider using Redis-backed rate limiting (slowapi + redis)
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple
import threading


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter.

    Note: This implementation is for development/testing.
    For production, use Redis-backed rate limiting (e.g., slowapi with Redis)
    """

    def __init__(self):
        self._requests: Dict[str, list[datetime]] = defaultdict(list)
        self._lock = threading.Lock()

    def is_rate_limited(
        self,
        key: str,
        max_requests: int,
        window_seconds: int
    ) -> Tuple[bool, int]:
        """
        Check if key is rate limited.

        Returns:
            (is_limited, retry_after_seconds)
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)

        with self._lock:
            # Clean up old requests
            self._requests[key] = [
                req_time for req_time in self._requests[key]
                if req_time > window_start
            ]

            # Check rate limit
            if len(self._requests[key]) >= max_requests:
                oldest_request = min(self._requests[key])
                retry_after = int((oldest_request + timedelta(seconds=window_seconds) - now).total_seconds()) + 1
                return True, max(retry_after, 1)

            # Record this request
            self._requests[key] = []
            return False, 0

    def clean_old_entries(self, max_age_seconds: int = 3600):
        """Clean entries older than max_age_seconds"""
        cutoff = datetime.utcnow() - timedelta(seconds=max_age_seconds)

        with self._lock:
            keys_to_delete = []
            for key, requests in self._requests.items():
                if not requests or max(requests) < cutoff:
                    keys_to_delete.append(key)

            for key in keys_to_delete:
                del self._requests[key]


# Global rate limiter instance
rate_limiter = InMemoryRateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware for authentication endpoints.

    Limits:
    - /auth/register: 5 requests per 15 minutes per IP
    - /auth/login: 10 requests per 15 minutes per IP
    """

    # Rate limit configurations (endpoint_pattern: (max_requests, window_seconds))
    RATE_LIMITS = {
        "/auth/register": (5, 900),   # 5 requests per 15 minutes
        "/auth/login": (10, 900),      # 10 requests per 15 minutes
    }

    def get_client_ip(self, request: Request) -> str:
        """Extract client IP address"""
        # Check for X-Forwarded-For header (behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # Fall back to direct client IP
        return request.client.host if request.client else "unknown"

    async def dispatch(self, request: Request, call_next):
        # Check if this endpoint has rate limiting
        endpoint = request.url.path
        if endpoint not in self.RATE_LIMITS:
            return await call_next(request)

        # Get rate limit config
        max_requests, window_seconds = self.RATE_LIMITS[endpoint]

        # Create rate limit key (IP + endpoint)
        client_ip = self.get_client_ip(request)
        rate_limit_key = f"{client_ip}:{endpoint}"

        # Check rate limit
        is_limited, retry_after = rate_limiter.is_rate_limited(
            rate_limit_key,
            max_requests,
            window_seconds
        )

        if is_limited:
            # Return 429 Too Many Requests
            from app.schemas.error import ErrorResponse, ErrorDetail
            from datetime import datetime

            error_response = ErrorResponse(
                success=False,
                error=ErrorDetail(
                    code="RATE_LIMIT_EXCEEDED",
                    message=f"Too many requests. Please try again in {retry_after} seconds.",
                    details={"retry_after": retry_after}
                ),
                timestamp=datetime.utcnow(),
            )

            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content=error_response.model_dump(exclude_none=True),
                headers={"Retry-After": str(retry_after)}
            )

        # Process request
        response = await call_next(request)

        # Add rate limit info headers
        response.headers["X-RateLimit-Limit"] = str(max_requests)
        response.headers["X-RateLimit-Window"] = str(window_seconds)

        return response
