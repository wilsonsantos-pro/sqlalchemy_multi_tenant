"""User Email Tenant Mapper

Revision ID: 17f01639bf2b
Revises: 05d7aa508e75
Create Date: 2022-12-28 19:46:27.359046

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "17f01639bf2b"
down_revision = "05d7aa508e75"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade() -> None:
    op.create_table(
        "tenant_user",
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("user_email", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "user_email"),
        schema="shared",
    )


def downgrade() -> None:
    op.drop_table("tenant_user", schema="shared")
