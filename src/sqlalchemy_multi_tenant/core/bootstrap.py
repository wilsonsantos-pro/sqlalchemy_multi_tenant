from .orm import start_orm_mappers


def bootstrap() -> None:
    start_orm_mappers()
