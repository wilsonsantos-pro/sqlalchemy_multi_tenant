"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

from sqlalchemy_multi_tenant.core.db.migrations import for_each_tenant_schema

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}
# pylint: enable=invalid-name


@for_each_tenant_schema
def upgrade(schema: str) -> None:
    preparer = sa.sql.compiler.IdentifierPreparer(op.get_bind().dialect)
    schema_quoted = preparer.format_schema(schema)

    # use schema_quoted in queries like op.execute(f"DROP TYPE {schema_quoted}.myenum")

    ${upgrades if upgrades else "pass"}


@for_each_tenant_schema
def downgrade(schema: str) -> None:
    preparer = sa.sql.compiler.IdentifierPreparer(op.get_bind().dialect)
    schema_quoted = preparer.format_schema(schema)

    ${downgrades if downgrades else "pass"}
