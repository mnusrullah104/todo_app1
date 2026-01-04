# API Endpoints: Full-Stack Todo Web Application

**Feature**: Phase II - Full-Stack Todo Web App
**Date**: 2026-01-02
**Status**: Draft

This document defines the RESTful API endpoints for the todo application backend.

---

## Base URL

**Development**: `http://localhost:8000`
**Production**: TBD (Vercel deployment)

---

## Authentication

All task endpoints require JWT authentication via the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

### JWT Token Structure

```json
{
  "sub": "user-uuid-here",
  "exp": 1234567890,
  "iss": "http://localhost:3000",
  "aud": "http://localhost:3000"
}
```

### Authentication Flow

1. User registers/logs in via Better Auth (frontend)
2. Better Auth generates JWT token signed with `BETTER_AUTH_SECRET`
3. Frontend retrieves token via `authClient.token()`
4. Frontend includes token in `Authorization: Bearer <token>` header
5. Backend validates token signature using same `BETTER_AUTH_SECRET`
6. Backend extracts `sub` claim as `user_id`
7. Backend verifies `sub` matches `user_id` URL parameter

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET/PATCH/DELETE |
| 201 | Created | Successful POST (resource created) |
| 400 | Bad Request | Invalid request body or parameters |
| 401 | Unauthorized | Missing, invalid, or expired JWT token |
| 403 | Forbidden | Valid token but user_id mismatch |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error (Pydantic) |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Database connection failure |

### 503 Service Unavailable Response

When database connection fails:

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 30

{
  "detail": "Database temporarily unavailable. Please retry in 30 seconds."
}
```

---

## Endpoints

### Health Check

#### GET /health

Health check endpoint (no authentication required).

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "unhealthy",
  "database": "disconnected"
}
```

---

### List Tasks

#### GET /api/{user_id}/tasks

Retrieve all tasks for the authenticated user, ordered by creation timestamp (newest first).

**Authentication**: Required

**Path Parameters:**
- `user_id` (UUID): Must match JWT token's `sub` claim

**Query Parameters:** None

**Request:**
```http
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-02T10:30:00Z",
      "updated_at": "2026-01-02T10:30:00Z"
    },
    {
      "id": 2,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Finish project",
      "description": "",
      "completed": true,
      "created_at": "2026-01-01T09:00:00Z",
      "updated_at": "2026-01-02T08:15:00Z"
    }
  ]
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Missing or invalid authentication token"
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "User ID in token does not match requested user_id"
}
```

---

### Get Single Task

#### GET /api/{user_id}/tasks/{task_id}

Retrieve a specific task by ID for the authenticated user.

**Authentication**: Required

**Path Parameters:**
- `user_id` (UUID): Must match JWT token's `sub` claim
- `task_id` (int): Task identifier

**Request:**
```http
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks/1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T10:30:00Z"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Task not found or does not belong to user"
}
```

---

### Create Task

#### POST /api/{user_id}/tasks

Create a new task for the authenticated user.

**Authentication**: Required

**Path Parameters:**
- `user_id` (UUID): Must match JWT token's `sub` claim

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Request Body Schema:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | Yes | Non-empty, max 200 characters |
| `description` | string | No | Max 2000 characters, defaults to "" |

**Request:**
```http
POST /api/550e8400-e29b-41d4-a716-446655440000/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T10:30:00Z"
}
```

**Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### Update Task

#### PATCH /api/{user_id}/tasks/{task_id}

Update an existing task's title, description, or completion status.

**Authentication**: Required

**Path Parameters:**
- `user_id` (UUID): Must match JWT token's `sub` claim
- `task_id` (int): Task identifier

**Request Body (all fields optional):**
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "completed": true
}
```

**Request Body Schema:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | No | Non-empty if provided, max 200 characters |
| `description` | string | No | Max 2000 characters |
| `completed` | boolean | No | true or false |

**Request:**
```http
PATCH /api/550e8400-e29b-41d4-a716-446655440000/tasks/1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T11:45:00Z"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Task not found or does not belong to user"
}
```

---

### Delete Task

#### DELETE /api/{user_id}/tasks/{task_id}

Permanently delete a task owned by the authenticated user.

**Authentication**: Required

**Path Parameters:**
- `user_id` (UUID): Must match JWT token's `sub` claim
- `task_id` (int): Task identifier

**Request:**
```http
DELETE /api/550e8400-e29b-41d4-a716-446655440000/tasks/1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Task not found or does not belong to user"
}
```

---

## Request/Response Schemas

### TaskCreate (Request)

```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "maxLength": 2000,
      "default": ""
    }
  },
  "required": ["title"]
}
```

### TaskUpdate (Request)

```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "maxLength": 2000
    },
    "completed": {
      "type": "boolean"
    }
  }
}
```

### TaskResponse (Response)

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer"
    },
    "user_id": {
      "type": "string",
      "format": "uuid"
    },
    "title": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "completed": {
      "type": "boolean"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": ["id", "user_id", "title", "description", "completed", "created_at", "updated_at"]
}
```

---

## Security Requirements

### Authorization Verification

Every task endpoint MUST:

1. Extract JWT token from `Authorization: Bearer <token>` header
2. Validate JWT signature using `BETTER_AUTH_SECRET`
3. Verify token expiration (`exp` claim)
4. Extract user ID from `sub` claim
5. Verify `sub` matches `user_id` path parameter
6. Execute database query with `WHERE user_id = ?` filter

### SQL Injection Prevention

- ALL database queries MUST use parameterized statements
- NEVER concatenate user input into SQL strings
- Use SQLModel ORM query methods (automatically parameterized)

### CORS Configuration

Development CORS policy:

```python
origins = [
    "http://localhost:3000",  # Next.js frontend
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## OpenAPI Specification

FastAPI automatically generates OpenAPI 3.0 specification at:

- **JSON**: `http://localhost:8000/openapi.json`
- **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc`

The generated OpenAPI spec includes:
- All endpoint definitions
- Request/response schemas
- Authentication requirements (Bearer token)
- Validation rules

---

## Implementation Notes

### Middleware Order

1. CORS middleware (first)
2. JWT authentication middleware
3. Route handlers

### Error Handling

- Pydantic validation errors → 422 Unprocessable Entity
- Database connection errors → 503 Service Unavailable
- JWT validation errors → 401 Unauthorized
- User mismatch errors → 403 Forbidden
- Not found errors → 404 Not Found
- Unexpected errors → 500 Internal Server Error (log details, return generic message)

### Logging

Log all authentication failures and authorization violations for security monitoring.

---

## Testing Checklist

- [ ] Health endpoint returns 200 without auth
- [ ] All task endpoints return 401 without JWT token
- [ ] All task endpoints return 403 when token user_id ≠ URL user_id
- [ ] List tasks returns only authenticated user's tasks
- [ ] Create task associates task with authenticated user
- [ ] Update task only works for authenticated user's tasks
- [ ] Delete task only works for authenticated user's tasks
- [ ] Get single task returns 404 for other user's tasks
- [ ] Database errors return 503 with Retry-After header
- [ ] Validation errors return 422 with field details

---

## References

- FastAPI Security Tutorial: https://fastapi.tiangolo.com/tutorial/security/
- OpenAPI 3.0 Specification: https://swagger.io/specification/
- RFC 7519 (JWT): https://tools.ietf.org/html/rfc7519
- Phase II Spec: `/specs/002-fullstack-todo-web/spec.md` (FR-003, FR-004, FR-016, FR-017)
