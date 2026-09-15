"""Role Definitions and Default Role-to-Permission Mapping Matrix."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set

from app.security.permissions import SystemPermissions


class SystemRole(str, Enum):
    """Predefined system roles for internal team and external clients."""

    # Internal Team Roles
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    SALES = "SALES"
    DEVELOPER = "DEVELOPER"
    DESIGNER = "DESIGNER"
    AI_ENGINEER = "AI_ENGINEER"
    ML_ENGINEER = "ML_ENGINEER"
    NLP_ENGINEER = "NLP_ENGINEER"
    QA = "QA"
    DEVOPS = "DEVOPS"
    SECURITY = "SECURITY"
    ANALYST = "ANALYST"
    SUPPORT = "SUPPORT"
    VIEWER = "VIEWER"

    # Client Roles
    CLIENT_OWNER = "CLIENT_OWNER"
    CLIENT_ADMIN = "CLIENT_ADMIN"
    CLIENT_MEMBER = "CLIENT_MEMBER"
    CLIENT_REVIEWER = "CLIENT_REVIEWER"
    CLIENT_VIEWER = "CLIENT_VIEWER"


@dataclass
class RoleDefinition:
    """Descriptor for a system role."""

    name: str
    description: str
    is_internal: bool = True
    permissions: Set[str] = field(default_factory=set)


# Authoritative Default Role-to-Permission Map
ROLE_PERMISSIONS_MAP: Dict[str, Set[str]] = {
    # OWNER — Unrestricted access
    SystemRole.OWNER.value: {
        # All permissions
        SystemPermissions.LEAD_READ, SystemPermissions.LEAD_CREATE, SystemPermissions.LEAD_UPDATE, SystemPermissions.LEAD_DELETE, SystemPermissions.LEAD_EXPORT,
        SystemPermissions.BUSINESS_READ, SystemPermissions.BUSINESS_CREATE, SystemPermissions.BUSINESS_UPDATE, SystemPermissions.BUSINESS_DELETE,
        SystemPermissions.RESEARCH_READ, SystemPermissions.RESEARCH_RUN, SystemPermissions.AUDIT_READ, SystemPermissions.AUDIT_RUN,
        SystemPermissions.SCORING_READ, SystemPermissions.SCORING_CALCULATE, SystemPermissions.QUALIFICATION_READ, SystemPermissions.QUALIFICATION_OVERRIDE,
        SystemPermissions.OUTREACH_READ, SystemPermissions.OUTREACH_CREATE, SystemPermissions.OUTREACH_APPROVE, SystemPermissions.OUTREACH_SEND,
        SystemPermissions.REQUIREMENTS_READ, SystemPermissions.REQUIREMENTS_CREATE, SystemPermissions.REQUIREMENTS_CONFIRM,
        SystemPermissions.SOLUTION_READ, SystemPermissions.SOLUTION_CREATE, SystemPermissions.PROPOSAL_READ, SystemPermissions.PROPOSAL_CREATE, SystemPermissions.PROPOSAL_APPROVE, SystemPermissions.PROPOSAL_SEND,
        SystemPermissions.ESTIMATE_READ, SystemPermissions.ESTIMATE_CREATE, SystemPermissions.ESTIMATE_APPROVE, SystemPermissions.PRICE_CHANGE,
        SystemPermissions.CONTRACT_READ, SystemPermissions.CONTRACT_CREATE, SystemPermissions.CONTRACT_APPROVE, SystemPermissions.CONTRACT_SIGN,
        SystemPermissions.PROJECT_READ, SystemPermissions.PROJECT_CREATE, SystemPermissions.PROJECT_UPDATE, SystemPermissions.PROJECT_DELETE, SystemPermissions.PROJECT_EXPORT,
        SystemPermissions.CHANGE_READ, SystemPermissions.CHANGE_CREATE, SystemPermissions.CHANGE_APPROVE,
        SystemPermissions.QA_READ, SystemPermissions.QA_EXECUTE, SystemPermissions.UAT_ACCEPT, SystemPermissions.RELEASE_APPROVE, SystemPermissions.HANDOVER_SIGN,
        SystemPermissions.SUPPORT_READ, SystemPermissions.SUPPORT_CREATE, SystemPermissions.SUPPORT_MANAGE,
        SystemPermissions.ANALYTICS_READ, SystemPermissions.ANALYTICS_EXPORT,
        SystemPermissions.AI_TRACE_READ, SystemPermissions.AI_EVALUATION_READ, SystemPermissions.AI_PROMPT_MANAGE, SystemPermissions.AI_MODEL_PROMOTE, SystemPermissions.AI_KILL_SWITCH,
        SystemPermissions.WORKFLOW_READ, SystemPermissions.WORKFLOW_START, SystemPermissions.WORKFLOW_CANCEL, SystemPermissions.WORKFLOW_REPLAY,
        SystemPermissions.AUTOMATION_READ, SystemPermissions.AUTOMATION_MANAGE, SystemPermissions.AUTOMATION_EXECUTE_SENSITIVE,
        SystemPermissions.USER_READ, SystemPermissions.USER_MANAGE, SystemPermissions.ROLE_MANAGE, SystemPermissions.TENANT_MANAGE, SystemPermissions.API_KEY_MANAGE, SystemPermissions.SECURITY_AUDIT_READ,
    },

    # ADMIN — Operational administration
    SystemRole.ADMIN.value: {
        SystemPermissions.LEAD_READ, SystemPermissions.LEAD_CREATE, SystemPermissions.LEAD_UPDATE, SystemPermissions.LEAD_DELETE, SystemPermissions.LEAD_EXPORT,
        SystemPermissions.BUSINESS_READ, SystemPermissions.BUSINESS_CREATE, SystemPermissions.BUSINESS_UPDATE, SystemPermissions.BUSINESS_DELETE,
        SystemPermissions.RESEARCH_READ, SystemPermissions.RESEARCH_RUN, SystemPermissions.AUDIT_READ, SystemPermissions.AUDIT_RUN,
        SystemPermissions.SCORING_READ, SystemPermissions.SCORING_CALCULATE, SystemPermissions.QUALIFICATION_READ, SystemPermissions.QUALIFICATION_OVERRIDE,
        SystemPermissions.OUTREACH_READ, SystemPermissions.OUTREACH_CREATE, SystemPermissions.OUTREACH_APPROVE, SystemPermissions.OUTREACH_SEND,
        SystemPermissions.REQUIREMENTS_READ, SystemPermissions.REQUIREMENTS_CREATE, SystemPermissions.REQUIREMENTS_CONFIRM,
        SystemPermissions.SOLUTION_READ, SystemPermissions.SOLUTION_CREATE, SystemPermissions.PROPOSAL_READ, SystemPermissions.PROPOSAL_CREATE, SystemPermissions.PROPOSAL_APPROVE, SystemPermissions.PROPOSAL_SEND,
        SystemPermissions.ESTIMATE_READ, SystemPermissions.ESTIMATE_CREATE, SystemPermissions.ESTIMATE_APPROVE,
        SystemPermissions.CONTRACT_READ, SystemPermissions.CONTRACT_CREATE, SystemPermissions.CONTRACT_APPROVE,
        SystemPermissions.PROJECT_READ, SystemPermissions.PROJECT_CREATE, SystemPermissions.PROJECT_UPDATE, SystemPermissions.PROJECT_EXPORT,
        SystemPermissions.CHANGE_READ, SystemPermissions.CHANGE_CREATE, SystemPermissions.CHANGE_APPROVE,
        SystemPermissions.QA_READ, SystemPermissions.QA_EXECUTE, SystemPermissions.RELEASE_APPROVE, SystemPermissions.HANDOVER_SIGN,
        SystemPermissions.SUPPORT_READ, SystemPermissions.SUPPORT_CREATE, SystemPermissions.SUPPORT_MANAGE,
        SystemPermissions.ANALYTICS_READ, SystemPermissions.ANALYTICS_EXPORT,
        SystemPermissions.AI_TRACE_READ, SystemPermissions.AI_EVALUATION_READ,
        SystemPermissions.WORKFLOW_READ, SystemPermissions.WORKFLOW_START, SystemPermissions.WORKFLOW_CANCEL,
        SystemPermissions.AUTOMATION_READ, SystemPermissions.AUTOMATION_MANAGE,
        SystemPermissions.USER_READ, SystemPermissions.USER_MANAGE, SystemPermissions.API_KEY_MANAGE, SystemPermissions.SECURITY_AUDIT_READ,
    },

    # SALES — Outreach, Proposals, CRM
    SystemRole.SALES.value: {
        SystemPermissions.LEAD_READ, SystemPermissions.LEAD_CREATE, SystemPermissions.LEAD_UPDATE, SystemPermissions.LEAD_EXPORT,
        SystemPermissions.BUSINESS_READ, SystemPermissions.BUSINESS_CREATE, SystemPermissions.BUSINESS_UPDATE,
        SystemPermissions.RESEARCH_READ, SystemPermissions.RESEARCH_RUN, SystemPermissions.AUDIT_READ, SystemPermissions.AUDIT_RUN,
        SystemPermissions.SCORING_READ, SystemPermissions.SCORING_CALCULATE, SystemPermissions.QUALIFICATION_READ,
        SystemPermissions.OUTREACH_READ, SystemPermissions.OUTREACH_CREATE, SystemPermissions.OUTREACH_APPROVE,
        SystemPermissions.REQUIREMENTS_READ, SystemPermissions.REQUIREMENTS_CREATE,
        SystemPermissions.SOLUTION_READ, SystemPermissions.PROPOSAL_READ, SystemPermissions.PROPOSAL_CREATE,
        SystemPermissions.ESTIMATE_READ, SystemPermissions.CONTRACT_READ,
        SystemPermissions.PROJECT_READ, SystemPermissions.ANALYTICS_READ,
    },

    # DEVELOPER — Assigned Projects, Tasks, Changes, AI Traces (read)
    SystemRole.DEVELOPER.value: {
        SystemPermissions.BUSINESS_READ, SystemPermissions.LEAD_READ,
        SystemPermissions.REQUIREMENTS_READ, SystemPermissions.SOLUTION_READ,
        SystemPermissions.ESTIMATE_READ, SystemPermissions.CONTRACT_READ,
        SystemPermissions.PROJECT_READ, SystemPermissions.PROJECT_UPDATE,
        SystemPermissions.CHANGE_READ, SystemPermissions.CHANGE_CREATE,
        SystemPermissions.QA_READ, SystemPermissions.QA_EXECUTE,
        SystemPermissions.SUPPORT_READ, SystemPermissions.AI_TRACE_READ,
        SystemPermissions.WORKFLOW_READ,
    },

    # QA — Testing, Defects, Releases
    SystemRole.QA.value: {
        SystemPermissions.PROJECT_READ, SystemPermissions.REQUIREMENTS_READ, SystemPermissions.SOLUTION_READ,
        SystemPermissions.QA_READ, SystemPermissions.QA_EXECUTE, SystemPermissions.CHANGE_READ,
        SystemPermissions.SUPPORT_READ,
    },

    # AI_ENGINEER — AI Traces, Models, Evaluations, Prompts
    SystemRole.AI_ENGINEER.value: {
        SystemPermissions.RESEARCH_READ, SystemPermissions.AUDIT_READ,
        SystemPermissions.AI_TRACE_READ, SystemPermissions.AI_EVALUATION_READ, SystemPermissions.AI_PROMPT_MANAGE,
        SystemPermissions.WORKFLOW_READ, SystemPermissions.AUTOMATION_READ,
    },

    # SECURITY — Audit, Policies, Users, Key management
    SystemRole.SECURITY.value: {
        SystemPermissions.SECURITY_AUDIT_READ, SystemPermissions.USER_READ, SystemPermissions.USER_MANAGE,
        SystemPermissions.ROLE_MANAGE, SystemPermissions.API_KEY_MANAGE, SystemPermissions.AI_TRACE_READ,
        SystemPermissions.AI_KILL_SWITCH, SystemPermissions.TENANT_MANAGE,
    },

    # ANALYST — Business Intelligence & Metrics Read
    SystemRole.ANALYST.value: {
        SystemPermissions.LEAD_READ, SystemPermissions.BUSINESS_READ, SystemPermissions.PROJECT_READ,
        SystemPermissions.PROPOSAL_READ, SystemPermissions.ESTIMATE_READ, SystemPermissions.CONTRACT_READ,
        SystemPermissions.ANALYTICS_READ, SystemPermissions.ANALYTICS_EXPORT,
    },

    # VIEWER — Internal Read-Only
    SystemRole.VIEWER.value: {
        SystemPermissions.LEAD_READ, SystemPermissions.BUSINESS_READ, SystemPermissions.PROJECT_READ,
        SystemPermissions.ANALYTICS_READ,
    },

    # CLIENT_OWNER — External Client Admin
    SystemRole.CLIENT_OWNER.value: {
        SystemPermissions.PROJECT_READ, SystemPermissions.CHANGE_READ, SystemPermissions.CHANGE_CREATE,
        SystemPermissions.UAT_ACCEPT, SystemPermissions.HANDOVER_SIGN,
        SystemPermissions.SUPPORT_READ, SystemPermissions.SUPPORT_CREATE,
        SystemPermissions.CONTRACT_READ, SystemPermissions.PROPOSAL_READ,
    },

    # CLIENT_ADMIN — External Client Project Admin
    SystemRole.CLIENT_ADMIN.value: {
        SystemPermissions.PROJECT_READ, SystemPermissions.CHANGE_READ, SystemPermissions.CHANGE_CREATE,
        SystemPermissions.UAT_ACCEPT, SystemPermissions.SUPPORT_READ, SystemPermissions.SUPPORT_CREATE,
        SystemPermissions.PROPOSAL_READ,
    },

    # CLIENT_MEMBER — External Client Collaborator
    SystemRole.CLIENT_MEMBER.value: {
        SystemPermissions.PROJECT_READ, SystemPermissions.SUPPORT_READ, SystemPermissions.SUPPORT_CREATE,
    },

    # CLIENT_REVIEWER — External Reviewer (UAT)
    SystemRole.CLIENT_REVIEWER.value: {
        SystemPermissions.PROJECT_READ, SystemPermissions.UAT_ACCEPT, SystemPermissions.SUPPORT_READ,
    },

    # CLIENT_VIEWER — External Read-Only
    SystemRole.CLIENT_VIEWER.value: {
        SystemPermissions.PROJECT_READ,
    },
}


def get_role_permissions(role_name: str) -> Set[str]:
    """Retrieve the set of permissions granted to a role."""
    return ROLE_PERMISSIONS_MAP.get(role_name, set()).copy()
