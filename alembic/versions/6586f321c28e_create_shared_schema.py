"""Create shared schema

Revision ID: 6586f321c28e
Revises: c04a24d88722
Create Date: 2022-12-27 11:59:46.175911

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "6586f321c28e"
down_revision = "c04a24d88722"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade() -> None:
    op.execute(sa.schema.CreateSchema("shared"))


def downgrade() -> None:
    op.execute(sa.schema.DropSchema("shared"))
