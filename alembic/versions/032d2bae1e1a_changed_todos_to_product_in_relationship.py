"""changed todos to product in relationship

Revision ID: 032d2bae1e1a
Revises: 4ed4075f04aa
Create Date: 2024-07-02 11:40:54.231743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '032d2bae1e1a'
down_revision: Union[str, None] = '4ed4075f04aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_foreign_key(
        'fk_products_owner_id_users', 'products', 'users', ['owner_id'], ['id']
    )


def downgrade() -> None:
    op.drop_constraint('fk_products_owner_id_users', 'products', type_='foreignkey')

