"""Granular Permission Registry and Risk Classification."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set


class RiskLevel(str, Enum):
    """Risk classification for sensitive permissions."""

    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class PermissionDefinition:
    """Descriptor for a registered system permission."""

    name: str
    resource: str
    action: str
    description: str
    risk_level: RiskLevel = RiskLevel.LOW
    requires_mfa: bool = False
    requires_step_up: bool = False
    requires_human_approval: bool = False


class SystemPermissions:
    """Predefined system permissions registry."""

    # Leads CRM
    LEAD_READ = "lead.read"
    LEAD_CREATE = "lead.create"
    LEAD_UPDATE = "lead.update"
    LEAD_DELETE = "lead.delete"
    LEAD_EXPORT = "lead.export"

    # Business CRM
    BUSINESS_READ = "business.read"
    BUSINESS_CREATE = "business.create"
    BUSINESS_UPDATE = "business.update"
    BUSINESS_DELETE = "business.delete"

    # Research & Audit
    RESEARCH_READ = "research.read"
    RESEARCH_RUN = "research.run"
    AUDIT_READ = "audit.read"
    AUDIT_RUN = "audit.run"

    # Scoring & Qualification
    SCORING_READ = "scoring.read"
    SCORING_CALCULATE = "scoring.calculate"
    QUALIFICATION_READ = "qualification.read"
    QUALIFICATION_OVERRIDE = "qualification.override"

    # Outreach & Communication
    OUTREACH_READ = "outreach.read"
    OUTREACH_CREATE = "outreach.create"
    OUTREACH_APPROVE = "outreach.approve"
    OUTREACH_SEND = "outreach.send"  # CRITICAL

    # Discovery & Requirements
    REQUIREMENTS_READ = "requirements.read"
    REQUIREMENTS_CREATE = "requirements.create"
    REQUIREMENTS_CONFIRM = "requirements.confirm"

    # Solution & Proposals
    SOLUTION_READ = "solution.read"
    SOLUTION_CREATE = "solution.create"
    PROPOSAL_READ = "proposal.read"
    PROPOSAL_CREATE = "proposal.create"
    PROPOSAL_APPROVE = "proposal.approve"
    PROPOSAL_SEND = "proposal.send"  # CRITICAL

    # Estimation & Commercials
    ESTIMATE_READ = "estimate.read"
    ESTIMATE_CREATE = "estimate.create"
    ESTIMATE_APPROVE = "estimate.approve"
    PRICE_CHANGE = "price.change"  # CRITICAL

    # Contracts & Commitments
    CONTRACT_READ = "contract.read"
    CONTRACT_CREATE = "contract.create"
    CONTRACT_APPROVE = "contract.approve"
    CONTRACT_SIGN = "contract.sign"  # CRITICAL

    # Project Management
    PROJECT_READ = "project.read"
    PROJECT_CREATE = "project.create"
    PROJECT_UPDATE = "project.update"
    PROJECT_DELETE = "project.delete"
    PROJECT_EXPORT = "project.export"

    # Change Requests
    CHANGE_READ = "change.read"
    CHANGE_CREATE = "change.create"
    CHANGE_APPROVE = "change.approve"  # HIGH

    # QA, UAT & Handover
    QA_READ = "qa.read"
    QA_EXECUTE = "qa.execute"
    UAT_ACCEPT = "uat.accept"  # HIGH
    RELEASE_APPROVE = "release.approve"  # CRITICAL
    HANDOVER_SIGN = "handover.sign"  # HIGH

    # Support & Maintenance
    SUPPORT_READ = "support.read"
    SUPPORT_CREATE = "support.create"
    SUPPORT_MANAGE = "support.manage"

    # Analytics & BI
    ANALYTICS_READ = "analytics.read"
    ANALYTICS_EXPORT = "analytics.export"

    # AI Governance
    AI_TRACE_READ = "ai_trace.read"
    AI_EVALUATION_READ = "ai_evaluation.read"
    AI_PROMPT_MANAGE = "ai_prompt.manage"
    AI_MODEL_PROMOTE = "ai_model.promote"  # CRITICAL
    AI_KILL_SWITCH = "ai_kill_switch.activate"  # CRITICAL

    # Workflow & Automation
    WORKFLOW_READ = "workflow.read"
    WORKFLOW_START = "workflow.start"
    WORKFLOW_CANCEL = "workflow.cancel"
    WORKFLOW_REPLAY = "workflow.replay"  # HIGH
    AUTOMATION_READ = "automation.read"
    AUTOMATION_MANAGE = "automation.manage"
    AUTOMATION_EXECUTE_SENSITIVE = "automation.execute_sensitive"  # CRITICAL

    # Security & Administration
    USER_READ = "user.read"
    USER_MANAGE = "user.manage"  # HIGH
    ROLE_MANAGE = "role.manage"  # CRITICAL
    TENANT_MANAGE = "tenant.manage"  # CRITICAL
    API_KEY_MANAGE = "api_key.manage"
    SECURITY_AUDIT_READ = "security.audit_read"


# Comprehensive catalog of registered permissions with risk metadata
PERMISSION_REGISTRY: Dict[str, PermissionDefinition] = {
    # Lead
    SystemPermissions.LEAD_READ: PermissionDefinition(
        name=SystemPermissions.LEAD_READ, resource="lead", action="read", description="View lead records", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.LEAD_CREATE: PermissionDefinition(
        name=SystemPermissions.LEAD_CREATE, resource="lead", action="create", description="Create new lead records", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.LEAD_UPDATE: PermissionDefinition(
        name=SystemPermissions.LEAD_UPDATE, resource="lead", action="update", description="Update lead status and details", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.LEAD_DELETE: PermissionDefinition(
        name=SystemPermissions.LEAD_DELETE, resource="lead", action="delete", description="Archive or remove lead records", risk_level=RiskLevel.MEDIUM
    ),
    SystemPermissions.LEAD_EXPORT: PermissionDefinition(
        name=SystemPermissions.LEAD_EXPORT, resource="lead", action="export", description="Export lead lists to CSV/JSON", risk_level=RiskLevel.MEDIUM
    ),

    # Business
    SystemPermissions.BUSINESS_READ: PermissionDefinition(
        name=SystemPermissions.BUSINESS_READ, resource="business", action="read", description="View business profiles", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.BUSINESS_CREATE: PermissionDefinition(
        name=SystemPermissions.BUSINESS_CREATE, resource="business", action="create", description="Register new businesses", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.BUSINESS_UPDATE: PermissionDefinition(
        name=SystemPermissions.BUSINESS_UPDATE, resource="business", action="update", description="Update business profiles", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.BUSINESS_DELETE: PermissionDefinition(
        name=SystemPermissions.BUSINESS_DELETE, resource="business", action="delete", description="Delete business records", risk_level=RiskLevel.MEDIUM
    ),

    # Research & Audit
    SystemPermissions.RESEARCH_READ: PermissionDefinition(
        name=SystemPermissions.RESEARCH_READ, resource="research", action="read", description="View research dossiers", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.RESEARCH_RUN: PermissionDefinition(
        name=SystemPermissions.RESEARCH_RUN, resource="research", action="run", description="Execute research gathering jobs", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.AUDIT_READ: PermissionDefinition(
        name=SystemPermissions.AUDIT_READ, resource="audit", action="read", description="View digital audit reports", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.AUDIT_RUN: PermissionDefinition(
        name=SystemPermissions.AUDIT_RUN, resource="audit", action="run", description="Execute digital audit scanners", risk_level=RiskLevel.LOW
    ),

    # Scoring & Qualification
    SystemPermissions.SCORING_READ: PermissionDefinition(
        name=SystemPermissions.SCORING_READ, resource="scoring", action="read", description="View opportunity scores", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.SCORING_CALCULATE: PermissionDefinition(
        name=SystemPermissions.SCORING_CALCULATE, resource="scoring", action="calculate", description="Recalculate lead scores", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.QUALIFICATION_READ: PermissionDefinition(
        name=SystemPermissions.QUALIFICATION_READ, resource="qualification", action="read", description="View qualification cards", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.QUALIFICATION_OVERRIDE: PermissionDefinition(
        name=SystemPermissions.QUALIFICATION_OVERRIDE, resource="qualification", action="override", description="Human override of qualification status", risk_level=RiskLevel.MEDIUM
    ),

    # Outreach
    SystemPermissions.OUTREACH_READ: PermissionDefinition(
        name=SystemPermissions.OUTREACH_READ, resource="outreach", action="read", description="View outreach drafts and history", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.OUTREACH_CREATE: PermissionDefinition(
        name=SystemPermissions.OUTREACH_CREATE, resource="outreach", action="create", description="Create or edit outreach drafts", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.OUTREACH_APPROVE: PermissionDefinition(
        name=SystemPermissions.OUTREACH_APPROVE, resource="outreach", action="approve", description="Approve outreach message drafts", risk_level=RiskLevel.HIGH
    ),
    SystemPermissions.OUTREACH_SEND: PermissionDefinition(
        name=SystemPermissions.OUTREACH_SEND, resource="outreach", action="send", description="Transmit external outreach message", risk_level=RiskLevel.CRITICAL, requires_human_approval=True
    ),

    # Requirements
    SystemPermissions.REQUIREMENTS_READ: PermissionDefinition(
        name=SystemPermissions.REQUIREMENTS_READ, resource="requirements", action="read", description="View discovery requirements", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.REQUIREMENTS_CREATE: PermissionDefinition(
        name=SystemPermissions.REQUIREMENTS_CREATE, resource="requirements", action="create", description="Extract and draft requirements", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.REQUIREMENTS_CONFIRM: PermissionDefinition(
        name=SystemPermissions.REQUIREMENTS_CONFIRM, resource="requirements", action="confirm", description="Confirm and lock requirement scope", risk_level=RiskLevel.MEDIUM
    ),

    # Solutions & Proposals
    SystemPermissions.SOLUTION_READ: PermissionDefinition(
        name=SystemPermissions.SOLUTION_READ, resource="solution", action="read", description="View solution architectures", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.SOLUTION_CREATE: PermissionDefinition(
        name=SystemPermissions.SOLUTION_CREATE, resource="solution", action="create", description="Create solution designs", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.PROPOSAL_READ: PermissionDefinition(
        name=SystemPermissions.PROPOSAL_READ, resource="proposal", action="read", description="View client proposals", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.PROPOSAL_CREATE: PermissionDefinition(
        name=SystemPermissions.PROPOSAL_CREATE, resource="proposal", action="create", description="Compose proposal drafts", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.PROPOSAL_APPROVE: PermissionDefinition(
        name=SystemPermissions.PROPOSAL_APPROVE, resource="proposal", action="approve", description="Approve proposal pricing and scope", risk_level=RiskLevel.HIGH
    ),
    SystemPermissions.PROPOSAL_SEND: PermissionDefinition(
        name=SystemPermissions.PROPOSAL_SEND, resource="proposal", action="send", description="Transmit proposal to client", risk_level=RiskLevel.CRITICAL, requires_human_approval=True
    ),

    # Estimates
    SystemPermissions.ESTIMATE_READ: PermissionDefinition(
        name=SystemPermissions.ESTIMATE_READ, resource="estimate", action="read", description="View internal cost & effort estimates", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.ESTIMATE_CREATE: PermissionDefinition(
        name=SystemPermissions.ESTIMATE_CREATE, resource="estimate", action="create", description="Generate project estimates", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.ESTIMATE_APPROVE: PermissionDefinition(
        name=SystemPermissions.ESTIMATE_APPROVE, resource="estimate", action="approve", description="Approve project estimates", risk_level=RiskLevel.HIGH
    ),
    SystemPermissions.PRICE_CHANGE: PermissionDefinition(
        name=SystemPermissions.PRICE_CHANGE, resource="price", action="change", description="Modify authoritative pricing models", risk_level=RiskLevel.CRITICAL, requires_step_up=True
    ),

    # Contracts
    SystemPermissions.CONTRACT_READ: PermissionDefinition(
        name=SystemPermissions.CONTRACT_READ, resource="contract", action="read", description="View contract agreements", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.CONTRACT_CREATE: PermissionDefinition(
        name=SystemPermissions.CONTRACT_CREATE, resource="contract", action="create", description="Draft legal agreements", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.CONTRACT_APPROVE: PermissionDefinition(
        name=SystemPermissions.CONTRACT_APPROVE, resource="contract", action="approve", description="Internal contract sign-off", risk_level=RiskLevel.HIGH
    ),
    SystemPermissions.CONTRACT_SIGN: PermissionDefinition(
        name=SystemPermissions.CONTRACT_SIGN, resource="contract", action="sign", description="Legally execute client contract", risk_level=RiskLevel.CRITICAL, requires_mfa=True, requires_step_up=True
    ),

    # Projects
    SystemPermissions.PROJECT_READ: PermissionDefinition(
        name=SystemPermissions.PROJECT_READ, resource="project", action="read", description="View delivery projects", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.PROJECT_CREATE: PermissionDefinition(
        name=SystemPermissions.PROJECT_CREATE, resource="project", action="create", description="Initiate delivery projects", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.PROJECT_UPDATE: PermissionDefinition(
        name=SystemPermissions.PROJECT_UPDATE, resource="project", action="update", description="Update tasks, schedules, and milestones", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.PROJECT_DELETE: PermissionDefinition(
        name=SystemPermissions.PROJECT_DELETE, resource="project", action="delete", description="Archive or delete project", risk_level=RiskLevel.HIGH
    ),
    SystemPermissions.PROJECT_EXPORT: PermissionDefinition(
        name=SystemPermissions.PROJECT_EXPORT, resource="project", action="export", description="Export project data and deliverables", risk_level=RiskLevel.MEDIUM
    ),

    # Changes
    SystemPermissions.CHANGE_READ: PermissionDefinition(
        name=SystemPermissions.CHANGE_READ, resource="change", action="read", description="View change requests", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.CHANGE_CREATE: PermissionDefinition(
        name=SystemPermissions.CHANGE_CREATE, resource="change", action="create", description="Intake change requests", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.CHANGE_APPROVE: PermissionDefinition(
        name=SystemPermissions.CHANGE_APPROVE, resource="change", action="approve", description="Approve scope & commercial changes", risk_level=RiskLevel.HIGH
    ),

    # QA / UAT / Handover
    SystemPermissions.QA_READ: PermissionDefinition(
        name=SystemPermissions.QA_READ, resource="qa", action="read", description="View test plans and test runs", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.QA_EXECUTE: PermissionDefinition(
        name=SystemPermissions.QA_EXECUTE, resource="qa", action="execute", description="Execute test suites and log defects", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.UAT_ACCEPT: PermissionDefinition(
        name=SystemPermissions.UAT_ACCEPT, resource="uat", action="accept", description="Client acceptance signoff", risk_level=RiskLevel.HIGH
    ),
    SystemPermissions.RELEASE_APPROVE: PermissionDefinition(
        name=SystemPermissions.RELEASE_APPROVE, resource="release", action="approve", description="Approve production release readiness", risk_level=RiskLevel.CRITICAL
    ),
    SystemPermissions.HANDOVER_SIGN: PermissionDefinition(
        name=SystemPermissions.HANDOVER_SIGN, resource="handover", action="sign", description="Sign delivery handover checklist", risk_level=RiskLevel.HIGH
    ),

    # Support
    SystemPermissions.SUPPORT_READ: PermissionDefinition(
        name=SystemPermissions.SUPPORT_READ, resource="support", action="read", description="View support tickets and warranty", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.SUPPORT_CREATE: PermissionDefinition(
        name=SystemPermissions.SUPPORT_CREATE, resource="support", action="create", description="Submit support request", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.SUPPORT_MANAGE: PermissionDefinition(
        name=SystemPermissions.SUPPORT_MANAGE, resource="support", action="manage", description="Triage and resolve support requests", risk_level=RiskLevel.MEDIUM
    ),

    # Analytics
    SystemPermissions.ANALYTICS_READ: PermissionDefinition(
        name=SystemPermissions.ANALYTICS_READ, resource="analytics", action="read", description="View executive intelligence reports", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.ANALYTICS_EXPORT: PermissionDefinition(
        name=SystemPermissions.ANALYTICS_EXPORT, resource="analytics", action="export", description="Export business intelligence metrics", risk_level=RiskLevel.MEDIUM
    ),

    # AI Governance
    SystemPermissions.AI_TRACE_READ: PermissionDefinition(
        name=SystemPermissions.AI_TRACE_READ, resource="ai_trace", action="read", description="View sanitized AI execution traces", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.AI_EVALUATION_READ: PermissionDefinition(
        name=SystemPermissions.AI_EVALUATION_READ, resource="ai_evaluation", action="read", description="View agent evaluation benchmarks", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.AI_PROMPT_MANAGE: PermissionDefinition(
        name=SystemPermissions.AI_PROMPT_MANAGE, resource="ai_prompt", action="manage", description="Manage prompt registry versions", risk_level=RiskLevel.HIGH
    ),
    SystemPermissions.AI_MODEL_PROMOTE: PermissionDefinition(
        name=SystemPermissions.AI_MODEL_PROMOTE, resource="ai_model", action="promote", description="Deploy AI agent to production", risk_level=RiskLevel.CRITICAL, requires_mfa=True, requires_step_up=True
    ),
    SystemPermissions.AI_KILL_SWITCH: PermissionDefinition(
        name=SystemPermissions.AI_KILL_SWITCH, resource="ai_kill_switch", action="activate", description="Activate emergency AI kill switches", risk_level=RiskLevel.CRITICAL, requires_step_up=True
    ),

    # Workflow & Automation
    SystemPermissions.WORKFLOW_READ: PermissionDefinition(
        name=SystemPermissions.WORKFLOW_READ, resource="workflow", action="read", description="View workflow state and timelines", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.WORKFLOW_START: PermissionDefinition(
        name=SystemPermissions.WORKFLOW_START, resource="workflow", action="start", description="Initiate business workflow instances", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.WORKFLOW_CANCEL: PermissionDefinition(
        name=SystemPermissions.WORKFLOW_CANCEL, resource="workflow", action="cancel", description="Cancel active workflow instances", risk_level=RiskLevel.MEDIUM
    ),
    SystemPermissions.WORKFLOW_REPLAY: PermissionDefinition(
        name=SystemPermissions.WORKFLOW_REPLAY, resource="workflow", action="replay", description="Replay event stream or workflows", risk_level=RiskLevel.HIGH, requires_step_up=True
    ),
    SystemPermissions.AUTOMATION_READ: PermissionDefinition(
        name=SystemPermissions.AUTOMATION_READ, resource="automation", action="read", description="View automation rules and executions", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.AUTOMATION_MANAGE: PermissionDefinition(
        name=SystemPermissions.AUTOMATION_MANAGE, resource="automation", action="manage", description="Configure automation rules", risk_level=RiskLevel.MEDIUM
    ),
    SystemPermissions.AUTOMATION_EXECUTE_SENSITIVE: PermissionDefinition(
        name=SystemPermissions.AUTOMATION_EXECUTE_SENSITIVE, resource="automation", action="execute_sensitive", description="Execute sensitive automated tasks", risk_level=RiskLevel.CRITICAL
    ),

    # Security & Administration
    SystemPermissions.USER_READ: PermissionDefinition(
        name=SystemPermissions.USER_READ, resource="user", action="read", description="View user directory and profiles", risk_level=RiskLevel.LOW
    ),
    SystemPermissions.USER_MANAGE: PermissionDefinition(
        name=SystemPermissions.USER_MANAGE, resource="user", action="manage", description="Invite, suspend, and configure users", risk_level=RiskLevel.HIGH, requires_step_up=True
    ),
    SystemPermissions.ROLE_MANAGE: PermissionDefinition(
        name=SystemPermissions.ROLE_MANAGE, resource="role", action="manage", description="Configure RBAC roles and permissions", risk_level=RiskLevel.CRITICAL, requires_mfa=True, requires_step_up=True
    ),
    SystemPermissions.TENANT_MANAGE: PermissionDefinition(
        name=SystemPermissions.TENANT_MANAGE, resource="tenant", action="manage", description="Manage multi-tenant isolation", risk_level=RiskLevel.CRITICAL, requires_mfa=True, requires_step_up=True
    ),
    SystemPermissions.API_KEY_MANAGE: PermissionDefinition(
        name=SystemPermissions.API_KEY_MANAGE, resource="api_key", action="manage", description="Create and revoke API keys", risk_level=RiskLevel.HIGH
    ),
    SystemPermissions.SECURITY_AUDIT_READ: PermissionDefinition(
        name=SystemPermissions.SECURITY_AUDIT_READ, resource="security", action="audit_read", description="View immutable security audit log", risk_level=RiskLevel.MEDIUM
    ),
}


def get_permission(permission_name: str) -> Optional[PermissionDefinition]:
    """Retrieve permission definition from registry."""
    return PERMISSION_REGISTRY.get(permission_name)


def list_permissions() -> List[PermissionDefinition]:
    """List all registered system permissions."""
    return list(PERMISSION_REGISTRY.values())
