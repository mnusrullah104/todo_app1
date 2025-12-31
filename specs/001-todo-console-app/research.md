# Research & Technical Decisions: Todo Console Application

**Feature**: 001-todo-console-app
**Date**: 2025-12-31
**Purpose**: Document technical decisions, alternatives considered, and rationale for implementation choices

---

## Research Summary

This document captures the research findings and technical decisions for implementing the Todo Console Application. All decisions align with constitution principles (simplicity, Python 3.13+, in-memory storage, standard library only) and spec requirements (5 CRUD operations, CLI interface, manual testing).

---

## Decision 1: Data Storage Structure

### Context
Need to store tasks in memory with efficient lookup by ID (primary access pattern) while maintaining insertion order for display purposes.

### Options Considered

#### Option A: List with Linear Search
```python
tasks = []  # List of Task objects
# Lookup: O(n) - must iterate to find by ID
# Insert: O(1) - append
# Delete: O(n) - find then remove
# Memory: Minimal overhead
```

**Pros:**
- Simple implementation
- Maintains insertion order naturally
- Minimal memory overhead

**Cons:**
- O(n) lookup performance for ID-based operations
- Degrades with large task lists (1000 tasks = slow)
- Violates performance goals (SC-005: 100 tasks in <3 seconds questionable)

#### Option B: Dictionary Keyed by ID
```python
tasks = {}  # {task_id: Task}
# Lookup: O(1) - direct key access
# Insert: O(1) - dict assignment
# Delete: O(1) - del tasks[id]
# Memory: Small overhead for hash table
```

**Pros:**
- O(1) lookup, insert, delete operations
- Meets performance goals confidently
- Natural mapping of ID to Task

**Cons:**
- Loses insertion order (Python 3.7+ dicts maintain insertion order, mitigated)
- Slightly higher memory overhead
- Requires separate counter for ID generation

#### Option C: Sorted Dictionary (collections.OrderedDict)
```python
from collections import OrderedDict
tasks = OrderedDict()  # Explicit ordering
```

**Pros:**
- Guaranteed insertion order
- O(1) operations
- Explicit contract

**Cons:**
- Unnecessary for Python 3.13 (dicts already ordered)
- Extra import (prefer standard dict)
- No functional advantage

### Decision: **Option B - Dictionary Keyed by ID**

**Rationale:**
1. **Performance**: O(1) operations meet performance goals (SC-001, SC-004, SC-005)
2. **Simplicity**: Python 3.7+ dicts maintain insertion order, no need for OrderedDict
3. **Natural mapping**: Task ID → Task object is semantically clear
4. **Scalability**: Handles 1000+ tasks efficiently per constitution constraints

**Implementation Notes:**
- Use separate `_next_id` counter starting at 1
- On delete, counter continues (IDs never reused per FR-003)
- Display tasks using `tasks.values()` or sorted `tasks.items()`

**Alternatives Rejected:**
- List rejected due to O(n) lookup performance concerns
- OrderedDict rejected as unnecessary overhead in Python 3.13

---

## Decision 2: CLI Interaction Pattern

### Context
Users need a clear, easy-to-use interface for 5 CRUD operations without prior command-line experience.

### Options Considered

#### Option A: Menu-Driven Numbered Options
```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit
Enter choice (1-6):
```

**Pros:**
- Zero learning curve (numbers are obvious)
- Clear error handling (invalid number)
- Fast user success (SC-007: 90% success after 2-min tutorial)
- Simple input validation

**Cons:**
- Less flexible than command parsing
- Requires multiple prompts (e.g., "Enter title:", "Enter description:")
- More verbose interaction

#### Option B: Command Parsing (CLI Arguments)
```bash
$ python main.py add "Buy groceries" "Milk, eggs"
$ python main.py list
$ python main.py update 1 --title "New title"
$ python main.py delete 1
$ python main.py toggle 1
```

**Pros:**
- Power user friendly
- Scriptable
- Single-command operations

**Cons:**
- Requires argument parsing library or manual parsing
- Steeper learning curve
- Error messages more complex
- Violates simplicity principle (constitution VI)

#### Option C: Interactive REPL
```
> add "Buy groceries" "Milk, eggs"
Task 1 added.
> list
[1] ✖ Buy groceries - Milk, eggs
> toggle 1
Task 1 marked complete.
```

**Pros:**
- Balance of power and simplicity
- Single session, multiple commands
- Easier than full CLI argument parsing

**Cons:**
- Requires command parsing logic
- More complex than menu
- Not significantly better UX than menu for Phase I

### Decision: **Option A - Menu-Driven Numbered Options**

**Rationale:**
1. **User success**: Meets SC-007 (90% success after 2-min tutorial) most reliably
2. **Simplicity**: Aligns with constitution principle VI (avoid over-engineering)
3. **Error handling**: Trivial validation (check if input is 1-6)
4. **Phase I appropriate**: Advanced CLI can be Phase II enhancement

**Implementation Notes:**
- Main loop displays menu, captures numeric choice
- Each option prompts for required data (title, ID, etc.)
- Clear prompts: "Enter task ID:", "Enter title (required):", "Enter description (optional, press Enter to skip):"
- Display confirmation after each operation

**Alternatives Rejected:**
- Command parsing rejected as over-engineering for Phase I
- REPL rejected as unnecessary complexity vs menu

---

## Decision 3: Error Handling Strategy

### Context
Need to handle invalid inputs (wrong ID, empty title) and edge cases (empty list) without crashing.

### Options Considered

#### Option A: Exception-Based
```python
def delete_task(task_id):
    if task_id not in tasks:
        raise TaskNotFoundError(f"Task ID {task_id} not found")
    del tasks[task_id]
```

**Pros:**
- Pythonic
- Clear separation of error path
- Easy to trace errors

**Cons:**
- Exceptions for expected conditions (user errors) is anti-pattern
- Requires try/except at CLI layer
- Mixes control flow with errors

#### Option B: Return Result Objects
```python
class Result:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

def delete_task(task_id):
    if task_id not in tasks:
        return Result(False, f"Task ID {task_id} not found")
    del tasks[task_id]
    return Result(True, f"Task {task_id} deleted")
```

**Pros:**
- Explicit success/failure
- Easy to test (check result.success)
- Clear error messages
- No exceptions for control flow

**Cons:**
- More verbose
- Manual checking at each call site

#### Option C: Return Tuples (success, message)
```python
def delete_task(task_id):
    if task_id not in tasks:
        return (False, f"Task ID {task_id} not found")
    del tasks[task_id]
    return (True, f"Task {task_id} deleted")
```

**Pros:**
- Simpler than Result class
- Clear success/failure

**Cons:**
- Less readable (tuple unpacking required)
- No type safety
- Hard to extend (what if we need data?)

### Decision: **Option B - Return Result Objects**

**Rationale:**
1. **Clarity**: Explicit success/error makes CLI layer simple
2. **Testability**: Easy to assert on result.success in tests
3. **Extensibility**: Can add data field for return values (e.g., created task)
4. **Error messages**: Built-in message field aligns with FR-010 (clear error messages)

**Implementation Notes:**
- Define Result class in services/task_manager.py
- All TaskManager methods return Result
- CLI layer checks result.success and displays result.message
- Use result.data for return values (e.g., result.data = list of tasks)

**Alternatives Rejected:**
- Exceptions rejected to avoid mixing control flow with errors
- Tuples rejected for poor extensibility

---

## Decision 4: ID Management Approach

### Context
Must assign unique, auto-incrementing IDs that are never reused (FR-003), even after deletion.

### Options Considered

#### Option A: Simple Counter
```python
class TaskManager:
    def __init__(self):
        self.tasks = {}
        self._next_id = 1

    def add_task(self, title, description):
        task_id = self._next_id
        self._next_id += 1
        # ... create task
```

**Pros:**
- Extremely simple
- Sequential IDs (1, 2, 3...)
- Meets FR-003 (IDs never reused)

**Cons:**
- Counter keeps incrementing (could reach integer limit theoretically)

#### Option B: Max ID + 1
```python
def add_task(self, title, description):
    task_id = max(self.tasks.keys(), default=0) + 1
```

**Pros:**
- No separate counter needed
- Handles any initial state

**Cons:**
- O(n) operation to find max
- Unnecessary complexity vs counter

#### Option C: UUID
```python
import uuid
task_id = uuid.uuid4()
```

**Pros:**
- Guaranteed unique globally
- No collision risk

**Cons:**
- Overkill for in-memory app
- Non-sequential (violates user expectation)
- String IDs harder to type in CLI
- Requires import (avoid if possible per constitution)

### Decision: **Option A - Simple Counter**

**Rationale:**
1. **Simplicity**: Aligns with constitution principle VI
2. **Sequential IDs**: User-friendly (easier to type "1" than "a3f2...")
3. **Performance**: O(1) ID generation
4. **Meets spec**: FR-003 satisfied (counter never decrements)

**Implementation Notes:**
- Initialize `_next_id = 1` in `__init__`
- Increment after each add: `task_id = self._next_id; self._next_id += 1`
- Never decrement or reset (even after delete)
- Integer limit (2^63-1 in Python) supports 1M tasks requirement easily

**Alternatives Rejected:**
- Max ID + 1 rejected as unnecessary complexity
- UUID rejected as overkill and user-unfriendly

---

## Decision 5: Task Data Structure

### Context
Need to represent Task with id, title, description, status fields.

### Options Considered

#### Option A: dataclass
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool = False
```

**Pros:**
- Modern Python idiom
- Auto-generates __init__, __repr__, __eq__
- Type hints included
- Minimal boilerplate

**Cons:**
- Requires Python 3.7+ (satisfied by 3.13 requirement)

#### Option B: NamedTuple
```python
from typing import NamedTuple

class Task(NamedTuple):
    id: int
    title: str
    description: str
    completed: bool = False
```

**Pros:**
- Immutable
- Lightweight

**Cons:**
- Immutability complicates updates (must create new instance)
- Less common pattern

#### Option C: Regular Class
```python
class Task:
    def __init__(self, id, title, description, completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
```

**Pros:**
- No imports
- Explicit control

**Cons:**
- More boilerplate
- No type hints enforcement

### Decision: **Option A - dataclass**

**Rationale:**
1. **Modern Python**: Idiomatic for Python 3.13
2. **Type safety**: Built-in type hints
3. **Less boilerplate**: Auto-generated methods
4. **Mutable**: Easy to update fields (needed for update/toggle operations)

**Implementation Notes:**
- Define in src/models/task.py
- Use type hints: int, str, bool
- Default completed=False matches spec (FR-004)
- Provides __repr__ for debugging

**Alternatives Rejected:**
- NamedTuple rejected due to immutability complications
- Regular class rejected for unnecessary boilerplate

---

## Decision 6: Input Validation Strategy

### Context
Must validate title (non-empty per FR-002), handle optional description, validate ID existence (FR-009).

### Options Considered

#### Option A: Validation in Service Layer
```python
def add_task(self, title, description):
    if not title or title.strip() == "":
        return Result(False, "Title cannot be empty")
    # ... proceed
```

**Pros:**
- Business logic in correct layer
- Reusable validation
- Testable in isolation

**Cons:**
- None significant

#### Option B: Validation in CLI Layer
```python
def add_task_ui(self):
    title = input("Enter title: ").strip()
    if not title:
        print("Error: Title cannot be empty")
        return
    # ... call service
```

**Pros:**
- Early exit (don't call service with invalid data)

**Cons:**
- Business rules leaked to UI layer
- Harder to test
- Duplicated if multiple UIs added later

### Decision: **Option A - Validation in Service Layer**

**Rationale:**
1. **Separation of concerns**: Business rules belong in service layer
2. **Testability**: Can test validation without UI
3. **Extensibility**: If multiple UIs added, validation is centralized

**Implementation Notes:**
- TaskManager methods validate inputs and return Result(False, ...) on error
- CLI layer displays error messages from Result
- Title validation: `if not title or not title.strip(): return Result(False, "Title cannot be empty")`
- ID validation: `if task_id not in self.tasks: return Result(False, f"Task ID {task_id} not found")`

**Alternatives Rejected:**
- CLI layer validation rejected for poor separation of concerns

---

## Technology Stack Summary

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.13+ | Constitution requirement, modern features |
| Package Manager | UV | Constitution requirement |
| Data Storage | Dictionary (dict) | O(1) operations, standard library |
| Data Model | dataclass | Modern Python, type hints, minimal boilerplate |
| CLI Pattern | Menu-driven | User success, simplicity |
| Error Handling | Result objects | Clear, testable, explicit |
| ID Generation | Auto-increment counter | Simple, sequential, user-friendly |
| Validation | Service layer | Separation of concerns, testability |
| Testing | Manual CLI testing | Constitution requirement for Phase I |

---

## Best Practices Applied

### Python 3.13 Features
- Type hints (PEP 484)
- dataclasses (PEP 557)
- F-strings for formatting
- Dictionary ordering (guaranteed since 3.7)

### Clean Code Principles
- Single Responsibility: Each module has one purpose
- Dependency Inversion: CLI depends on service interface, not implementation
- Explicit over implicit: Result objects make success/failure clear
- No magic numbers: Named constants for menu options

### Error Handling
- Expected errors return Result(False, message)
- Unexpected errors (e.g., system errors) raise exceptions
- User-facing error messages are clear and actionable (FR-010)

---

## Open Questions & Future Considerations

### Phase I Scope (Resolved)
✅ All technical decisions documented
✅ No blocking unknowns remain
✅ Architecture aligns with constitution

### Future Enhancements (Out of Scope)
- ❌ Persistent storage (database/files) - Phase II
- ❌ Command-line argument parsing - Phase II
- ❌ Task filtering/search - Phase II
- ❌ Task categories/tags - Phase II

---

## References

- **Spec**: [spec.md](./spec.md)
- **Plan**: [plan.md](./plan.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Python dataclasses**: https://docs.python.org/3/library/dataclasses.html
- **Type hints**: https://docs.python.org/3/library/typing.html

---

## Conclusion

All technical decisions are documented with clear rationale. The chosen approaches prioritize simplicity, user success, and alignment with constitution principles. No external dependencies are needed (standard library sufficient). The architecture supports all 5 CRUD operations efficiently while maintaining clean separation of concerns.

**Status**: ✅ Research complete - ready for Phase 1 (Design)
