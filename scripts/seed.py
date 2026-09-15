import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.system_log import SystemLog


def run_seed():
    if settings.app_env.lower() == "production":
        print("[ERROR] Seed script execution prohibited in production environment!")
        sys.exit(1)
        return

    print(f"[SEED] Starting database seed for environment: '{settings.app_env}'")

    # Ensure tables exist for local seed testing
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if initial system log seed exists (idempotency check)
        existing_log = db.query(SystemLog).filter(SystemLog.component == "seed").first()
        if existing_log:
            print("[SEED] Seed data already exists. Skipping.")
            return

        seed_log = SystemLog(
            level="INFO",
            component="seed",
            message="Development database foundation initialized",
            details="Database foundation seed completed successfully.",
        )
        db.add(seed_log)
        db.commit()

        from app.services.seed_catalog import seed_service_catalog
        count = seed_service_catalog(db)
        print(f"[SEED] Successfully seeded development database foundation ({count} services created).")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to seed database: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
