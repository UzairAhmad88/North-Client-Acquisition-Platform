"""Customer Success authorization, tenant isolation, and client privacy masking."""

from typing import Any, Dict, List, Optional
from copy import deepcopy


class CustomerSuccessAuthorizationManager:
    """Enforces multi-tenant boundaries and masks sensitive internal relationship notes from client roles."""

    SENSITIVE_INTERNAL_KEYS = {
        "internal_health_reasoning",
        "internal_risk_notes",
        "internal_margins",
        "internal_margin_pct",
        "cost_model",
        "developer_hourly_rates",
        "subcontractor_costs",
        "account_plan_strategy",
        "private_staff_notes",
        "expansion_probability_score",
        "churn_prediction_raw",
        "ai_trace_id",
    }

    @classmethod
    def mask_client_360_payload(cls, data: Dict[str, Any], is_client: bool) -> Dict[str, Any]:
        """Scrubs internal assessments, margins, and raw risk reasons for client portal users."""
        if not is_client:
            return data

        masked = deepcopy(data)

        # In client view, hide internal risks by default or mask internal details
        if "risks_overview" in masked:
            # Client only sees public action items or empty risks
            masked["risks_overview"] = {
                "total_open_risks": 0,
                "risks": [],
            }

        if "health" in masked:
            # Show high-level band but hide internal factor calculations
            masked["health"] = {
                "health_band": masked["health"].get("health_band", "HEALTHY"),
                "status": "active",
            }

        def _recursive_clean(obj: Any) -> Any:
            if isinstance(obj, dict):
                cleaned = {}
                for k, v in obj.items():
                    if k not in cls.SENSITIVE_INTERNAL_KEYS:
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
