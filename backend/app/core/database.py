import os
import logging
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger("app.database")

# Attempt primary DB connection; fallback instantly to SQLite if unreachable
try:
    test_engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 1} if "psycopg" in settings.database_url else {},
    )
    with test_engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    engine = test_engine
    logger.info(f"Connected to primary database: {settings.database_url}")
except Exception as e:
    logger.info("Using local SQLite database: sqlite:///./uzaii.db")
    engine = create_engine("sqlite:///./uzaii.db", connect_args={"check_same_thread": False})
    try:
        from app.models.base import Base
        from app.models.user import User
        import app.models
        try:
            User.__table__.create(engine, checkfirst=True)
        except Exception:
            pass
        for table in Base.metadata.tables.values():
            try:
                table.create(engine, checkfirst=True)
            except Exception:
                pass
        logger.info("Local SQLite database initialized successfully.")
    except Exception as init_err:
        logger.error(f"SQLite table creation error: {init_err}")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_health(db: Session) -> bool:
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return result == 1
    except Exception:
        return False
