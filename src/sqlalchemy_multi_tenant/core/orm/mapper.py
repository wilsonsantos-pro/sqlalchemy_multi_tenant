import logging

from sqlalchemy.orm import relation

from sqlalchemy_multi_tenant.items.models import Item
from sqlalchemy_multi_tenant.items.orm import item
from sqlalchemy_multi_tenant.tenant.models import Tenant
from sqlalchemy_multi_tenant.tenant.orm import tenant, tenant_user
from sqlalchemy_multi_tenant.users.models import User
from sqlalchemy_multi_tenant.users.orm import user

from .registry import mapper_registry

logger = logging.getLogger(__name__)


def start_orm_mappers():
    logger.info("Starting mappers")
    item_mapper = mapper_registry.map_imperatively(Item, item)
    mapper_registry.map_imperatively(
        User, user, properties={"items": relation(item_mapper)}
    )
    mapper_registry.map_imperatively(Tenant, tenant)
