# Data Model: Full-Stack Todo Web Application

**Feature**: Phase II - Full-Stack Todo Web App
**Date**: 2026-01-02
**Status**: Draft

This document defines the database schema and entity relationships for the multi-user todo application.

---

## Entity Overview

```
User (1) ----< (N) Task
```

A User can have zero or more Tasks. Each Task belongs to exactly one User.

---

## Entity: User

Represents an authenticated individual using the application.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Auto-generated | Unique identifier for the user |
| `email` | String | Unique, Not Null, RFC 5322 format | User's email address for login |
| `email_verified` | Boolean | Default: False | Whether email has been verified |
| `name` | String | Nullable | User's display name (optional) |
| `created_at` | DateTime | Not Null, Auto-generated | Account creation timestamp |
| `updated_at` | DateTime | Not Null, Auto-updated | Last profile update timestamp |

### Validation Rules

- **email**: Must be valid RFC 5322 format (validated by Better Auth)
- **email**: Must be unique across all users
- **password**: Minimum 8 characters (hashed by Better Auth, not stored in plain text)

### SQLModel Definition

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    """User account model managed by Better Auth."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    email_verified: bool = Field(default=False)
    name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### Notes

- User model is primarily managed by Better Auth
- Password hash is stored separately by Better Auth (not in this table)
- Additional Better Auth fields (sessions, etc.) are managed by the auth library
- For Phase II, only basic user fields are needed

---

## Entity: Task

Represents a single todo item owned by a user.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for the task |
| `user_id` | UUID | Foreign Key (User.id), Not Null, Indexed | Owner of the task |
| `title` | String | Not Null, Max 200 characters | Task title (required) |
| `description` | String | Nullable, Max 2000 characters | Optional task details |
| `completed` | Boolean | Default: False | Completion status |
| `created_at` | DateTime | Not Null, Auto-generated | Task creation timestamp |
| `updated_at` | DateTime | Not Null, Auto-updated | Last modification timestamp |

### Validation Rules

- **user_id**: Must reference valid User.id
- **title**: Required (not null, not empty after trimming whitespace)
- **title**: Maximum 200 characters (updated from Phase I's 500 chars per spec)
- **description**: Optional, empty string allowed
- **description**: Maximum 2000 characters
- **completed**: Boolean only (True/False)

### Indexes

- Primary key on `id`
- Foreign key index on `user_id` (for efficient user-scoped queries)
- Composite index on `(user_id, created_at DESC)` for ordered task lists

### SQLModel Definition

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from uuid import UUID

class Task(SQLModel, table=True):
    """Task model with user ownership."""

    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default="", max_length=2000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### Database Query Patterns

**List all tasks for a user (newest first):**
```sql
SELECT * FROM tasks
WHERE user_id = ?
ORDER BY created_at DESC;
```

**Get single task by ID and user:**
```sql
SELECT * FROM tasks
WHERE id = ? AND user_id = ?;
```

**Update task (with timestamp):**
```sql
UPDATE tasks
SET title = ?, description = ?, completed = ?, updated_at = NOW()
WHERE id = ? AND user_id = ?;
```

**Delete task:**
```sql
DELETE FROM tasks
WHERE id = ? AND user_id = ?;
```

### Notes

- Phase I used in-memory dataclass; Phase II uses SQLModel with database persistence
- Title length reduced from 500 → 200 characters per Phase II spec requirements
- All queries MUST include `user_id` filter to enforce data isolation
- `created_at` used for default sort order (newest first)
- `updated_at` automatically updated on modifications

---

## Entity Relationships

### User → Tasks (One-to-Many)

- A User can own 0 to N Tasks
- Each Task belongs to exactly 1 User
- Foreign key: `Task.user_id` references `User.id`
- Cascade behavior: ON DELETE CASCADE (when user deleted, all their tasks are deleted)

**SQLModel Relationship:**
```python
from typing import List, Optional
from sqlmodel import Relationship

class User(SQLModel, table=True):
    # ... fields ...
    tasks: List["Task"] = Relationship(back_populates="owner", cascade_delete=True)

class Task(SQLModel, table=True):
    # ... fields ...
    owner: Optional[User] = Relationship(back_populates="tasks")
```

---

## State Transitions

### Task Completion Status

```
[New Task]
    ↓
[completed = False]
    ↓ ← → (toggle)
[completed = True]
```

- Tasks are created with `completed = False`
- Users can toggle completion status via PATCH request
- No intermediate states (only True/False)

---

## Data Migration from Phase I

Phase I used in-memory Python dataclasses. Phase II requires database persistence.

### Schema Changes

| Aspect | Phase I | Phase II | Migration Impact |
|--------|---------|----------|------------------|
| **Storage** | In-memory list | PostgreSQL database | No migration (Phase I not deployed) |
| **User Model** | N/A (single user) | User table with auth | New entity |
| **Task.id** | int (manual assignment) | int (auto-increment) | ID generation automated |
| **Task.user_id** | N/A | UUID foreign key | New field (required) |
| **Task.title max** | 500 characters | 200 characters | Tighter constraint |
| **Timestamps** | N/A | created_at, updated_at | New fields |

### Migration Strategy

**No migration needed**: Phase I and Phase II are separate deployments. Phase II starts with empty database.

---

## Database Schema (SQL DDL)

```sql
-- Users table (managed by Better Auth)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(2000),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

---

## Validation Summary

### Application-Level Validation (Pydantic/SQLModel)

- Title: Required, non-empty after trim, max 200 chars
- Description: Optional, max 2000 chars
- Email: RFC 5322 format (Better Auth handles this)
- Password: Minimum 8 chars (Better Auth handles this)

### Database-Level Constraints

- Primary keys (auto-generated)
- Foreign keys (user_id references users.id)
- Unique constraints (user.email)
- Not null constraints (user_id, title, email)
- Max length constraints (via VARCHAR)

### Business Logic Validation

- User can only access their own tasks (JWT user_id must match task.user_id)
- Task ID must exist before update/delete
- Task must belong to authenticated user

---

## Security Considerations

### Data Isolation

- **Critical**: ALL task queries MUST include `WHERE user_id = ?` filter
- Backend MUST verify JWT token's user_id matches URL parameter
- Database queries MUST use parameterized statements (SQL injection prevention)

### Sensitive Data

- Passwords are hashed by Better Auth (never stored in plain text)
- JWT tokens contain user_id but not sensitive data
- Database credentials stored in environment variables only

### Access Control

- Tasks are private to the owning user
- No sharing/collaboration features in Phase II
- All API endpoints require valid JWT token

---

## Future Considerations (Out of Scope for Phase II)

- Task categories/tags
- Task priority levels
- Due dates and reminders
- Task sharing/collaboration
- File attachments
- Task history/audit log
- Soft deletes (recycle bin)

These features are explicitly out of scope per the Phase II specification.

---

## References

- Phase I Task Model: `/phase1/src/models/task.py`
- Phase II Spec: `/specs/002-fullstack-todo-web/spec.md` (FR-006 through FR-012)
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- PostgreSQL UUID Type: https://www.postgresql.org/docs/current/datatype-uuid.html
