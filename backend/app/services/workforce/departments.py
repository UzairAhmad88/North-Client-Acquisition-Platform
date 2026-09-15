"""
AI Department & Team Hierarchy Subsystem for Phase 52.
Organizes AI workers into functional departments (Sales, Delivery, Operations, Governance, Strategy) and collaborative squads.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.workforce.base import AIDepartment, AITeam, AIWorker
except ImportError:
    from app.services.workforce.base import AIDepartment, AITeam, AIWorker

logger = logging.getLogger(__name__)


class DepartmentManager:
    """Manages AI functional departments and cross-departmental budgeting."""

    DEFAULT_DEPARTMENTS = [
        {"code": "DEPT-SALES", "name": "Sales & Revenue AI Department", "budget": 600.0},
        {"code": "DEPT-DELIVERY", "name": "Engineering & Delivery AI Department", "budget": 800.0},
        {"code": "DEPT-OPERATIONS", "name": "Operations & Finance AI Department", "budget": 400.0},
        {"code": "DEPT-GOVERNANCE", "name": "Security & GRC AI Department", "budget": 300.0},
        {"code": "DEPT-STRATEGY", "name": "Executive & Strategic Intelligence Department", "budget": 400.0},
    ]

    def __init__(self):
        self._departments: Dict[str, AIDepartment] = {}
        self._teams: Dict[str, AITeam] = {}
        self._initialize_defaults()

    def _initialize_defaults(self):
        for d in self.DEFAULT_DEPARTMENTS:
            self._departments[d["code"]] = AIDepartment(
                department_code=d["code"],
                name=d["name"],
                monthly_budget_usd=d["budget"],
            )

        # Default squads
        self._teams["TEAM-DISCOVERY-01"] = AITeam(
            team_code="TEAM-DISCOVERY-01",
            department_code="DEPT-SALES",
            name="Autonomous Discovery & Outreach Squad",
            purpose="Conducts web discovery, website audits, qualification, and personalized draft creation.",
            workflow_template="SEQUENTIAL_PIPELINE",
            members=["WRK-RESEARCH-01", "WRK-LEAD_QUALIFICATION-01", "WRK-OUTREACH_DRAFTING-01"],
        )
        self._teams["TEAM-DELIVERY-01"] = AITeam(
            team_code="TEAM-DELIVERY-01",
            department_code="DEPT-DELIVERY",
            name="Solution Architecture & Estimation Squad",
            purpose="Analyzes requirements, designs architectural solutions, and generates commercial estimates.",
            workflow_template="PARALLEL_REVIEW",
            members=["WRK-REQUIREMENTS-01", "WRK-SOLUTION_ARCHITECT-01", "WRK-ESTIMATION-01"],
        )

    def create_department(self, name: str, monthly_budget_usd: float = 500.0, description: Optional[str] = None) -> AIDepartment:
        dept = AIDepartment(name=name, monthly_budget_usd=monthly_budget_usd, description=description)
        self._departments[dept.department_code] = dept
        return dept

    def list_departments(self) -> List[AIDepartment]:
        return list(self._departments.values())

    def create_team(
        self,
        department_code: str,
        name: str,
        purpose: Optional[str] = None,
        members: Optional[List[str]] = None,
        workflow_template: str = "PARALLEL_REVIEW",
        budget_limit_usd: float = 150.0,
    ) -> AITeam:
        team = AITeam(
            department_code=department_code,
            name=name,
            purpose=purpose,
            members=members or [],
            workflow_template=workflow_template,
            budget_limit_usd=budget_limit_usd,
        )
        self._teams[team.team_code] = team
        return team

    def list_teams(self, department_code: Optional[str] = None) -> List[AITeam]:
        res = list(self._teams.values())
        if department_code:
            res = [t for t in res if t.department_code == department_code]
        return res
