import asyncio
from datetime import UTC, datetime

from redis.asyncio import from_url

from app.settings import get_settings


async def run() -> None:
    settings = get_settings()
    redis = from_url(settings.redis_url, decode_responses=True)
    while True:
        now = datetime.now(UTC).isoformat()
        await redis.set("piaoliu:scheduler:heartbeat", now, ex=90)
        await redis.publish("piaoliu:scheduler:ticks", now)
        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(run())
