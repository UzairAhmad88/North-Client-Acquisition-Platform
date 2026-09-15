"""Proposal Service layer managing proposal generation, versioning, Risk Engine validation, and approval."""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.proposal.agent import proposal_agent
from app.models.business import Business
from app.models.proposal import Proposal, ProposalItem, ProposalVersion
from app.models.solution import SolutionDeliverable, SolutionDesign, SolutionFeature
from app.repositories.proposal import ProposalRepository
from app.services.risk import RiskService


class ProposalService:
    """Service layer for proposal generation, risk assessment, versioning, and human approval."""

    @staticmethod
    def create_proposal(
        db: Session, solution_id: uuid.UUID, proposal_type: str = "FULL", user_id: Optional[uuid.UUID] = None, title: Optional[str] = None
    ) -> Proposal:
        sol_obj = db.query(SolutionDesign).filter(SolutionDesign.id == solution_id).first()
        if not sol_obj:
            raise ValueError(f"SolutionDesign {solution_id} not found")

        biz = db.query(Business).filter(Business.id == sol_obj.business_id).first()
        biz_name = biz.name if biz else "Client Business"

        prop_data = {
            "solution_id": solution_id,
            "business_id": sol_obj.business_id,
            "lead_id": sol_obj.lead_id,
            "proposal_type": proposal_type,
            "title": title or f"Technical & Scope Proposal for {biz_name}",
            "summary": f"Proposal drafting in progress for {biz_name}.",
            "status": "DRAFT",
            "pricing_status": "PRICING_REQUIRES_HUMAN_REVIEW",
            "created_by_id": user_id,
        }
        return ProposalRepository.create_proposal(db, prop_data)

    @staticmethod
    def get_proposal(db: Session, proposal_id: uuid.UUID) -> Optional[Proposal]:
        return ProposalRepository.get_proposal(db, proposal_id)

    @staticmethod
    def list_proposals(db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[Proposal]:
        return ProposalRepository.list_proposals(db, status=status, limit=limit, offset=offset)

    @staticmethod
    async def generate_proposal(db: Session, proposal_id: uuid.UUID) -> Proposal:
        prop_obj = ProposalRepository.get_proposal(db, proposal_id)
        if not prop_obj:
            raise ValueError(f"Proposal {proposal_id} not found")

        sol_obj = db.query(SolutionDesign).filter(SolutionDesign.id == prop_obj.solution_id).first()
        biz = db.query(Business).filter(Business.id == prop_obj.business_id).first()
        biz_name = biz.name if biz else "Client Business"

        # Load solution features, deliverables, assumptions, etc.
        features = db.query(SolutionFeature).filter(SolutionFeature.solution_id == sol_obj.id).all()
        deliverables = db.query(SolutionDeliverable).filter(SolutionDeliverable.solution_id == sol_obj.id).all()

        sol_data = {
            "overview": sol_obj.overview,
            "architecture_summary": sol_obj.architecture_summary,
            "features": [{"title": f.title, "description": f.description, "category": f.category} for f in features],
            "deliverables": [{"name": d.name, "description": d.description, "id": str(d.id)} for d in deliverables],
            "assumptions": [{"assumption_text": "Client will provide branding and content assets."}],
            "out_of_scope": ["Custom Mobile Native App", "Legacy Data Migration"],
            "optional_features": [],
        }

        context = AgentContext(
            workflow_id=f"wf-prop-{str(proposal_id)[:8]}",
            task_id=f"task-prop-{str(proposal_id)[:8]}",
            agent_run_id=str(uuid.uuid4()),
            business_profile={"id": str(prop_obj.business_id), "name": biz_name},
            metadata={"solution_data": sol_data, "proposal_type": prop_obj.proposal_type},
        )

        agent_result = await proposal_agent.run(context)
        res_data = agent_result.result

        prop_obj.title = res_data.get("title", prop_obj.title)
        prop_obj.summary = res_data.get("summary", prop_obj.summary)
        prop_obj.pricing_status = res_data.get("pricing_status", "PRICING_REQUIRES_HUMAN_REVIEW")
        prop_obj.content_hash = res_data.get("content_hash")
        prop_obj.status = "IN_REVIEW"
        prop_obj.version += 1

        # Create proposal items
        for item_dict in res_data.get("items", []):
            ProposalRepository.create_item(
                db,
                {
                    "proposal_id": prop_obj.id,
                    "description": item_dict["description"],
                    "quantity": item_dict.get("quantity", 1.0),
                    "unit": item_dict.get("unit", "project"),
                    "is_optional": item_dict.get("is_optional", False),
                    "price": item_dict.get("price"),
                },
            )

        # Create Version Snapshot
        ProposalRepository.create_version(
            db,
            {
                "proposal_id": prop_obj.id,
                "version": prop_obj.version,
                "content_hash": prop_obj.content_hash or "hash-v1",
                "sections_json": res_data.get("sections", []),
                "created_by_id": prop_obj.created_by_id,
            },
        )

        # Run Phase 20 Risk & Quality Engine check
        sections_text = "\n\n".join([f"## {s.get('title')}\n{s.get('content')}" for s in res_data.get("sections", [])])
        await RiskService.evaluate_artifact(
            db,
            artifact_type="PROPOSAL",
            artifact_id=prop_obj.id,
            business_id=prop_obj.business_id,
            content=sections_text,
            recipient_address=biz.email if biz else "client@business.com",
            metadata={"unsupported_claims": [c for c in res_data.get("claims", []) if not c.get("is_supported")]},
        )

        db.commit()
        db.refresh(prop_obj)
        return prop_obj

    @staticmethod
    def approve_proposal(db: Session, proposal_id: uuid.UUID, user_id: uuid.UUID) -> Proposal:
        prop_obj = ProposalRepository.get_proposal(db, proposal_id)
        if not prop_obj:
            raise ValueError(f"Proposal {proposal_id} not found")

        prop_obj.status = "APPROVED"
        prop_obj.approved_by_id = user_id
        prop_obj.approved_at = datetime.utcnow()
        prop_obj.version += 1

        db.commit()
        db.refresh(prop_obj)
        return prop_obj
