"""rename user email to username

Revision ID: c1d2e3f4a5b6
Revises: bae9f92709e4
Create Date: 2026-07-01 21:20:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c1d2e3f4a5b6"
down_revision: Union[str, Sequence[str], None] = "bae9f92709e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index("ix_users_email", table_name="users")
    op.alter_column("users", "email", new_column_name="username")
    op.create_index("ix_users_username", "users", ["username"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_users_username", table_name="users")
    op.alter_column("users", "username", new_column_name="email")
    op.create_index("ix_users_email", "users", ["email"], unique=True)
