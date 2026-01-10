"""
Task API endpoints for Hackathon Todo App.

Provides REST endpoints for task CRUD operations with Better Auth authentication.
All endpoints enforce user data isolation - users can only access their own tasks.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.database import get_session
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from app.services.task_service import get_user_tasks, get_task_by_id, create_task as service_create_task, update_task as service_update_task, delete_task as service_delete_task
from app.auth.middleware import require_auth_dependency

router = APIRouter()


@router.get(
    "/tasks",
    response_model=TaskListResponse,
    summary="Get user's tasks",
    description="Retrieve all tasks for the authenticated user. Returns tasks ordered by creation date (newest first)."
)
async def get_tasks(
    current_user_id: UUID = Depends(require_auth_dependency),
    session: Session = Depends(get_session)
) -> TaskListResponse:
    """
    Get all tasks for the authenticated user.

    Enforces user data isolation - users can only retrieve their own tasks.
    """
    # Verify user is accessing their own tasks by using the authenticated user ID
    return await get_user_tasks(current_user_id, session)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a specific task",
    description="Retrieve a single task by ID."
)
async def get_task(
    task_id: UUID,
    current_user_id: UUID = Depends(require_auth_dependency),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a specific task by ID.

    Enforces user data isolation - users can only retrieve their own tasks.
    """
    # Verify user is accessing their own task by using the authenticated user ID
    return await get_task_by_id(task_id, current_user_id, session)


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user."
)
async def create_task_endpoint(
    task_data: TaskCreate,
    current_user_id: UUID = Depends(require_auth_dependency),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Enforces user data isolation - users can only create tasks for themselves.
    """
    # Create task for the authenticated user
    return await service_create_task(task_data, current_user_id, session)


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task. Only provided fields will be updated."
)
async def update_task_endpoint(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user_id: UUID = Depends(require_auth_dependency),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update an existing task.

    Enforces user data isolation - users can only update their own tasks.
    """
    # Verify user is updating their own task by using the authenticated user ID
    return await service_update_task(task_id, task_data, current_user_id, session)


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task permanently."
)
async def delete_task_endpoint(
    task_id: UUID,
    current_user_id: UUID = Depends(require_auth_dependency),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a task.

    Enforces user data isolation - users can only delete their own tasks.
    """
    # Verify user is deleting their own task by using the authenticated user ID
    await service_delete_task(task_id, current_user_id, session)