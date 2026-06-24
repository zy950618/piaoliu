from urllib.parse import urlparse

from app.settings import get_settings

try:
    from redis.asyncio import Redis
except ModuleNotFoundError:
    class _FallbackConnectionPool:
        def __init__(self, url: str) -> None:
            parsed = urlparse(url)
            self.connection_kwargs = {
                "host": parsed.hostname or "localhost",
                "port": parsed.port or 6379,
                "db": int((parsed.path or "/0").removeprefix("/") or 0),
            }

    class Redis:
        def __init__(self, url: str) -> None:
            self.connection_pool = _FallbackConnectionPool(url)

        @classmethod
        def from_url(cls, url: str, decode_responses: bool = True) -> "Redis":
            return cls(url)


_redis_client: Redis | None = None


def get_redis_client() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(get_settings().redis_url, decode_responses=True)
    return _redis_client
