from sqlalchemy import Boolean, Column, Integer, String, Table

from sqlalchemy_multi_tenant.core.orm.registry import mapper_registry

user = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255), unique=True),
    Column("password", String, nullable=False),
    Column("full_name", String(255)),
    Column("is_active", Boolean, nullable=False),
    Column("is_superuser", Boolean, nullable=False),
)
