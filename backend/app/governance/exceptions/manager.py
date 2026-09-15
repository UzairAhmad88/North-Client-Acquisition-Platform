"""
Policy Exceptions & Compensating Controls Manager (Section 22 & 23).
Enforces time-bound validity, mandatory compensating controls, and dual approval.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from backend.app.governance.base import (
    ExceptionStatus,
    GovernanceException,
    RiskLevel,
)


class ExceptionManager:
    """Governs policy and control exceptions with mandatory expiration and compensating safeguards."""

    def __init__(self):
        self._exceptions: Dict[str, GovernanceException] = {}

    def request_exception(
        self,
        exception_code: str,
        title: str,
        control_code: str,
        reason: str,
        compensating_controls: List[str],
        owner_id: str,
        requester_id: str,
        expiration_date: datetime,
        risk_level: RiskLevel = RiskLevel.MEDIUM
    ) -> GovernanceException:
        """Requests a new policy exception with mandatory compensating controls and expiration date."""
        if not expiration_date or expiration_date <= datetime.now(timezone.utc):
            raise ValueError("Safety violation: Exceptions must be time-bound with a valid future expiration date.")
        if not compensating_controls:
            raise ValueError("Safety violation: Exceptions must specify at least one verified compensating control.")
        if not requester_id:
            raise ValueError("Requester ID is required.")

        exc = GovernanceException(
            exception_code=exception_code,
            title=title,
            control_code=control_code,
            reason=reason,
            risk_level=risk_level,
            compensating_controls=compensating_controls,
            owner_id=owner_id,
            requester_id=requester_id,
            status=ExceptionStatus.REQUESTED,
            expiration_date=expiration_date
        )
        self._exceptions[exception_code] = exc
        return exc

    def approve_exception(
        self,
        exception_code: str,
        approver_id: str,
        is_ai_agent: bool = False
    ) -> GovernanceException:
        """Approves a requested exception. Strictly requires human approval and separation of duties."""
        if is_ai_agent:
            raise PermissionError("Safety violation: AI agents cannot approve compliance or security exceptions.")
        if not approver_id:
            raise ValueError("Approver ID is required.")

        exc = self._exceptions.get(exception_code)
        if not exc:
            raise KeyError(f"Exception '{exception_code}' not found.")

        # Separation of Duties: Requester cannot approve their own exception
        if exc.requester_id == approver_id:
            raise PermissionError("Separation of duties violation: Exception requester cannot be the approver.")

        exc.approver_id = approver_id
        exc.approved_at = datetime.now(timezone.utc)
        exc.status = ExceptionStatus.ACTIVE
        return exc

    def sweep_expired_exceptions(self) -> int:
        """Sweeps all active exceptions and marks those past their expiration date as EXPIRED."""
        now = datetime.now(timezone.utc)
        expired_count = 0
        for exc in self._exceptions.values():
            if exc.status == ExceptionStatus.ACTIVE and exc.expiration_date <= now:
                exc.status = ExceptionStatus.EXPIRED
                expired_count += 1
        return expired_count

    def get_exception(self, exception_code: str) -> Optional[GovernanceException]:
        return self._exceptions.get(exception_code)

    def list_exceptions(self, status: Optional[ExceptionStatus] = None) -> List[GovernanceException]:
        excs = list(self._exceptions.values())
        if status:
            excs = [e for e in excs if e.status == status]
        return excs
