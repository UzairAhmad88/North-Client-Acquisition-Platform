"""Base Domain Event model and core definitions for Phase 34 Event-Driven Architecture."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    """Immutable domain event representing a completed fact within the platform."""

    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:16]}")
    event_type: str
    event_version: str = "v1"
    tenant_id: str
    aggregate_type: str
    aggregate_id: str
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    producer: str
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:12]}")
    causation_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize domain event to dictionary with ISO datetime format."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "tenant_id": self.tenant_id,
            "aggregate_type": self.aggregate_type,
            "aggregate_id": self.aggregate_id,
            "occurred_at": self.occurred_at.isoformat(),
            "producer": self.producer,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "payload": self.payload,
        }
