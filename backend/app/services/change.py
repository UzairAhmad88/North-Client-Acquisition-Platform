"""Service layer for Phase 28 — Change Request, Scope Change & Commercial Change Management."""

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.change import (
    ChangeApproval,
    ChangeBaselineLink,
    ChangeCommercial,
    ChangeEstimate,
    ChangeEvidence,
    ChangeEvent,
    ChangeImpact,
    ChangeRequest,
    ChangeRequestVersion,
)
from app.models.contract import ContractBaseline
from app.models.project import Project, ProjectTask
from app.repositories.change import ChangeRepository
from app.repositories.contract import ContractRepository
from app.repositories.project import ProjectRepository
from agents.change_management.classifier import ChangeClassifier
from agents.change_management.impact_analyzer import ChangeImpactAnalyzer
from agents.change_management.effort_analyzer import ChangeEffortAnalyzer
from agents.change_management.commercial_analyzer import ChangeCommercialAnalyzer
from agents.change_management.contract_analyzer import ChangeContractAnalyzer
from agents.change_management.summary import ChangeSummaryEngine


class ChangeService:
    """Business logic engine for Change Requests, Triage, Impact Analysis, Re-estimation, Approvals, and Baseline Revisions."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ChangeRepository(session)
        self.project_repo = ProjectRepository(session)
        self.contract_repo = ContractRepository(session)

        # AI Engines
        self.classifier = ChangeClassifier()
        self.impact_analyzer = ChangeImpactAnalyzer()
        self.effort_analyzer = ChangeEffortAnalyzer()
        self.commercial_analyzer = ChangeCommercialAnalyzer()
        self.contract_analyzer = ChangeContractAnalyzer()
        self.summary_engine = ChangeSummaryEngine()

    async def create_change_request(
        self,
        project_id: str,
        title: str,
        description: str,
        requested_by: str,
        category: str = "SCOPE",
        source: str = "CLIENT_PORTAL",
        reason: Optional[str] = None,
    ) -> ChangeRequest:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project '{project_id}' not found.")

        change_number = await self.repo.generate_next_change_number(project_id)

        change_req = ChangeRequest(
            id=str(uuid.uuid4()),
            change_number=change_number,
            project_id=project_id,
            business_id=project.business_id,
            client_id=None,
            contract_id=project.contract_id,
            baseline_id=project.baseline_id,
            title=title,
            description=description,
            category=category,
            classification="UNKNOWN",
            status="REQUESTED",
            priority="MEDIUM",
            source=source,
            reason=reason,
            requested_by=requested_by,
            requested_at=datetime.now(timezone.utc),
        )

        change_req = await self.repo.create_change_request(change_req)

        # Initial Version v1
        payload_text = f"{title}:{description}"
        content_hash = hashlib.sha256(payload_text.encode("utf-8")).hexdigest()

        version_v1 = ChangeRequestVersion(
            id=str(uuid.uuid4()),
            change_request_id=change_req.id,
            version_number=1,
            description=description,
            content_hash=content_hash,
            created_by=requested_by,
        )
        await self.repo.create_version(version_v1)

        # Log event
        await self.repo.record_event(
            ChangeEvent(
                id=str(uuid.uuid4()),
                change_request_id=change_req.id,
                event_type="CHANGE_CREATED",
                actor_id=requested_by,
                event_data={"change_number": change_number, "title": title},
            )
        )

        return change_req

    async def triage_and_classify(self, change_id: str, actor_id: str = "SYSTEM") -> ChangeRequest:
        change_req = await self.repo.get_by_id(change_id)
        if not change_req:
            raise ValueError(f"Change Request '{change_id}' not found.")

        class_res = self.classifier.classify_change(
            change_request_id=change_id,
            title=change_req.title,
            description=change_req.description,
        )

        change_req.classification = class_res.classification
        if class_res.classification == "IN_SCOPE":
            change_req.status = "TRIAGED"
        elif class_res.classification == "DEFECT":
            change_req.status = "TRIAGED"
        else:
            change_req.status = "TRIAGED"

        await self.repo.update(change_req)

        await self.repo.record_event(
            ChangeEvent(
                id=str(uuid.uuid4()),
                change_request_id=change_req.id,
                event_type="CHANGE_CLASSIFIED",
                actor_id=actor_id,
                event_data={"classification": class_res.classification, "reasoning": class_res.reasoning},
            )
        )

        return change_req

    async def run_impact_analysis(self, change_id: str, actor_id: str = "SYSTEM") -> Dict[str, Any]:
        change_req = await self.repo.get_by_id(change_id)
        if not change_req:
            raise ValueError(f"Change Request '{change_id}' not found.")

        latest_version = change_req.versions[0] if change_req.versions else None
        if not latest_version:
            raise ValueError("No change request version found.")

        # AI Multi-dimensional Impact
        impact_res = self.impact_analyzer.analyze_impact(change_id, change_req.title, change_req.description)

        for imp in impact_res.impacts:
            db_imp = ChangeImpact(
                id=str(uuid.uuid4()),
                change_request_version_id=latest_version.id,
                impact_type=imp.impact_type,
                entity_type=imp.entity_type,
                entity_id=imp.entity_id,
                impact_action=imp.impact_action,
                impact_description=imp.impact_description,
                confidence=imp.confidence,
                evidence_reference=imp.evidence_reference,
            )
            await self.repo.add_impact(db_imp)

        # Effort Re-estimation
        effort_res = self.effort_analyzer.calculate_effort(change_id, change_req.title, change_req.description)
        db_est = ChangeEstimate(
            id=str(uuid.uuid4()),
            change_request_version_id=latest_version.id,
            optimistic_hours=effort_res.optimistic_hours,
            most_likely_hours=effort_res.most_likely_hours,
            pessimistic_hours=effort_res.pessimistic_hours,
            expected_hours=effort_res.expected_hours,
            confidence=effort_res.confidence,
            assumptions=effort_res.assumptions,
        )
        await self.repo.add_estimate(db_est)

        # Commercial Delta Analysis
        comm_res = self.commercial_analyzer.calculate_commercial_delta(
            change_id, effort_res.expected_hours, hourly_rate=5000.0, original_contract_value=0.0
        )
        db_comm = ChangeCommercial(
            id=str(uuid.uuid4()),
            change_request_version_id=latest_version.id,
            currency=comm_res.currency,
            original_value=comm_res.original_value,
            change_value=comm_res.change_value,
            revised_value=comm_res.revised_value,
            pricing_policy_version=comm_res.pricing_policy_version,
            status="DRAFT",
        )
        await self.repo.add_commercial(db_comm)

        # Update Summary
        summary = self.summary_engine.summarize_change(
            change_id,
            change_req.change_number,
            change_req.title,
            change_req.description,
            effort_res.expected_hours,
            comm_res.change_value,
        )
        latest_version.scope_summary = summary.scope_delta_description
        latest_version.commercial_summary = summary.commercial_impact_summary
        latest_version.schedule_summary = f"+{summary.estimated_schedule_impact_days} working days"
        latest_version.impact_summary = summary.executive_summary

        change_req.impact_status = "COMPLETED"
        change_req.status = "IMPACT_ANALYSIS"
        await self.repo.update(change_req)

        await self.repo.record_event(
            ChangeEvent(
                id=str(uuid.uuid4()),
                change_request_id=change_req.id,
                event_type="IMPACT_ANALYSIS_COMPLETED",
                actor_id=actor_id,
                event_data={
                    "expected_hours": effort_res.expected_hours,
                    "change_value": comm_res.change_value,
                    "overall_impact": impact_res.overall_impact_level,
                },
            )
        )

        return {
            "change_request": change_req,
            "impact_analysis": impact_res,
            "effort_estimate": effort_res,
            "commercial_analysis": comm_res,
            "summary": summary,
        }

    async def approve_internal(self, change_id: str, approver_id: str, reason: Optional[str] = None) -> ChangeRequest:
        change_req = await self.repo.get_by_id(change_id)
        if not change_req:
            raise ValueError(f"Change Request '{change_id}' not found.")

        latest_version = change_req.versions[0] if change_req.versions else None
        if not latest_version:
            raise ValueError("No active version found for change request.")

        approval = ChangeApproval(
            id=str(uuid.uuid4()),
            change_request_version_id=latest_version.id,
            approver_id=approver_id,
            approval_type="INTERNAL",
            status="APPROVED",
            approved_at=datetime.now(timezone.utc),
            reason=reason or "Internal engineering & commercial sign-off granted.",
            content_hash=latest_version.content_hash,
        )
        await self.repo.add_approval(approval)

        change_req.approval_status = "INTERNAL_APPROVED"
        change_req.status = "PENDING_CLIENT"
        await self.repo.update(change_req)

        await self.repo.record_event(
            ChangeEvent(
                id=str(uuid.uuid4()),
                change_request_id=change_req.id,
                event_type="INTERNAL_APPROVAL_GRANTED",
                actor_id=approver_id,
                event_data={"version_number": latest_version.version_number},
            )
        )

        return change_req

    async def approve_client(self, change_id: str, client_signer_id: str, approval_statement: str) -> ChangeRequest:
        change_req = await self.repo.get_by_id(change_id)
        if not change_req:
            raise ValueError(f"Change Request '{change_id}' not found.")

        latest_version = change_req.versions[0] if change_req.versions else None
        if not latest_version:
            raise ValueError("No active version found for change request.")

        approval = ChangeApproval(
            id=str(uuid.uuid4()),
            change_request_version_id=latest_version.id,
            approver_id=client_signer_id,
            approval_type="CLIENT",
            status="APPROVED",
            approved_at=datetime.now(timezone.utc),
            reason=approval_statement,
            content_hash=latest_version.content_hash,
        )
        await self.repo.add_approval(approval)

        change_req.client_approval_status = "CLIENT_APPROVED"
        change_req.status = "APPROVED"
        change_req.implementation_status = "READY"
        await self.repo.update(change_req)

        await self.repo.record_event(
            ChangeEvent(
                id=str(uuid.uuid4()),
                change_request_id=change_req.id,
                event_type="CLIENT_APPROVAL_GRANTED",
                actor_id=client_signer_id,
                event_data={"statement": approval_statement, "hash": latest_version.content_hash},
            )
        )

        return change_req

    async def update_baseline_revision(self, change_id: str, actor_id: str) -> ContractBaseline:
        change_req = await self.repo.get_by_id(change_id)
        if not change_req or change_req.status != "APPROVED":
            raise ValueError("Change Request must be fully APPROVED before revising baseline.")

        current_baseline = await self.contract_repo.get_baseline_by_id(change_req.baseline_id) if change_req.baseline_id else None
        next_ver = (current_baseline.version + 1) if current_baseline else 2

        # Hash new scope
        new_scope_text = f"Baseline v{next_ver} containing approved change {change_req.change_number}: {change_req.title}"
        scope_hash = hashlib.sha256(new_scope_text.encode("utf-8")).hexdigest()

        new_baseline = ContractBaseline(
            id=str(uuid.uuid4()),
            contract_id=change_req.contract_id or "cnt-1",
            version=next_ver,
            scope_hash=scope_hash,
            commercial_hash=scope_hash,
            locked_at=datetime.now(timezone.utc),
        )
        new_baseline = await self.contract_repo.create_baseline(new_baseline)

        # Save link
        if current_baseline:
            await self.repo.save_baseline_link(
                ChangeBaselineLink(
                    id=str(uuid.uuid4()),
                    change_request_id=change_id,
                    previous_baseline_id=current_baseline.id,
                    new_baseline_id=new_baseline.id,
                )
            )

        change_req.status = "BASELINE_UPDATE"
        await self.repo.update(change_req)

        await self.repo.record_event(
            ChangeEvent(
                id=str(uuid.uuid4()),
                change_request_id=change_id,
                event_type="BASELINE_UPDATED",
                actor_id=actor_id,
                event_data={"new_baseline_id": new_baseline.id, "version": next_ver},
            )
        )

        return new_baseline

    async def implement_change_tasks(self, change_id: str, actor_id: str) -> List[ProjectTask]:
        change_req = await self.repo.get_by_id(change_id)
        if not change_req:
            raise ValueError(f"Change Request '{change_id}' not found.")

        # Create new execution task for the project
        task = ProjectTask(
            id=str(uuid.uuid4()),
            project_id=change_req.project_id,
            name=f"[{change_req.change_number}] {change_req.title}",
            description=change_req.description,
            status="TODO",
            estimated_hours=20.0,
            actual_hours=0.0,
            created_at=datetime.now(timezone.utc),
        )
        self.session.add(task)
        await self.session.commit()

        change_req.implementation_status = "IN_PROGRESS"
        change_req.status = "IMPLEMENTATION"
        await self.repo.update(change_req)

        await self.repo.record_event(
            ChangeEvent(
                id=str(uuid.uuid4()),
                change_request_id=change_id,
                event_type="IMPLEMENTATION_STARTED",
                actor_id=actor_id,
                event_data={"created_task_id": task.id},
            )
        )

        return [task]
