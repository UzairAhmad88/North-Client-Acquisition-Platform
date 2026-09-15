"""AgentContext Least-Privilege Tenant Container."""

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentContext:
    """Least-privilege execution context container passed to agents."""

    workflow_id: str
    task_id: str
    agent_run_id: str
    user_id: Optional[uuid.UUID] = None
    lead_id: Optional[uuid.UUID] = None
    business_id: Optional[uuid.UUID] = None

    business_profile: Dict[str, Any] = field(default_factory=dict)
    lead_profile: Dict[str, Any] = field(default_factory=dict)
    research_data: Dict[str, Any] = field(default_factory=dict)
    audit_data: Dict[str, Any] = field(default_factory=dict)
    score_data: Dict[str, Any] = field(default_factory=dict)
    service_recommendations: List[Dict[str, Any]] = field(default_factory=list)

    conversation_context: List[Dict[str, Any]] = field(default_factory=list)
    previous_results: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
