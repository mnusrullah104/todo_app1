"""
FastAPI application entry point for Hackathon Todo App.

This module initializes the FastAPI application with all necessary
middleware, exception handlers, and API routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api import health, tasks
from app.core.exceptions import TodoAppException
from app.middleware.error_handler import (
    app_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    generic_exception_handler,
)
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
import os

app = FastAPI(
    title="Todo API",
    description="""
# Hackathon Todo App API

A modern, full-stack todo application backend built with FastAPI.

## Features

- **Task Management**: Full CRUD operations for personal tasks
- **Data Isolation**: Users can only access their own tasks
- **Security**: Rate limiting, input sanitization, security headers
- **Error Handling**: Standardized error responses with request tracking

## Quick Start

1. Register a new account via Better Auth
2. Login with credentials via Better Auth
3. Access your tasks using the authenticated token
4. Create and manage your tasks!

## Authentication

All task endpoints require a valid Better Auth JWT token. Include your JWT token in the Authorization header:

```
Authorization: Bearer your-better-auth-jwt-token-here
```

## Rate Limits

- Task Creation: 10 requests per minute per user
- Task Updates: 20 requests per minute per user
- Task Deletion: 10 requests per minute per user
- Task Retrieval: 30 requests per minute per user
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check endpoint for monitoring"
        },
        {
            "name": "tasks",
            "description": "Task management operations (CRUD)"
        },
    ],
    contact={
        "name": "Todo App Team",
        "email": "support@todoapp.hackathon.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS Configuration - Allow frontend origin
origins = [
    "http://localhost:3000",  # Next.js frontend (development)
    "http://127.0.0.1:3000",
    "http://localhost:3001",  # Next.js frontend when port 3000 is taken
    "http://127.0.0.1:3001",
]

# Allow configuring additional origins via env (.env)
# Example: BACKEND_CORS_ORIGINS=http://192.168.1.50:3000,http://myhost:3000
cors_env = os.getenv("BACKEND_CORS_ORIGINS")
if cors_env:
    origins.extend([o.strip() for o in cors_env.split(",") if o.strip()])

# In development, also allow typical LAN origins (helps when accessing the frontend via Network URL)
environment = os.getenv("ENVIRONMENT", "development").lower()
allow_origin_regex = None
if environment == "development":
    allow_origin_regex = r"^http://(localhost|127\\.0\\.0\\.1|192\\.168\\.\\d+\\.\\d+):(3000|3001)$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Register exception handlers
app.add_exception_handler(TodoAppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Todo API - Phase II",
        "docs": "/docs",
        "health": "/health",
    }