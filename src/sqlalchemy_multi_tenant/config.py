import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Multi Tenant"
    SQLALCHEMY_DATABASE_URI: Optional[Union[PostgresDsn, str]] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    FIRST_SUPERUSER: EmailStr = EmailStr("admin@admin.com")
    FIRST_SUPERUSER_PASSWORD: str = "admin@admin.com"
    MULTI_TENANT_ENABLED: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(  # pylint: disable=no-self-argument
        cls,
        value: Optional[str],
        values: Dict[str, Any],
    ) -> Any:
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
