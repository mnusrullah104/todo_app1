"""
Task service for business logic related to task management.

This module contains the business logic for creating, retrieving, updating,
and deleting tasks, ensuring proper data validation and user isolation.
"""
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime
from typing import List, Optional

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse


async def get_user_tasks(user_id: UUID, session: Session) -> TaskListResponse:
    """
    Get all tasks for a specific user.

    Args:
        user_id: The user's UUID
        session: Database session

    Returns:
        TaskListResponse containing all user's tasks ordered by creation date (newest first)
    """
    # Query tasks for the specific user, ordered by creation date (newest first)
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()

    # Convert to response model
    task_responses = [TaskResponse.model_validate(task) for task in tasks]

    return TaskListResponse(tasks=task_responses, total=len(tasks))


async def get_task_by_id(task_id: UUID, user_id: UUID, session: Session) -> TaskResponse:
    """
    Get a specific task by ID for a specific user.

    Args:
        task_id: The task's UUID
        user_id: The user's UUID (for data isolation)
        session: Database session

    Returns:
        TaskResponse for the requested task

    Raises:
        ValueError: If task doesn't exist or doesn't belong to the user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise ValueError(f"Task with ID {task_id} not found for user {user_id}")

    return TaskResponse.model_validate(task)


async def create_task(task_data: TaskCreate, user_id: UUID, session: Session) -> TaskResponse:
    """
    Create a new task for a specific user.

    Args:
        task_data: Task creation data
        user_id: The user's UUID
        session: Database session

    Returns:
        TaskResponse for the created task
    """
    # Create task instance with provided data and user ID
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add to database and commit
    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


async def update_task(task_id: UUID, task_data: TaskUpdate, user_id: UUID, session: Session) -> TaskResponse:
    """
    Update an existing task for a specific user.

    Args:
        task_id: The task's UUID
        task_data: Task update data
        user_id: The user's UUID (for data isolation)
        session: Database session

    Returns:
        TaskResponse for the updated task

    Raises:
        ValueError: If task doesn't exist or doesn't belong to the user
    """
    # Get the existing task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise ValueError(f"Task with ID {task_id} not found for user {user_id}")

    # Update task fields that are provided in task_data
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    # Update the timestamp
    task.updated_at = datetime.utcnow()

    # Commit changes
    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


async def delete_task(task_id: UUID, user_id: UUID, session: Session) -> None:
    """
    Delete a specific task for a specific user.

    Args:
        task_id: The task's UUID
        user_id: The user's UUID (for data isolation)
        session: Database session

    Raises:
        ValueError: If task doesn't exist or doesn't belong to the user
    """
    # Get the existing task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise ValueError(f"Task with ID {task_id} not found for user {user_id}")

    # Delete the task
    session.delete(task)
    session.commit()