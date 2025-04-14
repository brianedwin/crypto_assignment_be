"""Add balance column to users

Revision ID: f59e6cc2d1cd
Revises: d1062f17c2e3
Create Date: 2025-02-28 16:39:46.586703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f59e6cc2d1cd'
down_revision: Union[str, None] = 'd1062f17c2e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Tambahkan kolom balance ke tabel users
    op.add_column('users', sa.Column('balance', sa.Float(), nullable=False, server_default="0.0"))

def downgrade():
    # Hapus kolom balance jika rollback
    op.drop_column('users', 'balance')
