"""Disaster Recovery & Business Continuity Plan Registry and Recovery Hierarchy."""

from typing import Any, Dict, List
from app.reliability.base import DRPlanStatus


# Strict 14-step recovery priority hierarchy
DEFAULT_RECOVERY_PRIORITY = [
    {"step": 1, "service": "Identity & RBAC Access Control", "criticality": "TIER_0"},
    {"step": 2, "service": "PostgreSQL Primary Database", "criticality": "TIER_0"},
    {"step": 3, "service": "Core Backend API Gateway", "criticality": "TIER_0"},
    {"step": 4, "service": "Object & Document Storage", "criticality": "TIER_1"},
    {"step": 5, "service": "Event Bus & Transactional Outbox", "criticality": "TIER_1"},
    {"step": 6, "service": "Workflow Orchestration Engine", "criticality": "TIER_1"},
    {"step": 7, "service": "Communication & Notification Dispatcher", "criticality": "TIER_1"},
    {"step": 8, "service": "Finance & Double-Entry Ledger", "criticality": "TIER_1"},
    {"step": 9, "service": "CRM, Leads & Opportunities", "criticality": "TIER_2"},
    {"step": 10, "service": "Project Delivery & Tasks WBS", "criticality": "TIER_2"},
    {"step": 11, "service": "Customer Support & Incident Escalation", "criticality": "TIER_2"},
    {"step": 12, "service": "Analytics & Business Intelligence", "criticality": "TIER_3"},
    {"step": 13, "service": "AI Model Router & Agent Subsystems", "criticality": "TIER_3"},
    {"step": 14, "service": "Predictive Operations & Advanced Intelligence", "criticality": "TIER_4"},
]


class DisasterRecoveryPlanRegistry:
    """Manages active disaster recovery plans, RPO/RTO SLAs, and business continuity runbooks."""

    @staticmethod
    def get_standard_dr_plan() -> Dict[str, Any]:
        return {
            "name": "Uzaii Standard Platform Disaster Recovery Plan",
            "version": "1.0",
            "status": DRPlanStatus.ACTIVE.value,
            "rpo_targets": {
                "financial_records": "5 minutes",
                "core_crm_and_projects": "15 minutes",
                "communication_messages": "15 minutes",
                "analytics_and_traces": "24 hours",
            },
            "rto_targets": {
                "tier_0_core_platform": "30 minutes",
                "tier_1_financial_ops": "1 hour",
                "tier_2_customer_facing": "2 hours",
                "tier_3_ai_and_analytics": "4 hours",
            },
            "recovery_priority_sequence": DEFAULT_RECOVERY_PRIORITY,
        }
