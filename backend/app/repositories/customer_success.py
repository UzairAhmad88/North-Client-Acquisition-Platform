"""Database repository for Phase 41 Unified Client Relationship Intelligence & Customer Success Platform."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import desc, select, update, and_
from sqlalchemy.orm import Session

from app.models.customer_success import (
    ClientProfileModel,
    ClientRelationshipModel,
    ClientTimelineEventModel,
    ClientGoalModel,
    ClientSuccessPlanModel,
    ClientSuccessTaskModel,
    ClientHealthScoreModel,
    ClientHealthHistoryModel,
    ClientSurveyModel,
    ClientSurveyResponseModel,
    ClientSentimentAnalysisModel,
    ClientRiskModel,
    ClientOpportunityModel,
    ClientRenewalModel,
    ClientReferralModel,
    ClientSegmentModel,
    ClientAccountPlanModel,
    ClientReviewModel,
)


class CustomerSuccessRepository:
    """Database operations for client profiles, relationships, health scores, risks, opportunities, renewals, surveys, and reviews."""

    def __init__(self, db: Session):
        self.db = db

    # --- Client Profile ---

    def get_profile_by_client_id(self, tenant_id: str, client_id: str) -> Optional[ClientProfileModel]:
        stmt = select(ClientProfileModel).where(
            and_(
                ClientProfileModel.tenant_id == tenant_id,
                (ClientProfileModel.client_account_id == client_id) | (ClientProfileModel.id == client_id)
            )
        )
        return self.db.execute(stmt).scalars().first()

    def create_or_update_profile(self, tenant_id: str, data: Dict[str, Any]) -> ClientProfileModel:
        client_id = data.get("client_id") or data.get("client_account_id") or str(uuid.uuid4())
        profile = self.get_profile_by_client_id(tenant_id, client_id)
        if profile:
            for k, v in data.items():
                if hasattr(profile, k) and v is not None:
                    setattr(profile, k, v)
        else:
            profile = ClientProfileModel(
                tenant_id=tenant_id,
                client_account_id=client_id,
                business_id=data.get("business_id"),
                business_name=data.get("business_name") or data.get("company_name", "Organization"),
                lifecycle_stage=data.get("lifecycle_stage", "ACTIVE"),
                relationship_strength=data.get("relationship_strength", "ESTABLISHED"),
                relationship_owner_id=data.get("relationship_owner_id") or data.get("relationship_manager_id"),
                sales_owner_id=data.get("sales_owner_id"),
                project_owner_id=data.get("project_owner_id"),
                cs_owner_id=data.get("cs_owner_id"),
                target_contract_value=data.get("target_contract_value"),
                ltv_estimate=data.get("ltv_estimate"),
                churn_risk_band=data.get("churn_risk_band", "LOW"),
                summary=data.get("summary"),
                metadata_json=data.get("metadata_json") or data.get("custom_fields", {}),
            )
            self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def list_profiles(self, tenant_id: str, lifecycle_stage: Optional[str] = None, limit: int = 50) -> List[ClientProfileModel]:
        stmt = select(ClientProfileModel).where(ClientProfileModel.tenant_id == tenant_id)
        if lifecycle_stage:
            stmt = stmt.where(ClientProfileModel.lifecycle_stage == lifecycle_stage)
        stmt = stmt.order_by(desc(ClientProfileModel.created_at)).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    # --- Relationships ---

    def create_relationship(self, tenant_id: str, data: Dict[str, Any]) -> ClientRelationshipModel:
        client_profile_id = data.get("client_profile_id")
        if not client_profile_id:
            profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
            client_profile_id = profile.id if profile else data.get("client_id", str(uuid.uuid4()))

        record = ClientRelationshipModel(
            tenant_id=tenant_id,
            client_profile_id=client_profile_id,
            contact_id=data.get("contact_id", str(uuid.uuid4())),
            contact_name=data["contact_name"],
            contact_email=data.get("contact_email"),
            role_title=data.get("role_title") or data.get("contact_role"),
            decision_role=data.get("decision_role", "USER"),
            relationship_strength=data.get("relationship_strength", "ESTABLISHED"),
            notes=data.get("notes"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_relationships(self, tenant_id: str, client_id: str) -> List[ClientRelationshipModel]:
        profile = self.get_profile_by_client_id(tenant_id, client_id)
        pid = profile.id if profile else client_id
        stmt = select(ClientRelationshipModel).where(
            and_(ClientRelationshipModel.tenant_id == tenant_id, ClientRelationshipModel.client_profile_id == pid)
        ).order_by(ClientRelationshipModel.contact_name)
        return list(self.db.execute(stmt).scalars().all())

    # --- Timeline Events ---

    def create_timeline_event(self, tenant_id: str, data: Dict[str, Any]) -> ClientTimelineEventModel:
        profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
        pid = profile.id if profile else data.get("client_profile_id") or data.get("client_id", str(uuid.uuid4()))

        record = ClientTimelineEventModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            event_type=data.get("event_type", "GENERAL"),
            title=data["title"],
            description=data.get("description") or data.get("summary"),
            actor_type=data.get("actor_type", "SYSTEM"),
            actor_id=data.get("actor_id"),
            source_entity_type=data.get("source_entity_type"),
            source_entity_id=data.get("source_entity_id"),
            payload=data.get("payload") or data.get("metadata_payload", {}),
            occurred_at=data.get("occurred_at", datetime.now(timezone.utc)),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_timeline_events(
        self,
        tenant_id: str,
        client_id: str,
        limit: int = 50,
    ) -> List[ClientTimelineEventModel]:
        profile = self.get_profile_by_client_id(tenant_id, client_id)
        pid = profile.id if profile else client_id
        stmt = select(ClientTimelineEventModel).where(
            and_(ClientTimelineEventModel.tenant_id == tenant_id, ClientTimelineEventModel.client_profile_id == pid)
        ).order_by(desc(ClientTimelineEventModel.occurred_at)).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    # --- Goals ---

    def create_goal(self, tenant_id: str, data: Dict[str, Any]) -> ClientGoalModel:
        profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
        pid = profile.id if profile else data.get("client_profile_id") or data.get("client_id", str(uuid.uuid4()))

        record = ClientGoalModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            title=data["title"],
            description=data.get("description"),
            priority=data.get("priority", "MEDIUM"),
            owner_id=data.get("owner_id"),
            target_date=data.get("target_date"),
            status=data.get("status", "IN_PROGRESS"),
            success_metric=data.get("success_metric") or data.get("metric_target"),
            target_value=str(data.get("target_value", "100")),
            current_value=str(data.get("progress_percentage") or data.get("current_value", "0")),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_goals(self, tenant_id: str, client_id: str) -> List[ClientGoalModel]:
        profile = self.get_profile_by_client_id(tenant_id, client_id)
        pid = profile.id if profile else client_id
        stmt = select(ClientGoalModel).where(
            and_(ClientGoalModel.tenant_id == tenant_id, ClientGoalModel.client_profile_id == pid)
        ).order_by(desc(ClientGoalModel.created_at))
        return list(self.db.execute(stmt).scalars().all())

    # --- Health Scores & History ---

    def record_health_score(self, tenant_id: str, data: Dict[str, Any]) -> ClientHealthScoreModel:
        profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
        pid = profile.id if profile else data.get("client_profile_id") or data.get("client_id", str(uuid.uuid4()))

        record = ClientHealthScoreModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            overall_score=data.get("composite_score") or data.get("overall_score", Decimal("0.00")),
            health_band=str(data.get("health_band", "HEALTHY")),
            confidence=str(data.get("confidence") or data.get("confidence_score", "HIGH")),
            trend=data.get("trend", "STABLE"),
            engagement_score=data.get("engagement_score"),
            project_score=data.get("project_score") or data.get("project_health_score"),
            support_score=data.get("support_score") or data.get("support_satisfaction_score"),
            finance_score=data.get("finance_score") or data.get("financial_health_score"),
            satisfaction_score=data.get("satisfaction_score") or data.get("support_satisfaction_score"),
            relationship_score=data.get("relationship_score") or data.get("relationship_health_score"),
            goal_score=data.get("goal_score") or data.get("goal_progress_score"),
            explanation=data.get("explanation") or data.get("explanation_summary"),
            positive_factors=data.get("positive_factors", []),
            risk_factors=data.get("risk_factors", []),
        )
        self.db.add(record)

        # Also log to history
        history = ClientHealthHistoryModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            score=data.get("composite_score") or data.get("overall_score", Decimal("0.00")),
            health_band=str(data.get("health_band", "HEALTHY")),
            trend=data.get("trend", "STABLE"),
            factor_breakdown=data.get("calculation_breakdown") or data.get("factor_breakdown", {}),
            confidence=str(data.get("confidence") or data.get("confidence_score", "HIGH")),
        )
        self.db.add(history)

        self.db.commit()
        self.db.refresh(record)
        return record

    def get_latest_health_score(self, tenant_id: str, client_id: str) -> Optional[ClientHealthScoreModel]:
        profile = self.get_profile_by_client_id(tenant_id, client_id)
        pid = profile.id if profile else client_id
        stmt = select(ClientHealthScoreModel).where(
            and_(ClientHealthScoreModel.tenant_id == tenant_id, ClientHealthScoreModel.client_profile_id == pid)
        ).order_by(desc(ClientHealthScoreModel.calculated_at))
        return self.db.execute(stmt).scalars().first()

    def list_health_history(self, tenant_id: str, client_id: str, limit: int = 30) -> List[ClientHealthHistoryModel]:
        profile = self.get_profile_by_client_id(tenant_id, client_id)
        pid = profile.id if profile else client_id
        stmt = select(ClientHealthHistoryModel).where(
            and_(ClientHealthHistoryModel.tenant_id == tenant_id, ClientHealthHistoryModel.client_profile_id == pid)
        ).order_by(desc(ClientHealthHistoryModel.recorded_at)).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    # --- Risks ---

    def create_risk(self, tenant_id: str, data: Dict[str, Any]) -> ClientRiskModel:
        profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
        pid = profile.id if profile else data.get("client_profile_id") or data.get("client_id", str(uuid.uuid4()))

        record = ClientRiskModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            risk_category=str(data.get("category") or data.get("risk_category", "RELATIONSHIP")),
            title=data["title"],
            description=data.get("description"),
            severity=data.get("severity", "MEDIUM"),
            status=data.get("status", "OPEN"),
            evidence=data.get("evidence") or data.get("impact_summary"),
            recommended_action=data.get("recommended_action") or data.get("mitigation_plan"),
            assigned_to_user_id=data.get("owner_id") or data.get("assigned_to_user_id"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_risks(self, tenant_id: str, client_id: Optional[str] = None, status: Optional[str] = None) -> List[ClientRiskModel]:
        stmt = select(ClientRiskModel).where(ClientRiskModel.tenant_id == tenant_id)
        if client_id:
            profile = self.get_profile_by_client_id(tenant_id, client_id)
            pid = profile.id if profile else client_id
            stmt = stmt.where(ClientRiskModel.client_profile_id == pid)
        if status:
            stmt = stmt.where(ClientRiskModel.status == status)
        stmt = stmt.order_by(desc(ClientRiskModel.created_at))
        return list(self.db.execute(stmt).scalars().all())

    # --- Opportunities ---

    def create_opportunity(self, tenant_id: str, data: Dict[str, Any]) -> ClientOpportunityModel:
        profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
        pid = profile.id if profile else data.get("client_profile_id") or data.get("client_id", str(uuid.uuid4()))

        record = ClientOpportunityModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            opportunity_type=str(data.get("opportunity_type", "EXPANSION")),
            title=data["title"],
            description=data.get("description"),
            estimated_value=data.get("estimated_value", Decimal("0.00")),
            confidence=str(data.get("confidence") or data.get("confidence_score", "MEDIUM")),
            status=data.get("status", "IDENTIFIED"),
            target_service_id=data.get("target_service_id"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_opportunities(self, tenant_id: str, client_id: Optional[str] = None) -> List[ClientOpportunityModel]:
        stmt = select(ClientOpportunityModel).where(ClientOpportunityModel.tenant_id == tenant_id)
        if client_id:
            profile = self.get_profile_by_client_id(tenant_id, client_id)
            pid = profile.id if profile else client_id
            stmt = stmt.where(ClientOpportunityModel.client_profile_id == pid)
        stmt = stmt.order_by(desc(ClientOpportunityModel.created_at))
        return list(self.db.execute(stmt).scalars().all())

    # --- Renewals ---

    def create_renewal(self, tenant_id: str, data: Dict[str, Any]) -> ClientRenewalModel:
        profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
        pid = profile.id if profile else data.get("client_profile_id") or data.get("client_id", str(uuid.uuid4()))

        exp_date = data.get("renewal_date") or data.get("current_period_end") or datetime.now(timezone.utc)
        record = ClientRenewalModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            contract_id=data.get("contract_id"),
            expiration_date=exp_date,
            renewal_window_start=data.get("current_period_end", exp_date),
            renewal_window_end=exp_date,
            contract_value=data.get("estimated_renewal_value") or data.get("contract_value", Decimal("0.00")),
            status=data.get("status", "UPCOMING"),
            probability_pct=data.get("renewal_probability") or data.get("probability_pct", Decimal("50.00")),
            owner_id=data.get("assigned_owner_id") or data.get("owner_id"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_renewals(self, tenant_id: str, client_id: Optional[str] = None) -> List[ClientRenewalModel]:
        stmt = select(ClientRenewalModel).where(ClientRenewalModel.tenant_id == tenant_id)
        if client_id:
            profile = self.get_profile_by_client_id(tenant_id, client_id)
            pid = profile.id if profile else client_id
            stmt = stmt.where(ClientRenewalModel.client_profile_id == pid)
        stmt = stmt.order_by(ClientRenewalModel.expiration_date)
        return list(self.db.execute(stmt).scalars().all())

    # --- Surveys & Sentiment ---

    def create_survey(self, tenant_id: str, data: Dict[str, Any]) -> ClientSurveyModel:
        profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
        pid = profile.id if profile else data.get("client_profile_id") or data.get("client_id", str(uuid.uuid4()))

        record = ClientSurveyModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            survey_type=data.get("survey_type", "CSAT"),
            title=data["title"],
            status=data.get("status", "SENT"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def submit_survey_response(self, data: Dict[str, Any]) -> ClientSurveyResponseModel:
        record = ClientSurveyResponseModel(
            tenant_id=data.get("tenant_id", "default-tenant"),
            survey_id=data["survey_id"],
            client_profile_id=data.get("client_profile_id", str(uuid.uuid4())),
            contact_id=data.get("respondent_id") or data.get("contact_id"),
            score=data["score"],
            raw_feedback=data.get("feedback_text") or data.get("raw_feedback"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    # --- Account Plans & Reviews ---

    def create_account_plan(self, tenant_id: str, data: Dict[str, Any]) -> ClientAccountPlanModel:
        profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
        pid = profile.id if profile else data.get("client_profile_id") or data.get("client_id", str(uuid.uuid4()))

        record = ClientAccountPlanModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            title=data.get("title") or f"Account Plan {data.get('fiscal_year', '2026')}",
            status=data.get("status", "DRAFT"),
            service_summary=data.get("account_strategy"),
            opportunity_summary=str(data.get("revenue_target", "")),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_account_plans(self, tenant_id: str, client_id: str) -> List[ClientAccountPlanModel]:
        profile = self.get_profile_by_client_id(tenant_id, client_id)
        pid = profile.id if profile else client_id
        stmt = select(ClientAccountPlanModel).where(
            and_(ClientAccountPlanModel.tenant_id == tenant_id, ClientAccountPlanModel.client_profile_id == pid)
        ).order_by(desc(ClientAccountPlanModel.created_at))
        return list(self.db.execute(stmt).scalars().all())

    def create_review(self, tenant_id: str, data: Dict[str, Any]) -> ClientReviewModel:
        profile = self.get_profile_by_client_id(tenant_id, data.get("client_id", ""))
        pid = profile.id if profile else data.get("client_profile_id") or data.get("client_id", str(uuid.uuid4()))

        record = ClientReviewModel(
            tenant_id=tenant_id,
            client_profile_id=pid,
            review_type=data.get("review_type", "QBR"),
            scheduled_at=data.get("scheduled_date") or data.get("scheduled_at", datetime.now(timezone.utc)),
            attendees=data.get("attendees", []),
            summary_notes=data.get("meeting_notes") or data.get("summary_notes"),
            action_items=data.get("action_items", []),
            status=data.get("status", "SCHEDULED"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_reviews(self, tenant_id: str, client_id: str) -> List[ClientReviewModel]:
        profile = self.get_profile_by_client_id(tenant_id, client_id)
        pid = profile.id if profile else client_id
        stmt = select(ClientReviewModel).where(
            and_(ClientReviewModel.tenant_id == tenant_id, ClientReviewModel.client_profile_id == pid)
        ).order_by(desc(ClientReviewModel.scheduled_at))
        return list(self.db.execute(stmt).scalars().all())
