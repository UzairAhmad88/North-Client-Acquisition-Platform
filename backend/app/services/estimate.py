"""Estimate Service layer managing project estimation, Risk Engine evaluation, versioning, and human approvals."""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.estimation.agent import estimation_agent
from app.models.business import Business
from app.models.estimate import ProjectEstimate
from app.models.solution import SolutionDeliverable, SolutionDesign, SolutionFeature
from app.repositories.estimate import EstimateRepository
from app.services.risk import RiskService


class EstimateService:
    """Service layer for project estimation workflows, Risk Engine evaluation, and human operator approvals."""

    @staticmethod
    def create_estimate(
        db: Session, solution_id: uuid.UUID, user_id: Optional[uuid.UUID] = None
    ) -> ProjectEstimate:
        sol_obj = db.query(SolutionDesign).filter(SolutionDesign.id == solution_id).first()
        if not sol_obj:
            raise ValueError(f"SolutionDesign {solution_id} not found")

        est_data = {
            "solution_id": solution_id,
            "business_id": sol_obj.business_id,
            "lead_id": sol_obj.lead_id,
            "status": "DRAFT",
            "complexity": sol_obj.complexity_tier or "MEDIUM",
            "confidence": "MEDIUM",
            "estimated_hours": 0.0,
            "minimum_hours": 0.0,
            "maximum_hours": 0.0,
            "risk_buffer_percent": 20.0,
            "created_by_id": user_id,
        }
        return EstimateRepository.create_estimate(db, est_data)

    @staticmethod
    def get_estimate(db: Session, estimate_id: uuid.UUID) -> Optional[ProjectEstimate]:
        return EstimateRepository.get_estimate(db, estimate_id)

    @staticmethod
    def list_estimates(db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[ProjectEstimate]:
        return EstimateRepository.list_estimates(db, status=status, limit=limit, offset=offset)

    @staticmethod
    async def calculate_estimate(db: Session, estimate_id: uuid.UUID) -> ProjectEstimate:
        est_obj = EstimateRepository.get_estimate(db, estimate_id)
        if not est_obj:
            raise ValueError(f"ProjectEstimate {estimate_id} not found")

        sol_obj = db.query(SolutionDesign).filter(SolutionDesign.id == est_obj.solution_id).first()
        biz = db.query(Business).filter(Business.id == est_obj.business_id).first()
        biz_name = biz.name if biz else "Client Business"

        features = db.query(SolutionFeature).filter(SolutionFeature.solution_id == sol_obj.id).all()
        deliverables = db.query(SolutionDeliverable).filter(SolutionDeliverable.solution_id == sol_obj.id).all()

        sol_data = {
            "overview": sol_obj.overview,
            "architecture_summary": sol_obj.architecture_summary,
            "features": [{"title": f.title, "description": f.description, "category": f.category, "status": f.status} for f in features],
            "deliverables": [{"name": d.name, "description": d.description} for d in deliverables],
        }

        context = AgentContext(
            workflow_id=f"wf-est-{str(estimate_id)[:8]}",
            task_id=f"task-est-{str(estimate_id)[:8]}",
            agent_run_id=str(uuid.uuid4()),
            business_profile={"id": str(est_obj.business_id), "name": biz_name},
            metadata={"solution_data": sol_data},
        )

        agent_result = await estimation_agent.run(context)
        res_data = agent_result.result

        est_obj.status = "REVIEW"
        est_obj.complexity = res_data.get("complexity", "MEDIUM")
        est_obj.confidence = res_data.get("confidence", "MEDIUM")
        est_obj.estimated_hours = res_data.get("estimated_hours", 0.0)
        est_obj.minimum_hours = res_data.get("minimum_hours", 0.0)
        est_obj.maximum_hours = res_data.get("maximum_hours", 0.0)
        est_obj.risk_buffer_percent = res_data.get("risk_buffer_percent", 20.0)
        est_obj.internal_cost = res_data.get("internal_cost")
        est_obj.external_cost = res_data.get("external_cost")
        est_obj.recommended_min = res_data.get("recommended_min")
        est_obj.recommended_max = res_data.get("recommended_max")
        est_obj.content_hash = res_data.get("content_hash")
        est_obj.version += 1

        # Create Estimate Work Items
        for item_dict in res_data.get("work_items", []):
            EstimateRepository.create_work_item(
                db,
                {
                    "estimate_id": est_obj.id,
                    "name": item_dict["name"],
                    "category": item_dict.get("category", "BACKEND"),
                    "description": item_dict["description"],
                    "complexity": item_dict.get("complexity", "MEDIUM"),
                    "optimistic_hours": item_dict["optimistic_hours"],
                    "most_likely_hours": item_dict["most_likely_hours"],
                    "pessimistic_hours": item_dict["pessimistic_hours"],
                    "expected_hours": item_dict["expected_hours"],
                    "confidence": item_dict.get("confidence", "MEDIUM"),
                },
            )

        # Create Estimate Costs
        for cost_dict in res_data.get("costs", []):
            EstimateRepository.create_cost_item(
                db,
                {
                    "estimate_id": est_obj.id,
                    "cost_type": cost_dict["cost_type"],
                    "description": cost_dict["description"],
                    "amount": cost_dict["amount"],
                    "currency": cost_dict.get("currency", "USD"),
                    "source": cost_dict.get("source", "CONFIGURED_RATE"),
                },
            )

        # Create Estimate Scenarios
        for scen_dict in res_data.get("scenarios", []):
            EstimateRepository.create_scenario(
                db,
                {
                    "estimate_id": est_obj.id,
                    "name": scen_dict["name"],
                    "description": scen_dict["description"],
                    "scope": scen_dict["scope"],
                    "estimated_hours": scen_dict["estimated_hours"],
                    "internal_cost": scen_dict.get("internal_cost"),
                    "external_cost": scen_dict.get("external_cost"),
                    "recommended_min": scen_dict.get("recommended_min"),
                    "recommended_max": scen_dict.get("recommended_max"),
                    "risk_level": scen_dict.get("risk_level", "MEDIUM"),
                    "status": "PROPOSED",
                },
            )

        # Create Estimate Version Snapshot
        EstimateRepository.create_version(
            db,
            {
                "estimate_id": est_obj.id,
                "version": est_obj.version,
                "content_hash": est_obj.content_hash or "hash-v1",
                "snapshot_json": res_data,
                "created_by_id": est_obj.created_by_id,
            },
        )

        # Evaluate through Phase 20 Risk & Quality Engine
        summary_text = f"Project estimate for {biz_name}: {est_obj.estimated_hours}h. Commercial range: ${est_obj.recommended_min}-${est_obj.recommended_max}."
        await RiskService.evaluate_artifact(
            db,
            artifact_type="ESTIMATE",
            artifact_id=est_obj.id,
            business_id=est_obj.business_id,
            content=summary_text,
            recipient_address=biz.email if biz else "internal@norths.com",
            metadata={"estimated_hours": est_obj.estimated_hours, "complexity": est_obj.complexity},
        )

        db.commit()
        db.refresh(est_obj)
        return est_obj

    @staticmethod
    def approve_estimate(db: Session, estimate_id: uuid.UUID, user_id: uuid.UUID) -> ProjectEstimate:
        est_obj = EstimateRepository.get_estimate(db, estimate_id)
        if not est_obj:
            raise ValueError(f"ProjectEstimate {estimate_id} not found")

        est_obj.status = "APPROVED"
        est_obj.approved_by_id = user_id
        est_obj.approved_at = datetime.utcnow()
        est_obj.version += 1

        db.commit()
        db.refresh(est_obj)
        return est_obj
