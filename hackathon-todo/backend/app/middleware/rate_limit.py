"""
Rate limiting middleware for API endpoints.

This module provides rate limiting functionality to prevent abuse
and ensure fair usage of the API.
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from collections import defaultdict
import time
from typing import Dict, Tuple
import asyncio


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to implement rate limiting for API endpoints.
    Uses a simple in-memory sliding window approach.
    NOTE: For production, use Redis-backed rate limiting.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        # Dictionary to store request timestamps: {(user_id, endpoint): [timestamps]}
        self.requests: Dict[Tuple[str, str], list] = defaultdict(list)
        # Rate limits configuration (requests per minute)
        self.limits = {
            "/api/tasks": {"create": 10, "read": 30, "update": 20, "delete": 10},
            "/api/tasks/": {"read": 30, "update": 20, "delete": 10},  # For specific task endpoints
        }

    def is_rate_limited(self, user_id: str, endpoint: str, method: str) -> bool:
        """
        Check if the user is rate limited for the endpoint/method combination.

        Args:
            user_id: The authenticated user ID
            endpoint: The API endpoint
            method: The HTTP method (GET, POST, etc.)

        Returns:
            True if rate limited, False otherwise
        """
        current_time = time.time()
        window_size = 60  # 60 seconds (1 minute)

        # Determine the appropriate limit based on method
        limit = 0
        if endpoint in self.limits:
            method_lower = method.lower()
            if method_lower == "post":
                limit = self.limits[endpoint].get("create", 10)
            elif method_lower in ["get"]:
                limit = self.limits[endpoint].get("read", 30)
            elif method_lower in ["patch", "put"]:
                limit = self.limits[endpoint].get("update", 20)
            elif method_lower == "delete":
                limit = self.limits[endpoint].get("delete", 10)

        # If no specific limit is configured, allow the request
        if limit == 0:
            return False

        # Clean old requests outside the window
        key = (user_id, endpoint)
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if current_time - req_time < window_size
        ]

        # Check if the user has exceeded the limit
        if len(self.requests[key]) >= limit:
            return True

        # Add current request to the list
        self.requests[key].append(current_time)
        return False

    async def dispatch(self, request: Request, call_next):
        """
        Check rate limits and process the request.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            Response or rate limit error
        """
        # Extract user ID from request state (set by auth middleware)
        user_id = getattr(request.state, "current_user_id", "anonymous")

        # Only apply rate limiting to API endpoints
        if request.url.path.startswith("/api/"):
            # Determine the endpoint for rate limiting (without ID params for fairness)
            endpoint = request.url.path
            # Normalize task endpoints to generic form
            if "/api/tasks/" in endpoint:
                # Replace specific task IDs with placeholder for rate limiting
                import re
                endpoint = re.sub(r'/api/tasks/[^/]+', '/api/tasks/', endpoint)
            elif endpoint.startswith("/api/tasks") and endpoint != "/api/tasks":
                # For other specific task endpoints, use base path
                endpoint = "/api/tasks/"

            # Check if rate limited
            if self.is_rate_limited(user_id, endpoint, request.method):
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": "Too many requests. Please try again later.",
                            "request_id": getattr(request.state, "request_id", "unknown"),
                        }
                    },
                    headers={
                        "Retry-After": "60",  # Suggest retry after 60 seconds
                        "X-RateLimit-Limit": str(self.limits.get(endpoint, {}).get("read", 30)),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + 60),
                    }
                )

        response = await call_next(request)
        return response