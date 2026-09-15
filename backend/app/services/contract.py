"""Contract Service layer managing contract generation, Risk Engine evaluation, client acceptance, signatures, and locked baselines."""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from agents.contracts.agent import contract_agent
from agents.core.context import AgentContext
from app.models.business import Business
from app.models.contract import Contract, ContractBaseline, ContractSection
from app.models.estimate import ProjectEstimate
from app.models.proposal import Proposal, ProposalItem
from app.models.solution import SolutionDeliverable, SolutionDesign, SolutionFeature
from app.repositories.contract import ContractRepository
from app.services.risk import RiskService
from integrations.signature.models import SignatureRequest
from integrations.signature.service import SignatureService


class ContractService:
    """Service layer for contract drafting, risk evaluation, operator approval, client acceptance, signature execution, and baseline locking."""

    @staticmethod
    def create_contract(
        db: Session, proposal_id: uuid.UUID, estimate_id: uuid.UUID, user_id: Optional[uuid.UUID] = None, title: Optional[str] = None
    ) -> Contract:
        prop = db.query(Proposal).filter(Proposal.id == proposal_id).first()
        if not prop:
            raise ValueError(f"Proposal {proposal_id} not found")

        est = db.query(ProjectEstimate).filter(ProjectEstimate.id == estimate_id).first()
        if not est:
            raise ValueError(f"ProjectEstimate {estimate_id} not found")

        biz = db.query(Business).filter(Business.id == prop.business_id).first()
        biz_name = biz.name if biz else "Client Business"
        contract_number = f"CTR-2026-{str(uuid.uuid4())[:6].upper()}"

        contract_data = {
            "proposal_id": proposal_id,
            "estimate_id": estimate_id,
            "solution_id": prop.solution_id,
            "business_id": prop.business_id,
            "lead_id": prop.lead_id,
            "contract_number": contract_number,
            "title": title or f"Technical Services Agreement - {biz_name}",
            "summary": f"Technical services contract drafting in progress for {biz_name}.",
            "status": "DRAFT",
            "pricing_status": prop.pricing_status,
            "risk_status": "PENDING_REVIEW",
            "currency": "USD",
            "total_amount": est.recommended_min,
            "created_by_id": user_id,
        }
        return ContractRepository.create_contract(db, contract_data)

    @staticmethod
    def get_contract(db: Session, contract_id: uuid.UUID) -> Optional[Contract]:
        return ContractRepository.get_contract(db, contract_id)

    @staticmethod
    def list_contracts(db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[Contract]:
        return ContractRepository.list_contracts(db, status=status, limit=limit, offset=offset)

    @staticmethod
    async def generate_contract(db: Session, contract_id: uuid.UUID) -> Contract:
        contract_obj = ContractRepository.get_contract(db, contract_id)
        if not contract_obj:
            raise ValueError(f"Contract {contract_id} not found")

        prop = db.query(Proposal).filter(Proposal.id == contract_obj.proposal_id).first()
        est = db.query(ProjectEstimate).filter(ProjectEstimate.id == contract_obj.estimate_id).first()
        sol = db.query(SolutionDesign).filter(SolutionDesign.id == contract_obj.solution_id).first()
        biz = db.query(Business).filter(Business.id == contract_obj.business_id).first()
        biz_name = biz.name if biz else "Client Business"

        features = db.query(SolutionFeature).filter(SolutionFeature.solution_id == sol.id).all()
        deliverables = db.query(SolutionDeliverable).filter(SolutionDeliverable.solution_id == sol.id).all()

        proposal_data = {
            "summary": prop.summary,
            "pricing_status": prop.pricing_status,
            "version": prop.version,
        }
        estimate_data = {
            "recommended_min": est.recommended_min,
            "recommended_max": est.recommended_max,
            "version": est.version,
        }
        solution_data = {
            "features": [{"title": f.title, "description": f.description, "category": f.category} for f in features],
            "deliverables": [{"name": d.name, "description": d.description} for d in deliverables],
            "out_of_scope": ["Custom Native Mobile App", "Legacy Data Migration"],
        }

        context = AgentContext(
            workflow_id=f"wf-ctr-{str(contract_id)[:8]}",
            task_id=f"task-ctr-{str(contract_id)[:8]}",
            agent_run_id=str(uuid.uuid4()),
            business_profile={"id": str(contract_obj.business_id), "name": biz_name},
            metadata={
                "contract_number": contract_obj.contract_number,
                "proposal_data": proposal_data,
                "estimate_data": estimate_data,
                "solution_data": solution_data,
            },
        )

        agent_result = await contract_agent.run(context)
        res_data = agent_result.result

        contract_obj.title = res_data.get("title", contract_obj.title)
        contract_obj.summary = res_data.get("summary", contract_obj.summary)
        contract_obj.content_hash = res_data.get("content_hash")
        contract_obj.status = "IN_REVIEW"
        contract_obj.version += 1

        # Create contract sections
        for sec_dict in res_data.get("sections", []):
            ContractRepository.create_section(
                db,
                {
                    "contract_id": contract_obj.id,
                    "title": sec_dict["title"],
                    "section_type": sec_dict["section_type"],
                    "content": sec_dict["content"],
                    "order_index": sec_dict.get("order_index", 0),
                },
            )

        # Create contract discrepancies if any
        for disc_dict in res_data.get("discrepancies", []):
            ContractRepository.create_discrepancy(
                db,
                {
                    "contract_id": contract_obj.id,
                    "discrepancy_type": disc_dict["discrepancy_type"],
                    "description": disc_dict["description"],
                    "severity": disc_dict.get("severity", "HIGH"),
                    "status": "DETECTED",
                },
            )

        # Create Contract Version Snapshot
        ContractRepository.create_version(
            db,
            {
                "contract_id": contract_obj.id,
                "version": contract_obj.version,
                "content_hash": contract_obj.content_hash or "hash-v1",
                "sections_json": res_data.get("sections", []),
                "source_proposal_version": prop.version,
                "source_estimate_version": est.version,
                "source_solution_version": sol.version,
                "source_requirements_version": 1,
                "created_by_id": contract_obj.created_by_id,
            },
        )

        # Evaluate through Phase 20 Risk & Quality Engine
        sections_text = "\n\n".join([f"## {s.get('title')}\n{s.get('content')}" for s in res_data.get("sections", [])])
        await RiskService.evaluate_artifact(
            db,
            artifact_type="CONTRACT",
            artifact_id=contract_obj.id,
            business_id=contract_obj.business_id,
            content=sections_text,
            recipient_address=biz.email if biz else "client@business.com",
            metadata={"discrepancies": res_data.get("discrepancies", [])},
        )

        db.commit()
        db.refresh(contract_obj)
        return contract_obj

    @staticmethod
    def approve_contract_internally(db: Session, contract_id: uuid.UUID, user_id: uuid.UUID, reason: str = "Operator approved contract draft") -> Contract:
        contract_obj = ContractRepository.get_contract(db, contract_id)
        if not contract_obj:
            raise ValueError(f"Contract {contract_id} not found")

        contract_obj.status = "READY_FOR_CLIENT"
        contract_obj.approved_by_id = user_id
        contract_obj.approved_at = datetime.utcnow()

        ContractRepository.create_approval(
            db,
            {
                "contract_id": contract_obj.id,
                "version": contract_obj.version,
                "status": "APPROVED",
                "approval_reason": reason,
                "content_hash": contract_obj.content_hash or "hash-v1",
                "approved_by_id": user_id,
            },
        )

        db.commit()
        db.refresh(contract_obj)
        return contract_obj

    @staticmethod
    def client_accept_contract(db: Session, contract_id: uuid.UUID, client_email: str, acceptance_statement: str) -> Contract:
        contract_obj = ContractRepository.get_contract(db, contract_id)
        if not contract_obj:
            raise ValueError(f"Contract {contract_id} not found")

        contract_obj.status = "CLIENT_APPROVED"

        ContractRepository.create_client_acceptance(
            db,
            {
                "contract_id": contract_obj.id,
                "version": contract_obj.version,
                "status": "APPROVED",
                "acceptance_statement": acceptance_statement,
                "client_email": client_email,
                "content_hash": contract_obj.content_hash or "hash-v1",
                "accepted_at": datetime.utcnow(),
            },
        )

        db.commit()
        db.refresh(contract_obj)
        return contract_obj

    @staticmethod
    async def complete_contract_signature(db: Session, contract_id: uuid.UUID) -> Contract:
        contract_obj = ContractRepository.get_contract(db, contract_id)
        if not contract_obj:
            raise ValueError(f"Contract {contract_id} not found")

        biz = db.query(Business).filter(Business.id == contract_obj.business_id).first()

        # Trigger Mock Signature Service
        sig_req = SignatureRequest(
            contract_id=str(contract_obj.id),
            signer_email=biz.email if biz else "client@business.com",
            signer_name=biz.name if biz else "Client Signer",
            document_title=contract_obj.title,
            content_hash=contract_obj.content_hash or "hash-v1",
        )
        sig_init = await SignatureService.request_signature(sig_req)
        sig_done = await SignatureService.complete_signature(sig_init.provider_request_id)

        contract_obj.status = "SIGNED"

        ContractRepository.create_signature(
            db,
            {
                "contract_id": contract_obj.id,
                "provider_name": "mock",
                "provider_request_id": sig_done.provider_request_id,
                "signer_email": sig_req.signer_email,
                "status": "SIGNED",
                "signed_at": datetime.utcnow(),
            },
        )

        db.commit()
        db.refresh(contract_obj)
        return contract_obj

    @staticmethod
    def lock_contract_baseline(db: Session, contract_id: uuid.UUID) -> ContractBaseline:
        contract_obj = ContractRepository.get_contract(db, contract_id)
        if not contract_obj:
            raise ValueError(f"Contract {contract_id} not found")

        prop = db.query(Proposal).filter(Proposal.id == contract_obj.proposal_id).first()
        est = db.query(ProjectEstimate).filter(ProjectEstimate.id == contract_obj.estimate_id).first()
        sol = db.query(SolutionDesign).filter(SolutionDesign.id == contract_obj.solution_id).first()

        contract_obj.status = "ACTIVE"

        baseline = ContractRepository.create_baseline(
            db,
            {
                "contract_id": contract_obj.id,
                "contract_version": contract_obj.version,
                "requirements_version": 1,
                "solution_version": sol.version if sol else 1,
                "estimate_version": est.version if est else 1,
                "proposal_version": prop.version if prop else 1,
                "scope_hash": contract_obj.content_hash or "scope-hash",
                "commercial_hash": contract_obj.content_hash or "comm-hash",
                "contract_hash": contract_obj.content_hash or "contract-hash",
                "is_locked": True,
                "locked_at": datetime.utcnow(),
            },
        )

        db.commit()
        db.refresh(contract_obj)
        return baseline
