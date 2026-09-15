from sqlalchemy.orm import Session

from app.repositories.dashboard import DashboardRepository
from app.schemas.dashboard import (
    AttentionSummary,
    BusinessMetricsSummary,
    DashboardSummaryData,
    LeadMetricsSummary,
    LeadPipelineSnapshot,
    OverdueAction,
    RecentBusinessItem,
    RecentLeadItem,
    ServiceSummary,
    UpcomingAction,
)
from app.services.business import BusinessService


class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> DashboardSummaryData:
        biz_metrics = DashboardRepository.get_business_metrics(db)
        lead_metrics = DashboardRepository.get_lead_metrics(db)
        overdue_raw = DashboardRepository.get_overdue_actions(db, limit=5)
        upcoming_raw = DashboardRepository.get_upcoming_actions(db, limit=5)
        recent_leads_raw = DashboardRepository.get_recent_leads(db, limit=5)
        recent_businesses_raw = DashboardRepository.get_recent_businesses(db, limit=5)
        service_metrics = DashboardRepository.get_service_metrics(db)

        # Overdue action list mapping
        overdue_actions = [
            OverdueAction(
                lead_id=lead.id,
                lead_title=lead.title,
                business_id=business.id,
                business_name=business.name,
                next_action=lead.next_action,
                next_action_at=lead.next_action_at,
                priority=lead.priority,
            )
            for lead, business in overdue_raw
            if lead.next_action_at is not None
        ]

        # Upcoming action list mapping
        upcoming_actions = [
            UpcomingAction(
                lead_id=lead.id,
                lead_title=lead.title,
                business_id=business.id,
                business_name=business.name,
                next_action=lead.next_action,
                next_action_at=lead.next_action_at,
                priority=lead.priority,
            )
            for lead, business in upcoming_raw
            if lead.next_action_at is not None
        ]

        # Recent leads mapping
        recent_leads = [
            RecentLeadItem(
                id=lead.id,
                title=lead.title,
                business_id=business.id,
                business_name=business.name,
                status=lead.status,
                priority=lead.priority,
                qualification_status=lead.qualification_status,
                updated_at=lead.updated_at,
            )
            for lead, business in recent_leads_raw
        ]

        # Recent businesses mapping
        recent_businesses = [
            RecentBusinessItem(
                id=b.id,
                name=b.name,
                industry=b.industry,
                city=b.city,
                status=b.status,
                data_quality_score=BusinessService.calculate_data_quality(b).score,
                updated_at=b.updated_at,
            )
            for b in recent_businesses_raw
        ]

        # Attention summary construction
        attention = AttentionSummary(
            high_priority_leads_count=lead_metrics["high_priority_count"],
            overdue_actions_count=len(overdue_actions),
            incomplete_data_businesses_count=biz_metrics["incomplete_data_businesses_count"],
        )

        return DashboardSummaryData(
            businesses=BusinessMetricsSummary(
                active_count=biz_metrics["active_count"],
                total_count=biz_metrics["total_count"],
            ),
            leads=LeadMetricsSummary(
                open_count=lead_metrics["open_count"],
                qualified_count=lead_metrics["qualified_count"],
                high_priority_count=lead_metrics["high_priority_count"],
                total_count=lead_metrics["total_count"],
            ),
            pipeline=LeadPipelineSnapshot(counts=lead_metrics["pipeline_counts"]),
            attention=attention,
            overdue_actions=overdue_actions,
            upcoming_actions=upcoming_actions,
            recent_leads=recent_leads,
            recent_businesses=recent_businesses,
            services=ServiceSummary(
                active_services_count=service_metrics["active_services_count"],
                featured_services_count=service_metrics["featured_services_count"],
                total_services_count=service_metrics["total_services_count"],
                category_counts=service_metrics["category_counts"],
            ),
        )
