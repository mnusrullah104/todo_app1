"""Main application entry point."""

from src.cli.ui import (
    add_task_ui,
    delete_task_ui,
    display_menu,
    get_integer_input,
    toggle_status_ui,
    update_task_ui,
    view_tasks_ui,
)
from src.services.task_manager import TaskManager


def main():
    """Main application loop."""
    task_manager = TaskManager()

    while True:
        display_menu(task_manager)
        choice = get_integer_input("Enter your choice (1-6): ", min_val=1, max_val=6)

        if choice is None:
            print("✗ Invalid input. Please try again.")
            input("\nPress Enter to continue...")
            continue

        if choice == 6:
            print("\nThank you for using Todo App. Goodbye!")
            break

        # Menu option handlers
        if choice == 1:
            add_task_ui(task_manager)
        elif choice == 2:
            view_tasks_ui(task_manager)
        elif choice == 3:
            update_task_ui(task_manager)
        elif choice == 4:
            delete_task_ui(task_manager)
        elif choice == 5:
            toggle_status_ui(task_manager)

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
