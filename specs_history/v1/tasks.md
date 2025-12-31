---
description: "Task list for Todo Console Application implementation"
---

# Tasks: Todo Console Application

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-interface.md, quickstart.md

**Tests**: NOT INCLUDED - Manual CLI-based testing per quickstart.md (constitution requirement for Phase I)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root (per plan.md decision)
- Architecture: `src/models/`, `src/services/`, `src/cli/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure with src/, src/models/, src/services/, src/cli/ directories
- [X] T002 [P] Create __init__.py files in src/, src/models/, src/services/, src/cli/
- [X] T003 Initialize pyproject.toml with UV for Python 3.13+ project configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create Task dataclass with id, title, description, completed fields in src/models/task.py
- [X] T005 [P] Create Result dataclass with success, message, data fields in src/services/task_manager.py
- [X] T006 Create TaskManager class with __init__, tasks dict, and _next_id counter in src/services/task_manager.py
- [X] T007 [P] Implement input validation helper get_integer_input() in src/cli/ui.py
- [X] T008 [P] Implement input validation helper get_string_input() in src/cli/ui.py
- [X] T009 [P] Implement input validation helper get_confirmation() in src/cli/ui.py
- [X] T010 Create main menu display function display_menu() in src/cli/ui.py
- [X] T011 Create main application loop in src/main.py with menu handling

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks and view the current task list for basic task tracking

**Independent Test**: Add multiple tasks via CLI menu option 1, then view list via option 2 to confirm all tasks appear with correct titles, descriptions, and default incomplete status (✖)

### Implementation for User Story 1

- [X] T012 [P] [US1] Implement add_task(title, description) method in src/services/task_manager.py with validation, ID assignment, and storage
- [X] T013 [P] [US1] Implement get_all_tasks() method in src/services/task_manager.py returning list of all tasks
- [X] T014 [US1] Implement add_task_ui() function in src/cli/ui.py handling menu option 1 with title/description prompts
- [X] T015 [US1] Implement view_tasks_ui() function in src/cli/ui.py displaying all tasks with ID, status icon, title, description, and summary
- [X] T016 [US1] Integrate add_task_ui() as menu option 1 in src/main.py
- [X] T017 [US1] Integrate view_tasks_ui() as menu option 2 in src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create and view tasks independently

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Enable users to toggle task completion status for progress tracking

**Independent Test**: Create tasks using US1, toggle their status using task IDs via menu option 5, verify status indicators change between ✖ (incomplete) and ✔ (complete)

### Implementation for User Story 2

- [X] T018 [US2] Implement toggle_status(task_id) method in src/services/task_manager.py with ID validation and status flipping
- [X] T019 [US2] Implement toggle_status_ui() function in src/cli/ui.py handling menu option 5 with task ID prompt and status display
- [X] T020 [US2] Integrate toggle_status_ui() as menu option 5 in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can create, view, and toggle tasks

---

## Phase 5: User Story 3 - Update Task Content (Priority: P3)

**Goal**: Enable users to modify task titles and descriptions to correct mistakes or update details

**Independent Test**: Create tasks using US1, update their title and/or description by ID via menu option 3, view to confirm changes persisted

### Implementation for User Story 3

- [X] T021 [US3] Implement update_task(task_id, new_title, new_description) method in src/services/task_manager.py with validation
- [X] T022 [US3] Implement update_task_ui() function in src/cli/ui.py handling menu option 3 with task ID, display current task, and prompt for new values
- [X] T023 [US3] Integrate update_task_ui() as menu option 3 in src/main.py

**Checkpoint**: User Stories 1, 2, and 3 are independently functional - users can create, view, toggle, and update tasks

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable users to remove tasks to keep the task list clean and relevant

**Independent Test**: Create tasks using US1, delete specific tasks by ID via menu option 4 with confirmation, view to confirm removed tasks no longer appear

### Implementation for User Story 4

- [X] T024 [US4] Implement delete_task(task_id) method in src/services/task_manager.py with ID validation and removal
- [X] T025 [US4] Implement delete_task_ui() function in src/cli/ui.py handling menu option 4 with task ID prompt, task display, and confirmation
- [X] T026 [US4] Integrate delete_task_ui() as menu option 4 in src/main.py

**Checkpoint**: All user stories are independently functional - complete CRUD operations available

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T027 Add error handling for edge cases (empty task list messages, max retry attempts) across all UI functions in src/cli/ui.py
- [ ] T028 Implement exit functionality for menu option 6 with goodbye message in src/main.py
- [ ] T029 Add task count summary to menu display showing total, incomplete, and complete counts in src/cli/ui.py
- [ ] T030 [P] Create README.md with setup instructions (Python 3.13+, UV, WSL2), usage guide, and feature list
- [ ] T031 Validate all acceptance scenarios from spec.md using quickstart.md testing protocol
- [ ] T032 Create specs_history/v1/ directory and copy spec.md, plan.md, tasks.md for version tracking

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4) - RECOMMENDED for single developer
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses US1 view functionality but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses US1 view functionality but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Uses US1 view functionality but independently testable

### Within Each User Story

- Service layer methods before CLI UI functions
- CLI UI functions before main.py integration
- US1 establishes the pattern, other stories follow similar structure
- Each story should be testable via quickstart.md protocol after completion

### Parallel Opportunities

- **Phase 1**: T001 and T002 can run in parallel (different files)
- **Phase 2**: T004-T005 can run in parallel (different files), T007-T009 can run in parallel (different files but same module - only if no conflicts)
- **Phase 3 (US1)**: T012 and T013 can run in parallel (same file but different methods)
- **Once Foundational completes**: All user stories (Phase 3-6) CAN run in parallel by different developers, though sequential recommended for single developer
- **Phase 7**: T030 (README) can run in parallel with testing tasks

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes:

# Launch model methods in parallel (same file, different methods):
Task T012: "Implement add_task(title, description) method in src/services/task_manager.py"
Task T013: "Implement get_all_tasks() method in src/services/task_manager.py"

# Then launch UI functions sequentially (as they depend on service layer)
Task T014: "Implement add_task_ui() function in src/cli/ui.py"
Task T015: "Implement view_tasks_ui() function in src/cli/ui.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) - RECOMMENDED

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T011) - **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 (T012-T017)
4. **STOP and VALIDATE**: Test User Story 1 independently using quickstart.md test suite 1-2
5. User has working task creation and viewing - MVP delivered!

### Incremental Delivery (Build on MVP)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T012-T017) → Test independently → Working task tracker (MVP!)
3. Add User Story 2 (T018-T020) → Test independently → Can mark tasks complete
4. Add User Story 3 (T021-T023) → Test independently → Can edit tasks
5. Add User Story 4 (T024-T026) → Test independently → Can delete tasks
6. Add Polish (T027-T032) → Test all scenarios → Production ready
7. Each story adds value without breaking previous stories

### Full Sequential Strategy (Single Developer)

Execute tasks in exact order T001 → T032, testing each user story checkpoint:

1. T001-T003: Setup complete
2. T004-T011: Foundation complete (validate basic structure works)
3. T012-T017: US1 complete → **Test Suite 1-2 from quickstart.md**
4. T018-T020: US2 complete → **Test Suite 3 from quickstart.md**
5. T021-T023: US3 complete → **Test Suite 4 from quickstart.md**
6. T024-T026: US4 complete → **Test Suite 5 from quickstart.md**
7. T027-T032: Polish complete → **Full test protocol (Test Suite 1-8)**

---

## Task Mapping to Spec Requirements

### Functional Requirements Coverage

| Requirement | Tasks |
|-------------|-------|
| FR-001: Unique ID assignment | T006, T012 |
| FR-002: Task creation with title/description | T004, T012, T014 |
| FR-003: IDs never reused | T006, T012 |
| FR-004: Completion status tracking | T004, T012, T018 |
| FR-005: Display all tasks | T013, T015 |
| FR-006: Toggle task status | T018, T019 |
| FR-007: Update task content | T021, T022 |
| FR-008: Delete tasks | T024, T025 |
| FR-009: Validate task ID existence | T012, T018, T021, T024 |
| FR-010: Clear error messages | T005, T007-T009, T027 |
| FR-011: In-memory storage | T006 |
| FR-012: CLI interface | T007-T011, all UI tasks |
| FR-013: Handle empty list | T015, T027 |

### User Story Coverage

| User Story | Tasks | Test Suite |
|------------|-------|------------|
| US1: Create and View | T012-T017 | Test Suite 1-2 (quickstart.md) |
| US2: Mark Complete | T018-T020 | Test Suite 3 (quickstart.md) |
| US3: Update Content | T021-T023 | Test Suite 4 (quickstart.md) |
| US4: Delete Tasks | T024-T026 | Test Suite 5 (quickstart.md) |

---

## Success Criteria Validation

After completing all tasks, validate against spec.md success criteria:

- **SC-001**: Task creation <2 seconds → Validate with T031 using Test 6.1
- **SC-002**: All 5 CRUD operations functional → Validate with T031 using Test 7.1
- **SC-003**: ID uniqueness across 100+ operations → Validate with T031 using Test 5.3
- **SC-004**: Error messages <1 second → Validate with T031 using Test 6.2
- **SC-005**: View 100 tasks <3 seconds → Validate with T031 using Test 6.3
- **SC-006**: Handle edge cases without crashes → Validate with T031 using Test Suite 6
- **SC-007**: 90% user success after 2-min tutorial → Validate with T031 using Test 8.1

---

## Notes

- **[P]** tasks = different files or different methods in same file, no sequential dependencies
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No unit/integration tests included - manual CLI testing per constitution requirement
- Testing performed via quickstart.md protocol after each user story checkpoint
- Commit after completing each user story phase (after T017, T020, T023, T026, T032)
- Stop at any checkpoint to validate story independently before proceeding
- Total tasks: 32 (3 setup + 8 foundational + 6 US1 + 3 US2 + 3 US3 + 3 US4 + 6 polish)
- Estimated MVP (US1 only): 17 tasks (T001-T017)
- Constitution compliant: Python 3.13+, standard library only, clean architecture, spec-driven

---

## Quick Reference

**To implement MVP (US1 only)**: Execute T001-T017, then test with quickstart.md Test Suite 1-2
**To add toggle status (US2)**: Execute T018-T020, then test with Test Suite 3
**To add update (US3)**: Execute T021-T023, then test with Test Suite 4
**To add delete (US4)**: Execute T024-T026, then test with Test Suite 5
**To complete feature**: Execute all T001-T032, then test with full Test Suite 1-8

**Parallel execution**: Only recommended with multiple developers - single developer should execute sequentially in priority order
