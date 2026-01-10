"""
Task request/response schemas for API validation.

This module defines the Pydantic models for task-related requests and responses.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import UUID
from typing import Optional


class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: Optional[str] = Field(None, max_length=2000, description="Task description (optional, max 2000 characters)")
    completed: bool = Field(False, description="Completion status (default: false)")

    @validator('title')
    def validate_title(cls, v):
        """Validate title is not empty after stripping whitespace"""
        if not v.strip():
            raise ValueError('Title cannot be empty or just whitespace')
        return v.strip()


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (partial updates allowed)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: Optional[str] = Field(None, max_length=2000, description="Task description (max 2000 characters)")
    completed: Optional[bool] = Field(None, description="Completion status")

    @validator('title')
    def validate_title(cls, v):
        """Validate title is not empty after stripping whitespace if provided"""
        if v is not None:
            if not v.strip():
                raise ValueError('Title cannot be empty or just whitespace')
            return v.strip()
        return v


class TaskResponse(BaseModel):
    """Schema for task response"""
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "110e8400-e29b-41d4-a716-446655440000",
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the project",
                "completed": False,
                "created_at": "2026-01-02T10:00:00Z",
                "updated_at": "2026-01-02T10:00:00Z",
            }
        }


class TaskListResponse(BaseModel):
    """Schema for task list response"""
    tasks: list[TaskResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "user_id": "110e8400-e29b-41d4-a716-446655440000",
                        "title": "Complete project documentation",
                        "description": "Write comprehensive documentation for the project",
                        "completed": False,
                        "created_at": "2026-01-02T10:00:00Z",
                        "updated_at": "2026-01-02T10:00:00Z",
                    }
                ],
                "total": 1
            }
        }