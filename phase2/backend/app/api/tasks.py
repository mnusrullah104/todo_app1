"""
Task API endpoints for Phase II Todo App.

Provides REST endpoints for task CRUD operations with JWT authentication.
All endpoints enforce user data isolation - users can only access their own tasks.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.database import get_session
from app.middleware.auth import get_current_user_id
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from app.services import task_service

router = APIRouter()


@router.get(
    "/users/{user_id}/tasks",
    response_model=TaskListResponse,
    summary="Get user's tasks",
    description="Retrieve all tasks for the authenticated user. Returns tasks ordered by creation date (newest first)."
)
async def get_tasks(
    user_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskListResponse:
    """
    Get all tasks for a user.

    Enforces user data isolation - users can only retrieve their own tasks.
    """
    # Verify user is accessing their own tasks
    if current_user_id != user_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other users' tasks"
        )

    return await task_service.get_user_tasks(user_id, session)


@router.get(
    "/users/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a specific task",
    description="Retrieve a single task by ID."
)
async def get_task(
    user_id: UUID,
    task_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a specific task by ID.

    Enforces user data isolation - users can only retrieve their own tasks.
    """
    # Verify user is accessing their own tasks
    if current_user_id != user_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other users' tasks"
        )

    return await task_service.get_task_by_id(task_id, user_id, session)


@router.post(
    "/users/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user."
)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    current_user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for a user.

    Enforces user data isolation - users can only create tasks for themselves.
    """
    # Verify user is creating task for themselves
    if current_user_id != user_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create tasks for other users"
        )

    return await task_service.create_task(task_data, user_id, session)


@router.patch(
    "/users/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task. Only provided fields will be updated."
)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    current_user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update an existing task.

    Enforces user data isolation - users can only update their own tasks.
    """
    # Verify user is updating their own task
    if current_user_id != user_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other users' tasks"
        )

    return await task_service.update_task(task_id, task_data, user_id, session)


@router.delete(
    "/users/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task permanently."
)
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a task.

    Enforces user data isolation - users can only delete their own tasks.
    """
    # Verify user is deleting their own task
    if current_user_id != user_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other users' tasks"
        )

    await task_service.delete_task(task_id, user_id, session)
