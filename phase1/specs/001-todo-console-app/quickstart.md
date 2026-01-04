# Quickstart Guide & Testing Protocol: Todo Console Application

**Feature**: 001-todo-console-app
**Date**: 2025-12-31
**Purpose**: Setup instructions, usage guide, and manual testing protocol

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the Application](#running-the-application)
4. [Basic Usage](#basic-usage)
5. [Manual Testing Protocol](#manual-testing-protocol)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python**: 3.13 or higher
- **UV**: Python package manager
- **Platform**: WSL2 (Ubuntu-22.04) for Windows users, or native Linux/macOS

### Check Prerequisites

```bash
# Check Python version (must be 3.13+)
python --version

# Check UV installation
uv --version

# If UV not installed, install it:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Platform Setup (Windows Only)

If you're on Windows, you **must** use WSL2:

```powershell
# Install WSL2 (PowerShell as Administrator)
wsl --install -d Ubuntu-22.04

# Launch Ubuntu
wsl

# Inside WSL, update packages
sudo apt update && sudo apt upgrade -y
```

---

## Installation

### Step 1: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd todo_app1

# Verify branch
git branch
# Should show: * 001-todo-console-app
```

### Step 2: Setup Python Environment with UV

```bash
# Initialize UV project (if not already done)
uv init

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS/WSL
# OR
.venv\Scripts\activate  # Windows (if not using WSL)

# Verify Python version
python --version
# Should show: Python 3.13.x
```

### Step 3: Verify Project Structure

```bash
# List source files
ls -R src/

# Expected structure:
# src/
# ├── __init__.py
# ├── main.py
# ├── models/
# │   ├── __init__.py
# │   └── task.py
# ├── services/
# │   ├── __init__.py
# │   └── task_manager.py
# └── cli/
#     ├── __init__.py
#     └── ui.py
```

---

## Running the Application

### Basic Execution

```bash
# From project root directory
python src/main.py
```

### Expected Initial Screen

```
=== Todo Console Application ===

Current Tasks: 0 (0 incomplete, 0 complete)

Menu Options:
1. Add New Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Enter your choice (1-6):
```

### Exit Application

Enter `6` at main menu or press `Ctrl+C` for immediate exit.

---

## Basic Usage

### Create Your First Task

1. Start application: `python src/main.py`
2. Enter `1` to select "Add New Task"
3. Enter title: `Buy groceries`
4. Enter description: `Milk, eggs, bread` (or press Enter to skip)
5. Task created with ID 1

### View All Tasks

1. From main menu, enter `2` to select "View All Tasks"
2. See list of all tasks with IDs, status icons, and descriptions
3. Press Enter to return to menu

### Mark Task Complete

1. From main menu, enter `5` to select "Toggle Task Status"
2. Enter task ID (e.g., `1`)
3. Status toggles from ✖ (incomplete) to ✔ (complete)
4. Toggle again to mark incomplete

### Update Task

1. From main menu, enter `3` to select "Update Task"
2. Enter task ID (e.g., `1`)
3. Enter new title (or leave blank to keep current)
4. Enter new description (or leave blank to keep current)
5. Task updated with new information

### Delete Task

1. From main menu, enter `4` to select "Delete Task"
2. Enter task ID (e.g., `1`)
3. Confirm deletion by entering `y`
4. Task permanently removed (ID never reused)

---

## Manual Testing Protocol

### Overview

This protocol validates all functional requirements (FR-001 through FR-013) and success criteria (SC-001 through SC-007) from the specification.

**Testing Method**: Manual CLI interaction with documented observations
**Test Duration**: ~20-30 minutes for complete protocol
**Tester**: Any user with basic terminal experience

---

### Test Suite 1: Task Creation (User Story 1, Part 1)

**Objective**: Verify tasks can be created with unique IDs, titles, and optional descriptions

#### Test 1.1: Create Task with Title and Description

**Steps**:
1. Launch application
2. Select option 1 (Add New Task)
3. Enter title: `Buy groceries`
4. Enter description: `Milk, eggs, bread`

**Expected Result**:
- ✓ Task created with ID 1
- Title: "Buy groceries"
- Description: "Milk, eggs, bread"
- Status: Incomplete (✖)
- Success message displayed

**Acceptance Criteria**: FR-001, FR-002, FR-004

#### Test 1.2: Create Task with Title Only (No Description)

**Steps**:
1. From main menu, select option 1
2. Enter title: `Call dentist`
3. Press Enter (skip description)

**Expected Result**:
- ✓ Task created with ID 2
- Title: "Call dentist"
- Description: (empty)
- Status: Incomplete (✖)

**Acceptance Criteria**: FR-002 (optional description)

#### Test 1.3: Attempt to Create Task with Empty Title

**Steps**:
1. From main menu, select option 1
2. Press Enter without typing title

**Expected Result**:
- ✗ Error message: "Title cannot be empty"
- Re-prompt for title
- Task NOT created

**Acceptance Criteria**: FR-002 (title required), FR-010 (clear error messages)

#### Test 1.4: Verify Unique ID Assignment

**Steps**:
1. Create 3 tasks (any titles)
2. Note IDs assigned

**Expected Result**:
- IDs are 1, 2, 3 (sequential)
- Each ID is unique

**Acceptance Criteria**: FR-001 (unique IDs)

---

### Test Suite 2: View Tasks (User Story 1, Part 2)

**Objective**: Verify tasks can be viewed with correct details and status indicators

#### Test 2.1: View Multiple Tasks

**Steps**:
1. Ensure at least 3 tasks exist (from Test Suite 1)
2. Select option 2 (View All Tasks)

**Expected Result**:
- All tasks displayed with:
  - [ID] format (e.g., [1], [2], [3])
  - ✖ status indicator (all incomplete)
  - Title
  - Description (if present)
- Summary line: "Total: 3 tasks (3 incomplete, 0 complete)"

**Acceptance Criteria**: FR-005 (display all tasks)

#### Test 2.2: View Empty Task List

**Steps**:
1. Delete all tasks (or start fresh application)
2. Select option 2 (View All Tasks)

**Expected Result**:
- Message: "No tasks found. Add your first task using option 1!"
- No error or crash

**Acceptance Criteria**: FR-013 (handle empty list gracefully)

---

### Test Suite 3: Toggle Task Status (User Story 2)

**Objective**: Verify task completion status can be toggled

#### Test 3.1: Mark Task Complete

**Steps**:
1. Create task with ID 1 (if not exists)
2. Select option 5 (Toggle Task Status)
3. Enter task ID: `1`

**Expected Result**:
- Status changes from ✖ to ✔
- Confirmation message: "Status toggled successfully!"
- "Complete" displayed

**Acceptance Criteria**: FR-006 (toggle status)

#### Test 3.2: Mark Task Incomplete

**Steps**:
1. Use same task from Test 3.1 (now complete)
2. Select option 5 (Toggle Task Status)
3. Enter task ID: `1`

**Expected Result**:
- Status changes from ✔ back to ✖
- Confirmation message displayed
- "Incomplete" displayed

**Acceptance Criteria**: FR-006 (toggle bidirectional)

#### Test 3.3: Toggle Invalid Task ID

**Steps**:
1. Select option 5 (Toggle Task Status)
2. Enter task ID: `999`

**Expected Result**:
- Error message: "Task ID 999 not found"
- Re-prompt for task ID
- No crash

**Acceptance Criteria**: FR-009 (validate ID), FR-010 (clear error)

#### Test 3.4: Verify Status Indicator in View

**Steps**:
1. Toggle task 1 to complete
2. Create task 2 (leave incomplete)
3. Select option 2 (View All Tasks)

**Expected Result**:
- Task 1 displays ✔
- Task 2 displays ✖
- Summary shows correct counts: "1 incomplete, 1 complete"

**Acceptance Criteria**: FR-005 (status indicators)

---

### Test Suite 4: Update Tasks (User Story 3)

**Objective**: Verify task title and description can be updated

#### Test 4.1: Update Title Only

**Steps**:
1. Create task with ID 1: title "Buy grocries" (typo)
2. Select option 3 (Update Task)
3. Enter task ID: `1`
4. Enter new title: `Buy groceries` (fixed typo)
5. Press Enter (keep description)

**Expected Result**:
- Title updated to "Buy groceries"
- Description unchanged
- ID and status unchanged
- Confirmation message displayed

**Acceptance Criteria**: FR-007 (update task)

#### Test 4.2: Update Description Only

**Steps**:
1. Use task from Test 4.1
2. Select option 3 (Update Task)
3. Enter task ID: `1`
4. Press Enter (keep title)
5. Enter new description: `Milk, eggs, bread, chips`

**Expected Result**:
- Description updated
- Title unchanged
- ID and status unchanged

**Acceptance Criteria**: FR-007 (update task)

#### Test 4.3: Update Both Title and Description

**Steps**:
1. Select option 3 (Update Task)
2. Enter task ID: `1`
3. Enter new title: `Buy groceries and snacks`
4. Enter new description: `Milk, eggs, bread, chips, soda`

**Expected Result**:
- Both fields updated
- ID and status unchanged

**Acceptance Criteria**: FR-007 (update task)

#### Test 4.4: Update Invalid Task ID

**Steps**:
1. Select option 3 (Update Task)
2. Enter task ID: `999`

**Expected Result**:
- Error message: "Task ID 999 not found"
- Re-prompt for task ID
- No crash

**Acceptance Criteria**: FR-009 (validate ID), FR-010 (clear error)

---

### Test Suite 5: Delete Tasks (User Story 4)

**Objective**: Verify tasks can be deleted and IDs are not reused

#### Test 5.1: Delete Task with Confirmation

**Steps**:
1. Create tasks with IDs 1, 2, 3
2. Select option 4 (Delete Task)
3. Enter task ID: `2`
4. Confirm deletion: `y`

**Expected Result**:
- Task 2 removed
- Confirmation message: "Task deleted successfully!"
- View shows only tasks 1 and 3

**Acceptance Criteria**: FR-008 (delete task)

#### Test 5.2: Cancel Deletion

**Steps**:
1. Select option 4 (Delete Task)
2. Enter task ID: `1`
3. Enter `n` to cancel

**Expected Result**:
- Cancellation message displayed
- Task 1 still exists
- No changes to task list

**Acceptance Criteria**: User confirmation required

#### Test 5.3: Verify ID Not Reused

**Steps**:
1. Current state: Tasks 1 and 3 exist (2 was deleted)
2. Create new task (option 1)
3. Note the ID assigned

**Expected Result**:
- New task gets ID 4 (NOT 2)
- IDs: 1, 3, 4

**Acceptance Criteria**: FR-003 (IDs never reused)

#### Test 5.4: Delete Invalid Task ID

**Steps**:
1. Select option 4 (Delete Task)
2. Enter task ID: `2` (already deleted)

**Expected Result**:
- Error message: "Task ID 2 not found"
- Re-prompt for task ID

**Acceptance Criteria**: FR-009 (validate ID)

#### Test 5.5: Delete Last Task

**Steps**:
1. Delete all tasks until one remains
2. Delete the last task
3. View all tasks (option 2)

**Expected Result**:
- Empty task list
- "No tasks found" message
- No crash

**Acceptance Criteria**: FR-013 (handle empty list)

---

### Test Suite 6: Performance & Edge Cases

**Objective**: Verify performance goals and edge case handling

#### Test 6.1: Task Creation Performance (SC-001)

**Steps**:
1. Note current time
2. Create task with title and description
3. Note time when success message appears

**Expected Result**:
- Total time < 2 seconds

**Acceptance Criteria**: SC-001

#### Test 6.2: Error Message Performance (SC-004)

**Steps**:
1. Attempt to toggle invalid task ID (e.g., 999)
2. Note time until error message appears

**Expected Result**:
- Error displayed < 1 second

**Acceptance Criteria**: SC-004

#### Test 6.3: View Large Task List (SC-005)

**Steps**:
1. Create 100 tasks (can use script or manual entry)
2. Select option 2 (View All Tasks)
3. Note time until all tasks displayed

**Expected Result**:
- All 100 tasks displayed < 3 seconds

**Acceptance Criteria**: SC-005

#### Test 6.4: Special Characters in Title

**Steps**:
1. Create task with title: `Task with "quotes" and 'apostrophes'`
2. View task

**Expected Result**:
- Title stored and displayed correctly
- No escaping issues
- No crash

**Acceptance Criteria**: FR-002 (string handling)

#### Test 6.5: Very Long Title (Boundary)

**Steps**:
1. Create task with 500-character title
2. Attempt to create task with 501-character title

**Expected Result**:
- 500-char title accepted
- 501-char title rejected with error

**Acceptance Criteria**: Validation from data-model.md

#### Test 6.6: Empty Description Handling

**Steps**:
1. Create task, press Enter for description
2. View task

**Expected Result**:
- Description shown as empty/blank
- No "null" or placeholder text
- Layout still readable

**Acceptance Criteria**: FR-002 (optional description)

---

### Test Suite 7: Complete Workflow (Integration)

**Objective**: Verify complete task lifecycle works end-to-end

#### Test 7.1: Complete Task Lifecycle

**Steps**:
1. Create task: "Complete project report" with description "Due Friday"
2. View all tasks (verify creation)
3. Update title: "Complete Q4 project report"
4. Toggle status to complete
5. View all tasks (verify completion)
6. Toggle status back to incomplete
7. Update description: "Due Friday - include metrics"
8. Delete task
9. View all tasks (verify deletion)

**Expected Result**:
- All operations succeed
- Task state transitions correctly
- ID remains consistent throughout
- Final view shows task removed

**Acceptance Criteria**: SC-002 (all 5 CRUD operations in single session)

#### Test 7.2: Multiple Tasks Workflow

**Steps**:
1. Create 5 tasks with various titles/descriptions
2. Toggle 2 tasks to complete
3. Update 1 task
4. Delete 1 task
5. View all tasks

**Expected Result**:
- 4 tasks remain (1 deleted)
- Status indicators correct (2 complete, 2 incomplete)
- Updates reflected
- Summary line accurate

**Acceptance Criteria**: FR-005, SC-003 (ID consistency)

---

### Test Suite 8: User Experience (SC-007)

**Objective**: Verify 90% user success after 2-minute tutorial

#### Test 8.1: New User Onboarding

**Setup**: Recruit test user unfamiliar with application

**Steps**:
1. Provide 2-minute tutorial (show menu, explain numbered options)
2. Ask user to:
   - Create 2 tasks
   - View tasks
   - Mark 1 task complete
   - Update 1 task
   - Delete 1 task

**Expected Result**:
- User completes 5/5 operations without assistance
- User understands error messages when mistakes made
- User reports interface is "intuitive" or "easy to use"

**Acceptance Criteria**: SC-007 (90% success rate)

---

## Test Results Template

Use this template to record test results:

```markdown
### Test Execution Report

**Date**: YYYY-MM-DD
**Tester**: [Name]
**Environment**: [OS, Python version]
**Application Version**: [branch/commit]

| Test ID | Test Name | Status | Notes |
|---------|-----------|--------|-------|
| 1.1 | Create with Title+Description | ✅ PASS | |
| 1.2 | Create with Title Only | ✅ PASS | |
| 1.3 | Empty Title Error | ✅ PASS | |
| ... | ... | ... | |

**Summary**:
- Total Tests: X
- Passed: Y
- Failed: Z
- Pass Rate: Y/X %

**Issues Found**: [List any bugs or unexpected behavior]

**Overall Assessment**: [PASS / FAIL / NEEDS REVISION]
```

---

## Troubleshooting

### Issue: "Python version not found"

**Solution**:
```bash
# Install Python 3.13
sudo apt install python3.13 python3.13-venv

# Verify installation
python3.13 --version
```

### Issue: "UV command not found"

**Solution**:
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
source ~/.bashrc

# Verify installation
uv --version
```

### Issue: "Module not found" errors

**Solution**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Verify Python path
which python
# Should show: /path/to/todo_app1/.venv/bin/python

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/todo_app1"
```

### Issue: Unicode characters not displaying (✖, ✔)

**Solution**:
```bash
# Check terminal encoding
echo $LANG
# Should show UTF-8 (e.g., en_US.UTF-8)

# If not UTF-8, set encoding
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

### Issue: Application crashes on invalid input

**Diagnosis**: Likely a validation bug
**Action**: Report bug with exact steps to reproduce
**Workaround**: Restart application, avoid invalid input pattern

---

## Performance Benchmarks

Expected performance on modern hardware (2020+ laptop):

| Operation | Target | Typical |
|-----------|--------|---------|
| Task creation | <2s | ~0.1s |
| View 100 tasks | <3s | ~0.5s |
| Single operation | <1s | ~0.1s |
| Error message | <1s | <0.1s |

If performance degrades significantly, check:
- System resource usage (CPU, memory)
- Number of tasks in storage (should handle 1000+)
- Terminal rendering speed

---

## References

- **Spec**: [spec.md](./spec.md) - Functional requirements and success criteria
- **Plan**: [plan.md](./plan.md) - Architecture and design decisions
- **Data Model**: [data-model.md](./data-model.md) - Task structure and validation
- **CLI Contract**: [contracts/cli-interface.md](./contracts/cli-interface.md) - Interface specifications

---

## Conclusion

This quickstart guide provides complete setup instructions and a comprehensive manual testing protocol covering all functional requirements (FR-001 to FR-013) and success criteria (SC-001 to SC-007). Following this protocol ensures the application meets all specification requirements.

**Status**: ✅ Quickstart complete - ready for implementation
