import functools
from typing import Callable

from alembic import op
from typeguard import typechecked


@typechecked
def for_each_tenant_schema(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped():
        schemas = op.get_bind().execute("SELECT schema FROM shared.tenant").fetchall()
        for (schema,) in schemas:
            func(schema)
        func("tenant_default")

    return wrapped
