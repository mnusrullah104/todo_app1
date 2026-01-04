"""Task management service with CRUD operations."""

from dataclasses import dataclass
from typing import Any

from src.models.task import Task


@dataclass
class Result:
    """
    Represents the result of a service operation.

    Attributes:
        success: True if operation succeeded, False if error occurred
        message: Human-readable outcome or error message
        data: Optional return value (e.g., Task object, list of tasks, None)
    """

    success: bool
    message: str
    data: Any = None


class TaskManager:
    """
    Manages task storage and CRUD operations.

    Uses in-memory dictionary for O(1) task lookups by ID.
    Task IDs are auto-incremented and never reused.
    """

    def __init__(self):
        """Initialize empty task storage."""
        self.tasks: dict[int, Task] = {}  # Dictionary keyed by task ID
        self._next_id: int = 1  # Auto-increment counter for task IDs

    def add_task(self, title: str, description: str = "") -> Result:
        """
        Create a new task with validated inputs.

        Args:
            title: Task title (required, non-empty, max 500 characters)
            description: Optional task description (max 2000 characters)

        Returns:
            Result object with success status, message, and created Task
        """
        # Validate title
        if not title or not title.strip():
            return Result(False, "Title cannot be empty")

        if len(title) > 500:
            return Result(False, "Title too long (max 500 characters)")

        # Validate description
        if len(description) > 2000:
            return Result(False, "Description too long (max 2000 characters)")

        # Create task
        try:
            task = Task(
                id=self._next_id,
                title=title.strip(),
                description=description.strip(),
                completed=False,
            )
            self.tasks[task.id] = task
            self._next_id += 1

            return Result(
                True,
                f"Task {task.id} created successfully",
                data=task,
            )
        except ValueError as e:
            return Result(False, str(e))

    def get_all_tasks(self) -> Result:
        """
        Return all tasks in storage.

        Returns:
            Result object with success status and list of all tasks
        """
        tasks_list = list(self.tasks.values())
        return Result(
            True,
            f"Retrieved {len(tasks_list)} task(s)",
            data=tasks_list,
        )

    def toggle_status(self, task_id: int) -> Result:
        """
        Toggle task completion status between complete and incomplete.

        Args:
            task_id: ID of task to toggle

        Returns:
            Result object with success status, message, and updated Task
        """
        # Validate task exists
        if task_id not in self.tasks:
            return Result(False, f"Task ID {task_id} not found")

        # Toggle status
        task = self.tasks[task_id]
        task.completed = not task.completed

        status_text = "complete" if task.completed else "incomplete"
        return Result(
            True,
            f"Task {task_id} marked {status_text}",
            data=task,
        )

    def update_task(
        self, task_id: int, new_title: str | None = None, new_description: str | None = None
    ) -> Result:
        """
        Update task title and/or description.

        Args:
            task_id: ID of task to update
            new_title: New title (None to keep current)
            new_description: New description (None to keep current)

        Returns:
            Result object with success status, message, and updated Task
        """
        # Validate task exists
        if task_id not in self.tasks:
            return Result(False, f"Task ID {task_id} not found")

        task = self.tasks[task_id]

        # Update title if provided
        if new_title is not None:
            if not new_title or not new_title.strip():
                return Result(False, "Title cannot be empty")
            if len(new_title) > 500:
                return Result(False, "Title too long (max 500 characters)")
            task.title = new_title.strip()

        # Update description if provided
        if new_description is not None:
            if len(new_description) > 2000:
                return Result(False, "Description too long (max 2000 characters)")
            task.description = new_description.strip()

        return Result(
            True,
            f"Task {task_id} updated successfully",
            data=task,
        )

    def delete_task(self, task_id: int) -> Result:
        """
        Delete a task from storage.

        Args:
            task_id: ID of task to delete

        Returns:
            Result object with success status and message
        """
        # Validate task exists
        if task_id not in self.tasks:
            return Result(False, f"Task ID {task_id} not found")

        # Delete task
        del self.tasks[task_id]

        return Result(
            True,
            f"Task {task_id} deleted successfully",
        )
