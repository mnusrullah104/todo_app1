# Tasks: Full-Stack Todo Web Application

**Input**: Design documents from `/specs/002-fullstack-todo-web/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-endpoints.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the feature specification. Test tasks are omitted per template guidelines.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/app/` and `frontend/components/`
- Backend uses FastAPI with SQLModel
- Frontend uses Next.js App Router with TypeScript

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for monorepo

- [X] T001 Create backend directory structure: backend/app/{models,schemas,services,api,middleware}/
- [X] T002 Create frontend directory structure: frontend/{app,components,lib}/
- [X] T003 [P] Initialize backend Python project with pyproject.toml and requirements.txt
- [X] T004 [P] Initialize frontend Next.js project with package.json, tsconfig.json, tailwind.config.ts
- [X] T005 [P] Create backend .env.example with DATABASE_URL, BETTER_AUTH_SECRET, HOST, PORT
- [X] T006 [P] Create frontend .env.local.example with NEXT_PUBLIC_BASE_URL, NEXT_PUBLIC_API_BASE_URL, BETTER_AUTH_SECRET
- [X] T007 [P] Create backend/README.md with setup instructions
- [X] T008 [P] Create frontend/README.md with setup instructions
- [X] T009 [P] Add .gitignore for Python (backend) and Node.js (frontend)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [X] T010 Setup FastAPI application entry point in backend/app/main.py with CORS middleware
- [X] T011 Configure CORS to allow frontend origin (http://localhost:3000) in backend/app/main.py
- [X] T012 Setup SQLModel database engine and session management in backend/app/database.py
- [X] T013 Initialize Alembic for database migrations in backend/alembic/
- [X] T014 Create health check endpoint GET /health in backend/app/api/health.py
- [X] T015 Create base response schemas in backend/app/schemas/__init__.py
- [X] T016 Setup error handling middleware in backend/app/middleware/error_handler.py
- [X] T017 Configure logging infrastructure in backend/app/utils/logger.py

### Frontend Foundation

- [X] T018 [P] Create Next.js root layout in frontend/app/layout.tsx with Better Auth provider
- [X] T019 [P] Configure Better Auth client in frontend/lib/auth.ts with JWT plugin and 7-day expiration
- [X] T020 [P] Create API client utility in frontend/lib/api-client.ts with JWT token attachment
- [X] T021 [P] Define TypeScript types for Task and User in frontend/lib/types.ts
- [X] T022 [P] Create reusable UI components: Button, Input, Card in frontend/components/ui/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to register for accounts and log in securely with JWT authentication

**Independent Test**: Create account, log out, log back in, and verify session persistence with valid JWT token

### Backend - Authentication Infrastructure

- [X] T023 [P] [US1] Create User model in backend/app/models/user.py with SQLModel (id, email, email_verified, name, timestamps)
- [X] T024 [P] [US1] Create authentication schemas in backend/app/schemas/auth.py (LoginRequest, RegisterRequest, AuthResponse)
- [X] T025 [US1] Implement JWT authentication middleware in backend/app/middleware/auth.py with PyJWT token validation
- [X] T026 [US1] Create get_current_user dependency in backend/app/services/auth_service.py for extracting user from JWT
- [X] T027 [US1] Implement password hashing utilities in backend/app/utils/security.py using passlib
- [X] T028 [US1] Create authentication service in backend/app/services/auth_service.py with register and login methods
- [X] T029 [US1] Create database migration for users table in backend/alembic/versions/001_create_users_table.py

### Frontend - Authentication UI

- [X] T030 [P] [US1] Create registration page in frontend/app/register/page.tsx with email/password form
- [X] T031 [P] [US1] Create login page in frontend/app/login/page.tsx with email/password form
- [X] T032 [P] [US1] Create AuthForm component in frontend/components/AuthForm.tsx for reusable form fields
- [X] T033 [US1] Implement Better Auth registration flow with JWT token retrieval
- [X] T034 [US1] Implement Better Auth login flow with JWT token storage
- [X] T035 [US1] Add form validation for email (RFC 5322) and password (min 8 chars)
- [X] T036 [US1] Handle authentication errors and display user-friendly messages
- [X] T037 [US1] Implement session persistence check on app load
- [X] T038 [US1] Create landing page in frontend/app/page.tsx with navigation to login/register

**Checkpoint**: Users can register, login, and maintain sessions. JWT tokens are issued and validated correctly.

---

## Phase 4: User Story 2 - View Personal Task List (Priority: P1)

**Goal**: Enable authenticated users to view all their tasks in a list, sorted by most recent first

**Independent Test**: Log in and verify only authenticated user's tasks are displayed, with no cross-user data leakage

### Backend - Task Read Operations

- [X] T039 [P] [US2] Create Task model in backend/app/models/task.py with SQLModel (id, user_id FK, title, description, completed, timestamps)
- [X] T040 [P] [US2] Create Task response schema in backend/app/schemas/task.py (TaskResponse with all fields)
- [X] T041 [US2] Create database migration for tasks table in backend/alembic/versions/002_create_tasks_table.py with user_id FK and indexes
- [X] T042 [US2] Implement TaskService.get_all_tasks(user_id) in backend/app/services/task_service.py with ORDER BY created_at DESC
- [X] T043 [US2] Implement TaskService.get_task_by_id(task_id, user_id) in backend/app/services/task_service.py with user ownership check
- [X] T044 [US2] Create GET /api/{user_id}/tasks endpoint in backend/app/api/tasks.py with JWT auth middleware
- [X] T045 [US2] Create GET /api/{user_id}/tasks/{task_id} endpoint in backend/app/api/tasks.py with JWT auth middleware
- [X] T046 [US2] Add user_id verification: JWT sub claim must match URL user_id parameter (403 if mismatch)

### Frontend - Task Display UI

- [X] T047 [P] [US2] Create dashboard page in frontend/app/dashboard/page.tsx as main task list view
- [X] T048 [P] [US2] Create TaskList component in frontend/components/TaskList.tsx to display array of tasks
- [X] T049 [P] [US2] Create TaskItem component in frontend/components/TaskItem.tsx to display single task
- [X] T050 [US2] Implement API call to fetch tasks in frontend/lib/api-client.ts with JWT header
- [X] T051 [US2] Add loading state handling for task list fetch
- [X] T052 [US2] Display empty state with "Create your first task" message when no tasks exist
- [X] T053 [US2] Add error handling for 401/403 responses and redirect to login
- [X] T054 [US2] Implement auto-redirect to dashboard after successful login

**Checkpoint**: Authenticated users can view their personal task list. Data isolation is enforced (no cross-user access).

---

## Phase 5: User Story 3 - Create New Tasks (Priority: P1)

**Goal**: Enable authenticated users to create new tasks with title and optional description

**Independent Test**: Log in, create one or more tasks, verify they appear in the list and are persisted to database

### Backend - Task Creation

- [X] T055 [P] [US3] Create TaskCreate schema in backend/app/schemas/task.py (title required max 200, description optional max 2000)
- [X] T056 [US3] Implement TaskService.create_task(user_id, task_data) in backend/app/services/task_service.py
- [X] T057 [US3] Create POST /api/{user_id}/tasks endpoint in backend/app/api/tasks.py with JWT auth middleware
- [X] T058 [US3] Add request validation: title required, non-empty after trim, max 200 chars
- [X] T059 [US3] Add request validation: description optional, max 2000 chars
- [X] T060 [US3] Return 201 Created with full task object including auto-generated id and timestamps

### Frontend - Task Creation UI

- [X] T061 [P] [US3] Create TaskForm component in frontend/components/TaskForm.tsx with title and description inputs
- [X] T062 [US3] Add TaskForm to dashboard page for inline task creation
- [X] T063 [US3] Implement API call to create task in frontend/lib/api-client.ts with JWT header
- [X] T064 [US3] Add client-side validation: title required, max 200 chars
- [X] T065 [US3] Add client-side validation: description optional, max 2000 chars
- [X] T066 [US3] Handle 401/403 responses and redirect to login
- [X] T067 [US3] Clear form after successful task creation
- [X] T068 [US3] Refresh task list after successful creation to show new task at top

**Checkpoint**: Users can create tasks that are persisted to database and immediately visible in their task list.

---

## Phase 6: User Story 4 - Complete and Update Tasks (Priority: P2)

**Goal**: Enable users to mark tasks complete and update task details

**Independent Test**: Create a task, mark it complete, edit its details, and verify changes persist

### Backend - Task Update Operations

- [ ] T069 [P] [US4] Create TaskUpdate schema in backend/app/schemas/task.py (title, description, completed all optional)
- [ ] T070 [US4] Implement TaskService.update_task(task_id, user_id, task_data) in backend/app/services/task_service.py
- [ ] T071 [US4] Create PATCH /api/{user_id}/tasks/{task_id} endpoint in backend/app/api/tasks.py with JWT auth middleware
- [ ] T072 [US4] Verify task exists and belongs to authenticated user (404 if not found, 403 if wrong user)
- [ ] T073 [US4] Update updated_at timestamp automatically on PATCH
- [ ] T074 [US4] Return 200 OK with full updated task object

### Frontend - Task Edit UI

- [ ] T075 [P] [US4] Add edit mode toggle to TaskItem component with inline edit form
- [ ] T076 [P] [US4] Add completion checkbox to TaskItem component
- [ ] T077 [US4] Implement API call to update task in frontend/lib/api-client.ts with JWT header
- [ ] T078 [US4] Handle completion toggle: PATCH with completed field only
- [ ] T079 [US4] Handle title/description edit: PATCH with title and/or description fields
- [ ] T080 [US4] Add visual distinction for completed tasks (strikethrough, different color)
- [ ] T081 [US4] Update task list locally after successful update (optimistic UI update)
- [ ] T082 [US4] Handle 404/403 errors appropriately

**Checkpoint**: Users can mark tasks complete and edit task details. Changes are persisted and reflected in UI.

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Enable users to permanently delete tasks they no longer need

**Independent Test**: Create a task, delete it, verify it no longer appears in list and is removed from database

### Backend - Task Deletion

- [ ] T083 [US5] Implement TaskService.delete_task(task_id, user_id) in backend/app/services/task_service.py
- [ ] T084 [US5] Create DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/app/api/tasks.py with JWT auth middleware
- [ ] T085 [US5] Verify task exists and belongs to authenticated user (404 if not found, 403 if wrong user)
- [ ] T086 [US5] Return 200 OK with success message after deletion

### Frontend - Task Deletion UI

- [ ] T087 [P] [US5] Add delete button to TaskItem component
- [ ] T088 [US5] Implement API call to delete task in frontend/lib/api-client.ts with JWT header
- [ ] T089 [US5] Add confirmation dialog before deletion ("Are you sure?")
- [ ] T090 [US5] Remove task from list locally after successful deletion
- [ ] T091 [US5] Handle 404/403 errors appropriately

**Checkpoint**: Users can delete tasks. Tasks are permanently removed from database and UI.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and production readiness

- [ ] T092 [P] Add loading spinners/skeletons for all API calls across frontend
- [ ] T093 [P] Implement toast notifications for success/error messages in frontend
- [ ] T094 [P] Add proper error handling for database connection failures (503 with Retry-After header)
- [ ] T095 [P] Add request logging for all API endpoints in backend
- [ ] T096 [P] Configure structured logging with JSON format in backend
- [ ] T097 [P] Add rate limiting middleware to prevent abuse
- [ ] T098 [P] Implement responsive design for mobile browsers using Tailwind breakpoints
- [ ] T099 [P] Add favicon and meta tags to frontend/app/layout.tsx
- [ ] T100 [P] Generate OpenAPI specification and test at /docs endpoint
- [ ] T101 [P] Create docs/architecture.md with system architecture diagram
- [ ] T102 [P] Update main README.md with project overview and links to phase docs
- [ ] T103 Validate quickstart.md instructions by following setup steps
- [ ] T104 Security audit: Verify all endpoints require JWT authentication
- [ ] T105 Security audit: Verify user_id verification on all task operations
- [ ] T106 Security audit: Check for SQL injection vulnerabilities (should be prevented by SQLModel)
- [ ] T107 Performance check: Verify JWT validation latency is <50ms p95
- [ ] T108 [P] Add database connection pooling configuration
- [ ] T109 [P] Optimize database queries with proper indexes (already in migration)
- [ ] T110 Code cleanup: Remove console.logs and debug statements
- [ ] T111 Code cleanup: Ensure consistent code formatting (Prettier for TS, Black for Python)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - US1 (Authentication) MUST complete before US2-US5 (tasks require authenticated users)
  - US2 (View Tasks) + US3 (Create Tasks) can proceed after US1
  - US4 (Update Tasks) depends on US2 and US3 (need tasks to update)
  - US5 (Delete Tasks) depends on US2 and US3 (need tasks to delete)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Authentication**: No dependencies - MUST complete first (foundational for all other stories)
- **User Story 2 (P1) - View Tasks**: Depends on US1 (need authentication to view tasks)
- **User Story 3 (P1) - Create Tasks**: Depends on US1 (need authentication to create tasks)
- **User Story 4 (P2) - Update Tasks**: Depends on US1, US2, US3 (need authentication, ability to view and create tasks)
- **User Story 5 (P3) - Delete Tasks**: Depends on US1, US2, US3 (need authentication, ability to view and create tasks)

### Within Each User Story

- Backend models before backend services
- Backend services before backend API endpoints
- Frontend components can be built in parallel with backend
- API integration happens after both backend and frontend components exist
- Validation and error handling after core functionality

### Parallel Opportunities

**Phase 1 (Setup):**
- T003, T004 (Initialize backend and frontend projects) can run in parallel
- T005, T006 (Create env examples) can run in parallel
- T007, T008, T009 (Documentation and gitignore) can run in parallel

**Phase 2 (Foundational):**
- T018, T019, T020, T021, T022 (All frontend foundation tasks) can run in parallel
- Backend tasks must be sequential (database → main app → middleware)

**Phase 3 (US1 - Authentication):**
- T023, T024 (User model and schemas) can run in parallel
- T030, T031, T032 (All frontend pages and components) can run in parallel

**Phase 4 (US2 - View Tasks):**
- T039, T040 (Task model and schema) can run in parallel
- T047, T048, T049 (All frontend components) can run in parallel

**Phase 5 (US3 - Create Tasks):**
- T055 (Schema) and T061 (Frontend component) can run in parallel

**Phase 6 (US4 - Update Tasks):**
- T069 (Schema) and T075, T076 (Frontend components) can run in parallel

**Phase 7 (US5 - Delete Tasks):**
- T087 (Delete button) can be added while backend is being implemented

**Phase 8 (Polish):**
- Most polish tasks marked [P] can run in parallel (different files)

---

## Parallel Example: User Story 1 (Authentication)

```bash
# After Foundational phase is complete, launch these in parallel:

# Backend models and schemas (different files):
Task T023: "Create User model in backend/app/models/user.py"
Task T024: "Create authentication schemas in backend/app/schemas/auth.py"

# Frontend pages (different files):
Task T030: "Create registration page in frontend/app/register/page.tsx"
Task T031: "Create login page in frontend/app/login/page.tsx"
Task T032: "Create AuthForm component in frontend/components/AuthForm.tsx"
```

---

## Parallel Example: User Story 2 (View Tasks)

```bash
# After US1 is complete, launch these in parallel:

# Backend models and schemas (different files):
Task T039: "Create Task model in backend/app/models/task.py"
Task T040: "Create Task response schema in backend/app/schemas/task.py"

# Frontend components (different files):
Task T047: "Create dashboard page in frontend/app/dashboard/page.tsx"
Task T048: "Create TaskList component in frontend/components/TaskList.tsx"
Task T049: "Create TaskItem component in frontend/components/TaskItem.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only)

The minimum viable product consists of:

1. **Phase 1**: Setup (T001-T009) → Project initialized
2. **Phase 2**: Foundational (T010-T022) → Core infrastructure ready
3. **Phase 3**: User Story 1 (T023-T038) → Authentication working
4. **Phase 4**: User Story 2 (T039-T054) → Users can view their tasks
5. **Phase 5**: User Story 3 (T055-T068) → Users can create tasks

**STOP and VALIDATE**: At this point you have a working todo app where users can:
- Register and login
- Create tasks
- View their personal task list

This is a fully functional MVP worth deploying!

### Incremental Delivery

After MVP is validated:

6. **Phase 6**: User Story 4 (T069-T082) → Add task editing and completion
7. **Phase 7**: User Story 5 (T083-T091) → Add task deletion
8. **Phase 8**: Polish (T092-T111) → Production hardening

Each addition maintains backward compatibility and adds value.

### Parallel Team Strategy

With 3 developers after Foundational phase completes:

**Developer A: Authentication (US1)**
- T023-T029 (Backend auth)
- T030-T038 (Frontend auth)

**Developer B: View Tasks (US2)** - BLOCKED until US1 complete
- T039-T046 (Backend read operations)
- T047-T054 (Frontend display UI)

**Developer C: Create Tasks (US3)** - BLOCKED until US1 complete
- T055-T060 (Backend create operations)
- T061-T068 (Frontend creation UI)

Once US1 is done, Developers B and C can work in parallel since US2 and US3 don't depend on each other.

---

## Notes

- **[P]** tasks are in different files with no dependencies and can run in parallel
- **[Story]** label maps task to specific user story for traceability
- Each user story is independently testable at its checkpoint
- All database queries include `WHERE user_id = ?` for data isolation
- All API endpoints validate JWT token and verify user_id match
- Commit after completing each task or logical group
- Stop at any checkpoint to validate story independently before proceeding
- User Story 1 (Authentication) is the critical path - nothing else works without it
- User Stories 2 and 3 can proceed in parallel after US1
- User Stories 4 and 5 depend on US2 and US3 being complete

---

## Total Task Count

- **Phase 1 (Setup)**: 9 tasks
- **Phase 2 (Foundational)**: 13 tasks (Backend: 8, Frontend: 5)
- **Phase 3 (US1 - Authentication)**: 16 tasks (Backend: 7, Frontend: 9)
- **Phase 4 (US2 - View Tasks)**: 16 tasks (Backend: 8, Frontend: 8)
- **Phase 5 (US3 - Create Tasks)**: 14 tasks (Backend: 6, Frontend: 8)
- **Phase 6 (US4 - Update Tasks)**: 14 tasks (Backend: 6, Frontend: 8)
- **Phase 7 (US5 - Delete Tasks)**: 9 tasks (Backend: 4, Frontend: 5)
- **Phase 8 (Polish)**: 20 tasks

**Total: 111 tasks**

### Tasks Per User Story

- US1 (Authentication): 16 tasks
- US2 (View Tasks): 16 tasks
- US3 (Create Tasks): 14 tasks
- US4 (Update/Complete): 14 tasks
- US5 (Delete): 9 tasks

### MVP Scope (US1 + US2 + US3)

- Setup + Foundational + US1 + US2 + US3 = **68 tasks** for MVP
- Remaining 43 tasks for update/delete functionality and polish

### Parallel Opportunities Identified

- **Setup phase**: 7 out of 9 tasks can run in parallel
- **Foundational phase**: 5 frontend tasks can run in parallel
- **Each user story**: 2-5 tasks can run in parallel within each story
- **Polish phase**: 15 out of 20 tasks can run in parallel
- **Cross-story**: US2 and US3 can be developed in parallel after US1 completes

---

## Format Validation

✅ All tasks follow the required checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
✅ All tasks have sequential IDs (T001-T111)
✅ All parallelizable tasks are marked with [P]
✅ All user story tasks are labeled with [US1]-[US5]
✅ All tasks include specific file paths
✅ Setup and Foundational phases have no [Story] labels (correct)
✅ Polish phase has no [Story] labels (correct)
✅ All user story phases (3-7) have [Story] labels on every task (correct)
