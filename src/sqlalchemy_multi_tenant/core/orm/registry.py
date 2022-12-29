from sqlalchemy.orm import registry

mapper_registry = registry()
# https://docs.sqlalchemy.org/en/14/core/metadata.html#specifying-the-schema-name
# The “schema” name may also be associated with the MetaData object where it will take
# effect automatically for all Table objects associated with that MetaData that don’t
# otherwise specify their own name.
# Finally, SQLAlchemy also supports a “dynamic” schema name system that is often used
# for multi-tenant applications such that a single set of Table metadata may refer to a
# dynamically configured set of schema names on a per-connection or per-statement basis.
mapper_registry.metadata.schema = "tenant"
