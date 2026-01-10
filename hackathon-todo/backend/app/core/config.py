"""
Application configuration settings.

This module contains all configuration settings for the application,
loaded from environment variables with appropriate defaults.
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    DATABASE_URL: str = Field(..., description="Database connection string")

    # Better Auth settings
    BETTER_AUTH_SECRET: str = Field(..., description="Better Auth secret key")
    BETTER_AUTH_URL: str = Field(default="http://localhost:8888", description="Better Auth service URL")

    # Application settings
    PROJECT_NAME: str = "Todo API"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Default Next.js dev server
        "http://localhost:3001",  # Alternative Next.js dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    # Security settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    SECRET_KEY: str = Field(..., description="Secret key for JWT signing")

    # Environment settings
    ENVIRONMENT: str = Field(default="development", description="Environment (development/staging/production)")
    DEBUG: bool = Field(default=False, description="Debug mode")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()