import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.contact import ContactResponse


class LeadStatus(str, Enum):
    NEW = "NEW"
    RESEARCHING = "RESEARCHING"
    QUALIFIED = "QUALIFIED"
    CONTACTED = "CONTACTED"
    RESPONDED = "RESPONDED"
    INTERESTED = "INTERESTED"
    MEETING = "MEETING"
    PROPOSAL = "PROPOSAL"
    WON = "WON"
    FOLLOW_UP = "FOLLOW_UP"
    NOT_INTERESTED = "NOT_INTERESTED"
    LOST = "LOST"
    ARCHIVED = "ARCHIVED"


class LeadPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class QualificationStatus(str, Enum):
    UNQUALIFIED = "UNQUALIFIED"
    PENDING = "PENDING"
    QUALIFIED = "QUALIFIED"
    DISQUALIFIED = "DISQUALIFIED"


class ContactabilityStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    CONTACTABLE = "CONTACTABLE"
    UNCONTACTABLE = "UNCONTACTABLE"
    DO_NOT_CONTACT = "DO_NOT_CONTACT"


class BusinessSummary(BaseModel):
    id: uuid.UUID
    name: str
    city: Optional[str] = None
    industry: str

    model_config = ConfigDict(from_attributes=True)


class OwnerSummary(BaseModel):
    id: uuid.UUID
    full_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class LeadBase(BaseModel):
    business_id: uuid.UUID
    title: str = Field(..., min_length=1, max_length=255, description="Sales opportunity title")
    description: Optional[str] = None
    source: str = Field("MANUAL", max_length=100)
    source_detail: Optional[str] = Field(None, max_length=255)
    priority: LeadPriority = LeadPriority.MEDIUM
    owner_user_id: Optional[uuid.UUID] = None
    qualification_status: QualificationStatus = QualificationStatus.UNQUALIFIED
    contactability_status: ContactabilityStatus = ContactabilityStatus.UNKNOWN
    estimated_value: Optional[float] = Field(None, ge=0.0)
    currency: str = Field("USD", max_length=10)
    next_action: Optional[str] = Field(None, max_length=255)
    next_action_at: Optional[datetime] = None
    notes: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[LeadStatus] = None
    source: Optional[str] = Field(None, max_length=100)
    source_detail: Optional[str] = Field(None, max_length=255)
    priority: Optional[LeadPriority] = None
    owner_user_id: Optional[uuid.UUID] = None
    qualification_status: Optional[QualificationStatus] = None
    contactability_status: Optional[ContactabilityStatus] = None
    estimated_value: Optional[float] = Field(None, ge=0.0)
    currency: Optional[str] = Field(None, max_length=10)
    next_action: Optional[str] = Field(None, max_length=255)
    next_action_at: Optional[datetime] = None
    loss_reason: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class LeadTransitionInput(BaseModel):
    status: LeadStatus
    loss_reason: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class LeadAssignInput(BaseModel):
    owner_user_id: Optional[uuid.UUID] = None


class LeadDataQuality(BaseModel):
    score: int = Field(..., ge=0, le=100)
    missing_fields: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class LeadDuplicateMatch(BaseModel):
    lead_id: uuid.UUID
    title: str
    status: str
    confidence: float
    signals: List[str]


class LeadDuplicateCheckResponse(BaseModel):
    possible_duplicate: bool
    confidence: float
    signals: List[str]
    matches: List[LeadDuplicateMatch] = Field(default_factory=list)


class LeadResponse(LeadBase):
    id: uuid.UUID
    status: str
    first_contacted_at: Optional[datetime] = None
    last_contacted_at: Optional[datetime] = None
    converted_at: Optional[datetime] = None
    lost_at: Optional[datetime] = None
    loss_reason: Optional[str] = None
    archived_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    business: Optional[BusinessSummary] = None
    owner: Optional[OwnerSummary] = None
    contacts: List[ContactResponse] = Field(default_factory=list)
    data_quality: Optional[LeadDataQuality] = None

    model_config = ConfigDict(from_attributes=True)
