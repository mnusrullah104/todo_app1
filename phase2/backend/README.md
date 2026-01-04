# Todo Backend - FastAPI

Phase II Todo Web Application backend service.

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: PyJWT
- **Python**: 3.13+

## Setup

### Prerequisites

- Python 3.13 or later
- PostgreSQL database (Neon account or local instance)

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and configure:
# - DATABASE_URL: Your PostgreSQL connection string
# - BETTER_AUTH_SECRET: Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Database Migrations

```bash
# Initialize Alembic (first time only)
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### Running

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Project Structure

```
backend/
├── app/
│   ├── models/          # SQLModel database models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/        # Business logic
│   ├── api/             # API route handlers
│   ├── middleware/      # FastAPI middleware
│   ├── main.py          # Application entry point
│   └── database.py      # Database configuration
├── tests/               # Test suite
├── alembic/             # Database migrations
├── requirements.txt     # Python dependencies
└── .env.example        # Environment variables template
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_tasks.py
```

## Development

```bash
# Format code
black app/ tests/

# Lint code
ruff check app/ tests/
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Yes | JWT signing secret (min 32 chars) |
| `HOST` | No | Server host (default: 0.0.0.0) |
| `PORT` | No | Server port (default: 8000) |
| `ENVIRONMENT` | No | Environment name (development/production) |

## See Also

- [Project Root README](../README.md)
- [Frontend README](../frontend/README.md)
- [API Contracts](../specs/002-fullstack-todo-web/contracts/api-endpoints.md)
- [Quickstart Guide](../specs/002-fullstack-todo-web/quickstart.md)
