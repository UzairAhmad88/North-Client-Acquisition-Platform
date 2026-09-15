"""Customer Success Agent Safety & Guardrail Validation."""

from typing import Set
from agents.core.errors import AgentPermissionDeniedError


PROHIBITED_CUSTOMER_SUCCESS_ACTIONS: Set[str] = {
    "SEND_CLIENT_MESSAGE",
    "SEND_EXTERNAL_EMAIL",
    "APPROVE_RENEWAL",
    "CHANGE_CLIENT_PRICING",
    "CHANGE_CONTRACT_BASELINE",
    "DELETE_CLIENT_RECORD",
    "EXECUTE_PAYMENT",
    "MODIFY_HEALTH_BASELINE",
    "CLOSE_RISK_WITHOUT_REVIEW",
}


class CustomerSuccessSafetyValidator:
    """Validates that requested agent actions conform to strict decision-support boundaries."""

    @staticmethod
    def validate_action(action_name: str) -> None:
        if action_name.upper() in PROHIBITED_CUSTOMER_SUCCESS_ACTIONS:
            raise AgentPermissionDeniedError(
                f"CustomerSuccessAgent action '{action_name}' is strictly prohibited. "
                f"Customer Success AI operates strictly in an advisory / decision-support capacity."
            )
