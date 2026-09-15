"""Repository layer for Phase 31: Business Intelligence, Portfolio Analytics & Organizational Learning."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy import func, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.analytics import (
    AnalyticsAggregation,
    AnalyticsDimension,
    AnalyticsFact,
    AnalyticsMetric,
    AnalyticsMetricVersion,
    AnalyticsQueryRun,
    AnalyticsReport,
    AnalyticsSnapshot,
    BusinessInsight,
    BusinessInsightEvidence,
    BusinessRecommendation,
    DataQualityCheck,
    DataQualityResult,
    Experiment,
    ExperimentMetric,
    ExperimentResult,
    ModelEvaluation,
    ModelPrediction,
    ModelRegistry,
    RecommendationReview,
    InsightStatus,
    RecommendationStatus,
    ExperimentStatus,
    ModelStatus,
    DataQualityStatus,
)


class AnalyticsRepository:
    """Database persistence and aggregation queries for the BI & Organizational Learning subsystem."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # =========================================================================
    # 1. Metrics Registry
    # =========================================================================

    async def create_metric(self, metric: AnalyticsMetric) -> AnalyticsMetric:
        self.session.add(metric)
        await self.session.commit()
        await self.session.refresh(metric)
        return metric

    async def get_metric(self, metric_id: str) -> Optional[AnalyticsMetric]:
        stmt = (
            select(AnalyticsMetric)
            .where(AnalyticsMetric.id == metric_id)
            .options(selectinload(AnalyticsMetric.versions))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_metric_by_key(self, metric_key: str) -> Optional[AnalyticsMetric]:
        stmt = (
            select(AnalyticsMetric)
            .where(AnalyticsMetric.metric_key == metric_key)
            .options(selectinload(AnalyticsMetric.versions))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_metrics(
        self,
        tenant_id: str,
        category: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[AnalyticsMetric]:
        stmt = select(AnalyticsMetric).where(AnalyticsMetric.tenant_id == tenant_id)
        if category:
            stmt = stmt.where(AnalyticsMetric.category == category)
        if status:
            stmt = stmt.where(AnalyticsMetric.status == status)
        stmt = stmt.order_by(AnalyticsMetric.metric_key)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_metric_version(self, version: AnalyticsMetricVersion) -> AnalyticsMetricVersion:
        self.session.add(version)
        await self.session.commit()
        await self.session.refresh(version)
        return version

    # =========================================================================
    # 2. Facts, Snapshots & Aggregations
    # =========================================================================

    async def record_fact(self, fact: AnalyticsFact) -> AnalyticsFact:
        self.session.add(fact)
        await self.session.commit()
        await self.session.refresh(fact)
        return fact

    async def record_snapshot(self, snapshot: AnalyticsSnapshot) -> AnalyticsSnapshot:
        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)
        return snapshot

    async def get_latest_snapshot(self, tenant_id: str, snapshot_type: str) -> Optional[AnalyticsSnapshot]:
        stmt = (
            select(AnalyticsSnapshot)
            .where(
                AnalyticsSnapshot.tenant_id == tenant_id,
                AnalyticsSnapshot.snapshot_type == snapshot_type,
            )
            .order_by(desc(AnalyticsSnapshot.created_at))
            .limit(1)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # =========================================================================
    # 3. Insights & Evidence
    # =========================================================================

    async def create_insight(self, insight: BusinessInsight) -> BusinessInsight:
        self.session.add(insight)
        await self.session.commit()
        await self.session.refresh(insight)
        return insight

    async def get_insight(self, insight_id: str) -> Optional[BusinessInsight]:
        stmt = (
            select(BusinessInsight)
            .where(BusinessInsight.id == insight_id)
            .options(
                selectinload(BusinessInsight.evidence_items),
                selectinload(BusinessInsight.recommendations),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_insights(
        self,
        tenant_id: str,
        category: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[BusinessInsight]:
        stmt = select(BusinessInsight).where(BusinessInsight.tenant_id == tenant_id)
        if category:
            stmt = stmt.where(BusinessInsight.category == category)
        if status:
            stmt = stmt.where(BusinessInsight.status == status)
        stmt = (
            stmt.options(selectinload(BusinessInsight.evidence_items))
            .order_by(desc(BusinessInsight.created_at))
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update_insight_status(
        self,
        insight_id: str,
        status: InsightStatus,
        reviewed_by: Optional[str] = None,
    ) -> Optional[BusinessInsight]:
        insight = await self.get_insight(insight_id)
        if not insight:
            return None
        insight.status = status
        if reviewed_by:
            insight.reviewed_by = reviewed_by
            insight.reviewed_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(insight)
        return insight

    # =========================================================================
    # 4. Recommendations & Reviews
    # =========================================================================

    async def create_recommendation(self, rec: BusinessRecommendation) -> BusinessRecommendation:
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def get_recommendation(self, rec_id: str) -> Optional[BusinessRecommendation]:
        stmt = (
            select(BusinessRecommendation)
            .where(BusinessRecommendation.id == rec_id)
            .options(
                selectinload(BusinessRecommendation.reviews),
                selectinload(BusinessRecommendation.insight),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_recommendations(
        self,
        tenant_id: str,
        status: Optional[str] = None,
        workflow: Optional[str] = None,
        limit: int = 50,
    ) -> List[BusinessRecommendation]:
        stmt = select(BusinessRecommendation).where(BusinessRecommendation.tenant_id == tenant_id)
        if status:
            stmt = stmt.where(BusinessRecommendation.status == status)
        if workflow:
            stmt = stmt.where(BusinessRecommendation.affected_workflow == workflow)
        stmt = stmt.order_by(desc(BusinessRecommendation.created_at)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def review_recommendation(
        self,
        rec_id: str,
        reviewer: str,
        action: str,  # APPROVE, REJECT, IMPLEMENT
        notes: Optional[str] = None,
        policy_impact: Optional[Dict[str, Any]] = None,
    ) -> Optional[BusinessRecommendation]:
        rec = await self.get_recommendation(rec_id)
        if not rec:
            return None

        status_map = {
            "APPROVE": RecommendationStatus.APPROVED,
            "REJECT": RecommendationStatus.REJECTED,
            "IMPLEMENT": RecommendationStatus.IMPLEMENTED,
        }
        rec.status = status_map.get(action.upper(), rec.status)
        rec.reviewed_by = reviewer
        rec.reviewed_at = datetime.utcnow()
        rec.decision_reason = notes

        review = RecommendationReview(
            tenant_id=rec.tenant_id,
            recommendation_id=rec.id,
            reviewer=reviewer,
            action=action.upper(),
            notes=notes,
            policy_impact=policy_impact or {},
        )
        self.session.add(review)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    # =========================================================================
    # 5. Experiments & Results
    # =========================================================================

    async def create_experiment(self, exp: Experiment) -> Experiment:
        self.session.add(exp)
        await self.session.commit()
        await self.session.refresh(exp)
        return exp

    async def get_experiment(self, exp_id: str) -> Optional[Experiment]:
        stmt = (
            select(Experiment)
            .where(Experiment.id == exp_id)
            .options(
                selectinload(Experiment.metrics),
                selectinload(Experiment.results),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_experiments(
        self,
        tenant_id: str,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[Experiment]:
        stmt = select(Experiment).where(Experiment.tenant_id == tenant_id)
        if status:
            stmt = stmt.where(Experiment.status == status)
        stmt = (
            stmt.options(
                selectinload(Experiment.metrics),
                selectinload(Experiment.results),
            )
            .order_by(desc(Experiment.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def record_experiment_result(self, result: ExperimentResult) -> ExperimentResult:
        self.session.add(result)
        # Increment sample count on parent experiment
        exp = await self.get_experiment(result.experiment_id)
        if exp:
            exp.current_sample_count += 1
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def update_experiment_status(
        self,
        exp_id: str,
        status: ExperimentStatus,
        conclusion: Optional[str] = None,
    ) -> Optional[Experiment]:
        exp = await self.get_experiment(exp_id)
        if not exp:
            return None
        exp.status = status
        if status == ExperimentStatus.ACTIVE and not exp.started_at:
            exp.started_at = datetime.utcnow()
        elif status in (ExperimentStatus.COMPLETED, ExperimentStatus.EVALUATED):
            exp.completed_at = datetime.utcnow()
        if conclusion:
            exp.conclusion = conclusion
        await self.session.commit()
        await self.session.refresh(exp)
        return exp

    # =========================================================================
    # 6. Model Registry & Evaluations
    # =========================================================================

    async def register_model(self, model: ModelRegistry) -> ModelRegistry:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_model(self, model_id: str) -> Optional[ModelRegistry]:
        stmt = (
            select(ModelRegistry)
            .where(ModelRegistry.id == model_id)
            .options(
                selectinload(ModelRegistry.evaluations),
                selectinload(ModelRegistry.predictions),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_model_by_key(self, model_key: str) -> Optional[ModelRegistry]:
        stmt = (
            select(ModelRegistry)
            .where(ModelRegistry.model_key == model_key)
            .options(
                selectinload(ModelRegistry.evaluations),
                selectinload(ModelRegistry.predictions),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_models(self, tenant_id: str) -> List[ModelRegistry]:
        stmt = select(ModelRegistry).where(ModelRegistry.tenant_id == tenant_id).order_by(ModelRegistry.model_key)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def approve_model(self, model_id: str, approved_by: str) -> Optional[ModelRegistry]:
        model = await self.get_model(model_id)
        if not model:
            return None
        model.status = ModelStatus.APPROVED
        model.approved_by = approved_by
        model.approved_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def record_prediction(self, prediction: ModelPrediction) -> ModelPrediction:
        self.session.add(prediction)
        await self.session.commit()
        await self.session.refresh(prediction)
        return prediction

    # =========================================================================
    # 7. Data Quality Checks & Query Runs
    # =========================================================================

    async def record_data_quality_check(self, check: DataQualityCheck) -> DataQualityCheck:
        self.session.add(check)
        await self.session.commit()
        await self.session.refresh(check)
        return check

    async def get_data_quality_overview(self, tenant_id: str) -> List[DataQualityCheck]:
        stmt = select(DataQualityCheck).where(DataQualityCheck.tenant_id == tenant_id).order_by(DataQualityCheck.check_name)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def log_query_run(self, query_run: AnalyticsQueryRun) -> AnalyticsQueryRun:
        self.session.add(query_run)
        await self.session.commit()
        await self.session.refresh(query_run)
        return query_run

    async def create_report(self, report: AnalyticsReport) -> AnalyticsReport:
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def list_reports(self, tenant_id: str, limit: int = 20) -> List[AnalyticsReport]:
        stmt = select(AnalyticsReport).where(AnalyticsReport.tenant_id == tenant_id).order_by(desc(AnalyticsReport.created_at)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
