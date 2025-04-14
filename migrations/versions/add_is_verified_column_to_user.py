from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '<your_new_revision_id>'
down_revision = '6fc4ddaeeaa9'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=True))

def downgrade():
    op.drop_column('users', 'is_verified')

