import logging

from sqlalchemy_multi_tenant.users.models import User
from sqlalchemy_multi_tenant.users.orm import user

from .registry import mapper_registry

logger = logging.getLogger(__name__)


def start_orm_mappers():
    logger.info("Starting mappers")
    mapper_registry.map_imperatively(User, user)
