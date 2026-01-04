"""
Database seeding script for development and testing.

Usage:
    python -m app.scripts.seed_database
"""
import asyncio
from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.models.task import Task
from app.services.auth_service import hash_password
from datetime import datetime, timedelta
import uuid


def seed_users(session: Session):
    """Create demo users."""
    print("Seeding users...")

    users_data = [
        {
            "email": "demo@example.com",
            "name": "Demo User",
            "password": "password123",
        },
        {
            "email": "john@example.com",
            "name": "John Doe",
            "password": "password123",
        },
        {
            "email": "jane@example.com",
            "name": "Jane Smith",
            "password": "password123",
        },
    ]

    created_users = []

    for user_data in users_data:
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == user_data["email"])
        ).first()

        if existing_user:
            print(f"  ✓ User {user_data['email']} already exists")
            created_users.append(existing_user)
            continue

        # Create user
        user = User(
            id=uuid.uuid4(),
            email=user_data["email"],
            name=user_data["name"],
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        # Store password (in-memory for demo)
        from app.services.auth_service import _password_store
        _password_store[user.id] = hash_password(user_data["password"])

        print(f"  ✓ Created user: {user.email}")
        created_users.append(user)

    return created_users


def seed_tasks(session: Session, users: list[User]):
    """Create demo tasks for users."""
    print("\nSeeding tasks...")

    if not users:
        print("  ⚠ No users found, skipping task seeding")
        return

    # Demo user tasks (comprehensive examples)
    demo_user = users[0]

    demo_tasks = [
        {
            "title": "Complete project documentation",
            "description": "Write comprehensive API documentation and usage examples",
            "completed": False,
        },
        {
            "title": "Review pull requests",
            "description": "Review and merge pending pull requests from the team",
            "completed": True,
        },
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread, and vegetables",
            "completed": False,
        },
        {
            "title": "Schedule team meeting",
            "description": "Organize weekly sync-up meeting for next Monday",
            "completed": True,
        },
        {
            "title": "Update dependencies",
            "description": "Update all npm and pip packages to latest versions",
            "completed": False,
        },
        {
            "title": "Fix bug in authentication",
            "description": "JWT token expiration not working correctly",
            "completed": True,
        },
        {
            "title": "Implement pagination",
            "description": "Add pagination support to task list endpoint",
            "completed": False,
        },
        {
            "title": "Write unit tests",
            "description": "Add test coverage for task service layer",
            "completed": False,
        },
        {
            "title": "Deploy to production",
            "description": "Deploy latest changes to production environment",
            "completed": True,
        },
        {
            "title": "Respond to customer emails",
            "description": "Reply to pending customer support tickets",
            "completed": False,
        },
    ]

    # Create tasks for demo user
    created_count = 0
    for i, task_data in enumerate(demo_tasks):
        # Create tasks with different timestamps
        created_at = datetime.utcnow() - timedelta(days=len(demo_tasks) - i)

        task = Task(
            id=uuid.uuid4(),
            user_id=demo_user.id,
            title=task_data["title"],
            description=task_data["description"],
            completed=task_data["completed"],
            created_at=created_at,
            updated_at=created_at,
        )

        session.add(task)
        created_count += 1

    session.commit()
    print(f"  ✓ Created {created_count} tasks for {demo_user.email}")

    # Create fewer tasks for other users
    for user in users[1:]:
        user_tasks = [
            {
                "title": f"Welcome task for {user.name}",
                "description": "This is your first task!",
                "completed": False,
            },
            {
                "title": "Explore the app",
                "description": "Try creating, editing, and deleting tasks",
                "completed": True,
            },
        ]

        for task_data in user_tasks:
            task = Task(
                id=uuid.uuid4(),
                user_id=user.id,
                title=task_data["title"],
                description=task_data["description"],
                completed=task_data["completed"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(task)

        session.commit()
        print(f"  ✓ Created {len(user_tasks)} tasks for {user.email}")


def main():
    """Main seeding function."""
    print("\n" + "=" * 50)
    print("DATABASE SEEDING")
    print("=" * 50 + "\n")

    try:
        with Session(engine) as session:
            # Seed users
            users = seed_users(session)

            # Seed tasks
            seed_tasks(session, users)

            print("\n" + "=" * 50)
            print("✅ SEEDING COMPLETE")
            print("=" * 50)
            print("\nDemo credentials:")
            print("  Email: demo@example.com")
            print("  Password: password123")
            print("\nOther users:")
            print("  john@example.com / password123")
            print("  jane@example.com / password123")
            print("\n")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        raise


if __name__ == "__main__":
    main()
