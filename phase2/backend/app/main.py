"""
FastAPI application entry point for Phase II Todo Web Application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.api import health, auth, tasks
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
# Phase II Todo Web Application API

A modern, full-stack todo application backend built with FastAPI.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Task Management**: Full CRUD operations for personal tasks
- **Data Isolation**: Users can only access their own tasks
- **Security**: Rate limiting, input sanitization, security headers
- **Error Handling**: Standardized error responses with request tracking

## Quick Start

1. Register a new account at `/auth/register`
2. Login at `/auth/login` to receive a JWT token
3. Include the token in the `Authorization: Bearer <token>` header
4. Create and manage your tasks!

## Authentication

All task endpoints require authentication. Include your JWT token in the Authorization header:

```
Authorization: Bearer your-jwt-token-here
```

## Rate Limits

- Registration: 5 requests per 15 minutes
- Login: 10 requests per 15 minutes

## Resources

- [Frontend Repository](#)
- [Documentation](#)
- [GitHub Issues](#)
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
            "name": "authentication",
            "description": "User registration and login operations"
        },
        {
            "name": "tasks",
            "description": "Task management operations (CRUD)"
        },
    ],
    contact={
        "name": "Todo App Team",
        "email": "support@todoapp.example.com",
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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(tasks.router, tags=["tasks"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Todo API - Phase II",
        "docs": "/docs",
        "health": "/health",
    }
