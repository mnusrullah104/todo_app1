# Todo Console Application

A command-line Todo application for managing tasks in memory with 5 core CRUD operations (Create, Read, Update, Delete, Toggle status).

## Features

- ✅ **Create tasks** with title and optional description
- 📋 **View all tasks** with status indicators (✖ incomplete, ✔ complete)
- ✏️ **Update tasks** to modify title or description
- 🗑️ **Delete tasks** with confirmation
- 🔄 **Toggle task status** between complete and incomplete
- 💾 **In-memory storage** - tasks exist only while program runs
- 🎯 **Clean architecture** - separation of models, services, and CLI layers

## Requirements

- **Python**: 3.13 or higher
- **UV**: Python package manager
- **Platform**: WSL2 (Ubuntu-22.04) for Windows users, or native Linux/macOS

## Installation

### 1. Install Prerequisites

#### Python 3.13+

```bash
# Check Python version
python --version  # Should show 3.13 or higher

# If needed, install Python 3.13
sudo apt install python3.13 python3.13-venv
```

#### UV Package Manager

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

#### WSL2 (Windows Only)

```powershell
# Install WSL2 (PowerShell as Administrator)
wsl --install -d Ubuntu-22.04

# Launch Ubuntu
wsl
```

### 2. Clone Repository

```bash
git clone <repository-url>
cd todo_app1
```

### 3. Setup Python Environment

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
python --version  # Should show Python 3.13.x
```

## Usage

### Running the Application

```bash
# From project root directory
python src/main.py
```

### Main Menu

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

### Example Session

```bash
# 1. Add a task
> 1
Enter task title (required): Buy groceries
Enter task description (optional): Milk, eggs, bread

✓ Task 1 created successfully

# 2. View tasks
> 2
[1] ✖ Buy groceries
    Milk, eggs, bread

# 3. Toggle status
> 5
Enter task ID: 1

✓ Status toggled successfully!
[1] ✔ Buy groceries - Complete

# 4. Update task
> 3
Enter task ID: 1
Enter new title: Buy groceries and snacks
Enter new description: Milk, eggs, bread, chips

✓ Task updated successfully

# 5. Delete task
> 4
Enter task ID: 1
Are you sure? (y/n): y

✓ Task deleted successfully

# 6. Exit
> 6
Thank you for using Todo App. Goodbye!
```

## Project Structure

```
todo_app1/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task data class
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_manager.py  # CRUD operations
│   └── cli/
│       ├── __init__.py
│       └── ui.py            # Menu-driven interface
├── specs/
│   └── 001-todo-console-app/  # Feature specifications
├── pyproject.toml           # UV project configuration
├── README.md                # This file
└── .gitignore               # Git ignore patterns
```

## Architecture

The application follows clean architecture with three layers:

1. **Models Layer** (`src/models/`)
   - Task dataclass with id, title, description, completed fields
   - Data validation

2. **Services Layer** (`src/services/`)
   - TaskManager class with CRUD operations
   - Business logic and validation
   - In-memory dictionary storage (O(1) lookups)

3. **CLI Layer** (`src/cli/`)
   - Menu-driven user interface
   - Input validation helpers
   - Display formatting

**Dependencies flow inward**: CLI → Services → Models

## Technical Details

- **Storage**: In-memory dictionary keyed by task ID
- **ID Management**: Auto-incrementing counter, IDs never reused
- **Performance**: <2 seconds for task creation, <1 second for other operations
- **Capacity**: Supports up to 1 million tasks
- **Dependencies**: Python standard library only (no external packages)

## Limitations

- **No persistence**: Tasks are lost when application exits (Phase II feature)
- **Single user**: Only one user operates the CLI at a time
- **No search/filter**: View all tasks only (Phase II feature)
- **No categories/tags**: Simple flat task list (Phase II feature)

## Testing

Manual CLI-based testing is documented in `specs/001-todo-console-app/quickstart.md`.

To validate all features:
1. Create multiple tasks with various titles and descriptions
2. View task list to verify display
3. Toggle task status and verify indicators change
4. Update task content and confirm changes
5. Delete tasks with confirmation
6. Verify ID uniqueness across operations

## Development

This project follows AI-native, specification-driven development:

- **Spec**: `specs/001-todo-console-app/spec.md`
- **Plan**: `specs/001-todo-console-app/plan.md`
- **Tasks**: `specs/001-todo-console-app/tasks.md`
- **Testing Protocol**: `specs/001-todo-console-app/quickstart.md`

## Troubleshooting

### "Python version not found"

```bash
# Install Python 3.13
sudo apt install python3.13 python3.13-venv
python3.13 --version
```

### "UV command not found"

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv --version
```

### "Module not found" errors

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Verify Python path
which python
# Should show: /path/to/todo_app1/.venv/bin/python
```

### Unicode characters not displaying (✖, ✔)

```bash
# Check terminal encoding
echo $LANG
# Should show UTF-8 (e.g., en_US.UTF-8)

# If not UTF-8, set encoding
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

## License

This project was generated using Claude Code following the Spec-Kit Plus methodology.

## Contributing

This is an academic/learning project demonstrating AI-native development practices. Contributions should follow the specification-driven workflow.
