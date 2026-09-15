"""Service layer for Phase 29 — Quality Assurance, UAT, Delivery Acceptance & Handover System."""

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.qa import (
    AcceptanceCriteria,
    Defect,
    DeliveryPackage,
    HandoverChecklist,
    QAEvent,
    ReleaseVersion,
    TestCase,
    TestEvidence,
    TestPlan,
    TestResult,
    TestRun,
    UATFeedback,
    UATSession,
)
from app.repositories.project import ProjectRepository
from app.repositories.qa import QARepository
from agents.qa.defect_classifier import DefectClassifierEngine
from agents.qa.handover_engine import HandoverEngine
from agents.qa.readiness_evaluator import ReadinessEvaluatorEngine
from agents.qa.regression_analyzer import RegressionAnalyzerEngine
from agents.qa.test_generator import TestGeneratorEngine


class QAService:
    """Business logic for QA Test Planning, Test Execution, Defect Triage, Client UAT, Release Gates, Delivery Packaging, and Handover."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = QARepository(session)
        self.project_repo = ProjectRepository(session)

        # AI Subsystem Engines
        self.test_generator = TestGeneratorEngine()
        self.defect_classifier = DefectClassifierEngine()
        self.regression_analyzer = RegressionAnalyzerEngine()
        self.readiness_evaluator = ReadinessEvaluatorEngine()
        self.handover_engine = HandoverEngine()

    # --- Test Plans & Test Cases ---
    async def create_test_plan(
        self,
        project_id: str,
        title: str,
        description: Optional[str] = None,
        plan_type: str = "SYSTEM",
        actor_id: str = "SYSTEM",
    ) -> TestPlan:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project '{project_id}' not found.")

        plan = TestPlan(
            id=str(uuid.uuid4()),
            project_id=project_id,
            title=title,
            description=description,
            plan_type=plan_type,
            status="DRAFT",
            created_by=actor_id,
        )
        plan = await self.repo.create_test_plan(plan)

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=project_id,
                event_type="TEST_PLAN_CREATED",
                actor_id=actor_id,
                event_data={"test_plan_id": plan.id, "title": title},
            )
        )
        return plan

    async def generate_ai_test_cases(
        self,
        test_plan_id: str,
        requirements: Optional[List[Dict[str, Any]]] = None,
        deliverables: Optional[List[Dict[str, Any]]] = None,
        actor_id: str = "SYSTEM",
    ) -> List[TestCase]:
        plan = await self.repo.get_test_plan(test_plan_id)
        if not plan:
            raise ValueError(f"Test Plan '{test_plan_id}' not found.")

        draft_result = self.test_generator.generate_test_cases(
            test_plan_id=test_plan_id,
            requirements=requirements,
            deliverables=deliverables,
        )

        created_cases: List[TestCase] = []
        for item in draft_result.generated_test_cases:
            # Check unique code
            unique_code = f"{item.code}-{uuid.uuid4().hex[:4]}"
            tc = TestCase(
                id=str(uuid.uuid4()),
                test_plan_id=test_plan_id,
                code=unique_code,
                title=item.title,
                description=item.description,
                category=item.category,
                priority=item.priority,
                execution_type=item.execution_type,
                preconditions=item.preconditions,
                steps=item.steps,
                expected_results=item.expected_results,
                is_regression=item.is_regression,
                requirement_id=item.requirement_id,
                deliverable_id=item.deliverable_id,
                created_by=actor_id,
            )
            tc = await self.repo.create_test_case(tc)
            created_cases.append(tc)

        plan.status = "ACTIVE"
        await self.session.commit()

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=plan.project_id,
                event_type="TEST_CASES_GENERATED",
                actor_id=actor_id,
                event_data={"test_plan_id": test_plan_id, "count": len(created_cases)},
            )
        )
        return created_cases

    # --- Test Runs & Execution ---
    async def create_test_run(
        self,
        project_id: str,
        test_plan_id: str,
        name: str,
        environment: str = "STAGING",
        actor_id: str = "SYSTEM",
    ) -> TestRun:
        plan = await self.repo.get_test_plan(test_plan_id)
        if not plan:
            raise ValueError(f"Test Plan '{test_plan_id}' not found.")

        run = TestRun(
            id=str(uuid.uuid4()),
            project_id=project_id,
            test_plan_id=test_plan_id,
            name=name,
            environment=environment,
            status="IN_PROGRESS",
            executed_by=actor_id,
            started_at=datetime.now(timezone.utc),
        )
        run = await self.repo.create_test_run(run)

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=project_id,
                event_type="TEST_RUN_STARTED",
                actor_id=actor_id,
                event_data={"test_run_id": run.id, "environment": environment},
            )
        )
        return run

    async def record_test_result(
        self,
        test_run_id: str,
        test_case_id: str,
        status: str,  # PASSED, FAILED, BLOCKED, SKIPPED
        actual_results: Optional[str] = None,
        execution_notes: Optional[str] = None,
        executed_by: str = "SYSTEM",
        evidence_files: Optional[List[Dict[str, str]]] = None,
    ) -> TestResult:
        run = await self.repo.get_test_run(test_run_id)
        if not run:
            raise ValueError(f"Test Run '{test_run_id}' not found.")

        res = TestResult(
            id=str(uuid.uuid4()),
            test_run_id=test_run_id,
            test_case_id=test_case_id,
            status=status,
            actual_results=actual_results,
            execution_notes=execution_notes,
            executed_by=executed_by,
            executed_at=datetime.now(timezone.utc),
        )
        res = await self.repo.add_test_result(res)

        if evidence_files:
            for ev in evidence_files:
                path = ev.get("file_path", "")
                content = ev.get("content", path)
                content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                evidence_obj = TestEvidence(
                    id=str(uuid.uuid4()),
                    test_result_id=res.id,
                    evidence_type=ev.get("evidence_type", "SCREENSHOT"),
                    file_path=path,
                    description=ev.get("description"),
                    sha256_hash=content_hash,
                )
                await self.repo.add_test_evidence(evidence_obj)

        # Update run counts
        if status == "PASSED":
            run.passed_count += 1
        elif status == "FAILED":
            run.failed_count += 1
        elif status == "BLOCKED":
            run.blocked_count += 1
        elif status == "SKIPPED":
            run.skipped_count += 1

        await self.repo.update_test_run(run)
        return res

    # --- Defect Management & Triage ---
    async def create_defect(
        self,
        project_id: str,
        title: str,
        description: str,
        reported_by: str,
        test_case_id: Optional[str] = None,
        test_run_id: Optional[str] = None,
        deliverable_id: Optional[str] = None,
        requirement_id: Optional[str] = None,
        is_against_spec: bool = True,
    ) -> Defect:
        defect_num = await self.repo.generate_next_defect_number(project_id)

        # AI Defect Classification
        classification_res = self.defect_classifier.classify_defect(
            defect_id=None,
            title=title,
            description=description,
            is_against_baseline_spec=is_against_spec,
        )

        defect = Defect(
            id=str(uuid.uuid4()),
            defect_number=defect_num,
            project_id=project_id,
            test_case_id=test_case_id,
            test_run_id=test_run_id,
            deliverable_id=deliverable_id,
            requirement_id=requirement_id,
            title=title,
            description=description,
            severity=classification_res.severity,
            priority=classification_res.priority,
            status="OPEN",
            classification=classification_res.classification,
            reported_by=reported_by,
        )
        defect = await self.repo.create_defect(defect)

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=project_id,
                event_type="DEFECT_CREATED",
                actor_id=reported_by,
                event_data={
                    "defect_number": defect_num,
                    "severity": classification_res.severity,
                    "classification": classification_res.classification,
                },
            )
        )
        return defect

    async def update_defect_status(
        self,
        defect_id: str,
        status: str,  # OPEN, IN_PROGRESS, RESOLVED, CLOSED, VERIFIED, REOPENED
        actor_id: str,
        resolution_summary: Optional[str] = None,
    ) -> Defect:
        defect = await self.repo.get_defect(defect_id)
        if not defect:
            raise ValueError(f"Defect '{defect_id}' not found.")

        defect.status = status
        if resolution_summary:
            defect.resolution_summary = resolution_summary

        if status == "RESOLVED":
            defect.resolved_at = datetime.now(timezone.utc)
        elif status == "CLOSED":
            defect.closed_at = datetime.now(timezone.utc)

        defect = await self.repo.update_defect(defect)

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=defect.project_id,
                event_type="DEFECT_STATUS_UPDATED",
                actor_id=actor_id,
                event_data={"defect_id": defect_id, "new_status": status},
            )
        )
        return defect

    # --- Client UAT Management ---
    async def create_uat_session(
        self,
        project_id: str,
        client_account_id: str,
        title: str,
        scope_description: Optional[str] = None,
        scheduled_start: Optional[datetime] = None,
        scheduled_end: Optional[datetime] = None,
        actor_id: str = "SYSTEM",
    ) -> UATSession:
        session_obj = UATSession(
            id=str(uuid.uuid4()),
            project_id=project_id,
            client_account_id=client_account_id,
            title=title,
            scope_description=scope_description,
            status="IN_PROGRESS",
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            approved_by_client=False,
        )
        session_obj = await self.repo.create_uat_session(session_obj)

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=project_id,
                event_type="UAT_SESSION_CREATED",
                actor_id=actor_id,
                event_data={"uat_session_id": session_obj.id, "title": title},
            )
        )
        return session_obj

    async def submit_uat_feedback(
        self,
        uat_session_id: str,
        comments: str,
        submitted_by: str,
        deliverable_id: Optional[str] = None,
        feedback_type: str = "COMMENT",
        rating: Optional[int] = None,
        create_defect_if_issue: bool = False,
    ) -> UATFeedback:
        session_obj = await self.repo.get_uat_session(uat_session_id)
        if not session_obj:
            raise ValueError(f"UAT Session '{uat_session_id}' not found.")

        defect_id = None
        if create_defect_if_issue or feedback_type == "ISSUE":
            defect = await self.create_defect(
                project_id=session_obj.project_id,
                title=f"UAT Issue: {comments[:50]}",
                description=comments,
                reported_by=submitted_by,
                deliverable_id=deliverable_id,
            )
            defect_id = defect.id

        fb = UATFeedback(
            id=str(uuid.uuid4()),
            uat_session_id=uat_session_id,
            deliverable_id=deliverable_id,
            feedback_type=feedback_type,
            comments=comments,
            rating=rating,
            submitted_by=submitted_by,
            defect_id=defect_id,
        )
        fb = await self.repo.add_uat_feedback(fb)
        return fb

    async def signoff_uat_session(
        self,
        uat_session_id: str,
        client_signer_id: str,
        signoff_statement: str,
    ) -> UATSession:
        session_obj = await self.repo.get_uat_session(uat_session_id)
        if not session_obj:
            raise ValueError(f"UAT Session '{uat_session_id}' not found.")

        session_obj.approved_by_client = True
        session_obj.status = "APPROVED"
        session_obj.client_signoff_at = datetime.now(timezone.utc)
        session_obj = await self.repo.update_uat_session(session_obj)

        signoff_hash = hashlib.sha256(f"{uat_session_id}:{client_signer_id}:{signoff_statement}".encode("utf-8")).hexdigest()

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=session_obj.project_id,
                event_type="UAT_CLIENT_APPROVED",
                actor_id=client_signer_id,
                event_data={"signoff_hash": signoff_hash, "statement": signoff_statement},
            )
        )
        return session_obj

    # --- Release Gate & Packaging ---
    async def create_release_version(
        self,
        project_id: str,
        version_tag: str,
        target_environment: str = "PRODUCTION",
        release_notes: Optional[str] = None,
        actor_id: str = "SYSTEM",
    ) -> ReleaseVersion:
        release = ReleaseVersion(
            id=str(uuid.uuid4()),
            project_id=project_id,
            version_tag=version_tag,
            target_environment=target_environment,
            status="DRAFT",
            release_notes=release_notes,
            qa_approval_status="PENDING",
            client_approval_status="PENDING",
        )
        release = await self.repo.create_release_version(release)

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=project_id,
                event_type="RELEASE_CREATED",
                actor_id=actor_id,
                event_data={"release_id": release.id, "version_tag": version_tag},
            )
        )
        return release

    async def evaluate_release_gate(self, release_id: str, actor_id: str = "SYSTEM") -> Dict[str, Any]:
        release = await self.repo.get_release_version(release_id)
        if not release:
            raise ValueError(f"Release '{release_id}' not found.")

        test_runs = await self.repo.list_test_runs(release.project_id)
        total_tests = sum(tr.passed_count + tr.failed_count + tr.blocked_count + tr.skipped_count for tr in test_runs)
        passed_tests = sum(tr.passed_count for tr in test_runs)
        failed_tests = sum(tr.failed_count for tr in test_runs)

        defects = await self.repo.list_defects(release.project_id)
        open_crit = sum(1 for d in defects if d.status not in ["CLOSED", "VERIFIED"] and d.severity == "CRITICAL")
        open_high = sum(1 for d in defects if d.status not in ["CLOSED", "VERIFIED"] and d.severity == "HIGH")

        uat_sessions = await self.repo.list_uat_sessions(release.project_id)
        uat_approved = any(u.approved_by_client for u in uat_sessions)

        evaluation = self.readiness_evaluator.evaluate_readiness(
            project_id=release.project_id,
            version_tag=release.version_tag,
            total_test_count=total_tests,
            passed_test_count=passed_tests,
            failed_test_count=failed_tests,
            open_critical_defects=open_crit,
            open_high_defects=open_high,
            uat_approved=uat_approved,
        )

        if evaluation.is_ready_for_release:
            release.qa_approval_status = "APPROVED"
            release.status = "READY"
        else:
            release.qa_approval_status = "REJECTED"
            release.status = "BLOCKED"

        await self.repo.update_release_version(release)

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=release.project_id,
                event_type="RELEASE_EVALUATED",
                actor_id=actor_id,
                event_data={
                    "readiness_score": evaluation.readiness_score,
                    "is_ready": evaluation.is_ready_for_release,
                    "blocking_conditions": evaluation.blocking_conditions,
                },
            )
        )

        return {
            "release": release,
            "evaluation": evaluation,
        }

    async def add_delivery_package(
        self,
        project_id: str,
        package_name: str,
        storage_url: str,
        file_size_bytes: int,
        release_version_id: Optional[str] = None,
    ) -> DeliveryPackage:
        hash_source = f"{package_name}:{storage_url}:{file_size_bytes}"
        sha256_hash = hashlib.sha256(hash_source.encode("utf-8")).hexdigest()

        pkg = DeliveryPackage(
            id=str(uuid.uuid4()),
            project_id=project_id,
            release_version_id=release_version_id,
            package_name=package_name,
            storage_url=storage_url,
            sha256_hash=sha256_hash,
            file_size_bytes=file_size_bytes,
        )
        pkg = await self.repo.create_delivery_package(pkg)
        return pkg

    # --- Handover & Project Closure ---
    async def complete_handover_and_close_project(
        self,
        project_id: str,
        client_signer_id: str,
        signoff_statement: str,
    ) -> Dict[str, Any]:
        checklist = await self.repo.get_or_create_handover_checklist(project_id, title="Final Project Handover")

        # Compute SHA-256 Sign-off Hash
        hash_payload = f"{project_id}:{client_signer_id}:{signoff_statement}"
        signoff_hash = hashlib.sha256(hash_payload.encode("utf-8")).hexdigest()

        checklist.code_repository_transferred = True
        checklist.documentation_delivered = True
        checklist.credentials_transferred = True
        checklist.training_completed = True
        checklist.deployment_verified = True
        checklist.signed_off_by_client = True
        checklist.client_signoff_hash = signoff_hash
        checklist.signed_off_at = datetime.now(timezone.utc)
        checklist.status = "COMPLETED"

        checklist = await self.repo.update_handover_checklist(checklist)

        # Transition Project Status to COMPLETED
        project = await self.project_repo.get_by_id(project_id)
        if project:
            project.status = "COMPLETED"
            await self.session.commit()

        await self.repo.record_event(
            QAEvent(
                id=str(uuid.uuid4()),
                project_id=project_id,
                event_type="HANDOVER_COMPLETED",
                actor_id=client_signer_id,
                event_data={
                    "signoff_hash": signoff_hash,
                    "statement": signoff_statement,
                    "project_status": "COMPLETED",
                },
            )
        )

        return {
            "handover_checklist": checklist,
            "project_status": "COMPLETED",
            "sha256_signoff_hash": signoff_hash,
        }
