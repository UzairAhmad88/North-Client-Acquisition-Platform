"""Audit Planner for target URL selection and existing audit freshness policy."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple


class AuditPlanner:
    """Plans audit execution by selecting target website and assessing data freshness."""

    @staticmethod
    def select_target_url(
        business_profile: Dict[str, Any],
        research_data: Dict[str, Any],
        explicit_url: Optional[str] = None,
    ) -> Tuple[Optional[str], str]:
        """Selection Hierarchy:

        1. Explicitly requested URL
        2. Verified official website from Business Profile
        3. Trusted website from Research records
        4. User-provided website
        5. NO_WEBSITE
        """
        if explicit_url and isinstance(explicit_url, str) and explicit_url.strip():
            return explicit_url.strip(), "EXPLICIT_URL"

        biz_url = business_profile.get("website_url")
        if biz_url and isinstance(biz_url, str) and biz_url.strip():
            return biz_url.strip(), "OFFICIAL_WEBSITE"

        # Check research data for verified website
        records = research_data.get("records", [])
        for rec in records:
            if rec.get("field_name") in ("website", "website_url", "identity") and rec.get("source_url"):
                src_url = rec["source_url"]
                if src_url.startswith("http://") or src_url.startswith("https://"):
                    return src_url.strip(), "RESEARCHED_WEBSITE"

        return None, "NO_WEBSITE"

    @staticmethod
    def check_audit_freshness(
        existing_audit: Optional[Dict[str, Any]],
        max_age_days: int = 7,
    ) -> bool:
        """Returns True if existing audit is fresh (age <= max_age_days) and can be reused."""
        if not existing_audit:
            return False

        created_at_str = existing_audit.get("completed_at") or existing_audit.get("created_at")
        if not created_at_str:
            return False

        try:
            if isinstance(created_at_str, datetime):
                dt = created_at_str
            else:
                dt = datetime.fromisoformat(str(created_at_str).replace("Z", "+00:00"))

            now = datetime.now(timezone.utc)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            age = now - dt
            return age <= timedelta(days=max_age_days)
        except Exception:
            return False
