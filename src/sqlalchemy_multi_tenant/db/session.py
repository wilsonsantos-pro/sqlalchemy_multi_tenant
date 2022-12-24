from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


@lru_cache()
def get_engine() -> Engine:
    # local import so that settings can be overriden
    from sqlalchemy_multi_tenant.config import settings

    return create_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True)


@lru_cache()
def session_factory():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


@contextmanager
def dbsession_ctx():
    try:
        session = session_factory()()
        yield session
    finally:
        session.close()
