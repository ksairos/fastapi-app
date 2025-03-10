"""add users table

Revision ID: 15ea87a43094
Revises: 45ff6c729506
Create Date: 2025-01-14 16:57:52.548890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15ea87a43094'
down_revision: Union[str, None] = '45ff6c729506'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),

    )


def downgrade() -> None:
    op.drop_table('users')
    pass
