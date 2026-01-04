# CLI Interface Contract: Todo Console Application

**Feature**: 001-todo-console-app
**Date**: 2025-12-31
**Purpose**: Define the command-line interface contract for user interactions

---

## Overview

This document specifies the CLI interface contract including menu structure, input/output formats, error messages, and interaction flows for all 5 CRUD operations.

---

## Main Menu

### Display Format

```
=== Todo Console Application ===

Current Tasks: 5 (3 incomplete, 2 complete)

Menu Options:
1. Add New Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6):
```

### Input Validation

**Valid Input**: Integer 1-6
**Invalid Input Handling**:
- Non-integer: Display "Invalid input. Please enter a number between 1 and 6."
- Out of range: Display "Invalid choice. Please enter a number between 1 and 6."
- Empty input: Display "No input received. Please enter a number between 1-6."

### Exit Behavior

**Input**: 6
**Output**:
```
Thank you for using Todo App. Goodbye!
```
**Action**: Program terminates with exit code 0

---

## Operation 1: Add New Task

### User Flow

```
You selected: Add New Task

Enter task title (required): Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread

✓ Task created successfully!
Task ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Incomplete (✖)

Press Enter to continue...
```

### Input Specifications

| Field | Required | Max Length | Validation |
|-------|----------|------------|------------|
| Title | Yes | 500 chars | Non-empty after strip() |
| Description | No | 2000 chars | Can be empty |

### Success Response

```
✓ Task created successfully!
Task ID: {id}
Title: {title}
Description: {description}
Status: Incomplete (✖)
```

### Error Responses

#### Error 1: Empty Title
**Condition**: User presses Enter without typing title
**Response**:
```
✗ Error: Title cannot be empty.
Please enter a valid title:
```
**Action**: Re-prompt for title (up to 3 attempts, then return to menu)

#### Error 2: Title Too Long
**Condition**: len(title) > 500
**Response**:
```
✗ Error: Title too long (max 500 characters).
Please enter a shorter title:
```

#### Error 3: Description Too Long
**Condition**: len(description) > 2000
**Response**:
```
✗ Error: Description too long (max 2000 characters).
Please enter a shorter description:
```

---

## Operation 2: View All Tasks

### User Flow (With Tasks)

```
You selected: View All Tasks

=== Your Tasks ===

[1] ✖ Buy groceries
    Milk, eggs, bread

[2] ✔ Call dentist

[3] ✖ Finish report
    Due by end of week

Total: 3 tasks (2 incomplete, 1 complete)

Press Enter to continue...
```

### User Flow (Empty List)

```
You selected: View All Tasks

=== Your Tasks ===

No tasks found. Add your first task using option 1!

Press Enter to continue...
```

### Display Format Specification

**Task Entry Format**:
```
[{id}] {status_icon} {title}
    {description}  ← only if description is non-empty
```

**Status Icons**:
- Incomplete: ✖
- Complete: ✔

**Ordering**: Tasks displayed in creation order (dictionary insertion order)

**Summary Line**:
```
Total: {count} task(s) ({incomplete_count} incomplete, {complete_count} complete)
```

---

## Operation 3: Update Task

### User Flow

```
You selected: Update Task

Enter task ID to update: 1

Current task details:
[1] ✖ Buy groceries
    Milk, eggs, bread

Enter new title (leave blank to keep current): Buy groceries and snacks
Enter new description (leave blank to keep current): Milk, eggs, bread, chips

✓ Task updated successfully!
Task ID: 1
Title: Buy groceries and snacks
Description: Milk, eggs, bread, chips
Status: Incomplete (✖)

Press Enter to continue...
```

### Input Specifications

| Field | Required | Behavior |
|-------|----------|----------|
| Task ID | Yes | Must exist in storage |
| New Title | No | If empty, keep current title |
| New Description | No | If empty, keep current description |

### Success Response

```
✓ Task updated successfully!
Task ID: {id}
Title: {new_title}
Description: {new_description}
Status: {status}
```

### Error Responses

#### Error 1: Task Not Found
**Condition**: task_id not in storage
**Response**:
```
✗ Error: Task ID {id} not found.
Please enter a valid task ID:
```
**Action**: Re-prompt for task ID (up to 3 attempts, then return to menu)

#### Error 2: Both Fields Empty
**Condition**: User leaves both title and description blank
**Response**:
```
✗ Error: At least one field must be updated.
Please enter a new title or description:
```
**Action**: Re-prompt for fields

#### Error 3: New Title Empty (if provided)
**Condition**: User enters whitespace-only title
**Response**:
```
✗ Error: Title cannot be empty.
Please enter a valid title or leave blank to keep current:
```

---

## Operation 4: Delete Task

### User Flow

```
You selected: Delete Task

Enter task ID to delete: 2

Task to delete:
[2] ✔ Call dentist

Are you sure you want to delete this task? (y/n): y

✓ Task deleted successfully!
Task ID 2 has been removed.

Press Enter to continue...
```

### Input Specifications

| Field | Required | Validation |
|-------|----------|------------|
| Task ID | Yes | Must exist in storage |
| Confirmation | Yes | Must be 'y' or 'n' (case-insensitive) |

### Success Response

```
✓ Task deleted successfully!
Task ID {id} has been removed.
```

### Error Responses

#### Error 1: Task Not Found
**Condition**: task_id not in storage
**Response**:
```
✗ Error: Task ID {id} not found.
Please enter a valid task ID:
```

#### Error 2: Deletion Cancelled
**Condition**: User enters 'n' for confirmation
**Response**:
```
Deletion cancelled. Task {id} was not deleted.
```

#### Error 3: Invalid Confirmation
**Condition**: User enters anything other than 'y' or 'n'
**Response**:
```
Invalid input. Please enter 'y' to confirm or 'n' to cancel:
```

---

## Operation 5: Toggle Task Status

### User Flow (Incomplete → Complete)

```
You selected: Toggle Task Status

Enter task ID to toggle: 1

Current status:
[1] ✖ Buy groceries - Incomplete

✓ Status toggled successfully!
[1] ✔ Buy groceries - Complete

Press Enter to continue...
```

### User Flow (Complete → Incomplete)

```
You selected: Toggle Task Status

Enter task ID to toggle: 1

Current status:
[1] ✔ Buy groceries - Complete

✓ Status toggled successfully!
[1] ✖ Buy groceries - Incomplete

Press Enter to continue...
```

### Input Specifications

| Field | Required | Validation |
|-------|----------|------------|
| Task ID | Yes | Must exist in storage |

### Success Response

```
✓ Status toggled successfully!
[{id}] {new_status_icon} {title} - {new_status_text}
```

### Error Responses

#### Error 1: Task Not Found
**Condition**: task_id not in storage
**Response**:
```
✗ Error: Task ID {id} not found.
Please enter a valid task ID:
```

---

## Input Validation Standards

### Integer Input (Task ID, Menu Choice)

```python
def get_integer_input(prompt: str, min_val: int, max_val: int, max_attempts: int = 3) -> int | None:
    """
    Prompt user for integer within range.
    Returns integer or None if max attempts exceeded.
    """
```

**Behavior**:
- Strip whitespace from input
- Validate input is integer
- Validate input in range [min_val, max_val]
- Re-prompt on invalid input
- Return None after max_attempts failures

### String Input (Title, Description)

```python
def get_string_input(prompt: str, required: bool, max_length: int) -> str:
    """
    Prompt user for string with validation.
    Returns validated string.
    """
```

**Behavior**:
- Strip leading/trailing whitespace
- Validate non-empty if required
- Validate length <= max_length
- Re-prompt on validation failure
- Empty string allowed if not required

### Yes/No Confirmation

```python
def get_confirmation(prompt: str) -> bool:
    """
    Prompt user for yes/no confirmation.
    Returns True for yes, False for no.
    """
```

**Behavior**:
- Accept 'y', 'Y', 'yes', 'Yes', 'YES' as True
- Accept 'n', 'N', 'no', 'No', 'NO' as False
- Re-prompt on invalid input

---

## Error Message Standards

### Format

```
✗ Error: {error_description}
{optional_guidance}
```

### Examples

| Scenario | Error Message |
|----------|---------------|
| Task not found | ✗ Error: Task ID 999 not found.<br>Please enter a valid task ID: |
| Empty title | ✗ Error: Title cannot be empty.<br>Please enter a valid title: |
| Title too long | ✗ Error: Title too long (max 500 characters).<br>Please enter a shorter title: |
| Invalid menu choice | ✗ Error: Invalid choice. Please enter a number between 1 and 6. |
| Invalid integer | ✗ Error: Invalid input. Please enter a number. |

### Tone

- Clear and actionable
- Polite and non-judgmental
- Includes guidance on how to fix the error
- Uses symbols: ✓ for success, ✗ for error, ✖ for incomplete, ✔ for complete

---

## Display Formatting Standards

### Colors (Optional Enhancement)

For Phase I, plain text output is sufficient. Future enhancement could add:
- Green for success messages (✓)
- Red for error messages (✗)
- Yellow for warnings
- Bold for task titles

### Alignment

```
[  1] ✖ Short title
[999] ✔ Another title
```
**Rule**: Right-align task IDs within consistent width (e.g., 3 digits)

### Line Spacing

- One blank line between menu and options
- One blank line before "Press Enter to continue..."
- Two blank lines between operations for visual separation

---

## Screen Management

### Clear Screen (Optional)

**Not implemented in Phase I** - output scrolls naturally in terminal

Future enhancement: Use `os.system('clear')` or `os.system('cls')` to clear screen before each menu display

### Pagination (Out of Scope)

**Not implemented in Phase I** - all tasks displayed at once

Future enhancement: Paginate task list if >20 tasks

---

## Accessibility Considerations

### Unicode Support

- Status icons (✖, ✔) use Unicode characters
- Ensure terminal supports UTF-8 encoding
- Fall back to ASCII ([ ], [X]) if Unicode fails (future enhancement)

### Keyboard Navigation

- All interactions use standard keyboard input (no arrow keys, function keys)
- Enter key used for confirmation
- Ctrl+C allows immediate exit (standard terminal behavior)

---

## Performance Requirements

| Operation | Max Response Time | Requirement |
|-----------|-------------------|-------------|
| Display menu | <100ms | Instant feedback |
| Add task | <2 seconds | SC-001 |
| View tasks (100 items) | <3 seconds | SC-005 |
| Update task | <1 second | Standard CRUD |
| Delete task | <1 second | Standard CRUD |
| Toggle status | <1 second | Standard CRUD |
| Error message | <1 second | SC-004 |

---

## Example Complete Session

```
=== Todo Console Application ===

Current Tasks: 0 (0 incomplete, 0 complete)

Menu Options:
1. Add New Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6): 1

You selected: Add New Task

Enter task title (required): Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread

✓ Task created successfully!
Task ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Incomplete (✖)

Press Enter to continue...

=== Todo Console Application ===

Current Tasks: 1 (1 incomplete, 0 complete)

Menu Options:
1. Add New Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6): 2

You selected: View All Tasks

=== Your Tasks ===

[1] ✖ Buy groceries
    Milk, eggs, bread

Total: 1 task (1 incomplete, 0 complete)

Press Enter to continue...

=== Todo Console Application ===

Current Tasks: 1 (1 incomplete, 0 complete)

Menu Options:
1. Add New Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6): 5

You selected: Toggle Task Status

Enter task ID to toggle: 1

Current status:
[1] ✖ Buy groceries - Incomplete

✓ Status toggled successfully!
[1] ✔ Buy groceries - Complete

Press Enter to continue...

=== Todo Console Application ===

Current Tasks: 1 (0 incomplete, 1 complete)

Menu Options:
1. Add New Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6): 6

Thank you for using Todo App. Goodbye!
```

---

## References

- **Spec**: [spec.md](../spec.md) - User stories and acceptance scenarios
- **Data Model**: [data-model.md](../data-model.md) - Task structure and validation
- **Plan**: [plan.md](../plan.md) - Architecture decisions

---

## Conclusion

This CLI contract defines a clear, user-friendly interface for all 5 CRUD operations. The menu-driven approach minimizes learning curve while providing clear feedback for all operations. Error messages are actionable and polite. All contracts align with spec requirements and constitution principles.

**Status**: ✅ CLI contract complete
