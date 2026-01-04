# Todo Application Project

**A progressive implementation of a todo application across two phases.**

---

## Project Overview

This repository demonstrates the evolution of a todo application from a simple console app to a full-stack web application with authentication and data isolation.

### Phase 1: Console Todo Application ✅ Complete
**Location:** `phase1/`

A Python-based command-line todo application with local file persistence.

**Features:**
- Add, list, update, and delete tasks via CLI
- Task persistence using JSON file storage
- Interactive menu-driven interface
- Simple and educational implementation

**Tech Stack:** Python 3.11+, JSON file storage

[**View Phase 1 Details →**](phase1/README.md)

---

### Phase 2: Full-Stack Web Application ✅ MVP Complete (68/111 tasks)
**Location:** `phase2/`

A modern multi-user web application with JWT authentication and PostgreSQL database.

**Features:**
- ✅ User registration and login with JWT tokens
- ✅ Personal task lists with user data isolation
- ✅ Create, view, update, and delete tasks
- ✅ Real-time UI updates with React
- ✅ RESTful API with FastAPI
- ✅ Responsive design with Tailwind CSS

**Tech Stack:**
- **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend:** FastAPI, SQLModel, PostgreSQL
- **Auth:** JWT tokens with 7-day expiration, bcrypt password hashing

[**View Phase 2 Details →**](phase2/README.md)

[**View Implementation Report →**](phase2/IMPLEMENTATION_REPORT.md)

---

## Repository Structure

```
todo_app1/
├── .specify/                    # Specify framework configuration
│   └── memory/
│       └── constitution.md      # Project principles and guidelines
│
├── phase1/                      # Phase 1: Console Application
│   ├── src/                     # Python source code
│   │   ├── models/             # Task model
│   │   ├── services/           # Task manager service
│   │   └── cli/                # CLI interface
│   ├── specs/                   # Specifications and plans
│   ├── history/                 # Development history
│   ├── pyproject.toml          # Python project config
│   ├── run.bat                 # Windows run script
│   ├── README.md               # Phase 1 documentation
│   └── TESTING_GUIDE.md        # Testing instructions
│
├── phase2/                      # Phase 2: Web Application
│   ├── backend/                # FastAPI backend
│   │   ├── app/
│   │   │   ├── api/           # API endpoints
│   │   │   ├── models/        # SQLModel database models
│   │   │   ├── schemas/       # Pydantic request/response schemas
│   │   │   ├── services/      # Business logic
│   │   │   ├── middleware/    # JWT auth middleware
│   │   │   └── utils/         # Utilities (logging, security)
│   │   ├── alembic/           # Database migrations
│   │   └── main.py            # FastAPI app entry point
│   │
│   ├── frontend/               # Next.js frontend
│   │   ├── app/               # Next.js pages (App Router)
│   │   │   ├── dashboard/    # Main task management
│   │   │   ├── login/        # Login page
│   │   │   └── register/     # Registration page
│   │   ├── components/        # React components
│   │   │   ├── tasks/        # Task-related components
│   │   │   └── ui/           # Reusable UI components
│   │   └── lib/              # Utilities (API client, auth)
│   │
│   ├── specs/                  # Phase 2 specifications
│   ├── history/                # Development history
│   ├── IMPLEMENTATION_REPORT.md  # Detailed status report
│   └── README.md               # Phase 2 documentation
│
├── .gitignore                  # Git ignore patterns
├── CLAUDE.md                   # Project guidelines for Claude Code
└── README.md                   # This file
```

---

## Quick Start

### Phase 1: Console Application

```bash
cd phase1

# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e .

# Run
python -m src.main
```

### Phase 2: Web Application

**Backend:**
```bash
cd phase2/backend

# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Edit .env with your database URL and secret key

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd phase2/frontend

# Setup
npm install

# Configure .env.local
cp .env.local.example .env.local
# Edit .env.local with API URL

# Start dev server
npm run dev
```

Open http://localhost:3000 in your browser.

---

## Project Constitution

This project follows a set of guiding principles defined in `.specify/memory/constitution.md`:

**Core Values:**
- Incremental complexity (start simple, add features progressively)
- User data isolation and security
- Clear separation of concerns
- Comprehensive documentation
- Test-driven development (TDD)

**Code Standards:**
- Type safety (TypeScript on frontend, type hints in Python)
- RESTful API design
- Secure authentication (JWT tokens, password hashing)
- Input validation on both client and server
- Error handling with user-friendly messages

---

## Development Philosophy

### Phase 1 → Phase 2 Evolution

**Phase 1** demonstrates fundamental programming concepts:
- Data structures (Task model)
- CRUD operations
- File I/O
- Command-line interfaces

**Phase 2** builds on these concepts with production-ready patterns:
- Client-server architecture
- Database persistence with migrations
- Stateless authentication
- RESTful API design
- Modern frontend framework
- User data isolation

This progression mirrors real-world software development: start with a prototype, validate the concept, then scale to a multi-user production system.

---

## Technology Choices

### Phase 1
- **Python 3.11+:** Modern Python with type hints
- **JSON Storage:** Simple file-based persistence
- **Interactive CLI:** User-friendly terminal interface

### Phase 2 Backend
- **FastAPI:** High-performance async Python web framework
- **SQLModel:** Type-safe ORM combining Pydantic and SQLAlchemy
- **PostgreSQL:** Production-grade relational database
- **Alembic:** Database migration management
- **PyJWT:** JWT token generation and validation
- **Passlib:** Password hashing with bcrypt

### Phase 2 Frontend
- **Next.js 15:** React framework with App Router
- **React 19:** Latest React with modern hooks
- **TypeScript:** Type safety for JavaScript
- **Tailwind CSS:** Utility-first CSS framework
- **Better Auth:** Authentication library with JWT plugin

---

## Current Status

### Phase 1: ✅ Complete
- All features implemented and tested
- Full documentation available
- Testing guide included

### Phase 2: ✅ MVP Complete (61% - 68/111 tasks)

**Completed:**
- ✅ User authentication (registration, login, JWT)
- ✅ Task CRUD operations (create, read, update, delete)
- ✅ User data isolation (service-layer enforcement)
- ✅ Responsive UI with loading/error states
- ✅ Form validation (client and server)

**Pending (Phase 8 - Polish):**
- ❌ Security hardening (rate limiting, CSRF, httpOnly cookies)
- ❌ Performance optimization (pagination, caching)
- ❌ Test coverage (unit, integration, E2E)
- ❌ Advanced features (search, filtering, task editing UI)
- ❌ DevOps (Docker, CI/CD, deployment)

See [Phase 2 Implementation Report](phase2/IMPLEMENTATION_REPORT.md) for detailed status.

---

## API Documentation (Phase 2)

### Authentication Endpoints
```
POST /auth/register    - Create new user account
POST /auth/login       - Authenticate and get JWT token
```

### Task Endpoints (Requires JWT)
```
GET    /users/{user_id}/tasks          - List user's tasks
GET    /users/{user_id}/tasks/{id}     - Get specific task
POST   /users/{user_id}/tasks          - Create new task
PATCH  /users/{user_id}/tasks/{id}     - Update task
DELETE /users/{user_id}/tasks/{id}     - Delete task
```

### Health Check
```
GET /health            - API health status
```

**Interactive API Docs:** Available at http://localhost:8000/docs when backend is running.

---

## Testing

### Phase 1
```bash
cd phase1
pytest  # Run test suite
```

See `phase1/TESTING_GUIDE.md` for manual testing instructions.

### Phase 2
**Manual Testing:** See `phase2/IMPLEMENTATION_REPORT.md` for test checklist.

**Automated Testing:** Not yet implemented (Phase 8 task).

---

## Contributing

This is an educational project demonstrating:
- Progressive software development
- Transition from prototype to production
- Modern full-stack architecture
- Security best practices
- API design patterns

Feel free to use this as a learning resource or starting point for your own projects.

---

## Known Issues & Limitations

### Phase 1
- Single-user only (no authentication)
- File-based storage (not suitable for concurrent access)
- Limited error handling

### Phase 2
- JWT tokens stored in localStorage (should use httpOnly cookies)
- No rate limiting on auth endpoints
- Zero test coverage
- No pagination (will slow down with 100+ tasks)
- Password storage in memory (demo simplification)

See detailed limitations in [Phase 2 Implementation Report](phase2/IMPLEMENTATION_REPORT.md).

---

## Next Steps

### Phase 2 - Remaining Work

**High Priority (Security):**
1. Migrate JWT to httpOnly cookies
2. Implement rate limiting
3. Add CSRF protection
4. Input sanitization for XSS prevention

**Medium Priority (Features & Testing):**
5. Add pagination for task lists
6. Implement task editing UI
7. Add search and filtering
8. Write unit and E2E tests

**Low Priority (Polish):**
9. Docker setup for local development
10. CI/CD pipeline
11. Deployment guide
12. API documentation improvements

**Estimated effort:** 35-50 hours to production-ready.

---

## License

This project is for educational purposes. Feel free to use, modify, and learn from it.

---

## Documentation

- **Phase 1 README:** [phase1/README.md](phase1/README.md)
- **Phase 1 Testing Guide:** [phase1/TESTING_GUIDE.md](phase1/TESTING_GUIDE.md)
- **Phase 2 README:** [phase2/README.md](phase2/README.md)
- **Phase 2 Implementation Report:** [phase2/IMPLEMENTATION_REPORT.md](phase2/IMPLEMENTATION_REPORT.md)
- **Project Constitution:** [.specify/memory/constitution.md](.specify/memory/constitution.md)

---

**Project Status:** Phase 1 Complete | Phase 2 MVP Complete (68/111 tasks)

**Last Updated:** 2026-01-03
