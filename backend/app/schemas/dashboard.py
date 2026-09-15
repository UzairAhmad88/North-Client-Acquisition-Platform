import uuid
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BusinessMetricsSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    active_count: int = Field(default=0, ge=0)
    total_count: int = Field(default=0, ge=0)


class LeadMetricsSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    open_count: int = Field(default=0, ge=0)
    qualified_count: int = Field(default=0, ge=0)
    high_priority_count: int = Field(default=0, ge=0)
    total_count: int = Field(default=0, ge=0)


class LeadPipelineSnapshot(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    counts: Dict[str, int] = Field(default_factory=dict)


class AttentionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    high_priority_leads_count: int = Field(default=0, ge=0)
    overdue_actions_count: int = Field(default=0, ge=0)
    incomplete_data_businesses_count: int = Field(default=0, ge=0)


class OverdueAction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lead_id: uuid.UUID
    lead_title: str
    business_id: uuid.UUID
    business_name: str
    next_action: Optional[str] = None
    next_action_at: datetime
    priority: str


class UpcomingAction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lead_id: uuid.UUID
    lead_title: str
    business_id: uuid.UUID
    business_name: str
    next_action: Optional[str] = None
    next_action_at: datetime
    priority: str


class RecentLeadItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    business_id: uuid.UUID
    business_name: str
    status: str
    priority: str
    qualification_status: str
    updated_at: datetime


class RecentBusinessItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    industry: Optional[str] = None
    city: Optional[str] = None
    status: str
    data_quality_score: int
    updated_at: datetime


class ServiceSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    active_services_count: int = Field(default=0, ge=0)
    featured_services_count: int = Field(default=0, ge=0)
    total_services_count: int = Field(default=0, ge=0)
    category_counts: Dict[str, int] = Field(default_factory=dict)


class DashboardSummaryData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    businesses: BusinessMetricsSummary
    leads: LeadMetricsSummary
    pipeline: LeadPipelineSnapshot
    attention: AttentionSummary
    overdue_actions: List[OverdueAction] = Field(default_factory=list)
    upcoming_actions: List[UpcomingAction] = Field(default_factory=list)
    recent_leads: List[RecentLeadItem] = Field(default_factory=list)
    recent_businesses: List[RecentBusinessItem] = Field(default_factory=list)
    services: ServiceSummary


class DashboardSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: DashboardSummaryData
