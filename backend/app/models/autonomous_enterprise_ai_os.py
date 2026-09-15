"""
Phase 76: Autonomous Enterprise AI Operating System (AEAI-OS) SQLAlchemy Models.
Prefix: aeai_*
Ensuring zero namespace collisions with previous phases.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class AeaiAgentModel(BaseModel):
    __tablename__ = "aeai_agents"

    agent_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String(32), default="1.0.0", nullable=False)
    owner = Column(String(255), nullable=False)
    purpose = Column(Text, nullable=False)
    autonomy_level = Column(String(32), default="L2", nullable=False)  # L0, L1, L2, L3, L4, L5
    risk_level = Column(String(32), default="LOW", nullable=False)    # LOW, MEDIUM, HIGH, CRITICAL
    model_name = Column(String(128), default="claude-3-5-sonnet", nullable=False)
    fallback_model_name = Column(String(128), default="gpt-4o", nullable=True)
    status = Column(String(32), default="ACTIVE", nullable=False)     # ACTIVE, PAUSED, RETIRED, DRAFT
    capabilities = Column(JSON, default=list, nullable=False)
    permissions = Column(JSON, default=list, nullable=False)
    tools = Column(JSON, default=list, nullable=False)
    data_access = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class AeaiAgentVersionModel(BaseModel):
    __tablename__ = "aeai_agent_versions"

    agent_id = Column(String(64), nullable=False, index=True)
    version_number = Column(String(32), nullable=False)
    prompt_snapshot = Column(Text, nullable=True)
    configuration = Column(JSON, default=dict, nullable=False)
    author = Column(String(255), nullable=False)
    change_summary = Column(Text, nullable=True)


class AeaiTaskModel(BaseModel):
    __tablename__ = "aeai_tasks"

    task_code = Column(String(64), unique=True, nullable=False, index=True)
    goal = Column(Text, nullable=False)
    agent_id = Column(String(64), nullable=False, index=True)
    status = Column(String(32), default="PENDING", nullable=False, index=True)  # PENDING, RUNNING, COMPLETED, FAILED, ESCALATED
    priority = Column(String(32), default="MEDIUM", nullable=False)
    autonomy_level = Column(String(32), default="L3", nullable=False)
    inputs = Column(JSON, default=dict, nullable=False)
    outputs = Column(JSON, default=dict, nullable=True)
    cost_estimate = Column(Float, default=0.0, nullable=False)
    cost_actual = Column(Float, default=0.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class AeaiSubtaskModel(BaseModel):
    __tablename__ = "aeai_subtasks"

    task_id = Column(String(64), nullable=False, index=True)
    subtask_code = Column(String(64), nullable=False)
    assigned_agent_id = Column(String(64), nullable=False)
    status = Column(String(32), default="PENDING", nullable=False)
    step_order = Column(Integer, default=1, nullable=False)
    inputs = Column(JSON, default=dict, nullable=False)
    outputs = Column(JSON, default=dict, nullable=True)
    dependencies = Column(JSON, default=list, nullable=False)


class AeaiWorkflowModel(BaseModel):
    __tablename__ = "aeai_workflows"

    workflow_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    trigger_type = Column(String(64), default="EVENT", nullable=False)  # EVENT, SCHEDULE, MANUAL, WEBHOOK
    graph_definition = Column(JSON, default=dict, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    autonomy_level = Column(String(32), default="L4", nullable=False)
    execution_history = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False)


class AeaiToolRegistryModel(BaseModel):
    __tablename__ = "aeai_tool_registry"

    tool_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False)  # DATABASE, API, SEARCH, FINANCE, OPS, CODE, ETC.
    description = Column(Text, nullable=True)
    version = Column(String(32), default="1.0.0", nullable=False)
    sandbox_mode = Column(String(32), default="RESTRICTED", nullable=False)  # READ_ONLY, SANDBOX, RESTRICTED, PRODUCTION
    risk_level = Column(String(32), default="MEDIUM", nullable=False)
    input_schema = Column(JSON, default=dict, nullable=False)
    output_schema = Column(JSON, default=dict, nullable=False)
    rate_limit_per_minute = Column(Integer, default=60, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class AeaiMemoryItemModel(BaseModel):
    __tablename__ = "aeai_memory_items"

    memory_type = Column(String(64), nullable=False, index=True)  # WORKING, EPISODIC, SEMANTIC, PROCEDURAL, USER_CONTEXT, ORG, DECISION
    key = Column(String(255), nullable=False, index=True)
    content = Column(JSON, default=dict, nullable=False)
    confidence_score = Column(Float, default=1.0, nullable=False)
    owner = Column(String(255), nullable=False)
    sensitivity = Column(String(32), default="INTERNAL", nullable=False)  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    retention_days = Column(Integer, default=365, nullable=False)
    source_system = Column(String(128), default="AEAI_RUNTIME", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class AeaiKnowledgeSourceModel(BaseModel):
    __tablename__ = "aeai_knowledge_sources"

    source_name = Column(String(255), nullable=False)
    source_type = Column(String(64), default="DOCUMENT", nullable=False)  # DOCUMENT, DATABASE, API, CONTRACT, POLICY
    uri = Column(String(512), nullable=True)
    document_count = Column(Integer, default=0, nullable=False)
    vector_indexed = Column(Boolean, default=True, nullable=False)
    last_synced_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(32), default="SYNCED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False)


class AeaiPlanModel(BaseModel):
    __tablename__ = "aeai_plans"

    plan_code = Column(String(64), unique=True, nullable=False, index=True)
    goal = Column(Text, nullable=False)
    agent_id = Column(String(64), nullable=False, index=True)
    steps = Column(JSON, default=list, nullable=False)
    feasibility_score = Column(Float, default=0.95, nullable=False)
    validation_status = Column(String(32), default="VALIDATED", nullable=False)  # VALIDATED, REPAIRED, REJECTED
    estimated_cost = Column(Float, default=0.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False)


class AeaiApprovalModel(BaseModel):
    __tablename__ = "aeai_approvals"

    approval_code = Column(String(64), unique=True, nullable=False, index=True)
    task_id = Column(String(64), nullable=False, index=True)
    action_name = Column(String(255), nullable=False)
    risk_level = Column(String(32), default="HIGH", nullable=False)
    impact_summary = Column(Text, nullable=False)
    evidence = Column(JSON, default=dict, nullable=False)
    status = Column(String(32), default="PENDING", nullable=False, index=True)  # PENDING, APPROVED, REJECTED, EXPIRED
    approver_id = Column(String(64), nullable=True)
    decision_timestamp = Column(DateTime, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False)


class AeaiPolicyRuleModel(BaseModel):
    __tablename__ = "aeai_policy_rules"

    policy_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    scope = Column(String(64), default="GLOBAL", nullable=False)  # GLOBAL, AGENT, TOOL, WORKFLOW
    condition_expression = Column(Text, nullable=False)
    action_effect = Column(String(32), default="ALLOW", nullable=False)  # ALLOW, DENY, REQUIRE_APPROVAL, STEP_UP
    is_active = Column(Boolean, default=True, nullable=False)
    version = Column(String(32), default="1.0.0", nullable=False)


class AeaiAgentIncidentModel(BaseModel):
    __tablename__ = "aeai_agent_incidents"

    incident_code = Column(String(64), unique=True, nullable=False, index=True)
    agent_id = Column(String(64), nullable=False, index=True)
    incident_type = Column(String(64), nullable=False)  # POLICY_VIOLATION, TOOL_ABUSE, DATA_LEAKAGE, LOOP_DETECTED, COST_OVERRUN
    severity = Column(String(32), default="MEDIUM", nullable=False)
    status = Column(String(32), default="DETECTED", nullable=False)
    remediation_action = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False)


class AeaiActionLimitModel(BaseModel):
    __tablename__ = "aeai_action_limits"

    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)
    agent_id = Column(String(64), nullable=True, index=True)
    max_daily_spend = Column(Float, default=1000.0, nullable=False)
    max_tool_calls_per_run = Column(Integer, default=50, nullable=False)
    max_runtime_seconds = Column(Integer, default=300, nullable=False)
    max_external_messages = Column(Integer, default=100, nullable=False)
    current_daily_spend = Column(Float, default=0.0, nullable=False)


class AeaiKillSwitchEventModel(BaseModel):
    __tablename__ = "aeai_kill_switch_events"

    event_type = Column(String(64), nullable=False)  # EMERGENCY_LOCKDOWN, AGENT_PAUSE, TOOL_REVOKE
    target_scope = Column(String(128), default="GLOBAL", nullable=False)
    reason = Column(Text, nullable=False)
    triggered_by = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class AeaiRoiMetricModel(BaseModel):
    __tablename__ = "aeai_roi_metrics"

    reporting_period = Column(String(32), nullable=False, index=True)
    total_ai_benefit = Column(Float, default=0.0, nullable=False)
    total_ai_cost = Column(Float, default=0.0, nullable=False)
    net_roi_percentage = Column(Float, default=0.0, nullable=False)
    hours_saved = Column(Float, default=0.0, nullable=False)
    error_reduction_pct = Column(Float, default=0.0, nullable=False)
    automation_rate_pct = Column(Float, default=0.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False)


# Aliases
AeaiAgent = AeaiAgentModel
AeaiAgentVersion = AeaiAgentVersionModel
AeaiTask = AeaiTaskModel
AeaiSubtask = AeaiSubtaskModel
AeaiWorkflow = AeaiWorkflowModel
AeaiToolRegistry = AeaiToolRegistryModel
AeaiMemoryItem = AeaiMemoryItemModel
AeaiKnowledgeSource = AeaiKnowledgeSourceModel
AeaiPlan = AeaiPlanModel
AeaiApproval = AeaiApprovalModel
AeaiPolicyRule = AeaiPolicyRuleModel
AeaiAgentIncident = AeaiAgentIncidentModel
AeaiActionLimit = AeaiActionLimitModel
AeaiKillSwitchEvent = AeaiKillSwitchEventModel
AeaiRoiMetric = AeaiRoiMetricModel
