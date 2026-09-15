"""Communication Policies, Quiet-Hours Evaluation, and Mandatory Security Overrides."""

from dataclasses import dataclass, field
from datetime import datetime, time, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

from app.communication.base import (
    CommunicationType,
    DeliveryChannel,
    NotificationPriority,
)

MANDATORY_COMMUNICATION_CATEGORIES: Set[CommunicationType] = {
    CommunicationType.SECURITY,
}

SAFETY_CRITICAL_PRIORITIES: Set[NotificationPriority] = {
    NotificationPriority.CRITICAL,
}


@dataclass
class QuietHoursPolicy:
    """User-configured quiet-hours window."""

    enabled: bool = False
    start_hour: int = 22
    start_minute: int = 0
    end_hour: int = 7
    end_minute: int = 0
    timezone_offset_hours: int = 0

    def is_in_quiet_hours(self, dt: Optional[datetime] = None) -> bool:
        if not self.enabled:
            return False

        if dt is None:
            dt = datetime.now(timezone.utc)

        # Approximate local time with offset
        local_hour = (dt.hour + self.timezone_offset_hours) % 24
        local_time_val = local_hour * 60 + dt.minute
        start_val = self.start_hour * 60 + self.start_minute
        end_val = self.end_hour * 60 + self.end_minute

        if start_val <= end_val:
            return start_val <= local_time_val < end_val
        else:
            # Over midnight (e.g. 22:00 -> 07:00)
            return local_time_val >= start_val or local_time_val < end_val


class CommunicationPolicyEngine:
    """Evaluates communication rules, channel validity, and quiet-hours behavior."""

    @staticmethod
    def is_mandatory_notification(
        category: CommunicationType, priority: NotificationPriority
    ) -> bool:
        """Verify if notification is safety-critical and cannot be disabled."""
        if category in MANDATORY_COMMUNICATION_CATEGORIES:
            return True
        if priority in SAFETY_CRITICAL_PRIORITIES:
            return True
        return False

    @staticmethod
    def should_suppress_for_quiet_hours(
        priority: NotificationPriority,
        category: CommunicationType,
        quiet_hours: QuietHoursPolicy,
        now: Optional[datetime] = None,
    ) -> Tuple[bool, str]:
        """Check if notification delivery should be delayed during quiet hours."""
        if CommunicationPolicyEngine.is_mandatory_notification(category, priority):
            return False, "BYPASS_MANDATORY_SECURITY_OR_CRITICAL"

        if quiet_hours.is_in_quiet_hours(now):
            return True, "DELAYED_DUE_TO_QUIET_HOURS"

        return False, "PERMITTED"
