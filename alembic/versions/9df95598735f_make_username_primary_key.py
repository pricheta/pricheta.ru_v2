"""make username primary key

Revision ID: 9df95598735f
Revises: 42dcfdecbddc
Create Date: 2025-12-26 05:25:31.793918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9df95598735f'
down_revision: Union[str, Sequence[str], None] = '42dcfdecbddc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_primary_key(
        "pk_users_username",
        "users",
        ["username"]
    )


def downgrade():
    op.drop_constraint(
        "pk_users_username",
        "users",
        type_="primary"
    )