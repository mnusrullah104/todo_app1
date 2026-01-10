# REST API Endpoints Specification

## Base Configuration
- **Base URL**: `/api` (e.g., `https://yourdomain.com/api`)
- **Versioning**: No explicit versioning in this phase (future: `/api/v1/`)
- **Content-Type**: `application/json` for requests and responses
- **Authentication**: JWT token required in `Authorization: Bearer <token>` header for protected endpoints
- **Response Format**: JSON with consistent structure

## Authentication Endpoints
> Note: These are handled by Better Auth, not custom endpoints

## Task Management Endpoints

### Get All Tasks
```
GET /tasks
```
- **Authentication**: Required (JWT token in Authorization header)
- **Description**: Retrieve all tasks for the authenticated user
- **Query Parameters**: None in initial version (pagination in future)
- **Success Response**: `200 OK`
  ```json
  {
    "tasks": [
      {
        "id": "uuid",
        "userId": "uuid",
        "title": "string (max 200)",
        "description": "string (max 2000)",
        "completed": "boolean",
        "createdAt": "ISO date string",
        "updatedAt": "ISO date string"
      }
    ],
    "total": "number"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized`: Missing or invalid authentication token
  - `500 Internal Server Error`: Server error

### Get Specific Task
```
GET /tasks/{taskId}
```
- **Authentication**: Required (JWT token in Authorization header)
- **Description**: Retrieve a specific task by ID
- **Path Parameter**: `taskId: UUID`
- **Success Response**: `200 OK`
  ```json
  {
    "id": "uuid",
    "userId": "uuid",
    "title": "string (max 200)",
    "description": "string (max 2000)",
    "completed": "boolean",
    "createdAt": "ISO date string",
    "updatedAt": "ISO date string"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized`: Missing or invalid authentication token
  - `403 Forbidden`: User does not own this task
  - `404 Not Found`: Task does not exist
  - `500 Internal Server Error`: Server error

### Create Task
```
POST /tasks
```
- **Authentication**: Required (JWT token in Authorization header)
- **Description**: Create a new task for the authenticated user
- **Request Body**:
  ```json
  {
    "title": "string (required, max 200)",
    "description": "string (optional, max 2000)",
    "completed": "boolean (optional, default: false)"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": "uuid",
    "userId": "uuid",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "createdAt": "ISO date string",
    "updatedAt": "ISO date string"
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: Invalid request body or validation errors
  - `401 Unauthorized`: Missing or invalid authentication token
  - `500 Internal Server Error`: Server error

### Update Task
```
PATCH /tasks/{taskId}
```
- **Authentication**: Required (JWT token in Authorization header)
- **Description**: Update a specific task (partial updates allowed)
- **Path Parameter**: `taskId: UUID`
- **Request Body** (all optional):
  ```json
  {
    "title": "string (optional, max 200)",
    "description": "string (optional, max 2000)",
    "completed": "boolean (optional)"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "id": "uuid",
    "userId": "uuid",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "createdAt": "ISO date string",
    "updatedAt": "ISO date string"
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: Invalid request body or validation errors
  - `401 Unauthorized`: Missing or invalid authentication token
  - `403 Forbidden`: User does not own this task
  - `404 Not Found`: Task does not exist
  - `500 Internal Server Error`: Server error

### Delete Task
```
DELETE /tasks/{taskId}
```
- **Authentication**: Required (JWT token in Authorization header)
- **Description**: Delete a specific task
- **Path Parameter**: `taskId: UUID`
- **Success Response**: `204 No Content`
- **Error Responses**:
  - `401 Unauthorized`: Missing or invalid authentication token
  - `403 Forbidden`: User does not own this task
  - `404 Not Found`: Task does not exist
  - `500 Internal Server Error`: Server error

## Health Check Endpoint

### Health Check
```
GET /health
```
- **Authentication**: Not required
- **Description**: Health check endpoint for monitoring
- **Success Response**: `200 OK`
  ```json
  {
    "status": "healthy",
    "timestamp": "ISO date string"
  }
  ```
- **Error Responses**:
  - `500 Internal Server Error`: Service is unhealthy

## Common Error Response Format
All error responses follow this format:
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object (optional)"
  }
}
```

## Authentication Validation Rules
1. **JWT Token Required**: All task endpoints require valid JWT token
2. **Token Validation**: Backend validates JWT by calling Better Auth service
3. **User ID Extraction**: Extract user ID from validated JWT token
4. **Data Isolation**: Compare JWT user ID with requested resource ownership
5. **Access Control**: Return 403 Forbidden if user ID mismatch

## Security Headers
All responses include appropriate security headers:
- `Content-Type: application/json`
- `Cache-Control: no-store` for sensitive data
- Proper CORS headers configured for frontend domain

## Rate Limiting
- **Task Creation**: Limited to 10 requests per minute per user
- **Task Updates**: Limited to 20 requests per minute per user
- **Task Deletions**: Limited to 10 requests per minute per user
- **Task Retrieval**: Limited to 30 requests per minute per user

## Pagination (Future Enhancement)
When implemented, all collection endpoints will support:
- `?limit=10` (default: 50, max: 100)
- `?offset=0` (default: 0)
- `?sortBy=createdAt` (default: createdAt, options: createdAt, updatedAt, title)
- `?sortOrder=desc` (default: desc, options: asc, desc)

## Filtering (Future Enhancement)
When implemented, endpoints will support:
- `?completed=true/false` (filter by completion status)
- `?search=text` (search in title/description)
- `?dateFrom=YYYY-MM-DD` (filter by creation date range)
- `?dateTo=YYYY-MM-DD` (filter by creation date range)