"""Create the initial users."""
from sqlalchemy.orm import Session

from sqlalchemy_multi_tenant.config import settings
from sqlalchemy_multi_tenant.core.orm import start_orm_mappers
from sqlalchemy_multi_tenant.db.session import dbsession_ctx
from sqlalchemy_multi_tenant.users import crud_user as crud
from sqlalchemy_multi_tenant.users.adapters import UserCreate

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(dbsession: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(dbsession, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(dbsession, obj_in=user_in)  # noqa: F841


def main() -> None:
    start_orm_mappers()
    with dbsession_ctx() as dbsession:
        init_db(dbsession)
