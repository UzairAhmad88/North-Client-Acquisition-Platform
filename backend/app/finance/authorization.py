"""Financial authorization, tenant isolation, and client visibility masking.
"""

from typing import Any, Dict, List, Optional
from copy import deepcopy


class FinancialAuthorizationManager:
    """Enforces multi-tenant isolation, role permissions, and client-safe payload masking."""

    ROLE_PERMISSIONS = {
        "admin": {
            "can_view_internal_costs": True,
            "can_view_margins": True,
            "can_view_ledger": True,
            "can_create_invoice": True,
            "can_approve_invoice": True,
            "can_issue_invoice": True,
            "can_record_payment": True,
            "can_process_refund": True,
            "can_manage_tax": True,
            "can_manage_accounts": True,
        },
        "finance_manager": {
            "can_view_internal_costs": True,
            "can_view_margins": True,
            "can_view_ledger": True,
            "can_create_invoice": True,
            "can_approve_invoice": True,
            "can_issue_invoice": True,
            "can_record_payment": True,
            "can_process_refund": True,
            "can_manage_tax": True,
            "can_manage_accounts": True,
        },
        "accountant": {
            "can_view_internal_costs": True,
            "can_view_margins": True,
            "can_view_ledger": True,
            "can_create_invoice": True,
            "can_approve_invoice": False,
            "can_issue_invoice": False,
            "can_record_payment": True,
            "can_process_refund": False,
            "can_manage_tax": False,
            "can_manage_accounts": False,
        },
        "project_manager": {
            "can_view_internal_costs": False,
            "can_view_margins": False,
            "can_view_ledger": False,
            "can_create_invoice": True,
            "can_approve_invoice": False,
            "can_issue_invoice": False,
            "can_record_payment": False,
            "can_process_refund": False,
            "can_manage_tax": False,
            "can_manage_accounts": False,
        },
        "client": {
            "can_view_internal_costs": False,
            "can_view_margins": False,
            "can_view_ledger": False,
            "can_create_invoice": False,
            "can_approve_invoice": False,
            "can_issue_invoice": False,
            "can_record_payment": False,
            "can_process_refund": False,
            "can_manage_tax": False,
            "can_manage_accounts": False,
        },
    }

    @classmethod
    def check_permission(cls, role: str, permission: str) -> bool:
        """Returns True if the role has the specific financial capability."""
        perms = cls.ROLE_PERMISSIONS.get(role.lower(), {})
        return perms.get(permission, False)

    @classmethod
    def mask_client_payload(cls, data: Dict[str, Any], is_client: bool) -> Dict[str, Any]:
        """Scrubs sensitive internal financial data (labor cost rates, margins, AI token costs, internal ledger notes) for client roles."""
        if not is_client:
            return data

        masked = deepcopy(data)

        # Keys to completely strip from client responses
        sensitive_keys = {
            "cost_breakdown",
            "profitability_metrics",
            "internal_cost",
            "internal_cost_rate",
            "developer_hourly_rate",
            "ai_token_cost",
            "infrastructure_cost",
            "subcontractor_cost",
            "margin_pct",
            "gross_profit",
            "commercial_health",
            "ledger_entries",
        }

        def _recursive_clean(obj: Any) -> Any:
            if isinstance(obj, dict):
                cleaned = {}
                for k, v in obj.items():
                    if k not in sensitive_keys:
                        cleaned[k] = _recursive_clean(v)
                return cleaned
            elif isinstance(obj, list):
                return [_recursive_clean(item) for item in obj]
            return obj

        return _recursive_clean(masked)

    @staticmethod
    def verify_tenant_isolation(entity_tenant_id: str, request_tenant_id: str) -> bool:
        """Verifies multi-tenant access boundaries."""
        if not entity_tenant_id or not request_tenant_id:
            return False
        return entity_tenant_id == request_tenant_id
