import sys
import uuid
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure root path is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app.core.database import check_db_health
from app.models.base import Base
from app.models.system_log import SystemLog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scripts.seed import run_seed

# Use in-memory SQLite for fast database unit testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def setup_module():
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def test_model_uuid_and_timestamp_generation():
    db = TestingSessionLocal()
    try:
        log = SystemLog(level="INFO", component="test", message="Test message")
        db.add(log)
        db.commit()
        db.refresh(log)

        assert isinstance(log.id, uuid.UUID)
        assert isinstance(log.created_at, datetime)
        assert isinstance(log.updated_at, datetime)
        assert log.created_at is not None
        assert log.level == "INFO"
    finally:
        db.close()


def test_transaction_rollback_on_failure():
    db = TestingSessionLocal()
    try:
        log = SystemLog(level="ERROR", component="test_rollback", message="Rollback test")
        db.add(log)
        # Explicit rollback before commit
        db.rollback()

        query_result = db.query(SystemLog).filter(SystemLog.component == "test_rollback").first()
        assert query_result is None
    finally:
        db.close()


def test_check_db_health_success():
    db = TestingSessionLocal()
    try:
        assert check_db_health(db) is True
    finally:
        db.close()


def test_check_db_health_failure():
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("DB error")
    assert check_db_health(mock_db) is False


def test_seed_production_protection():
    with patch("scripts.seed.settings.app_env", "production"):
        with patch("sys.exit") as mock_exit:
            run_seed()
            mock_exit.assert_called_once_with(1)


def test_seed_execution():
    with patch("scripts.seed.settings.app_env", "development"):
        with patch("scripts.seed.SessionLocal", TestingSessionLocal):
            with patch("scripts.seed.engine", engine):
                run_seed()
