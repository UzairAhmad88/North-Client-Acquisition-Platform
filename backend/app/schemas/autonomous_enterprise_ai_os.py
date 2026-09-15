"""
Phase 76: Autonomous Enterprise AI Operating System (AEAI-OS) Pydantic Schemas.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime


# -------------------------------------------------------------------
# 1. AI Command Center Summary & Natural Language Control
# -------------------------------------------------------------------
class AeaiCommandCenterSummaryResponse(BaseModel):
    system_health_score: float = 98.4
    active_agents_count: int = 16
    running_tasks_count: int = 5
    completed_tasks_count: int = 248
    failed_tasks_count: int = 2
    pending_approvals_count: int = 3
    autonomous_actions_executed: int = 1240
    human_interventions_count: int = 18
    autonomy_lockdown_active: bool = False
    total_cost_usd: float = 485.60
    total_tokens_used_today: int = 1420500
    active_tools_count: int = 32
    memory_items_count: int = 8940
    roi_percentage: float = 384.2


class AeaiNaturalLanguageControlRequest(BaseModel):
    query: str
    tenant_id: str = "tenant-default"
    requested_autonomy: str = "L4"  # L0-L5


class AeaiNaturalLanguageControlResponse(BaseModel):
    query: str
    intent: str
    assigned_supervisor: str
    decomposed_tasks: List[str]
    required_approval: bool
    status: str
    response_summary: str


# -------------------------------------------------------------------
# 2. Agent Registry & Capabilities
# -------------------------------------------------------------------
class AeaiAgentCreate(BaseModel):
    agent_code: str
    name: str
    description: Optional[str] = None
    version: str = "1.0.0"
    owner: str
    purpose: str
    autonomy_level: str = "L2"
    risk_level: str = "LOW"
    model_name: str = "claude-3-5-sonnet"
    fallback_model_name: Optional[str] = "gpt-4o"
    capabilities: List[str] = []
    permissions: List[str] = []
    tools: List[str] = []
    data_access: Dict[str, Any] = {}


class AeaiAgentResponse(BaseModel):
    id: str
    agent_code: str
    name: str
    description: Optional[str] = None
    version: str
    owner: str
    purpose: str
    autonomy_level: str
    risk_level: str
    model_name: str
    fallback_model_name: Optional[str] = None
    status: str
    capabilities: List[str]
    permissions: List[str]
    tools: List[str]
    data_access: Dict[str, Any]
    tenant_id: str


# -------------------------------------------------------------------
# 3. Tasks & Task Graphs
# -------------------------------------------------------------------
class AeaiTaskCreate(BaseModel):
    task_code: str
    goal: str
    agent_id: str
    priority: str = "MEDIUM"
    autonomy_level: str = "L3"
    inputs: Dict[str, Any] = {}
    cost_estimate: float = 0.0


class AeaiTaskResponse(BaseModel):
    id: str
    task_code: str
    goal: str
    agent_id: str
    status: str
    priority: str
    autonomy_level: str
    inputs: Dict[str, Any]
    outputs: Optional[Dict[str, Any]] = None
    cost_estimate: float
    cost_actual: float
    tenant_id: str


class AeaiTaskGraphResponse(BaseModel):
    task_id: str
    goal: str
    subtasks: List[Dict[str, Any]]
    status: str
    critical_path: List[str]
    requires_human_approval: bool


# -------------------------------------------------------------------
# 4. Workflows & Execution
# -------------------------------------------------------------------
class AeaiWorkflowCreate(BaseModel):
    workflow_code: str
    name: str
    trigger_type: str = "EVENT"
    graph_definition: Dict[str, Any]
    autonomy_level: str = "L4"


class AeaiWorkflowResponse(BaseModel):
    id: str
    workflow_code: str
    name: str
    trigger_type: str
    graph_definition: Dict[str, Any]
    status: str
    autonomy_level: str
    execution_history: List[Dict[str, Any]]


# -------------------------------------------------------------------
# 5. Tools & Sandboxed Execution
# -------------------------------------------------------------------
class AeaiToolRegisterRequest(BaseModel):
    tool_code: str
    name: str
    category: str
    description: Optional[str] = None
    version: str = "1.0.0"
    sandbox_mode: str = "RESTRICTED"
    risk_level: str = "MEDIUM"
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    rate_limit_per_minute: int = 60


class AeaiToolResponse(BaseModel):
    id: str
    tool_code: str
    name: str
    category: str
    description: Optional[str] = None
    version: str
    sandbox_mode: str
    risk_level: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    rate_limit_per_minute: int
    is_active: bool


class AeaiToolExecuteRequest(BaseModel):
    tool_code: str
    agent_id: str
    inputs: Dict[str, Any]
    sandbox_override: Optional[str] = None


class AeaiToolRunResponse(BaseModel):
    execution_id: str
    tool_code: str
    status: str
    sandbox_mode: str
    outputs: Dict[str, Any]
    execution_time_ms: float
    audit_hash: str


# -------------------------------------------------------------------
# 6. Memory Fabric (7 Layers)
# -------------------------------------------------------------------
class AeaiMemoryStoreRequest(BaseModel):
    memory_type: str  # WORKING, EPISODIC, SEMANTIC, PROCEDURAL, USER_CONTEXT, ORG, DECISION
    key: str
    content: Dict[str, Any]
    confidence_score: float = 1.0
    owner: str = "AEAI_RUNTIME"
    sensitivity: str = "INTERNAL"
    retention_days: int = 365
    source_system: str = "AEAI_RUNTIME"


class AeaiMemoryRetrieveRequest(BaseModel):
    memory_type: Optional[str] = None
    query: str
    min_confidence: float = 0.70
    limit: int = 10


class AeaiMemoryItemResponse(BaseModel):
    id: str
    memory_type: str
    key: str
    content: Dict[str, Any]
    confidence_score: float
    owner: str
    sensitivity: str
    source_system: str
    created_at: datetime


# -------------------------------------------------------------------
# 7. Approvals, Policies & Kill Switch
# -------------------------------------------------------------------
class AeaiApprovalActionRequest(BaseModel):
    action: str  # APPROVE, REJECT
    reason: Optional[str] = None
    approver_id: str = "human-exec-1"


class AeaiApprovalResponse(BaseModel):
    id: str
    approval_code: str
    task_id: str
    action_name: str
    risk_level: str
    impact_summary: str
    evidence: Dict[str, Any]
    status: str
    approver_id: Optional[str] = None
    decision_timestamp: Optional[datetime] = None


class AeaiPolicyRuleResponse(BaseModel):
    id: str
    policy_code: str
    name: str
    scope: str
    condition_expression: str
    action_effect: str
    is_active: bool
    version: str


class AeaiKillSwitchRequest(BaseModel):
    event_type: str = "EMERGENCY_LOCKDOWN"  # EMERGENCY_LOCKDOWN, AGENT_PAUSE, TOOL_REVOKE
    target_scope: str = "GLOBAL"
    reason: str
    triggered_by: str = "chief-security-officer"


class AeaiKillSwitchResponse(BaseModel):
    status: str
    event_type: str
    target_scope: str
    reason: str
    triggered_by: str
    lockdown_active: bool
    timestamp: datetime


class AeaiRoiMetricResponse(BaseModel):
    reporting_period: str
    total_ai_benefit: float
    total_ai_cost: float
    net_roi_percentage: float
    hours_saved: float
    error_reduction_pct: float
    automation_rate_pct: float
