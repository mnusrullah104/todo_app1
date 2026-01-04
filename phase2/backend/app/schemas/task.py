"""
Task schemas for Phase II Todo App API.

Request/response models for task operations.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from app.core.sanitization import sanitize_string


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: str | None = Field(None, max_length=2000, description="Optional task description (max 2000 characters)")

    @field_validator('title')
    @classmethod
    def sanitize_title(cls, v: str) -> str:
        """Sanitize title to prevent XSS attacks."""
        sanitized = sanitize_string(v, max_length=200)
        if not sanitized or len(sanitized) == 0:
            raise ValueError("Title cannot be empty after sanitization")
        return sanitized

    @field_validator('description')
    @classmethod
    def sanitize_description(cls, v: str | None) -> str | None:
        """Sanitize description to prevent XSS attacks."""
        if v is None:
            return None
        return sanitize_string(v, max_length=2000)


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: str | None = Field(None, min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: str | None = Field(None, max_length=2000, description="Task description (max 2000 characters)")
    completed: bool | None = Field(None, description="Task completion status")

    @field_validator('title')
    @classmethod
    def sanitize_title(cls, v: str | None) -> str | None:
        """Sanitize title to prevent XSS attacks."""
        if v is None:
            return None
        sanitized = sanitize_string(v, max_length=200)
        if sanitized is not None and len(sanitized) == 0:
            raise ValueError("Title cannot be empty after sanitization")
        return sanitized

    @field_validator('description')
    @classmethod
    def sanitize_description(cls, v: str | None) -> str | None:
        """Sanitize description to prevent XSS attacks."""
        if v is None:
            return None
        return sanitize_string(v, max_length=2000)


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: UUID = Field(..., description="Task unique identifier")
    user_id: UUID = Field(..., description="User ID (owner of this task)")
    title: str = Field(..., description="Task title")
    description: str | None = Field(None, description="Task description")
    completed: bool = Field(..., description="Task completion status")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }


class TaskListResponse(BaseModel):
    """Schema for task list response."""
    tasks: list[TaskResponse] = Field(..., description="List of user's tasks")
    total: int = Field(..., description="Total number of tasks")

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "user_id": "123e4567-e89b-12d3-a456-426614174001",
                        "title": "Buy groceries",
                        "description": "Milk, eggs, bread",
                        "completed": False,
                        "created_at": "2024-01-01T12:00:00Z",
                        "updated_at": "2024-01-01T12:00:00Z"
                    }
                ],
                "total": 1
            }
        }
