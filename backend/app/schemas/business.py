import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BusinessStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"


class BusinessBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Business display name")
    legal_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None)
    business_type: str = Field("OTHER", max_length=100)
    industry: str = Field("OTHER", max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=255)
    website_url: Optional[str] = Field(None, max_length=500)
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field("Pakistan", max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    timezone: Optional[str] = Field(None, max_length=50)
    source: str = Field("MANUAL", max_length=100)
    source_url: Optional[str] = Field(None, max_length=500)
    external_id: Optional[str] = Field(None, max_length=255)


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    legal_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None)
    business_type: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=255)
    website_url: Optional[str] = Field(None, max_length=500)
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    timezone: Optional[str] = Field(None, max_length=50)
    status: Optional[BusinessStatus] = Field(None)
    source: Optional[str] = Field(None, max_length=100)
    source_url: Optional[str] = Field(None, max_length=500)
    external_id: Optional[str] = Field(None, max_length=255)


class BusinessDataQuality(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Data quality percentage (0-100)")
    missing_fields: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class BusinessDuplicateMatch(BaseModel):
    business_id: uuid.UUID
    name: str
    confidence: float
    signals: List[str]


class BusinessDuplicateCheckResponse(BaseModel):
    possible_duplicate: bool
    confidence: float
    signals: List[str]
    matches: List[BusinessDuplicateMatch] = Field(default_factory=list)


class BusinessResponse(BusinessBase):
    id: uuid.UUID
    normalized_name: str
    normalized_phone: Optional[str] = None
    normalized_email: Optional[str] = None
    normalized_website: Optional[str] = None
    status: str
    created_by_user_id: Optional[uuid.UUID] = None
    archived_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    data_quality: Optional[BusinessDataQuality] = None

    model_config = ConfigDict(from_attributes=True)
