"""Task data model."""

from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single todo task.

    Attributes:
        id: Unique positive integer identifier (auto-assigned, never reused)
        title: Task title (required, non-empty string, max 500 characters)
        description: Optional task details (can be empty string, max 2000 characters)
        completed: Completion status (True = complete, False = incomplete)
    """

    id: int
    title: str
    description: str
    completed: bool = False

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Task ID must be a positive integer")
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 500:
            raise ValueError("Title too long (max 500 characters)")
        if len(self.description) > 2000:
            raise ValueError("Description too long (max 2000 characters)")
