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
    user_token_secret: str = "dev-user-token-secret"
    user_token_expires_seconds: int = 7200
    wechat_app_id: str = ""
    wechat_app_secret: str = ""
    wechat_mch_id: str = ""
    wechat_pay_api_v3_key: str = ""
    payment_mock_secret: str = "dev-payment-mock-secret-change-me"
    payment_mock_ttl_seconds: int = 300
    cors_origins: str = "http://127.0.0.1:5173,http://localhost:5173,http://127.0.0.1:5174,http://localhost:5174"
    object_storage_endpoint: str = "localhost:9000"
    object_storage_public_endpoint: str = "http://localhost:9000"
    object_storage_access_key: str = ""
    object_storage_secret_key: str = ""
    object_storage_bucket: str = "piaoliu-media"
    object_storage_secure: bool = False


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
        user_token_secret=os.getenv("USER_TOKEN_SECRET", Settings.model_fields["user_token_secret"].default),
        user_token_expires_seconds=int(
            os.getenv("USER_TOKEN_EXPIRES_SECONDS", str(Settings.model_fields["user_token_expires_seconds"].default))
        ),
        wechat_app_id=os.getenv("WECHAT_APP_ID", Settings.model_fields["wechat_app_id"].default),
        wechat_app_secret=os.getenv("WECHAT_APP_SECRET", Settings.model_fields["wechat_app_secret"].default),
        wechat_mch_id=os.getenv("WECHAT_MCH_ID", Settings.model_fields["wechat_mch_id"].default),
        wechat_pay_api_v3_key=os.getenv("WECHAT_PAY_API_V3_KEY", Settings.model_fields["wechat_pay_api_v3_key"].default),
        payment_mock_secret=os.getenv("PAYMENT_MOCK_SECRET", Settings.model_fields["payment_mock_secret"].default),
        payment_mock_ttl_seconds=int(
            os.getenv("PAYMENT_MOCK_TTL_SECONDS", str(Settings.model_fields["payment_mock_ttl_seconds"].default))
        ),
        cors_origins=os.getenv("CORS_ORIGINS", Settings.model_fields["cors_origins"].default),
        object_storage_endpoint=os.getenv("OBJECT_STORAGE_ENDPOINT", Settings.model_fields["object_storage_endpoint"].default),
        object_storage_public_endpoint=os.getenv("OBJECT_STORAGE_PUBLIC_ENDPOINT", Settings.model_fields["object_storage_public_endpoint"].default),
        object_storage_access_key=os.getenv("OBJECT_STORAGE_ACCESS_KEY", Settings.model_fields["object_storage_access_key"].default),
        object_storage_secret_key=os.getenv("OBJECT_STORAGE_SECRET_KEY", Settings.model_fields["object_storage_secret_key"].default),
        object_storage_bucket=os.getenv("OBJECT_STORAGE_BUCKET", Settings.model_fields["object_storage_bucket"].default),
        object_storage_secure=os.getenv("OBJECT_STORAGE_SECURE", "false").lower() in {"1", "true", "yes"},
    )
