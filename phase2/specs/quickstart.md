# Quickstart Guide: Full-Stack Todo Web Application

**Feature**: Phase II - Full-Stack Todo Web App
**Date**: 2026-01-02
**Audience**: Developers setting up the project for the first time

This guide walks through setting up the development environment and running the application locally.

---

## Prerequisites

### Required Software

- **Node.js**: 20.x or later (for Next.js frontend)
- **Python**: 3.13 or later (for FastAPI backend)
- **PostgreSQL**: Neon account or local PostgreSQL 15+ instance
- **Git**: For version control

### Required Accounts

- **Neon PostgreSQL**: Sign up at https://neon.tech/ for serverless PostgreSQL database

---

## Project Structure

```
todo_app1/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── specs/             # Specifications and documentation
│   └── 002-fullstack-todo-web/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md (this file)
│       └── contracts/
└── phase1/            # Phase I console app (reference)
```

---

## Setup Instructions

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd todo_app1
git checkout 002-fullstack-todo-web
```

### Step 2: Database Setup

#### Option A: Neon PostgreSQL (Recommended)

1. Create account at https://neon.tech/
2. Create a new project named "todo-app-phase2"
3. Copy the connection string (format: `postgresql://user:pass@host/db?sslmode=require`)
4. Save connection string for environment variable setup

#### Option B: Local PostgreSQL

```bash
# Create database
createdb todo_app_phase2

# Connection string format
postgresql://localhost/todo_app_phase2
```

### Step 3: Backend Setup

```bash
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

**Edit `backend/.env`:**

```env
# Database
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your-secure-random-secret-key-min-32-chars

# Server
HOST=0.0.0.0
PORT=8000
```

**Generate BETTER_AUTH_SECRET:**

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or OpenSSL
openssl rand -base64 32
```

**Run database migrations:**

```bash
# Initialize Alembic (first time only)
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

**Start backend server:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify backend is running:**

Open http://localhost:8000/docs in browser to see Swagger UI.

### Step 4: Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local
```

**Edit `frontend/.env.local`:**

```env
# Frontend URL
NEXT_PUBLIC_BASE_URL=http://localhost:3000

# API URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Authentication (MUST match backend)
BETTER_AUTH_SECRET=your-secure-random-secret-key-min-32-chars
```

**CRITICAL**: `BETTER_AUTH_SECRET` MUST be identical in both `backend/.env` and `frontend/.env.local`.

**Start frontend development server:**

```bash
npm run dev
```

**Verify frontend is running:**

Open http://localhost:3000 in browser.

---

## Development Workflow

### Running Both Servers

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Testing the Application

1. **Register**: Navigate to http://localhost:3000/register
   - Enter email and password (min 8 chars)
   - Submit registration form

2. **Login**: You'll be redirected to dashboard after registration
   - Or manually navigate to http://localhost:3000/login

3. **Create Task**: On dashboard
   - Enter task title (required)
   - Optionally add description
   - Submit form

4. **View Tasks**: Tasks appear in list (newest first)

5. **Complete Task**: Click checkbox to toggle completion status

6. **Edit Task**: Click edit button to modify title/description

7. **Delete Task**: Click delete button to remove task

### API Testing (via Swagger UI)

1. Navigate to http://localhost:8000/docs
2. Click "Authorize" button
3. Enter JWT token in format: `Bearer <token>`
4. Test endpoints interactively

**To get JWT token:**
- Login via frontend
- Open browser developer tools
- Run in console: `authClient.token()` (requires importing authClient)
- Or inspect Network tab for Authorization headers

---

## Common Issues & Troubleshooting

### Issue: "Database connection failed"

**Symptoms**: 503 errors from API endpoints

**Solutions:**
- Verify DATABASE_URL in `backend/.env` is correct
- Test connection: `psql $DATABASE_URL`
- Check Neon dashboard for database status
- Ensure database accepts connections from your IP

### Issue: "401 Unauthorized" on all API requests

**Symptoms**: Can't create/view tasks after login

**Solutions:**
- Verify BETTER_AUTH_SECRET is identical in frontend and backend
- Check JWT token is being sent in Authorization header (DevTools Network tab)
- Verify token hasn't expired (default: 7 days)
- Check backend logs for JWT validation errors

### Issue: "403 Forbidden" on task operations

**Symptoms**: Can login but can't access tasks

**Solutions:**
- Verify user_id in URL matches JWT token's `sub` claim
- Check backend logs for user_id mismatch errors
- Clear browser cookies and re-login

### Issue: CORS errors in browser console

**Symptoms**: Network requests blocked by CORS policy

**Solutions:**
- Verify frontend URL (http://localhost:3000) is in backend CORS origins
- Check backend middleware configuration
- Restart backend server after CORS changes

### Issue: Port already in use

**Symptoms**: `EADDRINUSE: address already in use`

**Solutions:**
- Kill process using port: `npx kill-port 3000` or `npx kill-port 8000`
- Or use different ports in `.env` files

---

## Development Tools

### VS Code Extensions (Recommended)

- **Python**: ms-python.python
- **Pylance**: ms-python.vscode-pylance
- **ES7+ React/Redux/React-Native snippets**: dsznajder.es7-react-js-snippets
- **Tailwind CSS IntelliSense**: bradlc.vscode-tailwindcss
- **REST Client**: humao.rest-client (for API testing)

### Database Tools

- **pgAdmin**: GUI for PostgreSQL management
- **psql**: Command-line PostgreSQL client
- **Neon Web Console**: Built-in SQL editor and monitoring

### API Testing Tools

- **Swagger UI**: Built into FastAPI (http://localhost:8000/docs)
- **ReDoc**: Alternative API docs (http://localhost:8000/redoc)
- **Postman**: Standalone API testing tool
- **HTTPie**: Command-line HTTP client

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_tasks.py

# Run with verbose output
pytest -v
```

### Frontend Tests

```bash
cd frontend

# Run unit tests (Vitest)
npm run test

# Run E2E tests (Playwright)
npm run test:e2e

# Run tests in watch mode
npm run test:watch
```

---

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `postgresql://user:pass@host/db` | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Yes | `abc123...` | JWT signing secret (min 32 chars) |
| `HOST` | No | `0.0.0.0` | Server host (default: 0.0.0.0) |
| `PORT` | No | `8000` | Server port (default: 8000) |

### Frontend (.env.local)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_BASE_URL` | Yes | `http://localhost:3000` | Frontend base URL |
| `NEXT_PUBLIC_API_BASE_URL` | Yes | `http://localhost:8000` | Backend API URL |
| `BETTER_AUTH_SECRET` | Yes | `abc123...` | JWT signing secret (MUST match backend) |

---

## Next Steps

After completing setup:

1. Review architecture in `specs/002-fullstack-todo-web/plan.md`
2. Understand data model in `specs/002-fullstack-todo-web/data-model.md`
3. Study API contracts in `specs/002-fullstack-todo-web/contracts/`
4. Read full specification in `specs/002-fullstack-todo-web/spec.md`

---

## Getting Help

- **Spec Issues**: Review `/specs/002-fullstack-todo-web/spec.md`
- **API Questions**: Check Swagger UI at http://localhost:8000/docs
- **Database Issues**: Consult Neon documentation or PostgreSQL docs
- **Next.js Questions**: https://nextjs.org/docs
- **FastAPI Questions**: https://fastapi.tiangolo.com/

---

## Deployment

Deployment instructions are out of scope for Phase II initial development. Refer to Phase V specifications for production deployment to cloud infrastructure.

For Phase II, focus on local development and ensuring all features work correctly in the development environment.
