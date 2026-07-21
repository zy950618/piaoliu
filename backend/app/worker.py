import asyncio
import json
from datetime import UTC, datetime

from redis.asyncio import from_url
from redis.exceptions import TimeoutError as RedisTimeoutError

from app.settings import get_settings


QUEUE_NAME = "piaoliu:jobs"


async def run() -> None:
    settings = get_settings()
    redis = from_url(settings.redis_url, decode_responses=True)
    while True:
        await redis.set("piaoliu:worker:heartbeat", datetime.now(UTC).isoformat(), ex=90)
        try:
            item = await redis.blpop(QUEUE_NAME, timeout=5)
        except RedisTimeoutError:
            # A quiet queue must not terminate the worker when the Redis
            # socket timeout and BLPOP deadline land on the same boundary.
            await asyncio.sleep(1)
            continue
        if item is None:
            continue
        _, body = item
        try:
            job = json.loads(body)
            await redis.hset(f"piaoliu:job:{job['id']}", mapping={"status": "completed", "finished_at": datetime.now(UTC).isoformat()})
        except (json.JSONDecodeError, KeyError):
            await redis.lpush("piaoliu:jobs:dead", body)


if __name__ == "__main__":
    asyncio.run(run())
