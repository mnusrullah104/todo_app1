"""CLI user interface functions."""

from src.services.task_manager import TaskManager


def display_menu(task_manager: TaskManager) -> None:
    """
    Display the main menu with current task statistics.

    Args:
        task_manager: TaskManager instance to get task counts
    """
    # Count tasks
    total = len(task_manager.tasks)
    incomplete = sum(1 for task in task_manager.tasks.values() if not task.completed)
    complete = total - incomplete

    print("\n" + "=" * 50)
    print("=== Todo Console Application ===")
    print("=" * 50)
    print(f"\nCurrent Tasks: {total} ({incomplete} incomplete, {complete} complete)")
    print("\nMenu Options:")
    print("1. Add New Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Task Status")
    print("6. Exit")
    print()


def get_integer_input(
    prompt: str, min_val: int = 1, max_val: int = 999999, max_attempts: int = 3
) -> int | None:
    """
    Prompt user for integer input within a specified range.

    Args:
        prompt: Message to display to the user
        min_val: Minimum acceptable value (inclusive)
        max_val: Maximum acceptable value (inclusive)
        max_attempts: Maximum number of retry attempts

    Returns:
        Valid integer within range, or None if max attempts exceeded
    """
    for attempt in range(max_attempts):
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("✗ Error: No input received. Please enter a number.")
                continue

            value = int(user_input)
            if value < min_val or value > max_val:
                print(
                    f"✗ Error: Number must be between {min_val} and {max_val}."
                )
                continue

            return value
        except ValueError:
            print("✗ Error: Invalid input. Please enter a valid number.")

    print(f"✗ Error: Maximum attempts ({max_attempts}) exceeded.")
    return None


def get_string_input(
    prompt: str, required: bool = True, max_length: int = 500
) -> str:
    """
    Prompt user for string input with validation.

    Args:
        prompt: Message to display to the user
        required: Whether the string must be non-empty
        max_length: Maximum allowed string length

    Returns:
        Valid string input
    """
    while True:
        user_input = input(prompt).strip()

        # Check if empty when required
        if required and not user_input:
            print("✗ Error: This field cannot be empty.")
            continue

        # Check length
        if len(user_input) > max_length:
            print(f"✗ Error: Input too long (max {max_length} characters).")
            continue

        return user_input


def get_confirmation(prompt: str) -> bool:
    """
    Prompt user for yes/no confirmation.

    Args:
        prompt: Message to display to the user

    Returns:
        True for yes, False for no
    """
    while True:
        user_input = input(prompt).strip().lower()

        if user_input in ("y", "yes"):
            return True
        elif user_input in ("n", "no"):
            return False
        else:
            print("✗ Error: Please enter 'y' for yes or 'n' for no.")


def add_task_ui(task_manager: TaskManager) -> None:
    """
    Handle the Add New Task menu option.

    Prompts user for title and description, then creates the task.

    Args:
        task_manager: TaskManager instance to add task to
    """
    print("\n" + "=" * 50)
    print("You selected: Add New Task")
    print("=" * 50)

    # Get title
    title = get_string_input(
        "\nEnter task title (required): ", required=True, max_length=500
    )

    # Get description
    description = get_string_input(
        "Enter task description (optional, press Enter to skip): ",
        required=False,
        max_length=2000,
    )

    # Create task
    result = task_manager.add_task(title, description)

    if result.success:
        task = result.data
        status_icon = "✔" if task.completed else "✖"
        status_text = "Complete" if task.completed else "Incomplete"

        print(f"\n✓ {result.message}")
        print(f"Task ID: {task.id}")
        print(f"Title: {task.title}")
        if task.description:
            print(f"Description: {task.description}")
        print(f"Status: {status_text} ({status_icon})")
    else:
        print(f"\n✗ Error: {result.message}")


def view_tasks_ui(task_manager: TaskManager) -> None:
    """
    Handle the View All Tasks menu option.

    Displays all tasks with ID, status icon, title, and description.

    Args:
        task_manager: TaskManager instance to retrieve tasks from
    """
    print("\n" + "=" * 50)
    print("You selected: View All Tasks")
    print("=" * 50)
    print("\n=== Your Tasks ===\n")

    result = task_manager.get_all_tasks()

    if not result.data:
        print("No tasks found. Add your first task using option 1!")
    else:
        for task in result.data:
            status_icon = "✔" if task.completed else "✖"
            print(f"[{task.id}] {status_icon} {task.title}")
            if task.description:
                print(f"    {task.description}")
            print()  # Blank line between tasks

        # Summary
        total = len(result.data)
        incomplete = sum(1 for t in result.data if not t.completed)
        complete = total - incomplete
        print(f"Total: {total} task(s) ({incomplete} incomplete, {complete} complete)")


def toggle_status_ui(task_manager: TaskManager) -> None:
    """
    Handle the Toggle Task Status menu option.

    Prompts for task ID and toggles its completion status.

    Args:
        task_manager: TaskManager instance to toggle task status
    """
    print("\n" + "=" * 50)
    print("You selected: Toggle Task Status")
    print("=" * 50)

    task_id = get_integer_input("\nEnter task ID to toggle: ")

    if task_id is None:
        return

    # Show current status first
    if task_id in task_manager.tasks:
        task = task_manager.tasks[task_id]
        status_icon = "✔" if task.completed else "✖"
        status_text = "Complete" if task.completed else "Incomplete"
        print(f"\nCurrent status:")
        print(f"[{task.id}] {status_icon} {task.title} - {status_text}")

    # Toggle status
    result = task_manager.toggle_status(task_id)

    if result.success:
        task = result.data
        status_icon = "✔" if task.completed else "✖"
        status_text = "Complete" if task.completed else "Incomplete"

        print(f"\n✓ Status toggled successfully!")
        print(f"[{task.id}] {status_icon} {task.title} - {status_text}")
    else:
        print(f"\n✗ Error: {result.message}")


def update_task_ui(task_manager: TaskManager) -> None:
    """
    Handle the Update Task menu option.

    Prompts for task ID and new title/description values.

    Args:
        task_manager: TaskManager instance to update task
    """
    print("\n" + "=" * 50)
    print("You selected: Update Task")
    print("=" * 50)

    task_id = get_integer_input("\nEnter task ID to update: ")

    if task_id is None:
        return

    # Show current task
    if task_id not in task_manager.tasks:
        print(f"\n✗ Error: Task ID {task_id} not found")
        return

    task = task_manager.tasks[task_id]
    status_icon = "✔" if task.completed else "✖"
    print(f"\nCurrent task details:")
    print(f"[{task.id}] {status_icon} {task.title}")
    if task.description:
        print(f"    {task.description}")

    # Get new values
    print("\nEnter new values (leave blank to keep current):")
    new_title_input = input("Enter new title: ").strip()
    new_description_input = input("Enter new description: ").strip()

    # Determine what to update
    new_title = new_title_input if new_title_input else None
    new_description = new_description_input if new_description_input else None

    # Check if at least one field provided
    if new_title is None and new_description is None:
        print("\n✗ Error: At least one field must be updated")
        return

    # Update task
    result = task_manager.update_task(task_id, new_title, new_description)

    if result.success:
        task = result.data
        status_icon = "✔" if task.completed else "✖"
        status_text = "Complete" if task.completed else "Incomplete"

        print(f"\n✓ {result.message}")
        print(f"Task ID: {task.id}")
        print(f"Title: {task.title}")
        if task.description:
            print(f"Description: {task.description}")
        print(f"Status: {status_text} ({status_icon})")
    else:
        print(f"\n✗ Error: {result.message}")


def delete_task_ui(task_manager: TaskManager) -> None:
    """
    Handle the Delete Task menu option.

    Prompts for task ID and confirmation, then deletes the task.

    Args:
        task_manager: TaskManager instance to delete task from
    """
    print("\n" + "=" * 50)
    print("You selected: Delete Task")
    print("=" * 50)

    task_id = get_integer_input("\nEnter task ID to delete: ")

    if task_id is None:
        return

    # Show task to delete
    if task_id not in task_manager.tasks:
        print(f"\n✗ Error: Task ID {task_id} not found")
        return

    task = task_manager.tasks[task_id]
    status_icon = "✔" if task.completed else "✖"
    print(f"\nTask to delete:")
    print(f"[{task.id}] {status_icon} {task.title}")
    if task.description:
        print(f"    {task.description}")

    # Get confirmation
    confirmed = get_confirmation("\nAre you sure you want to delete this task? (y/n): ")

    if not confirmed:
        print("\nDeletion cancelled. Task was not deleted.")
        return

    # Delete task
    result = task_manager.delete_task(task_id)

    if result.success:
        print(f"\n✓ {result.message}")
        print(f"Task ID {task_id} has been removed.")
    else:
        print(f"\n✗ Error: {result.message}")
