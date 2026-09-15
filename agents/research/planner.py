"""Bounded Research Planner."""

from typing import Any, Dict, List, Set


class ResearchPlanner:
    """Analyzes existing research records vs requested sections to target missing or stale fields."""

    @staticmethod
    def plan_research(
        requested_sections: List[str],
        existing_records: List[Dict[str, Any]],
        max_age_days: int = 30,
    ) -> Dict[str, Any]:
        """Produce a bounded research plan focusing on missing or stale fields."""
        existing_fields: Set[str] = set()
        stale_fields: Set[str] = set()

        for rec in existing_records:
            field_name = rec.get("field_name")
            if field_name:
                existing_fields.add(field_name)

        target_fields: List[str] = []
        for sec in requested_sections:
            if sec not in existing_fields:
                target_fields.append(sec)

        return {
            "requested_sections": requested_sections,
            "existing_fields_count": len(existing_fields),
            "target_fields": target_fields,
            "should_search_web": len(target_fields) > 0 or len(existing_records) == 0,
        }
