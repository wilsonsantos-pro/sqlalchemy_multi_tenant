from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.routers import api_router
from .config import settings
from .core.bootstrap import bootstrap


def _add_middleware_cors(app: FastAPI) -> None:
    """Set all CORS enabled origins."""
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def main(start_orm_mappers: bool = True) -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, openapi_url="/api/openapi.json")

    _add_middleware_cors(app)

    app.include_router(api_router, prefix="/api")
    if start_orm_mappers:
        bootstrap()

    return app
