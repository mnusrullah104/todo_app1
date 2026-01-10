# Backend Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-09

## Active Technologies

- **Framework**: FastAPI (Python 3.11+)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Authentication**: Better Auth (JWT-based)
- **Environment**: Python Virtual Environment

## Project Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Common dependencies
│   │   ├── health.py           # Health check endpoints
│   │   └── tasks.py            # Task management endpoints
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── config.py           # Better Auth configuration
│   │   ├── middleware.py       # Authentication middleware
│   │   └── dependencies.py     # Auth-related dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User data model
│   │   └── task.py             # Task data model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User request/response schemas
│   │   └── task.py             # Task request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py     # Task business logic
│   │   └── user_service.py     # User business logic
│   ├── database/
│   │   ├── __init__.py
│   │   └── session.py          # Database session management
│   └── core/
│       ├── __init__.py
│       ├── config.py           # Application configuration
│       └── security.py         # Security utilities
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   └── test_tasks.py
├── requirements.txt
├── alembic.ini
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

## Commands

### Development
- `uvicorn app.main:app --reload` - Start development server
- `python -m pytest` - Run tests
- `alembic upgrade head` - Apply database migrations
- `alembic revision --autogenerate -m "description"` - Create migration

### Setup
- `python -m venv venv` - Create virtual environment
- `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows) - Activate venv
- `pip install -r requirements.txt` - Install dependencies

### Database
- `alembic revision --autogenerate -m "migration message"` - Generate migration
- `alembic upgrade head` - Apply migrations
- `alembic downgrade -1` - Rollback migration

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for all public functions/classes
- Use meaningful variable and function names
- Keep functions small and focused
- Use dependency injection for testability

### FastAPI
- Use Pydantic models for request/response validation
- Implement proper error handling with HTTPException
- Use dependency injection for shared functionality
- Follow RESTful API design principles
- Implement proper status codes

### SQLModel
- Define table relationships clearly
- Use proper indexing for performance
- Implement proper validation constraints
- Use transactions for data consistency

## Recent Changes

- Initial project structure setup
- Better Auth integration specifications
- Clean API endpoint design
- Professional database schema

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->