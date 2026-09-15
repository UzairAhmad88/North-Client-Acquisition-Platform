"""Distributed and database-backed concurrency locking for Phase 34."""

import uuid
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orchestration import WorkflowTaskLock


class DistributedLockManager:
    """Manages acquisition and release of non-blocking distributed task locks."""

    @staticmethod
    async def acquire_lock(
        db: AsyncSession,
        lock_key: str,
        owner_id: str,
        ttl_seconds: int = 300,
    ) -> bool:
        """Attempt to acquire a unique lock key. Returns True if acquired, False if already held."""
        # 1. Purge expired locks first
        stmt_cleanup = delete(WorkflowTaskLock).where(
            WorkflowTaskLock.lock_key == lock_key,
            WorkflowTaskLock.expires_at < datetime.utcnow(),
        )
        await db.execute(stmt_cleanup)

        # 2. Check existing active lock
        stmt_check = select(WorkflowTaskLock).where(WorkflowTaskLock.lock_key == lock_key)
        result = await db.execute(stmt_check)
        existing = result.scalar_one_or_none()

        if existing:
            if existing.owner_id == owner_id:
                # Refresh TTL
                existing.expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
                await db.commit()
                return True
            return False

        # 3. Create new lock
        new_lock = WorkflowTaskLock(
            id=str(uuid.uuid4()),
            lock_key=lock_key,
            owner_id=owner_id,
            expires_at=datetime.utcnow() + timedelta(seconds=ttl_seconds),
            created_at=datetime.utcnow(),
        )
        db.add(new_lock)
        try:
            await db.commit()
            return True
        except Exception:
            await db.rollback()
            return False

    @staticmethod
    async def release_lock(
        db: AsyncSession,
        lock_key: str,
        owner_id: str,
    ) -> bool:
        """Release a lock held by owner_id."""
        stmt = delete(WorkflowTaskLock).where(
            WorkflowTaskLock.lock_key == lock_key,
            WorkflowTaskLock.owner_id == owner_id,
        )
        await db.execute(stmt)
        await db.commit()
        return True
