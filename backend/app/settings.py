import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Drift Bottle Social API"
    environment: str = "mock"
    database_url: str = "postgresql+asyncpg://drift:drift@localhost:5432/drift_bottle"
    redis_url: str = "redis://localhost:6379/0"
    admin_mock_username: str = "admin"
    admin_mock_password: str = "admin_mock_password"
    admin_mock_token: str = "mock-admin-token"
    admin_accounts: str = "admin:admin_mock_password:admin,moderator;moderator:moderator_mock_password:moderator;risk:risk_mock_password:risk"
    admin_token_secret: str = "dev-admin-token-secret"
    admin_token_expires_seconds: int = 3600


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", Settings.model_fields["app_name"].default),
        environment=os.getenv("APP_ENV", Settings.model_fields["environment"].default),
        database_url=os.getenv("DATABASE_URL", Settings.model_fields["database_url"].default),
        redis_url=os.getenv("REDIS_URL", Settings.model_fields["redis_url"].default),
        admin_mock_username=os.getenv("ADMIN_MOCK_USERNAME", Settings.model_fields["admin_mock_username"].default),
        admin_mock_password=os.getenv("ADMIN_MOCK_PASSWORD", Settings.model_fields["admin_mock_password"].default),
        admin_mock_token=os.getenv("ADMIN_MOCK_TOKEN", Settings.model_fields["admin_mock_token"].default),
        admin_accounts=os.getenv("ADMIN_ACCOUNTS", Settings.model_fields["admin_accounts"].default),
        admin_token_secret=os.getenv("ADMIN_TOKEN_SECRET", Settings.model_fields["admin_token_secret"].default),
        admin_token_expires_seconds=int(
            os.getenv(
                "ADMIN_TOKEN_EXPIRES_SECONDS",
                str(Settings.model_fields["admin_token_expires_seconds"].default),
            )
        ),
    )
