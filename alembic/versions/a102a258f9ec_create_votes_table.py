"""create Votes table


Revision ID: a102a258f9ec
Revises: 5083c23d8637
Create Date: 2025-01-14 17:22:10.359641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a102a258f9ec'
down_revision: Union[str, None] = '5083c23d8637'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "votes",
    )


def downgrade() -> None:
    op.drop_table("votes")
    pass
