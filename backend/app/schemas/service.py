import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ServiceCategory(str, Enum):
    WEB_DEVELOPMENT = "WEB_DEVELOPMENT"
    SOFTWARE_DEVELOPMENT = "SOFTWARE_DEVELOPMENT"
    BUSINESS_AUTOMATION = "BUSINESS_AUTOMATION"
    AI_SYSTEMS = "AI_SYSTEMS"
    DATA_ANALYTICS = "DATA_ANALYTICS"
    UI_UX = "UI_UX"
    MAINTENANCE = "MAINTENANCE"
    CONSULTING = "CONSULTING"
    OTHER = "OTHER"


class ServiceStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ARCHIVED = "ARCHIVED"


class DeliveryModel(str, Enum):
    FIXED_PROJECT = "FIXED_PROJECT"
    CUSTOM_QUOTE = "CUSTOM_QUOTE"
    SUBSCRIPTION = "SUBSCRIPTION"
    RETAINER = "RETAINER"
    HOURLY = "HOURLY"
    CONSULTATION = "CONSULTATION"


class PricingModel(str, Enum):
    FIXED = "FIXED"
    STARTING_AT = "STARTING_AT"
    RANGE = "RANGE"
    CUSTOM = "CUSTOM"
    NOT_SET = "NOT_SET"


class LeadServiceRelationshipType(str, Enum):
    CONSIDERED = "CONSIDERED"
    RECOMMENDED = "RECOMMENDED"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"


class LeadServiceSource(str, Enum):
    HUMAN = "HUMAN"
    RULE = "RULE"
    AI = "AI"
    IMPORT = "IMPORT"
    OTHER = "OTHER"


class ServiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    short_description: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    category: ServiceCategory = ServiceCategory.WEB_DEVELOPMENT
    subcategory: Optional[str] = Field(None, max_length=100)
    status: ServiceStatus = ServiceStatus.ACTIVE
    delivery_model: DeliveryModel = DeliveryModel.FIXED_PROJECT
    pricing_model: PricingModel = PricingModel.CUSTOM
    base_price: Optional[float] = Field(None, ge=0.0)
    price_min: Optional[float] = Field(None, ge=0.0)
    price_max: Optional[float] = Field(None, ge=0.0)
    currency: str = Field("USD", max_length=10)
    estimated_duration_days: Optional[int] = Field(None, ge=1)
    is_featured: bool = False
    is_active: bool = True
    features: List[str] = Field(default_factory=list)
    requirements: List[str] = Field(default_factory=list)
    target_business_types: List[str] = Field(default_factory=list)


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    short_description: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    category: Optional[ServiceCategory] = None
    subcategory: Optional[str] = Field(None, max_length=100)
    status: Optional[ServiceStatus] = None
    delivery_model: Optional[DeliveryModel] = None
    pricing_model: Optional[PricingModel] = None
    base_price: Optional[float] = Field(None, ge=0.0)
    price_min: Optional[float] = Field(None, ge=0.0)
    price_max: Optional[float] = Field(None, ge=0.0)
    currency: Optional[str] = Field(None, max_length=10)
    estimated_duration_days: Optional[int] = Field(None, ge=1)
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    features: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    target_business_types: Optional[List[str]] = None


class ServiceResponse(ServiceBase):
    id: uuid.UUID
    slug: str
    archived_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LeadServiceCreate(BaseModel):
    service_id: uuid.UUID
    relationship_type: LeadServiceRelationshipType = LeadServiceRelationshipType.CONSIDERED
    source: LeadServiceSource = LeadServiceSource.HUMAN
    notes: Optional[str] = None


class LeadServiceResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    service_id: uuid.UUID
    relationship_type: str
    source: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    service: Optional[ServiceResponse] = None

    model_config = ConfigDict(from_attributes=True)
