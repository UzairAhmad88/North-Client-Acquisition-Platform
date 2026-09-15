"""Repository layer for Phase 29 — Quality Assurance, UAT, Delivery Acceptance & Handover System."""

from typing import Any, Dict, List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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


class QARepository:
    """Database persistence operations for QA Test Plans, Test Cases, Runs, Results, Defects, UAT, Releases, Handover, and Events."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # --- Test Plan & Cases ---
    async def create_test_plan(self, test_plan: TestPlan) -> TestPlan:
        self.session.add(test_plan)
        await self.session.commit()
        await self.session.refresh(test_plan)
        return test_plan

    async def get_test_plan(self, plan_id: str) -> Optional[TestPlan]:
        stmt = select(TestPlan).where(TestPlan.id == plan_id).options(selectinload(TestPlan.test_cases))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_test_plans(self, project_id: str) -> List[TestPlan]:
        stmt = (
            select(TestPlan)
            .where(TestPlan.project_id == project_id)
            .options(selectinload(TestPlan.test_cases))
            .order_by(TestPlan.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_test_case(self, test_case: TestCase) -> TestCase:
        self.session.add(test_case)
        await self.session.commit()
        await self.session.refresh(test_case)
        return test_case

    async def get_test_case(self, case_id: str) -> Optional[TestCase]:
        stmt = select(TestCase).where(TestCase.id == case_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_test_cases(self, plan_id: str) -> List[TestCase]:
        stmt = select(TestCase).where(TestCase.test_plan_id == plan_id).order_by(TestCase.code.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Test Runs & Results ---
    async def create_test_run(self, test_run: TestRun) -> TestRun:
        self.session.add(test_run)
        await self.session.commit()
        await self.session.refresh(test_run)
        return test_run

    async def get_test_run(self, run_id: str) -> Optional[TestRun]:
        stmt = (
            select(TestRun)
            .where(TestRun.id == run_id)
            .options(selectinload(TestRun.results).selectinload(TestResult.evidence))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_test_runs(self, project_id: str) -> List[TestRun]:
        stmt = select(TestRun).where(TestRun.project_id == project_id).order_by(TestRun.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def add_test_result(self, result: TestResult) -> TestResult:
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def add_test_evidence(self, evidence: TestEvidence) -> TestEvidence:
        self.session.add(evidence)
        await self.session.commit()
        return evidence

    async def update_test_run(self, test_run: TestRun) -> TestRun:
        await self.session.commit()
        await self.session.refresh(test_run)
        return test_run

    # --- Defects ---
    async def create_defect(self, defect: Defect) -> Defect:
        self.session.add(defect)
        await self.session.commit()
        await self.session.refresh(defect)
        return defect

    async def get_defect(self, defect_id: str) -> Optional[Defect]:
        stmt = select(Defect).where(Defect.id == defect_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_defects(self, project_id: str) -> List[Defect]:
        stmt = select(Defect).where(Defect.project_id == project_id).order_by(Defect.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def generate_next_defect_number(self, project_id: str) -> str:
        stmt = select(func.count(Defect.id)).where(Defect.project_id == project_id)
        res = await self.session.execute(stmt)
        count = res.scalar() or 0
        return f"DEF-{(count + 1):04d}"

    async def update_defect(self, defect: Defect) -> Defect:
        await self.session.commit()
        await self.session.refresh(defect)
        return defect

    # --- UAT & Acceptance ---
    async def create_uat_session(self, session_obj: UATSession) -> UATSession:
        self.session.add(session_obj)
        await self.session.commit()
        await self.session.refresh(session_obj)
        return session_obj

    async def get_uat_session(self, session_id: str) -> Optional[UATSession]:
        stmt = (
            select(UATSession)
            .where(UATSession.id == session_id)
            .options(selectinload(UATSession.feedbacks))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_uat_sessions(self, project_id: str) -> List[UATSession]:
        stmt = select(UATSession).where(UATSession.project_id == project_id).order_by(UATSession.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def add_uat_feedback(self, feedback: UATFeedback) -> UATFeedback:
        self.session.add(feedback)
        await self.session.commit()
        await self.session.refresh(feedback)
        return feedback

    async def update_uat_session(self, session_obj: UATSession) -> UATSession:
        await self.session.commit()
        await self.session.refresh(session_obj)
        return session_obj

    async def create_acceptance_criteria(self, criteria: AcceptanceCriteria) -> AcceptanceCriteria:
        self.session.add(criteria)
        await self.session.commit()
        await self.session.refresh(criteria)
        return criteria

    async def list_acceptance_criteria(self, project_id: str) -> List[AcceptanceCriteria]:
        stmt = select(AcceptanceCriteria).where(AcceptanceCriteria.project_id == project_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Release & Delivery Packages ---
    async def create_release_version(self, release: ReleaseVersion) -> ReleaseVersion:
        self.session.add(release)
        await self.session.commit()
        await self.session.refresh(release)
        return release

    async def get_release_version(self, release_id: str) -> Optional[ReleaseVersion]:
        stmt = select(ReleaseVersion).where(ReleaseVersion.id == release_id).options(selectinload(ReleaseVersion.packages))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_release_versions(self, project_id: str) -> List[ReleaseVersion]:
        stmt = select(ReleaseVersion).where(ReleaseVersion.project_id == project_id).order_by(ReleaseVersion.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_delivery_package(self, package: DeliveryPackage) -> DeliveryPackage:
        self.session.add(package)
        await self.session.commit()
        await self.session.refresh(package)
        return package

    async def update_release_version(self, release: ReleaseVersion) -> ReleaseVersion:
        await self.session.commit()
        await self.session.refresh(release)
        return release

    # --- Handover Checklist ---
    async def get_or_create_handover_checklist(self, project_id: str, title: str) -> HandoverChecklist:
        stmt = select(HandoverChecklist).where(HandoverChecklist.project_id == project_id)
        res = await self.session.execute(stmt)
        checklist = res.scalar_one_or_none()

        if not checklist:
            checklist = HandoverChecklist(
                project_id=project_id,
                title=title,
                status="IN_PROGRESS",
            )
            self.session.add(checklist)
            await self.session.commit()
            await self.session.refresh(checklist)

        return checklist

    async def update_handover_checklist(self, checklist: HandoverChecklist) -> HandoverChecklist:
        await self.session.commit()
        await self.session.refresh(checklist)
        return checklist

    # --- QA Events ---
    async def record_event(self, event: QAEvent) -> QAEvent:
        self.session.add(event)
        await self.session.commit()
        return event

    async def list_events(self, project_id: str) -> List[QAEvent]:
        stmt = select(QAEvent).where(QAEvent.project_id == project_id).order_by(QAEvent.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
