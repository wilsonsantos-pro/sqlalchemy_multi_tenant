from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_multi_tenant.config import settings


@lru_cache()
def get_engine() -> Engine:
    return create_engine(str(settings().SQLALCHEMY_DATABASE_URI), pool_pre_ping=True)


@lru_cache()
def session_factory(bind: Engine):
    bind = bind or get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=bind)


@contextmanager
def _dbsession_ctx(engine: Engine):
    try:
        session = session_factory(engine)()
        yield session
    finally:
        session.close()


@contextmanager
def dbsession_ctx_for_tenant(tenant_schema: str = "tenant_default"):
    schema_translate_map = dict(tenant=tenant_schema)

    new_engine = get_engine().execution_options(
        schema_translate_map=schema_translate_map
    )

    with _dbsession_ctx(new_engine) as dbsession:
        yield dbsession
