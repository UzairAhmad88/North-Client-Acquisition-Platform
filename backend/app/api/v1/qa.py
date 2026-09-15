"""REST API router for Phase 29 — Quality Assurance, UAT, Delivery Acceptance & Handover System."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.qa import (
    DefectCreateSchema,
    DefectResponseSchema,
    DefectStatusUpdateSchema,
    DeliveryPackageCreateSchema,
    HandoverSignoffSchema,
    ReleaseVersionCreateSchema,
    ReleaseVersionResponseSchema,
    TestCaseCreateSchema,
    TestCaseResponseSchema,
    TestPlanCreateSchema,
    TestPlanResponseSchema,
    TestResultRecordSchema,
    TestRunCreateSchema,
    TestRunResponseSchema,
    UATFeedbackCreateSchema,
    UATSessionCreateSchema,
    UATSessionResponseSchema,
    UATSignoffSchema,
)
from app.services.qa import QAService

router = APIRouter()


# --- Test Plans & Test Cases ---
@router.get("/projects/{project_id}/test-plans", response_model=List[TestPlanResponseSchema])
async def list_test_plans(project_id: str, db: AsyncSession = Depends(get_db)):
    """List test plans for a project."""
    service = QAService(db)
    plans = await service.repo.list_test_plans(project_id)
    return [TestPlanResponseSchema.model_validate(p) for p in plans]


@router.post("/projects/{project_id}/test-plans", response_model=TestPlanResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_test_plan(project_id: str, payload: TestPlanCreateSchema, db: AsyncSession = Depends(get_db)):
    """Create a new QA test plan."""
    service = QAService(db)
    try:
        plan = await service.create_test_plan(
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            plan_type=payload.plan_type,
        )
        loaded = await service.repo.get_test_plan(plan.id)
        return TestPlanResponseSchema.model_validate(loaded)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test-plans/{test_plan_id}/generate-cases", response_model=List[TestCaseResponseSchema])
async def generate_ai_test_cases(test_plan_id: str, db: AsyncSession = Depends(get_db)):
    """Generate structured test cases automatically using QAAgent test generator."""
    service = QAService(db)
    try:
        cases = await service.generate_ai_test_cases(test_plan_id=test_plan_id)
        return [TestCaseResponseSchema.model_validate(c) for c in cases]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Test Runs & Execution ---
@router.get("/projects/{project_id}/test-runs", response_model=List[TestRunResponseSchema])
async def list_test_runs(project_id: str, db: AsyncSession = Depends(get_db)):
    """List test runs for a project."""
    service = QAService(db)
    runs = await service.repo.list_test_runs(project_id)
    return [TestRunResponseSchema.model_validate(r) for r in runs]


@router.post("/projects/{project_id}/test-runs", response_model=TestRunResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_test_run(project_id: str, payload: TestRunCreateSchema, db: AsyncSession = Depends(get_db)):
    """Start a new test execution run."""
    service = QAService(db)
    try:
        run = await service.create_test_run(
            project_id=project_id,
            test_plan_id=payload.test_plan_id,
            name=payload.name,
            environment=payload.environment,
        )
        return TestRunResponseSchema.model_validate(run)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test-runs/{test_run_id}/results")
async def record_test_result(test_run_id: str, payload: TestResultRecordSchema, db: AsyncSession = Depends(get_db)):
    """Record execution result for a test case."""
    service = QAService(db)
    try:
        res = await service.record_test_result(
            test_run_id=test_run_id,
            test_case_id=payload.test_case_id,
            status=payload.status,
            actual_results=payload.actual_results,
            execution_notes=payload.execution_notes,
            evidence_files=payload.evidence_files,
        )
        return {"result_id": res.id, "status": res.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Defects ---
@router.get("/projects/{project_id}/defects", response_model=List[DefectResponseSchema])
async def list_defects(project_id: str, db: AsyncSession = Depends(get_db)):
    """List defect reports for a project."""
    service = QAService(db)
    defects = await service.repo.list_defects(project_id)
    return [DefectResponseSchema.model_validate(d) for d in defects]


@router.post("/projects/{project_id}/defects", response_model=DefectResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_defect(project_id: str, payload: DefectCreateSchema, db: AsyncSession = Depends(get_db)):
    """Report a new defect with AI classification & severity evaluation."""
    service = QAService(db)
    try:
        defect = await service.create_defect(
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            reported_by=payload.reported_by,
            test_case_id=payload.test_case_id,
            test_run_id=payload.test_run_id,
            deliverable_id=payload.deliverable_id,
            requirement_id=payload.requirement_id,
            is_against_spec=payload.is_against_spec,
        )
        return DefectResponseSchema.model_validate(defect)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/defects/{defect_id}/status", response_model=DefectResponseSchema)
async def update_defect_status(
    defect_id: str,
    payload: DefectStatusUpdateSchema,
    actor_id: str = Query(default="QA Lead"),
    db: AsyncSession = Depends(get_db),
):
    """Update defect status (resolution, closure, verification)."""
    service = QAService(db)
    try:
        defect = await service.update_defect_status(
            defect_id=defect_id,
            status=payload.status,
            actor_id=actor_id,
            resolution_summary=payload.resolution_summary,
        )
        return DefectResponseSchema.model_validate(defect)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Client UAT & Sign-off ---
@router.get("/projects/{project_id}/uat-sessions", response_model=List[UATSessionResponseSchema])
async def list_uat_sessions(project_id: str, db: AsyncSession = Depends(get_db)):
    """List client UAT sessions for a project."""
    service = QAService(db)
    sessions = await service.repo.list_uat_sessions(project_id)
    return [UATSessionResponseSchema.model_validate(s) for s in sessions]


@router.post("/projects/{project_id}/uat-sessions", response_model=UATSessionResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_uat_session(project_id: str, payload: UATSessionCreateSchema, db: AsyncSession = Depends(get_db)):
    """Initiate a formal client UAT session."""
    service = QAService(db)
    try:
        session_obj = await service.create_uat_session(
            project_id=project_id,
            client_account_id=payload.client_account_id,
            title=payload.title,
            scope_description=payload.scope_description,
        )
        return UATSessionResponseSchema.model_validate(session_obj)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/uat-sessions/{uat_session_id}/feedback")
async def submit_uat_feedback(uat_session_id: str, payload: UATFeedbackCreateSchema, submitted_by: str = Query(default="Client Stakeholder"), db: AsyncSession = Depends(get_db)):
    """Submit client feedback or report issue during UAT session."""
    service = QAService(db)
    try:
        fb = await service.submit_uat_feedback(
            uat_session_id=uat_session_id,
            comments=payload.comments,
            submitted_by=submitted_by,
            deliverable_id=payload.deliverable_id,
            feedback_type=payload.feedback_type,
            rating=payload.rating,
            create_defect_if_issue=payload.create_defect_if_issue,
        )
        return {"feedback_id": fb.id, "defect_id": fb.defect_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/uat-sessions/{uat_session_id}/signoff", response_model=UATSessionResponseSchema)
async def signoff_uat_session(uat_session_id: str, payload: UATSignoffSchema, db: AsyncSession = Depends(get_db)):
    """Submit formal client UAT sign-off with SHA-256 hash."""
    service = QAService(db)
    try:
        session_obj = await service.signoff_uat_session(
            uat_session_id=uat_session_id,
            client_signer_id=payload.client_signer_id,
            signoff_statement=payload.signoff_statement,
        )
        return UATSessionResponseSchema.model_validate(session_obj)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Release Gates & Delivery Packages ---
@router.get("/projects/{project_id}/releases", response_model=List[ReleaseVersionResponseSchema])
async def list_release_versions(project_id: str, db: AsyncSession = Depends(get_db)):
    """List release versions for a project."""
    service = QAService(db)
    releases = await service.repo.list_release_versions(project_id)
    return [ReleaseVersionResponseSchema.model_validate(r) for r in releases]


@router.post("/projects/{project_id}/releases", response_model=ReleaseVersionResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_release_version(project_id: str, payload: ReleaseVersionCreateSchema, db: AsyncSession = Depends(get_db)):
    """Draft a new release version."""
    service = QAService(db)
    try:
        rel = await service.create_release_version(
            project_id=project_id,
            version_tag=payload.version_tag,
            target_environment=payload.target_environment,
            release_notes=payload.release_notes,
        )
        return ReleaseVersionResponseSchema.model_validate(rel)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/releases/{release_id}/evaluate-gate")
async def evaluate_release_gate(release_id: str, db: AsyncSession = Depends(get_db)):
    """Evaluate release readiness score and enforce quality gate conditions."""
    service = QAService(db)
    try:
        res = await service.evaluate_release_gate(release_id)
        rel = res["release"]
        eval_res = res["evaluation"]
        return {
            "release_id": rel.id,
            "version_tag": rel.version_tag,
            "status": rel.status,
            "qa_approval_status": rel.qa_approval_status,
            "readiness_score": eval_res.readiness_score,
            "is_ready_for_release": eval_res.is_ready_for_release,
            "blocking_conditions": eval_res.blocking_conditions,
            "recommendations": eval_res.recommendations,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/delivery-packages")
async def add_delivery_package(project_id: str, payload: DeliveryPackageCreateSchema, db: AsyncSession = Depends(get_db)):
    """Register a final delivery package artifact with SHA-256 hash."""
    service = QAService(db)
    try:
        pkg = await service.add_delivery_package(
            project_id=project_id,
            package_name=payload.package_name,
            storage_url=payload.storage_url,
            file_size_bytes=payload.file_size_bytes,
            release_version_id=payload.release_version_id,
        )
        return {
            "package_id": pkg.id,
            "package_name": pkg.package_name,
            "sha256_hash": pkg.sha256_hash,
            "file_size_bytes": pkg.file_size_bytes,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Handover & Final Project Acceptance ---
@router.get("/projects/{project_id}/handover")
async def get_handover_checklist(project_id: str, db: AsyncSession = Depends(get_db)):
    """Get project handover checklist state."""
    service = QAService(db)
    checklist = await service.repo.get_or_create_handover_checklist(project_id, title="Final Project Handover")
    return {
        "id": checklist.id,
        "project_id": checklist.project_id,
        "title": checklist.title,
        "code_repository_transferred": checklist.code_repository_transferred,
        "documentation_delivered": checklist.documentation_delivered,
        "credentials_transferred": checklist.credentials_transferred,
        "training_completed": checklist.training_completed,
        "deployment_verified": checklist.deployment_verified,
        "status": checklist.status,
        "signed_off_by_client": checklist.signed_off_by_client,
        "client_signoff_hash": checklist.client_signoff_hash,
        "signed_off_at": checklist.signed_off_at,
    }


@router.post("/projects/{project_id}/handover/complete")
async def complete_handover_and_close(project_id: str, payload: HandoverSignoffSchema, db: AsyncSession = Depends(get_db)):
    """Complete final project handover and transition project status to COMPLETED."""
    service = QAService(db)
    try:
        res = await service.complete_handover_and_close_project(
            project_id=project_id,
            client_signer_id=payload.client_signer_id,
            signoff_statement=payload.signoff_statement,
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
