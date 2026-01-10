# Database Schema Specification

## Database System
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel (combines Pydantic + SQLAlchemy)
- **Migration Tool**: Alembic
- **Connection Pooling**: Built-in PostgreSQL connection pooling

## Naming Conventions
- **Tables**: Lowercase with underscores (e.g., `users`, `tasks`)
- **Columns**: Lowercase with underscores (e.g., `user_id`, `created_at`)
- **Primary Keys**: `id` as UUID (except special cases)
- **Foreign Keys**: `{referenced_table}_id` (e.g., `user_id` for users table)
- **Indexes**: `ix_{table}_{column}` (e.g., `ix_tasks_user_id`)
- **Constraints**: Descriptive names with prefixes (e.g., `fk_tasks_user_id`)

## User Table
> Note: User records are primarily managed by Better Auth, but we maintain a reference for application-specific data and relationships

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_users_email ON users(email);
```

**Fields Description**:
- `id`: UUID primary key matching Better Auth user ID
- `email`: User's email address (unique constraint)
- `email_verified`: Whether email has been verified (synced from Better Auth)
- `name`: User's display name (synced from Better Auth)
- `created_at`: Timestamp when record was created
- `updated_at`: Timestamp when record was last updated

**Relationships**:
- One-to-many: users → tasks (via user_id foreign key)

## Task Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_tasks_user_id
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX ix_tasks_user_id ON tasks(user_id);
CREATE INDEX ix_tasks_completed ON tasks(completed);
CREATE INDEX ix_tasks_created_at ON tasks(created_at DESC);
```

**Fields Description**:
- `id`: UUID primary key
- `user_id`: Foreign key to users table (enforces data isolation)
- `title`: Task title (max 200 characters, required)
- `description`: Task description (text field, optional)
- `completed`: Boolean indicating completion status (default: false)
- `created_at`: Timestamp when task was created
- `updated_at`: Timestamp when task was last updated

**Constraints**:
- `fk_tasks_user_id`: Foreign key constraint with cascade delete
- `title_not_empty`: Check constraint ensuring title is not empty after trimming

**Indexes**:
- `ix_tasks_user_id`: For efficient user-based queries
- `ix_tasks_completed`: For filtering by completion status
- `ix_tasks_created_at`: For ordering by creation date (descending)

## Audit Trail Tables (Future Enhancement)
For future audit trail implementation:

```sql
CREATE TABLE task_audit_log (
    id UUID PRIMARY KEY,
    task_id UUID NOT NULL,
    user_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'CREATE', 'UPDATE', 'DELETE'
    old_values JSONB,
    new_values JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_task_audit_task_id
        FOREIGN KEY (task_id)
        REFERENCES tasks(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_task_audit_user_id
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX ix_task_audit_task_id ON task_audit_log(task_id);
CREATE INDEX ix_task_audit_user_id ON task_audit_log(user_id);
CREATE INDEX ix_task_audit_created_at ON task_audit_log(created_at DESC);
```

## Database Models (SQLModel)

### User Model
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    email_verified: bool = Field(default=False)
    name: Optional[str] = Field(max_length=255, default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### Task Model
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

## Indexing Strategy
1. **Primary Keys**: Auto-indexed by UUID primary key
2. **Foreign Keys**: Indexed for JOIN operations
3. **Filtering Fields**: Indexed for common query patterns
4. **Sorting Fields**: Indexed for ORDER BY operations
5. **Unique Constraints**: Indexed to enforce uniqueness

## Partitioning Strategy (Future Enhancement)
- **Time-based partitioning**: Partition tasks table by month/year for large datasets
- **User-based partitioning**: Consider hash partitioning by user_id for massive scale

## Connection Pooling
- **Min Connections**: 1
- **Max Connections**: 20 (adjustable based on load)
- **Connection Timeout**: 30 seconds
- **Pool Recycling**: Every 3600 seconds (1 hour)

## Backup Strategy
- **Automated Backups**: Daily automated backups via Neon
- **Point-in-Time Recovery**: Available through Neon's branching feature
- **Retention Policy**: 7-day retention for point-in-time recovery
- **Manual Snapshots**: Available on-demand for major deployments

## Performance Optimization
1. **Query Optimization**: Use EXPLAIN ANALYZE for slow query identification
2. **Connection Management**: Proper connection lifecycle with context managers
3. **Batch Operations**: Use bulk operations for multiple record updates
4. **Caching**: Implement Redis caching for frequently accessed data
5. **Read Replicas**: Consider read replicas for read-heavy operations

## Security Considerations
1. **Encryption at Rest**: Enabled via Neon's default encryption
2. **Encryption in Transit**: Enforced with SSL/TLS connections
3. **Row Level Security**: Future implementation for multi-tenant scenarios
4. **Audit Logging**: Track sensitive operations (implemented via audit tables)
5. **Access Control**: Proper database user permissions (separate users for different services)

## Migration Strategy
- **Alembic**: Use Alembic for database migrations
- **Versioning**: Sequential versioning with descriptive names
- **Downgrade Support**: Ensure all migrations are reversible
- **Testing**: Test migrations in staging before production
- **Backup**: Automated backup before running migrations in production