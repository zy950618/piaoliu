from collections.abc import AsyncIterator

from app.settings import get_settings

settings = get_settings()

try:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
except ModuleNotFoundError:
    AsyncSession = object
    async_session_factory = None

    class _FallbackUrl:
        drivername = settings.database_url.split("://", 1)[0]

    class _FallbackEngine:
        url = _FallbackUrl()

    engine = _FallbackEngine()


async def get_db_session() -> AsyncIterator[AsyncSession]:
    if async_session_factory is None:
        raise RuntimeError("SQLAlchemy is required before opening database sessions")
    async with async_session_factory() as session:
        yield session
