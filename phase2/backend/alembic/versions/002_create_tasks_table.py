"""create tasks table

Revision ID: 002
Revises: 001
Create Date: 2026-01-03

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create tasks table with foreign key to users."""
    op.create_table(
        'tasks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=2000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Create index on user_id for faster queries
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])


def downgrade() -> None:
    """Drop tasks table."""
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
