# Data Model: Todo Console Application

**Feature**: 001-todo-console-app
**Date**: 2025-12-31
**Purpose**: Define data structures, validation rules, and state management for the Todo application

---

## Overview

The Todo application has a single entity (**Task**) stored in an in-memory dictionary structure managed by the TaskManager service. This document defines the Task structure, validation rules, state transitions, and storage mechanisms.

---

## Entity: Task

### Purpose
Represents a single todo item with unique identifier, content, and completion status.

### Structure

```python
from dataclasses import dataclass

@dataclass
class Task:
    """
    Represents a single todo task.

    Attributes:
        id: Unique positive integer identifier (auto-assigned, never reused)
        title: Task title (required, non-empty string)
        description: Optional task details (can be empty string)
        completed: Completion status (True = complete, False = incomplete)
    """
    id: int
    title: str
    description: str
    completed: bool = False
```

### Field Definitions

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| id | int | Yes | Auto-assigned | Must be positive integer ≥ 1, unique across all tasks (past and present) |
| title | str | Yes | (none) | Must be non-empty after stripping whitespace, max 500 characters |
| description | str | No | "" (empty) | Optional, max 2000 characters |
| completed | bool | Yes | False | True = complete (✔), False = incomplete (✖) |

### Validation Rules

#### Rule 1: ID Uniqueness
- **Requirement**: FR-001, FR-003
- **Rule**: Each task MUST have a unique ID that is never reused, even after deletion
- **Implementation**: Auto-incrementing counter starting at 1, never decrements
- **Violation**: System error (should never occur with proper counter)

#### Rule 2: Title Non-Empty
- **Requirement**: FR-002
- **Rule**: Title MUST be non-empty after stripping leading/trailing whitespace
- **Implementation**: Validate `title.strip() != ""` before task creation/update
- **Violation**: Return Result(False, "Title cannot be empty")

#### Rule 3: Title Length
- **Requirement**: Assumption from spec (reasonable limits)
- **Rule**: Title MUST NOT exceed 500 characters
- **Implementation**: Check `len(title) <= 500`
- **Violation**: Return Result(False, "Title too long (max 500 characters)")

#### Rule 4: Description Length
- **Requirement**: Assumption from spec (reasonable limits)
- **Rule**: Description MUST NOT exceed 2000 characters
- **Implementation**: Check `len(description) <= 2000`
- **Violation**: Return Result(False, "Description too long (max 2000 characters)")

#### Rule 5: Completed Boolean
- **Requirement**: FR-004
- **Rule**: Completed status MUST be boolean (True or False)
- **Implementation**: Type hint enforces this (bool type)
- **Violation**: Type error (should not occur with proper CLI input handling)

---

## State Management

### Storage Structure

**Container**: TaskManager class in src/services/task_manager.py

```python
class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}  # Dictionary keyed by task ID
        self._next_id: int = 1             # Auto-increment counter
```

**Rationale**: Dictionary provides O(1) lookup by ID (primary access pattern) while Python 3.13+ guarantees insertion order preservation for display.

### State Transitions

#### State 1: Task Creation
```
[Empty] → [Incomplete Task]
Trigger: add_task(title, description)
Result: New task with ID = _next_id, completed = False
Side effect: _next_id increments
```

#### State 2: Toggle Completion (Incomplete → Complete)
```
[Incomplete Task] → [Complete Task]
Trigger: toggle_status(task_id) where task.completed == False
Result: task.completed = True
```

#### State 3: Toggle Completion (Complete → Incomplete)
```
[Complete Task] → [Incomplete Task]
Trigger: toggle_status(task_id) where task.completed == True
Result: task.completed = False
```

#### State 4: Task Update
```
[Task] → [Updated Task]
Trigger: update_task(task_id, new_title, new_description)
Result: task.title and/or task.description modified
Invariant: task.id and task.completed unchanged
```

#### State 5: Task Deletion
```
[Task] → [Removed from storage]
Trigger: delete_task(task_id)
Result: Task removed from dictionary
Invariant: _next_id does NOT decrement (ID never reused)
```

### State Invariants

1. **ID Uniqueness**: At any point, no two tasks have the same ID
2. **ID Monotonicity**: _next_id only increases, never decreases
3. **Task Existence**: All tasks in dictionary have valid Task structure
4. **Boolean Status**: completed field is always boolean (True or False)

---

## Data Access Patterns

### Pattern 1: Lookup by ID
**Operation**: Get, Update, Delete, Toggle
**Access**: `self.tasks[task_id]` or `self.tasks.get(task_id)`
**Performance**: O(1)
**Example**: `task = self.tasks.get(task_id)`

### Pattern 2: List All Tasks
**Operation**: View all tasks
**Access**: `self.tasks.values()` or `self.tasks.items()`
**Performance**: O(n) where n = number of tasks
**Example**: `for task in self.tasks.values(): print(task)`

### Pattern 3: Check Existence
**Operation**: Validation before Update/Delete/Toggle
**Access**: `task_id in self.tasks`
**Performance**: O(1)
**Example**: `if task_id not in self.tasks: return error`

---

## Data Lifecycle

### Creation Flow
1. User provides title and description via CLI
2. CLI calls `task_manager.add_task(title, description)`
3. TaskManager validates title (non-empty, length)
4. TaskManager creates Task with:
   - id = current _next_id
   - title = validated title
   - description = description (can be empty)
   - completed = False (default)
5. TaskManager increments _next_id
6. TaskManager stores task: `self.tasks[task.id] = task`
7. Return Result(True, f"Task {task.id} created", data=task)

### Update Flow
1. User provides task_id, new_title, new_description via CLI
2. CLI calls `task_manager.update_task(task_id, new_title, new_description)`
3. TaskManager validates task_id exists
4. TaskManager validates new_title (non-empty, length)
5. TaskManager updates task fields:
   - task.title = new_title
   - task.description = new_description
6. Return Result(True, f"Task {task_id} updated", data=task)

### Toggle Flow
1. User provides task_id via CLI
2. CLI calls `task_manager.toggle_status(task_id)`
3. TaskManager validates task_id exists
4. TaskManager toggles: `task.completed = not task.completed`
5. Return Result(True, f"Task {task_id} marked {'complete' if task.completed else 'incomplete'}", data=task)

### Deletion Flow
1. User provides task_id via CLI
2. CLI calls `task_manager.delete_task(task_id)`
3. TaskManager validates task_id exists
4. TaskManager removes: `del self.tasks[task_id]`
5. Note: _next_id does NOT change (ID never reused)
6. Return Result(True, f"Task {task_id} deleted")

### Viewing Flow
1. User selects "View All Tasks" via CLI
2. CLI calls `task_manager.get_all_tasks()`
3. TaskManager returns list of all tasks: `list(self.tasks.values())`
4. CLI formats and displays each task with status indicator

---

## Validation Summary

### Pre-Conditions (Checked Before Operation)

| Operation | Pre-Condition | Error Message |
|-----------|---------------|---------------|
| Add | title.strip() != "" | "Title cannot be empty" |
| Add | len(title) <= 500 | "Title too long (max 500 characters)" |
| Add | len(description) <= 2000 | "Description too long (max 2000 characters)" |
| Update | task_id in tasks | "Task ID {task_id} not found" |
| Update | title.strip() != "" | "Title cannot be empty" |
| Update | len(title) <= 500 | "Title too long (max 500 characters)" |
| Update | len(description) <= 2000 | "Description too long (max 2000 characters)" |
| Delete | task_id in tasks | "Task ID {task_id} not found" |
| Toggle | task_id in tasks | "Task ID {task_id} not found" |

### Post-Conditions (Guaranteed After Operation)

| Operation | Post-Condition |
|-----------|----------------|
| Add | Task exists with unique ID, completed = False, _next_id incremented |
| Update | Task title/description changed, ID and completed unchanged |
| Delete | Task no longer in dictionary, _next_id unchanged |
| Toggle | Task completed status flipped (True ↔ False) |
| View | Returns current snapshot of all tasks, no state change |

---

## Example Data Instances

### Example 1: New Task (Incomplete)
```python
Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False
)
```
**Display**: `[1] ✖ Buy groceries - Milk, eggs, bread`

### Example 2: Completed Task
```python
Task(
    id=2,
    title="Call dentist",
    description="",
    completed=True
)
```
**Display**: `[2] ✔ Call dentist`

### Example 3: Task with No Description
```python
Task(
    id=3,
    title="Finish report",
    description="",
    completed=False
)
```
**Display**: `[3] ✖ Finish report`

### Example 4: Storage State After Operations
```python
# Initial state
tasks = {}
_next_id = 1

# After add_task("Task A", "Description A")
tasks = {1: Task(1, "Task A", "Description A", False)}
_next_id = 2

# After add_task("Task B", "")
tasks = {
    1: Task(1, "Task A", "Description A", False),
    2: Task(2, "Task B", "", False)
}
_next_id = 3

# After toggle_status(1)
tasks = {
    1: Task(1, "Task A", "Description A", True),  # completed changed
    2: Task(2, "Task B", "", False)
}
_next_id = 3  # unchanged

# After delete_task(1)
tasks = {
    2: Task(2, "Task B", "", False)  # task 1 removed
}
_next_id = 3  # unchanged - ID 1 never reused

# After add_task("Task C", "Description C")
tasks = {
    2: Task(2, "Task B", "", False),
    3: Task(3, "Task C", "Description C", False)  # ID = 3, not 1
}
_next_id = 4  # incremented
```

---

## Performance Characteristics

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| Add | O(1) | O(1) per task | Constant time ID assignment and dictionary insert |
| Get by ID | O(1) | O(1) | Direct dictionary lookup |
| Update | O(1) | O(1) | Lookup + field modification |
| Delete | O(1) | O(1) | Direct dictionary removal |
| Toggle | O(1) | O(1) | Lookup + boolean flip |
| List All | O(n) | O(n) | Must iterate all n tasks |
| Check Exists | O(1) | O(1) | Dictionary membership test |

**Overall Space**: O(n) where n = number of tasks currently stored

**Meets Performance Goals**:
- ✅ SC-001: Task creation <2 seconds (O(1) operation)
- ✅ SC-004: Error messages <1 second (O(1) validation)
- ✅ SC-005: View 100 tasks <3 seconds (O(n) = 100 iterations acceptable)

---

## Edge Cases

### Edge Case 1: Empty Task List
- **State**: `tasks = {}, _next_id = 1`
- **View Operation**: Return empty list, CLI displays "No tasks exist"
- **Delete/Update/Toggle**: Return Result(False, "Task ID not found")

### Edge Case 2: After All Tasks Deleted
- **State**: `tasks = {}, _next_id = N` (where N > 1)
- **Behavior**: Next task gets ID = N (not 1)
- **Rationale**: Maintains ID uniqueness invariant (FR-003)

### Edge Case 3: Large Task List
- **State**: 1000 tasks in dictionary
- **Performance**: O(1) operations remain constant, O(n) view takes ~0.1-1 second (acceptable)
- **Memory**: ~1MB for 1000 tasks (well under 100MB constraint)

### Edge Case 4: Special Characters in Title/Description
- **Input**: Title = "Task with "quotes" and \n newlines"
- **Storage**: Stored as-is (Python strings handle UTF-8)
- **Display**: CLI may need to escape/format for readability

### Edge Case 5: ID Counter Overflow
- **Scenario**: _next_id reaches max integer (2^63-1 in Python)
- **Likelihood**: Negligible (1M tasks requirement << 2^63)
- **Mitigation**: Not needed for Phase I scope

---

## Integration with Services Layer

### TaskManager Interface

```python
class TaskManager:
    def add_task(self, title: str, description: str) -> Result:
        """Create new task with validated inputs"""

    def get_all_tasks(self) -> Result:
        """Return list of all tasks"""

    def get_task(self, task_id: int) -> Result:
        """Return single task by ID"""

    def update_task(self, task_id: int, title: str, description: str) -> Result:
        """Update existing task"""

    def delete_task(self, task_id: int) -> Result:
        """Remove task from storage"""

    def toggle_status(self, task_id: int) -> Result:
        """Flip task completion status"""
```

**Result Object Structure**:
```python
@dataclass
class Result:
    success: bool           # True = operation succeeded, False = error
    message: str            # Human-readable outcome/error message
    data: Any = None        # Optional return value (e.g., Task object or list)
```

---

## References

- **Spec**: [spec.md](./spec.md) - Functional requirements (FR-001 through FR-013)
- **Plan**: [plan.md](./plan.md) - Architecture decisions
- **Research**: [research.md](./research.md) - Decision rationale

---

## Conclusion

The Task data model is intentionally simple with clear validation rules and state transitions. The dictionary-based storage provides efficient O(1) operations for all single-task operations while maintaining insertion order for display. All design decisions align with constitution principles (simplicity, standard library, clean architecture) and meet specification requirements.

**Status**: ✅ Data model complete - ready for contracts and quickstart
