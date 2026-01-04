"""
Database configuration and session management.
"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine
# For PostgreSQL, we use a connection pool
engine = create_engine(
    DATABASE_URL,
    echo=True if os.getenv("ENVIRONMENT") == "development" else False,
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,
    max_overflow=10,
)


def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting database session.
    Yields a database session and ensures it's closed after use.
    """
    with Session(engine) as session:
        yield session
