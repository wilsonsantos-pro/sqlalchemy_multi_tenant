from sqlalchemy import Column, ForeignKey, Integer, String, Table

from sqlalchemy_multi_tenant.core.orm.registry import mapper_registry

item = Table(
    "item",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), index=True),
    Column("description", String, nullable=True),
    Column("owner_id", Integer, ForeignKey("user.id")),
)
# owner = relationship("User", back_populates="items")
