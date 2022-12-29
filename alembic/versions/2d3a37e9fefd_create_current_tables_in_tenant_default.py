"""Create current tables in tenant_default

Revision ID: 2d3a37e9fefd
Revises: ac0748dcfdd4
Create Date: 2022-12-27 19:14:04.565137

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "2d3a37e9fefd"
down_revision = "ac0748dcfdd4"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        schema="tenant_default",
    )
    op.create_table(
        "item",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["tenant_default.user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="tenant_default",
    )
    op.create_index(
        op.f("ix_tenant_default_item_title"),
        "item",
        ["title"],
        unique=False,
        schema="tenant_default",
    )


def downgrade() -> None:
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
    op.drop_index(
        op.f("ix_tenant_default_item_title"), table_name="item", schema="tenant_default"
    )
    op.drop_table("item", schema="tenant_default")
    op.drop_table("user", schema="tenant_default")
