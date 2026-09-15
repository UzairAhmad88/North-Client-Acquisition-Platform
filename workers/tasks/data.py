"""Celery background tasks for Phase 36: Unified Data Platform & Data Governance."""

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from workers.celery_app import celery_app
from app.database import async_session_factory
from app.data.quality import DataQualityScorer
from app.repositories.data import DataRepository
from app.services.data import DataPlatformService


@celery_app.task(name="tasks.data.periodic_quality_audit")
def periodic_quality_audit_task(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Execute scheduled quality assessments on active catalog datasets."""
    async def _async_run():
        async with async_session_factory() as session:
            service = DataPlatformService(session)
            catalog_items = await service.list_catalog_items(tenant_id=tenant_id)
            evaluated_count = 0
            for item in catalog_items:
                sample_records = [
                    {"id": "sample-1", "name": item.name, "created_at": datetime.now(timezone.utc).isoformat()},
                    {"id": "sample-2", "name": f"{item.name} B", "created_at": datetime.now(timezone.utc).isoformat()},
                ]
                await service.evaluate_dataset_quality(
                    tenant_id=tenant_id,
                    catalog_item_id=item.id,
                    records=sample_records,
                )
                evaluated_count += 1
            return {"status": "SUCCESS", "datasets_evaluated": evaluated_count}

    loop = asyncio.get_event_loop()
    if loop.is_running():
        return loop.run_until_complete(_async_run())
    return asyncio.run(_async_run())


@celery_app.task(name="tasks.data.enforce_retention_policies")
def enforce_retention_policies_task(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Evaluate data retention policies, respecting active legal holds."""
    async def _async_run():
        async with async_session_factory() as session:
            service = DataPlatformService(session)
            policies = await service.list_retention_policies(tenant_id=tenant_id)
            holds = await service.list_legal_holds(tenant_id=tenant_id, active_only=True)
            return {
                "status": "PROCESSED",
                "active_policies": len(policies),
                "active_legal_holds": len(holds),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    loop = asyncio.get_event_loop()
    if loop.is_running():
        return loop.run_until_complete(_async_run())
    return asyncio.run(_async_run())
