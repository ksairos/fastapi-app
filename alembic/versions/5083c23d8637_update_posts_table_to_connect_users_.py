"""update posts table to connect users table via owner_id

Revision ID: 5083c23d8637
Revises: 15ea87a43094
Create Date: 2025-01-14 17:00:17.160510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5083c23d8637'
down_revision: Union[str, None] = '15ea87a43094'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(constraint_name='fkey_post_owner_id',
                          source_table='posts',
                          referent_table='users',
                          local_cols=["owner_id"],
                          remote_cols=["id"])


def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
