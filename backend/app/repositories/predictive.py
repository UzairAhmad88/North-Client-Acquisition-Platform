"""Repository layer for Phase 32: Advanced AI/ML Decision Intelligence & Predictive Operations."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy import func, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.predictive import (
    DecisionOverride,
    DecisionPolicy,
    DecisionPolicyVersion,
    DecisionReview,
    DecisionSupportRecord,
    DecisionState,
    FeatureDefinition,
    FeatureValue,
    FeatureVersion,
    ForecastRun,
    ModelDeployment,
    ModelDriftEvent,
    ModelLifecycleStatus,
    PredictionExplanation,
    PredictionModel,
    PredictionOutcome,
    PredictionRecord,
    PredictionType,
    RiskBand,
    TrainingDataset,
    TrainingRun,
)


class PredictiveRepository:
    """Database persistence and query operations for predictive inference, model governance, and decision support."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # =========================================================================
    # 1. Feature Store & Feature Registry
    # =========================================================================

    async def create_feature(self, feature: FeatureDefinition) -> FeatureDefinition:
        self.session.add(feature)
        await self.session.commit()
        await self.session.refresh(feature)
        return feature

    async def list_features(self, tenant_id: str) -> List[FeatureDefinition]:
        stmt = (
            select(FeatureDefinition)
            .where(FeatureDefinition.tenant_id == tenant_id)
            .options(selectinload(FeatureDefinition.versions))
            .order_by(FeatureDefinition.feature_key)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # =========================================================================
    # 2. Model Registry & Deployments
    # =========================================================================

    async def register_model(self, model: PredictionModel) -> PredictionModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_model(self, model_id: str) -> Optional[PredictionModel]:
        stmt = (
            select(PredictionModel)
            .where(PredictionModel.id == model_id)
            .options(selectinload(PredictionModel.deployments))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_model_by_key(self, model_key: str) -> Optional[PredictionModel]:
        stmt = (
            select(PredictionModel)
            .where(PredictionModel.model_key == model_key)
            .options(selectinload(PredictionModel.deployments))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_models(
        self,
        tenant_id: str,
        prediction_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[PredictionModel]:
        stmt = select(PredictionModel).where(PredictionModel.tenant_id == tenant_id)
        if prediction_type:
            stmt = stmt.where(PredictionModel.prediction_type == prediction_type)
        if status:
            stmt = stmt.where(PredictionModel.status == status)
        stmt = stmt.order_by(PredictionModel.model_key)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def approve_model(self, model_id: str, approved_by: str) -> Optional[PredictionModel]:
        model = await self.get_model(model_id)
        if not model:
            return None
        model.status = ModelLifecycleStatus.APPROVED
        model.approved_by = approved_by
        model.approved_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def deploy_model(self, model_id: str, deployed_by: str, mode: str = "PRODUCTION") -> Optional[ModelDeployment]:
        model = await self.get_model(model_id)
        if not model:
            return None
        model.status = ModelLifecycleStatus.PRODUCTION
        deployment = ModelDeployment(
            tenant_id=model.tenant_id,
            model_id=model.id,
            version=model.current_version,
            deployed_by=deployed_by,
            deployment_mode=mode,
        )
        self.session.add(deployment)
        await self.session.commit()
        await self.session.refresh(deployment)
        return deployment

    # =========================================================================
    # 3. Predictions, Explanations & Outcomes
    # =========================================================================

    async def create_prediction(
        self,
        prediction: PredictionRecord,
        explanation: Optional[PredictionExplanation] = None,
    ) -> PredictionRecord:
        self.session.add(prediction)
        await self.session.flush()
        if explanation:
            explanation.prediction_id = prediction.id
            self.session.add(explanation)
        await self.session.commit()
        await self.session.refresh(prediction)
        return prediction

    async def get_prediction(self, prediction_id: str) -> Optional[PredictionRecord]:
        stmt = (
            select(PredictionRecord)
            .where(PredictionRecord.id == prediction_id)
            .options(
                selectinload(PredictionRecord.explanation),
                selectinload(PredictionRecord.outcome),
                selectinload(PredictionRecord.decision_support),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_predictions(
        self,
        tenant_id: str,
        prediction_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        risk_band: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[PredictionRecord]:
        stmt = select(PredictionRecord).where(PredictionRecord.tenant_id == tenant_id)
        if prediction_type:
            stmt = stmt.where(PredictionRecord.prediction_type == prediction_type)
        if entity_id:
            stmt = stmt.where(PredictionRecord.entity_id == entity_id)
        if risk_band:
            stmt = stmt.where(PredictionRecord.risk_band == risk_band)
        stmt = (
            stmt.options(
                selectinload(PredictionRecord.explanation),
                selectinload(PredictionRecord.outcome),
                selectinload(PredictionRecord.decision_support),
            )
            .order_by(desc(PredictionRecord.inference_timestamp))
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def record_prediction_outcome(
        self,
        prediction_id: str,
        actual_numeric_outcome: float,
        outcome_label: str,
        recorded_by: str = "system",
    ) -> Optional[PredictionOutcome]:
        pred = await self.get_prediction(prediction_id)
        if not pred:
            return None

        err = abs(actual_numeric_outcome - pred.probability)
        outcome = PredictionOutcome(
            tenant_id=pred.tenant_id,
            prediction_id=prediction_id,
            actual_numeric_outcome=actual_numeric_outcome,
            outcome_label=outcome_label,
            error_magnitude=err,
            recorded_by=recorded_by,
        )
        self.session.add(outcome)
        await self.session.commit()
        await self.session.refresh(outcome)
        return outcome

    # =========================================================================
    # 4. Decision Intelligence & Support Records
    # =========================================================================

    async def create_decision_support_record(self, record: DecisionSupportRecord) -> DecisionSupportRecord:
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def get_decision_support_record(self, record_id: str) -> Optional[DecisionSupportRecord]:
        stmt = (
            select(DecisionSupportRecord)
            .where(DecisionSupportRecord.id == record_id)
            .options(
                selectinload(DecisionSupportRecord.prediction),
                selectinload(DecisionSupportRecord.reviews),
                selectinload(DecisionSupportRecord.overrides),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_decision_support_records(
        self,
        tenant_id: str,
        state: Optional[str] = None,
        limit: int = 50,
    ) -> List[DecisionSupportRecord]:
        stmt = select(DecisionSupportRecord).where(DecisionSupportRecord.tenant_id == tenant_id)
        if state:
            stmt = stmt.where(DecisionSupportRecord.state == state)
        stmt = (
            stmt.options(
                selectinload(DecisionSupportRecord.prediction),
                selectinload(DecisionSupportRecord.overrides),
            )
            .order_by(desc(DecisionSupportRecord.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def review_decision_support(
        self,
        record_id: str,
        reviewer: str,
        action: str,  # ACCEPT, OVERRIDE, REJECT
        notes: Optional[str] = None,
        override_reason: Optional[str] = None,
        chosen_action: Optional[str] = None,
    ) -> Optional[DecisionSupportRecord]:
        record = await self.get_decision_support_record(record_id)
        if not record:
            return None

        state_map = {
            "ACCEPT": DecisionState.ACCEPTED,
            "OVERRIDE": DecisionState.OVERRIDDEN,
            "REJECT": DecisionState.REJECTED,
        }
        record.state = state_map.get(action.upper(), record.state)
        record.reviewed_by = reviewer
        record.reviewed_at = datetime.utcnow()

        review = DecisionReview(
            tenant_id=record.tenant_id,
            decision_record_id=record.id,
            reviewer=reviewer,
            action=action.upper(),
            notes=notes,
        )
        self.session.add(review)

        if action.upper() == "OVERRIDE" and override_reason:
            override = DecisionOverride(
                tenant_id=record.tenant_id,
                decision_record_id=record.id,
                original_recommendation=record.recommended_action,
                chosen_action=chosen_action or notes or "Operator overridden",
                override_reason=override_reason,
                operator=reviewer,
            )
            self.session.add(override)

        await self.session.commit()
        await self.session.refresh(record)
        return record

    # =========================================================================
    # 5. Forecasts & Drift Monitoring
    # =========================================================================

    async def create_forecast_run(self, forecast: ForecastRun) -> ForecastRun:
        self.session.add(forecast)
        await self.session.commit()
        await self.session.refresh(forecast)
        return forecast

    async def list_forecast_runs(self, tenant_id: str, limit: int = 20) -> List[ForecastRun]:
        stmt = (
            select(ForecastRun)
            .where(ForecastRun.tenant_id == tenant_id)
            .order_by(desc(ForecastRun.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def record_drift_event(self, drift: ModelDriftEvent) -> ModelDriftEvent:
        self.session.add(drift)
        await self.session.commit()
        await self.session.refresh(drift)
        return drift

    async def list_drift_events(self, tenant_id: str, limit: int = 30) -> List[ModelDriftEvent]:
        stmt = (
            select(ModelDriftEvent)
            .where(ModelDriftEvent.tenant_id == tenant_id)
            .order_by(desc(ModelDriftEvent.detected_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
