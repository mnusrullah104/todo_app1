---
id: 003
title: create-implementation-plan
stage: plan
date: 2026-01-02
surface: claude-code-cli
model: claude-sonnet-4-5
feature: 002-fullstack-todo-web
branch: 002-fullstack-todo-web
user: developer
command: /sp.plan
labels: [plan, architecture, design, research, phase-ii]
links:
  spec: /specs/002-fullstack-todo-web/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: /specs/002-fullstack-todo-web/plan.md
    status: created
    lines: 207
  - path: /specs/002-fullstack-todo-web/research.md
    status: created
    lines: 358
  - path: /specs/002-fullstack-todo-web/data-model.md
    status: created
    lines: 318
  - path: /specs/002-fullstack-todo-web/contracts/api-endpoints.md
    status: created
    lines: 558
  - path: /specs/002-fullstack-todo-web/quickstart.md
    status: created
    lines: 417
  - path: /CLAUDE.md
    status: created
    lines: unknown
tests:
  - type: none
    status: N/A
    note: Planning phase - no tests generated
---

## Prompt

Execute the /sp.plan command for Phase II: Full-Stack Todo Web Application.

User input provided:
```
Phase II: Full-Stack Todo Web App (Concise)

Create:
- Architecture sketch
- Spec structure and implementation flow
- Development approach
- Validation and acceptance checks

Architecture Sketch:
- Frontend: Next.js 16+ (App Router), Better Auth for login, JWT attached to API calls
- Backend: FastAPI REST service, JWT verification middleware, SQLModel ORM
- Database: Neon Serverless PostgreSQL, users via Better Auth, tasks linked by user_id
- Security Flow: Frontend receives JWT → attaches to API request → backend verifies → filters user data

Spec Structure:
- /specs/overview.md – Phase II scope
- /specs/features/task-crud.md
- /specs/features/authentication.md
- /specs/api/rest-endpoints.md
- /specs/database/schema.md
- /specs/ui/components.md & pages.md
- All implementation references specs using @specs paths

Implementation Approach:
- Workflow: Research-concurrent, spec-driven
- Research & Alignment: Review requirements, validate JWT & DB integration, identify secrets
- Foundation: Lock API contracts, DB schema, auth rules, CLAUDE.md conventions
- Implementation: Backend (JWT middleware, CRUD endpoints, user-scoped queries), Frontend (Better Auth config, API client, responsive UI)
- Validation: API tests, user isolation, spec compliance, iterate if needed

Key Decisions:
- Auth: JWT (stateless) over session-based
- API Design: URL user_id + JWT verification (explicit ownership)
- Repo Structure: Monorepo for single Claude Code context
- ORM: SQLModel (type-safe, clear)
- Spec Granularity: Structured layered specs for clarity

Testing / Validation:
- Auth: 401 for missing/invalid JWT, 403 for user mismatch
- Task Ownership: No cross-user access/modification
- API Contract: HTTP methods, status codes, schemas as spec
- Frontend: JWT auto-attached, UI shows only user tasks, CRUD updates reflected
- Database: Tasks stored with user_id, queries filtered by user
- Spec Compliance: Claude Code follows specs, no Phase III features

Definition of Done:
- Phase II fully implemented, secure, and user-isolated
- All success criteria met
- Specs fully referenceable, enabling Claude Code re-implementation
- No manual coding outside spec-driven workflow
```

## Response snapshot

Successfully executed the /sp.plan workflow, completing both Phase 0 (Research) and Phase 1 (Design):

**Phase 0: Research**
- Resolved frontend testing framework: Vitest (unit/component) + Playwright (E2E)
- Resolved API contract testing: OpenAPI (FastAPI auto-gen) + Schemathesis
- Resolved JWT validation performance: <50ms p95 latency target, PyJWT with dependency injection
- Resolved Better Auth integration: JWT plugin with 7-day expiration, authClient.token() for extraction
- Generated comprehensive research.md with decisions, rationale, alternatives, and sources

**Phase 1: Design**
- Generated data-model.md: User and Task entities with SQLModel, relationships, validation rules, indexes
- Generated contracts/api-endpoints.md: Complete REST API specification with all CRUD endpoints, authentication flow, error handling, and security requirements
- Generated quickstart.md: Developer setup guide with prerequisites, step-by-step instructions, troubleshooting, and environment variables reference
- Updated CLAUDE.md: Agent context file updated with Phase II technology stack

**Technical Context Filled:**
- Backend: Python 3.13+, FastAPI, SQLModel, PyJWT
- Frontend: TypeScript 5.x, Next.js 16+, Better Auth, Tailwind CSS
- Database: Neon Serverless PostgreSQL
- Testing: pytest (backend), Vitest + Playwright (frontend)
- Project Type: Web application monorepo

**Constitution Check:**
- Initial evaluation: ✅ PASS - All Phase II requirements align with constitution
- Post-design re-evaluation: ✅ PASS - All design artifacts complete, no violations

**Architecture Decisions:**
- Monorepo structure (frontend + backend) for Claude Code single context
- JWT stateless authentication with shared BETTER_AUTH_SECRET
- RESTful API with explicit user_id path parameters for authorization clarity
- SQLModel ORM for type-safe database operations
- Vitest (unit) + Playwright (E2E) for frontend testing
- OpenAPI + Schemathesis for API contract testing

## Outcome

- ✅ Impact: Phase 0 and Phase 1 of planning workflow complete. All design artifacts generated and validated. Ready for /sp.tasks to generate implementation tasks.
- 🧪 Tests: No tests generated (planning phase). Testing strategy documented in research.md and contracts.
- 📁 Files: 6 files created (plan.md, research.md, data-model.md, contracts/api-endpoints.md, quickstart.md, CLAUDE.md)
- 🔁 Next prompts: Execute /sp.tasks to generate tasks.md from design artifacts, then /sp.implement to begin implementation
- 🧠 Reflection: Spec-driven planning workflow successfully executed. All NEEDS CLARIFICATION items from Technical Context were resolved through web search and documentation research. Design phase established clear architecture, data model, API contracts, and developer guidance. Constitution compliance verified at both pre-research and post-design gates.

## Evaluation notes (flywheel)

- Failure modes observed: Initial research agents encountered API errors (400 Bad Request). Fallback to direct WebSearch and Context7 documentation lookup succeeded.
- Graders run and results (PASS/FAIL): Constitution Check (PASS at both gates), Technical Context completeness (PASS), Design artifact generation (PASS)
- Prompt variant (if applicable): Standard /sp.plan workflow execution per command template
- Next experiment (smallest change to try): Execute /sp.tasks to validate that design artifacts are sufficient for task generation
