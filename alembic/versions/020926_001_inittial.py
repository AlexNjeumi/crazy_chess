"""${message}

Revision ID: 020926_001_inittial
Revises: ${down_revision | comma,n}
Create Date: 02/09/26 00:01:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector
# ${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = "020926_001_inittial"
down_revision: Union[str, Sequence[str], None] = None
# branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
# depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    # ${upgrades if upgrades else "pass"}
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        'game',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('board_state', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('effects', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('num_effects', sa.Integer(), nullable=False, server_default="0"),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # ${downgrades if downgrades else "pass"}
    op.drop_table('game')
