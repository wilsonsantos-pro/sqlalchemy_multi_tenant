"""Create tenant table

Revision ID: 05d7aa508e75
Revises: 2d3a37e9fefd
Create Date: 2022-12-27 19:19:06.842796

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "05d7aa508e75"
down_revision = "2d3a37e9fefd"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade() -> None:
    op.create_table(
        "tenant",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("schema", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="shared",
    )
    op.create_index(
        op.f("ix_shared_tenant_name"), "tenant", ["name"], unique=False, schema="shared"
    )
    op.create_index(
        op.f("ix_shared_tenant_schema"),
        "tenant",
        ["schema"],
        unique=False,
        schema="shared",
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_shared_tenant_schema"), table_name="tenant", schema="shared")
    op.drop_index(op.f("ix_shared_tenant_name"), table_name="tenant", schema="shared")
    op.drop_table("tenant", schema="shared")
