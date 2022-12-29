from sqlalchemy import Column, Integer, String, Table

from sqlalchemy_multi_tenant.core.orm.registry import mapper_registry

tenant = Table(
    "tenant",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), index=True, nullable=False),
    Column("schema", String(255), index=True, nullable=False),
    schema="shared",
)
# __table_args__ = ({"schema": "shared"},)

# map the user email to the tenant
tenant_user = Table(
    "tenant_user",
    mapper_registry.metadata,
    Column("tenant_id", Integer, primary_key=True),
    Column("user_email", String(255), primary_key=True),
    schema="shared",
)
# __table_args__ = ({"schema": "shared"},)
