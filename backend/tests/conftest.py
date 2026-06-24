import sys
import os
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

TEST_PLAZA_DB = BACKEND_ROOT / "runtime" / "test_plaza.sqlite3"
os.environ["PLAZA_SQLITE_PATH"] = str(TEST_PLAZA_DB)
if TEST_PLAZA_DB.exists():
    TEST_PLAZA_DB.unlink()
