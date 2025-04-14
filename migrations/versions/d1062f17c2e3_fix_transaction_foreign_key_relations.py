"""Fix transaction foreign key relations

Revision ID: d1062f17c2e3
Revises: dbf42af9081b
Create Date: 2025-02-28 00:40:29.434059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd1062f17c2e3'
down_revision: Union[str, None] = 'dbf42af9081b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Hapus foreign key lama
    op.drop_constraint('transactions_sender_fkey', 'transactions', type_='foreignkey')
    op.drop_constraint('transactions_receiver_fkey', 'transactions', type_='foreignkey')

    # Buat foreign key baru dengan ondelete CASCADE
    op.create_foreign_key(
        'transactions_sender_fkey', 'transactions', 'users', ['sender_id'], ['id'], ondelete='CASCADE'
    )
    op.create_foreign_key(
        'transactions_receiver_fkey', 'transactions', 'users', ['receiver_id'], ['id'], ondelete='CASCADE'
    )


def downgrade() -> None:
    # Hapus foreign key baru
    op.drop_constraint('transactions_sender_fkey', 'transactions', type_='foreignkey')
    op.drop_constraint('transactions_receiver_fkey', 'transactions', type_='foreignkey')

    # Buat kembali foreign key lama
    op.create_foreign_key(
        'transactions_sender_id_fkey', 'transactions', 'users', ['sender_id'], ['id']
    )
    op.create_foreign_key(
        'transactions_receiver_id_fkey', 'transactions', 'users', ['receiver_id'], ['id']
    )

