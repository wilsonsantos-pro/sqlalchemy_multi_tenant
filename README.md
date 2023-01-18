# Example implementing Multinancy with SQLAlchemy, PostgreSQL and FastAPI

Simple TODO app.

### TODO

- [x] Create basic app as single tenant
- [x] Implement multi-schema as tenant separation strategy
- [x] Alembic migrationss
- [ ] add "tenant_default" to the "tenant" table using a migration
- [ ] add custom types to shared (eg, enum)
- [ ] CLI tool for adding tenants
- [ ] Celery support
- [ ] Multi-database support (hybrid with multi-schema)
