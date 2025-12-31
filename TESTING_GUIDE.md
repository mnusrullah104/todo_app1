# Testing Guide: Todo Console Application

## Quick Start

### Running the Application

**Option 1: Run as Python module (Recommended)**
```bash
cd D:\todo_app1
python -m src.main
```

**Option 2: Run with PYTHONPATH**
```bash
cd D:\todo_app1
set PYTHONPATH=%CD%  # Windows
python src/main.py
```

**Option 3: Add to Python path temporarily**
```bash
cd D:\todo_app1
python -c "import sys; sys.path.insert(0, '.'); exec(open('src/main.py').read())"
```

**Best Practice**: Use Option 1 (`python -m src.main`)

### Expected Initial Screen

```
==================================================
=== Todo Console Application ===
==================================================

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

---

## 🧪 Complete Testing Protocol

### Test 1: Create Your First Task (User Story 1 - Part 1)

**Steps:**
1. Launch application: `python -m src.main`
2. Enter `1` (Add New Task)
3. Enter title: `Buy groceries`
4. Enter description: `Milk, eggs, bread`

**Expected Output:**
```
You selected: Add New Task
==================================================

Enter task title (required): Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread

✓ Task 1 created successfully
Task ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Incomplete (✖)

Press Enter to continue...
```

**Validation:**
- ✅ Task ID is 1 (first task)
- ✅ Title and description displayed correctly
- ✅ Status is Incomplete (✖)
- ✅ Success message shown

---

### Test 2: View All Tasks (User Story 1 - Part 2)

**Steps:**
1. From main menu, enter `2` (View All Tasks)

**Expected Output:**
```
You selected: View All Tasks
==================================================

=== Your Tasks ===

[1] ✖ Buy groceries
    Milk, eggs, bread

Total: 1 task(s) (1 incomplete, 0 complete)

Press Enter to continue...
```

**Validation:**
- ✅ Task displayed with ID [1]
- ✅ Status icon ✖ shown
- ✅ Title and description visible
- ✅ Summary shows 1 incomplete, 0 complete

---

### Test 3: Create Task Without Description

**Steps:**
1. Enter `1` (Add New Task)
2. Enter title: `Call dentist`
3. Press Enter (skip description)

**Expected Output:**
```
✓ Task 2 created successfully
Task ID: 2
Title: Call dentist
Status: Incomplete (✖)
```

**Validation:**
- ✅ Task ID is 2 (incremented)
- ✅ No description shown
- ✅ Task created successfully

---

### Test 4: Toggle Task Status (User Story 2)

**Steps:**
1. Enter `5` (Toggle Task Status)
2. Enter task ID: `1`

**Expected Output:**
```
You selected: Toggle Task Status
==================================================

Enter task ID to toggle: 1

Current status:
[1] ✖ Buy groceries - Incomplete

✓ Status toggled successfully!
[1] ✔ Buy groceries - Complete

Press Enter to continue...
```

**Then view tasks again (option 2):**
```
[1] ✔ Buy groceries
    Milk, eggs, bread

[2] ✖ Call dentist

Total: 2 task(s) (1 incomplete, 1 complete)
```

**Validation:**
- ✅ Status changed from ✖ to ✔
- ✅ Menu summary updated (1 complete, 1 incomplete)
- ✅ Toggle works in both directions

---

### Test 5: Toggle Back to Incomplete

**Steps:**
1. Enter `5` (Toggle Task Status)
2. Enter task ID: `1`

**Expected:**
- Status changes from ✔ back to ✖
- Summary shows 2 incomplete, 0 complete

---

### Test 6: Update Task Content (User Story 3)

**Steps:**
1. Enter `3` (Update Task)
2. Enter task ID: `1`
3. Enter new title: `Buy groceries and snacks`
4. Enter new description: `Milk, eggs, bread, chips, soda`

**Expected Output:**
```
You selected: Update Task
==================================================

Enter task ID to update: 1

Current task details:
[1] ✖ Buy groceries
    Milk, eggs, bread

Enter new values (leave blank to keep current):
Enter new title: Buy groceries and snacks
Enter new description: Milk, eggs, bread, chips, soda

✓ Task 1 updated successfully
Task ID: 1
Title: Buy groceries and snacks
Description: Milk, eggs, bread, chips, soda
Status: Incomplete (✖)
```

**Validation:**
- ✅ Title updated
- ✅ Description updated
- ✅ Status unchanged
- ✅ ID unchanged

---

### Test 7: Update Only Title (Keep Description)

**Steps:**
1. Enter `3` (Update Task)
2. Enter task ID: `2`
3. Enter new title: `Call dentist for appointment`
4. Press Enter (skip description)

**Expected:**
- Title updated to "Call dentist for appointment"
- Description remains empty
- Success message shown

---

### Test 8: Delete Task (User Story 4)

**Steps:**
1. Create a third task first (option 1):
   - Title: `Test task for deletion`
   - Description: `This will be deleted`
2. Enter `4` (Delete Task)
3. Enter task ID: `3`
4. Enter `y` to confirm

**Expected Output:**
```
You selected: Delete Task
==================================================

Enter task ID to delete: 3

Task to delete:
[3] ✖ Test task for deletion
    This will be deleted

Are you sure you want to delete this task? (y/n): y

✓ Task 3 deleted successfully
Task ID 3 has been removed.

Press Enter to continue...
```

**Validation:**
- ✅ Task details shown before deletion
- ✅ Confirmation required
- ✅ Task removed from list
- ✅ View tasks confirms task 3 is gone

---

### Test 9: Delete Cancellation

**Steps:**
1. Enter `4` (Delete Task)
2. Enter task ID: `1`
3. Enter `n` to cancel

**Expected:**
```
Deletion cancelled. Task was not deleted.
```

**Validation:**
- ✅ Task still exists when viewing
- ✅ No changes made

---

### Test 10: ID Never Reused

**Steps:**
1. Note current tasks (should have IDs 1, 2)
2. Delete task ID 1
3. Create a new task (any title)

**Expected:**
- New task gets ID 4 (NOT 1 or 3)
- IDs: 2, 4 exist
- Confirms IDs are never reused

---

### Test 11: Empty Task List

**Steps:**
1. Delete all tasks
2. Enter `2` (View All Tasks)

**Expected Output:**
```
=== Your Tasks ===

No tasks found. Add your first task using option 1!

Press Enter to continue...
```

**Validation:**
- ✅ Graceful handling of empty list
- ✅ Helpful message shown
- ✅ No errors or crashes

---

### Test 12: Error Handling - Invalid Task ID

**Steps:**
1. Enter `5` (Toggle Status)
2. Enter task ID: `999`

**Expected Output:**
```
✗ Error: Task ID 999 not found

Press Enter to continue...
```

**Try with other operations (Update, Delete):**
- Same error message should appear
- Application doesn't crash

---

### Test 13: Error Handling - Empty Title

**Steps:**
1. Enter `1` (Add New Task)
2. Press Enter without typing title

**Expected Output:**
```
Enter task title (required):
✗ Error: This field cannot be empty.
Enter task title (required):
```

**Validation:**
- ✅ Re-prompts for title
- ✅ Doesn't create task with empty title
- ✅ Clear error message

---

### Test 14: Error Handling - Invalid Menu Choice

**Steps:**
1. At main menu, enter `9`

**Expected:**
```
✗ Error: Number must be between 1 and 6.
```

**Try with:**
- Letters: `abc`
- Empty input: Press Enter
- Out of range: `0`, `7`

**Validation:**
- ✅ Clear error messages for each case
- ✅ Re-prompts for valid input
- ✅ No crashes

---

### Test 15: Complete Task Lifecycle

**Steps:**
1. Create task: "Complete project report" / "Due Friday"
2. View tasks (verify creation)
3. Update title: "Complete Q4 project report"
4. Update description: "Due Friday - include metrics"
5. Toggle to complete
6. View tasks (verify complete status ✔)
7. Toggle back to incomplete
8. View tasks (verify incomplete status ✖)
9. Delete task
10. View tasks (verify removal)

**Validation:**
- ✅ All operations work sequentially
- ✅ Task state transitions correctly
- ✅ No errors throughout lifecycle

---

### Test 16: Multiple Tasks Management

**Steps:**
1. Create 5 different tasks with various titles/descriptions
2. View all (should show 5 tasks)
3. Toggle 2 tasks to complete
4. View all (should show 3 incomplete, 2 complete)
5. Update 1 task
6. Delete 1 task
7. View all (should show 4 tasks remaining)

**Validation:**
- ✅ Menu shows correct counts
- ✅ All tasks tracked properly
- ✅ Summary line accurate

---

### Test 17: Exit Application

**Steps:**
1. Enter `6` (Exit)

**Expected Output:**
```
Thank you for using Todo App. Goodbye!
```

**Validation:**
- ✅ Goodbye message displayed
- ✅ Application exits cleanly
- ✅ No errors

---

## 📋 Quick Test Checklist

Use this checklist for rapid validation:

### Core Operations (5-10 minutes)
- [ ] Create task with description
- [ ] Create task without description
- [ ] View task list
- [ ] Toggle status (incomplete → complete)
- [ ] Toggle status (complete → incomplete)
- [ ] Update task title
- [ ] Update task description
- [ ] Delete task with confirmation
- [ ] Cancel deletion
- [ ] Exit application

### Edge Cases (5 minutes)
- [ ] View empty list
- [ ] Invalid task ID (toggle)
- [ ] Invalid task ID (update)
- [ ] Invalid task ID (delete)
- [ ] Empty title attempt
- [ ] Invalid menu choice
- [ ] Non-numeric menu input

### Success Criteria
- [ ] All 5 CRUD operations work
- [ ] Status indicators display correctly (✖/✔)
- [ ] Task counts accurate in menu
- [ ] No crashes or unhandled errors
- [ ] Error messages clear and helpful

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

**Solution:**
```bash
# Use module execution instead
python -m src.main

# OR set PYTHONPATH
set PYTHONPATH=%CD%  # Windows
export PYTHONPATH=$PWD  # Linux/macOS
```

### "Unicode characters not displaying"

If ✖ and ✔ show as boxes or question marks:

**Windows Command Prompt:**
```bash
chcp 65001  # Enable UTF-8
```

**Windows Terminal / PowerShell:**
- Already supports UTF-8 by default

**WSL/Linux:**
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

### Application doesn't start

**Check Python version:**
```bash
python --version  # Should be 3.13+
```

**Try alternative Python command:**
```bash
python3 -m src.main
# OR
python3.13 -m src.main
```

---

## 📊 Test Results Template

Copy this template to record your test results:

```markdown
### Test Execution Report

**Date:** YYYY-MM-DD
**Tester:** [Your Name]
**Environment:** [OS, Python version]

| Test | Status | Notes |
|------|--------|-------|
| Create task | ✅/❌ | |
| View tasks | ✅/❌ | |
| Toggle status | ✅/❌ | |
| Update task | ✅/❌ | |
| Delete task | ✅/❌ | |
| Empty list | ✅/❌ | |
| Invalid ID | ✅/❌ | |
| Exit app | ✅/❌ | |

**Issues Found:**
- [List any bugs or unexpected behavior]

**Overall Assessment:** PASS / FAIL
```

---

## 🎯 Performance Validation

### Expected Performance (per spec.md success criteria)

| Operation | Target | How to Measure |
|-----------|--------|----------------|
| Task creation | <2 seconds | Time from Enter to success message |
| View 100 tasks | <3 seconds | Create 100 tasks, time view operation |
| Error message | <1 second | Instant for invalid input |
| All operations | <1 second | Should feel instant |

**Note:** With in-memory storage, all operations should be nearly instant on modern hardware.

---

## 🚀 Advanced Testing Scenarios

### Stress Test: Many Tasks

```bash
# Create 50 tasks quickly
# Option 1: Add manually (test UI responsiveness)
# Option 2: Test with automated script (future enhancement)
```

**Expected:**
- View operation still fast (<3 seconds per spec)
- No performance degradation
- Task counts accurate

### Edge Case: Special Characters

**Test with:**
- Title: `Task with "quotes" and 'apostrophes'`
- Description: `Multiple
newlines
and special chars: @#$%`

**Expected:**
- Characters stored and displayed correctly
- No crashes or encoding errors

### Edge Case: Very Long Input

**Test with:**
- 500-character title (should work)
- 501-character title (should reject with error)
- 2000-character description (should work)
- 2001-character description (should reject)

---

## ✅ Final Validation

Before considering testing complete:

1. **All user stories tested independently:**
   - [ ] US1: Create and View
   - [ ] US2: Toggle Status
   - [ ] US3: Update Content
   - [ ] US4: Delete Tasks

2. **All acceptance scenarios passed:**
   - [ ] Spec.md scenarios verified
   - [ ] No unhandled errors
   - [ ] Edge cases handled gracefully

3. **Constitution compliance verified:**
   - [ ] Python 3.13+ used
   - [ ] Standard library only
   - [ ] Clean architecture maintained
   - [ ] In-memory storage working

**READY FOR PRODUCTION:** Yes / No

---

## 📞 Support

For issues or questions:
- Check README.md for setup instructions
- Review specs/001-todo-console-app/quickstart.md for detailed test protocol
- Verify Python version and environment setup

**Happy Testing! 🎉**
