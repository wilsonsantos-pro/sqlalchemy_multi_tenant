"""Add item table

Revision ID: c04a24d88722
Revises: bff9d3c48506
Create Date: 2022-12-25 19:56:53.410250

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "c04a24d88722"
down_revision = "bff9d3c48506"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade() -> None:
    op.create_table(
        "item",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_item_title"), "item", ["title"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_item_title"), table_name="item")
    op.drop_table("item")
