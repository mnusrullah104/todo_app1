# Phase II: Full-Stack Todo Web Application

**Complete implementation of a multi-user todo web application with JWT authentication.**

---

## Project Overview

This is Phase II of the todo application project - a complete rewrite as a modern full-stack web application with separate frontend and backend services.

**Tech Stack:**
- **Frontend:** Next.js 15 (React 19) + Tailwind CSS + TypeScript
- **Backend:** FastAPI (Python 3.11+) + SQLModel + PostgreSQL
- **Authentication:** JWT tokens with 7-day expiration
- **Database:** PostgreSQL with Alembic migrations

---

## Features Implemented ✅

### User Authentication
- ✅ User registration with email/password
- ✅ Secure login with JWT token generation
- ✅ Password hashing with bcrypt
- ✅ Session persistence via localStorage
- ✅ Auto-redirect on authentication errors

### Task Management
- ✅ View all personal tasks (ordered by creation date)
- ✅ Create new tasks with title and description
- ✅ Mark tasks as complete/incomplete with checkbox
- ✅ Delete tasks with confirmation dialog
- ✅ Update task fields (title, description, completion)
- ✅ Task statistics (total, completed, pending)
- ✅ Empty state when no tasks exist

### Security & Data Isolation
- ✅ JWT-based authentication on all task endpoints
- ✅ User can only access their own tasks (enforced at service layer)
- ✅ 403 Forbidden if JWT user_id doesn't match URL user_id
- ✅ Token expiration handling with auto-logout

### User Experience
- ✅ Loading states during async operations
- ✅ Error messages with user-friendly text
- ✅ Form validation with inline errors
- ✅ Character counters for long text fields
- ✅ Responsive design (mobile-friendly)
- ✅ Grouped task display (pending/completed)

---

## Project Structure

```
phase2/
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── auth.py       # POST /auth/register, /auth/login
│   │   │   ├── health.py     # GET /health
│   │   │   └── tasks.py      # Task CRUD endpoints
│   │   ├── middleware/
│   │   │   ├── auth.py       # JWT validation middleware
│   │   │   └── error_handler.py
│   │   ├── models/
│   │   │   ├── task.py       # Task SQLModel
│   │   │   └── user.py       # User SQLModel
│   │   ├── schemas/
│   │   │   ├── auth.py       # Auth request/response schemas
│   │   │   └── task.py       # Task request/response schemas
│   │   ├── services/
│   │   │   ├── auth_service.py   # Auth business logic
│   │   │   └── task_service.py   # Task business logic
│   │   ├── utils/
│   │   │   ├── logger.py     # Logging config
│   │   │   └── security.py   # Password hashing
│   │   ├── database.py       # SQLModel engine & sessions
│   │   └── main.py           # FastAPI app entry point
│   ├── alembic/
│   │   └── versions/
│   │       ├── 001_create_users_table.py
│   │       └── 002_create_tasks_table.py
│   ├── .env.example
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                  # Next.js frontend
│   ├── app/
│   │   ├── dashboard/        # Main task management page
│   │   │   └── page.tsx
│   │   ├── login/            # Login page
│   │   │   └── page.tsx
│   │   ├── register/         # Registration page
│   │   │   └── page.tsx
│   │   ├── layout.tsx        # Root layout
│   │   ├── page.tsx          # Landing page
│   │   └── globals.css       # Global styles
│   ├── components/
│   │   ├── tasks/
│   │   │   ├── TaskForm.tsx  # Task creation form
│   │   │   ├── TaskItem.tsx  # Individual task component
│   │   │   └── TaskList.tsx  # Task list with stats
│   │   └── ui/
│   │       ├── Button.tsx    # Reusable button
│   │       ├── Card.tsx      # Container component
│   │       └── Input.tsx     # Form input
│   ├── lib/
│   │   ├── api-client.ts     # API request wrapper
│   │   ├── auth.ts           # Better Auth client
│   │   └── types.ts          # TypeScript interfaces
│   ├── .env.local.example
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── README.md
│
├── IMPLEMENTATION_REPORT.md  # Detailed status report
└── README.md                  # This file
```

---

## Quick Start

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.11+ (for backend)
- **PostgreSQL** 14+ (database)
- **Git** (version control)

### 1. Clone & Navigate

```bash
cd phase2
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your settings:
#   DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
#   BETTER_AUTH_SECRET=your-secret-key-here (min 32 chars)
#   NEXT_PUBLIC_BASE_URL=http://localhost:3000

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --port 8000
```

Backend will run at: http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local
# Edit .env.local with:
#   NEXT_PUBLIC_API_URL=http://localhost:8000
#   NEXT_PUBLIC_BASE_URL=http://localhost:3000

# Start frontend dev server
npm run dev
```

Frontend will run at: http://localhost:3000

### 4. Test the Application

1. Open http://localhost:3000 in your browser
2. Click "Get Started" to register
3. Fill in email and password (min 8 characters)
4. You'll be redirected to the dashboard
5. Create a task using the form
6. Toggle completion with the checkbox
7. Delete tasks with the delete button

---

## API Endpoints

### Authentication

```
POST /auth/register
Body: { "email": "user@example.com", "password": "password123", "name": "John" }
Response: { "user": {...}, "token": "jwt_token" }

POST /auth/login
Body: { "email": "user@example.com", "password": "password123" }
Response: { "user": {...}, "token": "jwt_token" }
```

### Tasks (Requires JWT Authentication)

```
GET /users/{user_id}/tasks
Headers: Authorization: Bearer {jwt_token}
Response: { "tasks": [...], "total": 5 }

GET /users/{user_id}/tasks/{task_id}
Headers: Authorization: Bearer {jwt_token}
Response: { "id": "...", "title": "...", ... }

POST /users/{user_id}/tasks
Headers: Authorization: Bearer {jwt_token}
Body: { "title": "Buy groceries", "description": "Milk, eggs" }
Response: { "id": "...", "title": "...", ... }

PATCH /users/{user_id}/tasks/{task_id}
Headers: Authorization: Bearer {jwt_token}
Body: { "completed": true }
Response: { "id": "...", "completed": true, ... }

DELETE /users/{user_id}/tasks/{task_id}
Headers: Authorization: Bearer {jwt_token}
Response: 204 No Content
```

### Health Check

```
GET /health
Response: { "status": "healthy" }
```

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### Tasks Table

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description VARCHAR(2000),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE INDEX ix_tasks_user_id ON tasks(user_id);
```

---

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-secret-key-at-least-32-characters-long
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

---

## Development Commands

### Backend

```bash
# Run server with auto-reload
uvicorn app.main:app --reload --port 8000

# Create new migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Run tests (when implemented)
pytest

# Format code
black app/
ruff check app/
```

### Frontend

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests (when implemented)
npm test

# Run E2E tests (when implemented)
npm run test:e2e

# Lint code
npm run lint
```

---

## Testing

### Manual Testing Checklist

- [ ] Register new user account
- [ ] Login with credentials
- [ ] Create task with title only
- [ ] Create task with title + description
- [ ] Mark task as complete
- [ ] Mark task as incomplete
- [ ] Delete task (with confirmation)
- [ ] Logout
- [ ] Login again and verify tasks persist
- [ ] Try accessing dashboard without login (should redirect)
- [ ] Test form validation (empty title, too long description)

### Automated Testing (Not Yet Implemented)

```bash
# Backend unit tests
cd backend
pytest

# Frontend unit tests
cd frontend
npm test

# E2E tests
cd frontend
npm run test:e2e
```

---

## Known Issues & Limitations

### Security Considerations

⚠️ **JWT in localStorage**: Tokens are stored in localStorage for simplicity. Production apps should use httpOnly cookies to prevent XSS attacks.

⚠️ **Password storage**: Passwords are currently stored in-memory rather than in the database. This is a demo simplification.

⚠️ **No rate limiting**: Auth endpoints lack rate limiting, making them vulnerable to brute force attacks.

⚠️ **No input sanitization**: Task content is not sanitized for XSS (though React escapes by default).

### Performance Considerations

⚠️ **No pagination**: All tasks load at once. With 100+ tasks, performance will degrade.

⚠️ **No caching**: Every page load refetches all data from the database.

### Feature Gaps

⚠️ **No task editing UI**: Can toggle completion and delete, but no inline edit form for title/description.

⚠️ **No filtering/sorting**: Cannot filter by status or sort by different criteria.

⚠️ **No search**: Cannot search tasks by title/description.

---

## Next Steps (Phase 8 - Polish)

See `IMPLEMENTATION_REPORT.md` for detailed recommendations:

1. **Security Hardening**
   - Migrate to httpOnly cookies
   - Add rate limiting
   - Implement CSRF protection
   - Add input sanitization

2. **Performance**
   - Implement pagination
   - Add caching layer
   - Optimize database queries

3. **Testing**
   - Backend unit tests (pytest)
   - Frontend unit tests (Vitest)
   - E2E tests (Playwright)

4. **Features**
   - Task editing UI
   - Filtering and sorting
   - Search functionality
   - Task due dates

5. **DevOps**
   - Docker setup
   - CI/CD pipeline
   - Deployment guide

---

## Documentation

- **Full Implementation Report:** See `IMPLEMENTATION_REPORT.md`
- **Backend README:** See `backend/README.md`
- **Frontend README:** See `frontend/README.md`
- **API Docs:** Available at http://localhost:8000/docs (when server is running)

---

## Contributing

This is a learning/demo project. Key architectural decisions:

1. **Monorepo structure** - Single repo for frontend + backend for easier context management with Claude Code
2. **JWT authentication** - Stateless auth with 7-day token expiration
3. **User data isolation** - Enforced at service layer (403 if user_id mismatch)
4. **SQLModel** - Type-safe ORM combining Pydantic + SQLAlchemy

---

## License

This project is for educational purposes. Use freely for learning and experimentation.

---

## Support & Issues

For questions or issues:
1. Check `IMPLEMENTATION_REPORT.md` for detailed status
2. Review API documentation at http://localhost:8000/docs
3. Verify environment variables are configured correctly
4. Check logs: Backend in terminal, Frontend in browser console

---

**Project Status:** MVP Complete (68/111 tasks) - See IMPLEMENTATION_REPORT.md for details
