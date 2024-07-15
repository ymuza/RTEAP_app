"""add adminUsers table

Revision ID: 988938d080b0
Revises: 032d2bae1e1a
Create Date: 2024-07-03 10:40:45.588897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '988938d080b0'
down_revision: Union[str, None] = '032d2bae1e1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'adminUsers',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('firstname', sa.String),
        sa.Column('lastname', sa.String),
        sa.Column('hashed_password', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('phone_number', sa.String),
        sa.Column('role', sa.String)
    )


def downgrade() -> None:
    op.drop_table('adminUsers')

