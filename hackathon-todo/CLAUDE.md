# Hackathon Todo App Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-09

## Active Technologies

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python 3.11+)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Authentication**: Better Auth (JWT)
- **Architecture**: Monorepo with spec-driven development

## Project Structure

```text
hackathon-todo/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   └── authentication.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── frontend/
│   ├── CLAUDE.md
│   └── (Next.js app)
├── backend/
│   ├── CLAUDE.md
│   └── (FastAPI app)
├── CLAUDE.md
└── README.md
```

## Commands

### Development
- `cd frontend && npm run dev` - Start frontend development server
- `cd backend && uvicorn app.main:app --reload` - Start backend development server
- `cd auth-server && npm run dev` - Start auth server

### Database
- `cd backend && alembic upgrade head` - Run database migrations
- `cd backend && alembic revision --autogenerate -m "description"` - Create migration

### Testing
- `cd backend && pytest` - Run backend tests
- `cd frontend && npm test` - Run frontend tests

## Code Style

### General
- Follow standard conventions for each technology
- Use TypeScript for type safety in frontend
- Use Pydantic models for data validation in backend
- Follow RESTful API design principles
- Implement proper error handling

### Frontend
- Use Next.js App Router
- Component-based architecture
- Type safety with TypeScript interfaces
- Responsive design with Tailwind CSS
- Proper state management

### Backend
- Clean architecture with services layer
- Dependency injection where appropriate
- Proper middleware for authentication
- Comprehensive error handling
- Input validation

## Recent Changes

- Initial spec-driven architecture setup
- Better Auth integration specifications
- Clean API endpoint design
- Professional UI/UX specifications

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->