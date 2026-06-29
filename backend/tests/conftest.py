import sys
import os
from pathlib import Path
import asyncio

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

TEST_BUSINESS_DB = BACKEND_ROOT / "runtime" / "test_business.sqlite3"
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_BUSINESS_DB.as_posix()}"
os.environ["PLAZA_SQLITE_PATH"] = str(TEST_BUSINESS_DB)
if TEST_BUSINESS_DB.exists():
    TEST_BUSINESS_DB.unlink()

from app.db import engine
from app.models import Base


async def _create_business_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(_create_business_schema())
