"""modify adminUsers table

Revision ID: e1b395729051
Revises: 988938d080b0
Create Date: 2024-07-03 11:19:14.581842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1b395729051'
down_revision: Union[str, None] = '988938d080b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename column 'hashed_password' to 'password'
    op.alter_column('adminUsers', 'hashed_password', new_column_name='password', existing_type=sa.String())


def downgrade() -> None:
    # Rename column 'password' back to 'hashed_password'
    op.alter_column('adminUsers', 'password', new_column_name='hashed_password', existing_type=sa.String())
