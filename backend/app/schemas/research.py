import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ResearchJobCreate(BaseModel):
    business_id: uuid.UUID
    sections: List[str] = Field(default_factory=lambda: ["ALL"])
    provider_type: str = Field(default="MOCK")  # "MOCK" or "WEB"


class ResearchJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    status: str
    requested_sections: List[str]
    source_count: int
    records_found: int
    records_validated: int
    records_rejected: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ResearchRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID
    research_job_id: Optional[uuid.UUID] = None
    source_url: Optional[str] = None
    source_trust: str
    research_type: str
    field_name: str
    raw_value: Optional[str] = None
    normalized_value: str
    confidence: str
    evidence_text: Optional[str] = None
    observed_at: datetime
    expires_at: Optional[datetime] = None
    status: str
    meta_info: Optional[Dict[str, Any]] = None
    created_at: datetime


class ResearchConflictResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID
    field_name: str
    competing_values: List[Dict[str, Any]]
    status: str
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class BusinessResearchProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    business_id: uuid.UUID
    business_name: str
    total_jobs: int
    total_records: int
    active_conflicts_count: int
    last_researched_at: Optional[datetime] = None
    confidence_score: int  # 0 to 100 percentage
    records: List[ResearchRecordResponse] = Field(default_factory=list)
    conflicts: List[ResearchConflictResponse] = Field(default_factory=list)
