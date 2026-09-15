"""Solution Service layer managing solution design creation, analysis, and approval."""

import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.solution.agent import solution_agent
from app.models.requirements import ClientRequirement, DiscoverySession
from app.models.solution import SolutionDesign
from app.repositories.solution import SolutionRepository


class SolutionService:
    """Service layer managing Solution Design workflows and Agent execution."""

    @staticmethod
    def create_solution_design(
        db: Session, discovery_session_id: uuid.UUID, user_id: Optional[uuid.UUID] = None, overview: Optional[str] = None
    ) -> SolutionDesign:
        disc_session = db.query(DiscoverySession).filter(DiscoverySession.id == discovery_session_id).first()
        if not disc_session:
            raise ValueError(f"DiscoverySession {discovery_session_id} not found")

        sol_data = {
            "discovery_session_id": discovery_session_id,
            "business_id": disc_session.business_id,
            "lead_id": disc_session.lead_id,
            "status": "DRAFT",
            "overview": overview or f"Solution design for Discovery Session #{str(discovery_session_id)[:8]}",
            "architecture_summary": "Pending analysis",
            "complexity_tier": disc_session.scope_complexity or "MEDIUM",
            "created_by_id": user_id,
        }
        return SolutionRepository.create_solution(db, sol_data)

    @staticmethod
    def get_solution(db: Session, solution_id: uuid.UUID) -> Optional[SolutionDesign]:
        return SolutionRepository.get_solution(db, solution_id)

    @staticmethod
    def list_solutions(db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[SolutionDesign]:
        return SolutionRepository.list_solutions(db, status=status, limit=limit, offset=offset)

    @staticmethod
    async def analyze_solution_design(db: Session, solution_id: uuid.UUID) -> SolutionDesign:
        sol_obj = SolutionRepository.get_solution(db, solution_id)
        if not sol_obj:
            raise ValueError(f"SolutionDesign {solution_id} not found")

        # Fetch confirmed or proposed requirements for this discovery session
        reqs = (
            db.query(ClientRequirement)
            .filter(ClientRequirement.discovery_session_id == sol_obj.discovery_session_id)
            .all()
        )
        reqs_data = [
            {
                "id": str(r.id),
                "title": r.title,
                "category": r.category,
                "explicit": r.explicit,
                "priority": r.priority,
                "status": r.status,
            }
            for r in reqs
        ]

        context = AgentContext(
            workflow_id=f"wf-sol-{str(solution_id)[:8]}",
            task_id=f"task-sol-{str(solution_id)[:8]}",
            agent_run_id=str(uuid.uuid4()),
            business_profile={"id": str(sol_obj.business_id)},
            metadata={"requirements": reqs_data},
        )

        agent_result = await solution_agent.run(context)
        res_data = agent_result.result

        # Update solution overview and architecture summary
        sol_obj.overview = res_data.get("overview", sol_obj.overview)
        sol_obj.architecture_summary = res_data.get("architecture_summary", sol_obj.architecture_summary)
        sol_obj.complexity_tier = res_data.get("complexity_tier", "MEDIUM")
        sol_obj.status = "GENERATED"
        sol_obj.version += 1

        # Create features
        feature_map = {}
        for feat_dict in res_data.get("features", []):
            feat_obj = SolutionRepository.create_feature(
                db,
                {
                    "solution_id": sol_obj.id,
                    "title": feat_dict["title"],
                    "description": feat_dict["description"],
                    "category": feat_dict["category"],
                    "status": feat_dict.get("status", "RECOMMENDED"),
                    "priority": feat_dict.get("priority", "MEDIUM"),
                },
            )
            feature_map[feat_dict["title"]] = feat_obj.id

        # Create deliverables
        for deliv_dict in res_data.get("deliverables", []):
            SolutionRepository.create_deliverable(
                db,
                {
                    "solution_id": sol_obj.id,
                    "name": deliv_dict["name"],
                    "description": deliv_dict["description"],
                    "status": deliv_dict.get("status", "PROPOSED"),
                    "priority": deliv_dict.get("priority", "HIGH"),
                },
            )

        # Create integrations
        for integ_dict in res_data.get("integrations", []):
            SolutionRepository.create_integration(
                db,
                {
                    "solution_id": sol_obj.id,
                    "purpose": integ_dict["purpose"],
                    "provider": integ_dict["provider"],
                    "data_flow": integ_dict["data_flow"],
                    "status": integ_dict.get("status", "PROPOSED"),
                },
            )

        # Create assumptions
        for assump_dict in res_data.get("assumptions", []):
            SolutionRepository.create_assumption(
                db,
                {
                    "solution_id": sol_obj.id,
                    "assumption_text": assump_dict["assumption_text"],
                    "status": assump_dict.get("status", "UNCONFIRMED"),
                    "risk_level": assump_dict.get("risk_level", "MEDIUM"),
                },
            )

        db.commit()
        db.refresh(sol_obj)
        return sol_obj

    @staticmethod
    def approve_solution_design(db: Session, solution_id: uuid.UUID, user_id: uuid.UUID) -> SolutionDesign:
        sol_obj = SolutionRepository.get_solution(db, solution_id)
        if not sol_obj:
            raise ValueError(f"SolutionDesign {solution_id} not found")

        sol_obj.status = "APPROVED"
        sol_obj.approved_by_id = user_id
        sol_obj.approved_at = datetime.utcnow()
        sol_obj.version += 1

        db.commit()
        db.refresh(sol_obj)
        return sol_obj
