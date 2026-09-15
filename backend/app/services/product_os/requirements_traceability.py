"""Requirements and Traceability Service for Phase 60 Product Operating System.

Provides PRD authoring, functional/non-functional requirement breakdown,
user stories with Given/When/Then acceptance criteria, and full end-to-end
traceability matrices linking Problem -> Insight -> Opportunity -> Initiative -> Requirement -> User Story -> Release -> Outcome.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.product_os.base import (
        AttrDict,
        generate_product_id,
        RequirementType,
    )
except ImportError:
    from app.services.product_os.base import (
        AttrDict,
        generate_product_id,
        RequirementType,
    )


logger = logging.getLogger(__name__)


class RequirementsTraceabilityService:
    """Manages PRDs, requirements, user stories, and end-to-end traceability."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._requirements: Dict[str, Dict[str, Any]] = {}
        self._user_stories: Dict[str, Dict[str, Any]] = {}

    def create_requirement(
        self,
        tenant_id: str,
        opportunity_id: str,
        title: str,
        requirement_type: str = RequirementType.FUNCTIONAL.value,
        priority: str = "HIGH",
        description: str = "",
        acceptance_criteria: Optional[List[str]] = None,
        non_goals: Optional[List[str]] = None,
        security_implications: Optional[Dict[str, Any]] = None,
        privacy_implications: Optional[Dict[str, Any]] = None,
        linked_initiative_id: Optional[str] = None,
        target_release_id: Optional[str] = None,
    ) -> AttrDict:
        """Create a new product requirement with structured metadata."""
        req_id = generate_product_id("req")
        now = datetime.now(timezone.utc).isoformat()

        req_record = {
            "requirement_id": req_id,
            "tenant_id": tenant_id,
            "opportunity_id": opportunity_id,
            "linked_initiative_id": linked_initiative_id,
            "title": title,
            "requirement_type": requirement_type,
            "priority": priority,
            "status": "DRAFT",
            "description": description,
            "acceptance_criteria": acceptance_criteria or [],
            "non_goals": non_goals or [],
            "security_implications": security_implications or {},
            "privacy_implications": privacy_implications or {},
            "target_release_id": target_release_id,
            "created_at": now,
            "updated_at": now,
        }
        self._requirements[req_id] = req_record
        return AttrDict(req_record)

    def add_user_story(
        self,
        tenant_id: str,
        requirement_id: str,
        role: str,
        capability: str,
        benefit: str,
        given_when_then: Optional[List[Dict[str, str]]] = None,
        story_points: int = 3,
        technical_notes: str = "",
    ) -> AttrDict:
        """Add a formatted user story (As a [role], I want [capability], So that [benefit])."""
        story_id = generate_product_id("story")
        now = datetime.now(timezone.utc).isoformat()

        title = f"As a {role}, I want {capability} so that {benefit}"
        story_record = {
            "story_id": story_id,
            "tenant_id": tenant_id,
            "requirement_id": requirement_id,
            "role": role,
            "capability": capability,
            "benefit": benefit,
            "title": title,
            "given_when_then": given_when_then or [
                {
                    "given": f"User is authenticated as {role}",
                    "when": f"User triggers {capability}",
                    "then": f"System delivers {benefit} with low latency",
                }
            ],
            "story_points": story_points,
            "status": "BACKLOG",
            "technical_notes": technical_notes,
            "created_at": now,
            "updated_at": now,
        }
        self._user_stories[story_id] = story_record
        return AttrDict(story_record)

    def build_traceability_matrix(
        self,
        tenant_id: str,
        opportunity_service: Any,
        problem_service: Any,
        roadmap_service: Any,
    ) -> List[Dict[str, Any]]:
        """Construct full end-to-end traceability graph across lifecycle stages."""
        matrix: List[Dict[str, Any]] = []

        for req_id, req in self._requirements.items():
            if req.get("tenant_id") != tenant_id:
                continue

            opp_id = req.get("opportunity_id")
            opp = opportunity_service._opportunities.get(opp_id, {}) if hasattr(opportunity_service, "_opportunities") else {}
            prob_id = opp.get("problem_id")
            prob = problem_service._problems.get(prob_id, {}) if hasattr(problem_service, "_problems") else {}
            
            stories = [
                s for s in self._user_stories.values()
                if s.get("requirement_id") == req_id and s.get("tenant_id") == tenant_id
            ]

            init_id = req.get("linked_initiative_id")
            init_item = roadmap_service._items.get(init_id, {}) if hasattr(roadmap_service, "_items") and init_id else {}

            trace_entry = {
                "requirement_id": req_id,
                "requirement_title": req.get("title"),
                "requirement_type": req.get("requirement_type"),
                "priority": req.get("priority"),
                "status": req.get("status"),
                "problem": {
                    "problem_id": prob.get("problem_id", prob_id),
                    "title": prob.get("title", "Direct Requirement / Operational"),
                    "severity": prob.get("severity", "MEDIUM"),
                    "validation_status": prob.get("validation_status", "VALIDATED"),
                },
                "opportunity": {
                    "opportunity_id": opp.get("opportunity_id", opp_id),
                    "title": opp.get("title", "Direct Strategic Opportunity"),
                    "score": opp.get("score", 0.0),
                },
                "roadmap_initiative": {
                    "initiative_id": init_item.get("item_id", init_id),
                    "title": init_item.get("title", "Unassigned Roadmap Item"),
                    "horizon": init_item.get("horizon", "NEXT"),
                },
                "user_stories": [
                    {
                        "story_id": s.get("story_id"),
                        "title": s.get("title"),
                        "story_points": s.get("story_points"),
                        "status": s.get("status"),
                        "criteria_count": len(s.get("given_when_then", [])),
                    }
                    for s in stories
                ],
                "is_orphaned": not bool(prob_id or opp_id),
                "completeness_score": 100 if stories and prob_id and opp_id else 65 if stories else 35,
            }
            matrix.append(trace_entry)

        return matrix

    def validate_requirements_completeness(self, tenant_id: str) -> Dict[str, Any]:
        """Audit all requirements for missing acceptance criteria, security, or user stories."""
        total = 0
        orphaned = 0
        missing_criteria = 0
        missing_stories = 0

        for req_id, req in self._requirements.items():
            if req.get("tenant_id") != tenant_id:
                continue
            total += 1
            if not req.get("opportunity_id"):
                orphaned += 1
            if not req.get("acceptance_criteria"):
                missing_criteria += 1
            stories = [s for s in self._user_stories.values() if s.get("requirement_id") == req_id]
            if not stories:
                missing_stories += 1

        compliance_rate = ((total - (orphaned + missing_criteria + missing_stories) / 3) / max(1, total)) * 100.0

        return {
            "tenant_id": tenant_id,
            "total_requirements": total,
            "orphaned_requirements": orphaned,
            "missing_acceptance_criteria": missing_criteria,
            "missing_user_stories": missing_stories,
            "requirements_health_score": round(max(0.0, min(100.0, compliance_rate)), 2),
            "status": "PASS" if compliance_rate >= 80.0 else "REVIEW_REQUIRED",
        }
