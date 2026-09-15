"""Phase 64 — Engineering Projects, Requirements & Spec Generator Service."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from backend.app.services.autonomous_engineering_os.base import (
    BaseAutonomousEngineeringOsService,
    AttrDict,
    EngineeringProjectWorkspaceModel,
    EngineeringRequirementModel,
    RequirementAcceptanceCriteriaModel,
)


class ProjectsRequirementsSpecsService(BaseAutonomousEngineeringOsService):
    """Service managing project workspaces, requirements, and specifications."""

    def __init__(self, db: Optional[Session] = None):
        super().__init__(db)
        self._workspaces: Dict[str, Any] = {}
        self._requirements: Dict[str, Any] = {}
        self._acceptance_criteria: Dict[str, Any] = {}

    def create_project_workspace(
        self,
        tenant_id: str,
        name: str,
        owner: str,
        team: str,
        description: Optional[str] = None,
        repository_url: Optional[str] = None,
        tech_stack: Optional[List[str]] = None,
        budget_allocated_usd: float = 20000.0,
    ) -> Any:
        """Create new engineering project workspace."""
        workspace_id = self.generate_id("eng_proj")
        now = datetime.utcnow()
        tech_stack_val = tech_stack or ["Python", "FastAPI", "Next.js", "Docker", "PostgreSQL"]

        if self.db is not None and EngineeringProjectWorkspaceModel is not None:
            workspace = EngineeringProjectWorkspaceModel(
                id=workspace_id,
                tenant_id=tenant_id,
                name=name,
                owner=owner,
                team=team,
                description=description or f"Autonomous engineering workspace for {name}",
                repository_url=repository_url or f"https://github.com/uzaii-enterprise/{name.lower().replace(' ', '-')}",
                tech_stack=tech_stack_val,
                budget_allocated_usd=budget_allocated_usd,
                budget_spent_usd=0.0,
                status="ACTIVE",
                created_at=now,
                updated_at=now,
            )
            self.db.add(workspace)
            self.db.commit()
            self.db.refresh(workspace)
            return workspace
        else:
            workspace = AttrDict({
                "id": workspace_id,
                "tenant_id": tenant_id,
                "name": name,
                "owner": owner,
                "team": team,
                "description": description or f"Autonomous engineering workspace for {name}",
                "repository_url": repository_url or f"https://github.com/uzaii-enterprise/{name.lower().replace(' ', '-')}",
                "tech_stack": tech_stack_val,
                "budget_allocated_usd": budget_allocated_usd,
                "budget_spent_usd": 0.0,
                "status": "ACTIVE",
                "created_at": now,
                "updated_at": now,
            })
            self._workspaces[workspace_id] = workspace
            return workspace

    def list_project_workspaces(self, tenant_id: str) -> List[Any]:
        """List all engineering project workspaces for tenant."""
        if self.db is not None and EngineeringProjectWorkspaceModel is not None:
            return (
                self.db.query(EngineeringProjectWorkspaceModel)
                .filter(EngineeringProjectWorkspaceModel.tenant_id == tenant_id)
                .all()
            )
        return [w for w in self._workspaces.values() if w.tenant_id == tenant_id]

    def create_requirement(
        self,
        tenant_id: str,
        project_id: str,
        title: str,
        description: str,
        owner: str,
        requirement_type: str = "FUNCTIONAL",
        priority: str = "HIGH",
        dependencies: Optional[List[str]] = None,
    ) -> Any:
        """Create versioned requirement with automated ambiguity analysis."""
        vague_terms = ["fast", "seamless", "scalable", "user-friendly", "robust", "modern"]
        vague_count = sum(1 for term in vague_terms if term in description.lower())
        ambiguity_score = min(0.95, max(0.02, 0.05 + (vague_count * 0.15) if len(description) < 80 else 0.04))
        req_id = self.generate_id("eng_req")
        now = datetime.utcnow()

        if self.db is not None and EngineeringRequirementModel is not None:
            req = EngineeringRequirementModel(
                id=req_id,
                tenant_id=tenant_id,
                project_id=project_id,
                title=title,
                description=description,
                requirement_type=requirement_type,
                priority=priority,
                owner=owner,
                status="APPROVED",
                ambiguity_score=round(ambiguity_score, 2),
                dependencies=dependencies or [],
                created_at=now,
            )
            self.db.add(req)
            self.db.commit()
            self.db.refresh(req)
            return req
        else:
            req = AttrDict({
                "id": req_id,
                "tenant_id": tenant_id,
                "project_id": project_id,
                "title": title,
                "description": description,
                "requirement_type": requirement_type,
                "priority": priority,
                "owner": owner,
                "status": "APPROVED",
                "ambiguity_score": round(ambiguity_score, 2),
                "dependencies": dependencies or [],
                "created_at": now,
            })
            self._requirements[req_id] = req
            return req

    def list_requirements(self, tenant_id: str, project_id: Optional[str] = None) -> List[Any]:
        """List requirements filtered by tenant and optional project."""
        if self.db is not None and EngineeringRequirementModel is not None:
            query = self.db.query(EngineeringRequirementModel).filter(EngineeringRequirementModel.tenant_id == tenant_id)
            if project_id:
                query = query.filter(EngineeringRequirementModel.project_id == project_id)
            return query.all()
        results = [r for r in self._requirements.values() if r.tenant_id == tenant_id]
        if project_id:
            results = [r for r in results if r.project_id == project_id]
        return results

    def add_acceptance_criteria(
        self,
        tenant_id: str,
        requirement_id: str,
        given_clause: str,
        when_clause: str,
        then_clause: str,
        is_automated_test_created: bool = False,
    ) -> Any:
        """Add deterministic acceptance criteria (BDD Gherkin style)."""
        crit_id = self.generate_id("eng_crit")
        now = datetime.utcnow()

        if self.db is not None and RequirementAcceptanceCriteriaModel is not None:
            criteria = RequirementAcceptanceCriteriaModel(
                id=crit_id,
                tenant_id=tenant_id,
                requirement_id=requirement_id,
                given_clause=given_clause,
                when_clause=when_clause,
                then_clause=then_clause,
                is_automated_test_created=is_automated_test_created,
                created_at=now,
            )
            self.db.add(criteria)
            self.db.commit()
            self.db.refresh(criteria)
            return criteria
        else:
            criteria = AttrDict({
                "id": crit_id,
                "tenant_id": tenant_id,
                "requirement_id": requirement_id,
                "given_clause": given_clause,
                "when_clause": when_clause,
                "then_clause": then_clause,
                "is_automated_test_created": is_automated_test_created,
                "created_at": now,
            })
            self._acceptance_criteria[crit_id] = criteria
            return criteria

    def generate_technical_specification(
        self,
        tenant_id: str,
        requirement_id: str,
    ) -> Dict[str, Any]:
        """Synthesize versioned technical specification from requirement and acceptance criteria."""
        req = None
        if self.db is not None and EngineeringRequirementModel is not None:
            req = (
                self.db.query(EngineeringRequirementModel)
                .filter(
                    EngineeringRequirementModel.tenant_id == tenant_id,
                    EngineeringRequirementModel.id == requirement_id,
                )
                .first()
            )
            criteria = (
                self.db.query(RequirementAcceptanceCriteriaModel)
                .filter(
                    RequirementAcceptanceCriteriaModel.tenant_id == tenant_id,
                    RequirementAcceptanceCriteriaModel.requirement_id == requirement_id,
                )
                .all()
            )
        else:
            req = self._requirements.get(requirement_id)
            criteria = [c for c in self._acceptance_criteria.values() if c.tenant_id == tenant_id and c.requirement_id == requirement_id]

        if not req:
            raise ValueError(f"Requirement '{requirement_id}' not found.")

        return {
            "spec_id": self.generate_id("eng_spec"),
            "requirement_id": req.id,
            "project_id": req.project_id,
            "title": f"Technical Spec: {req.title}",
            "architecture_boundary": "Microservice Domain / API Gateway",
            "acceptance_criteria_count": len(criteria),
            "acceptance_criteria": [
                {
                    "id": c.id,
                    "given": c.given_clause,
                    "when": c.when_clause,
                    "then": c.then_clause,
                    "automated": c.is_automated_test_created,
                }
                for c in criteria
            ],
            "security_requirements": [
                "Strict Tenant Isolation enforcement via BaseAutonomousEngineeringOsService",
                "RBAC/ABAC token validation on all exposed endpoints",
                "Deny-by-default execution policy for autonomous side-effects",
            ],
            "testing_matrix": ["Unit Test Suite", "Integration Contract Validation", "SAST Security Scan"],
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat(),
        }
