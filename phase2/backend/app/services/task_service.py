"""
Task service for Phase II Todo App.

Business logic for task CRUD operations with user data isolation.
"""
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate


async def get_user_tasks(user_id: UUID, session: Session) -> TaskListResponse:
    """
    Retrieve all tasks for a specific user.

    Args:
        user_id: User's unique identifier
        session: Database session

    Returns:
        TaskListResponse with user's tasks and total count
    """
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()

    return TaskListResponse(
        tasks=[TaskResponse.model_validate(task) for task in tasks],
        total=len(tasks)
    )


async def get_task_by_id(task_id: UUID, user_id: UUID, session: Session) -> TaskResponse:
    """
    Retrieve a specific task by ID.

    Args:
        task_id: Task's unique identifier
        user_id: User's unique identifier (for access verification)
        session: Database session

    Returns:
        TaskResponse

    Raises:
        HTTPException: 404 if task not found or doesn't belong to user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found or access denied"
        )

    return TaskResponse.model_validate(task)


async def create_task(task_data: TaskCreate, user_id: UUID, session: Session) -> TaskResponse:
    """
    Create a new task for a user.

    Args:
        task_data: Task creation data
        user_id: User's unique identifier
        session: Database session

    Returns:
        TaskResponse for the newly created task
    """
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    user_id: UUID,
    session: Session
) -> TaskResponse:
    """
    Update an existing task.

    Args:
        task_id: Task's unique identifier
        task_data: Task update data
        user_id: User's unique identifier (for access verification)
        session: Database session

    Returns:
        TaskResponse for the updated task

    Raises:
        HTTPException: 404 if task not found or doesn't belong to user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found or access denied"
        )

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


async def delete_task(task_id: UUID, user_id: UUID, session: Session) -> None:
    """
    Delete a task.

    Args:
        task_id: Task's unique identifier
        user_id: User's unique identifier (for access verification)
        session: Database session

    Raises:
        HTTPException: 404 if task not found or doesn't belong to user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found or access denied"
        )

    session.delete(task)
    session.commit()
