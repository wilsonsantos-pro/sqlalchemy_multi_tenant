import sqlalchemy as sa
from alembic import config as alembic_config
from alembic import script
from alembic.runtime.migration import MigrationContext
from sqlalchemy import insert
from sqlalchemy.sql.schema import MetaData

from sqlalchemy_multi_tenant.core.db import dbsession_ctx_for_tenant

from .orm import mapper_registry, tenant


def get_shared_metadata():
    meta = MetaData()
    for table in mapper_registry.metadata.tables.values():
        if table.schema != "tenant":
            table.to_metadata(meta)
    return meta


def get_tenant_specific_metadata():
    meta = MetaData(schema="tenant")
    for table in mapper_registry.metadata.tables.values():
        if table.schema == "tenant":
            table.to_metadata(meta)
    return meta


def tenant_create(name: str, schema: str) -> int:
    with dbsession_ctx_for_tenant(schema) as dbsession:
        alembic_cfg = alembic_config.Config("alembic.ini")
        context = MigrationContext.configure(dbsession.connection())
        script_ = script.ScriptDirectory.from_config(alembic_cfg)
        if context.get_current_revision() != script_.get_current_head():
            raise RuntimeError(
                "Database is not up-to-date. Execute migrations before adding new tenants."
            )

        stmt = insert(tenant).values(name=name, schema=schema).returning(tenant.c.id)
        result = dbsession.execute(stmt).fetchone()
        if not result:
            raise RuntimeError("Failed to create tenant")
        tenant_id = int(result[0])

        dbsession.execute(sa.schema.CreateSchema(schema))
        get_tenant_specific_metadata().create_all(bind=dbsession.connection())

        dbsession.commit()
        return tenant_id
