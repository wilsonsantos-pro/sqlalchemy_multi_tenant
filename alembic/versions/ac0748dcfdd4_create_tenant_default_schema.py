"""Create tenant_default schema

Revision ID: ac0748dcfdd4
Revises: 6586f321c28e
Create Date: 2022-12-27 19:11:54.650184

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "ac0748dcfdd4"
down_revision = "6586f321c28e"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade() -> None:
    op.execute(sa.schema.CreateSchema("tenant_default"))


def downgrade() -> None:
    op.execute(sa.schema.DropSchema("tenant_default"))
