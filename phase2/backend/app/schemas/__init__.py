"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel
from typing import Optional


class MessageResponse(BaseModel):
    """Standard message response format"""
    message: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    database: str
