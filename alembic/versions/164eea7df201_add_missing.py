"""Drop the tables from the 'public' schema.

Revision ID: 164eea7df201
Revises: 17f01639bf2b
Create Date: 2023-01-15 15:48:09.600398

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "164eea7df201"
down_revision = "17f01639bf2b"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade() -> None:
    op.drop_index("ix_item_title", table_name="item")
    op.drop_table("item")
    op.drop_table("user")


def downgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email", sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column(
            "full_name", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("is_superuser", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("password", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
        sa.UniqueConstraint("email", name="user_email_key"),
    )
    op.create_table(
        "item",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("title", sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("owner_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"], name="item_owner_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="item_pkey"),
    )
    op.create_index("ix_item_title", "item", ["title"], unique=False)
