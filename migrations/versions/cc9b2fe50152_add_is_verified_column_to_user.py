"""Add is_verified column to User

Revision ID: cc9b2fe50152
Revises: cc9b2fe50152
Create Date: 2025-02-27 19:20:55.081783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc9b2fe50152'
down_revision: Union[str, None] = '<your_new_revision_id>'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
