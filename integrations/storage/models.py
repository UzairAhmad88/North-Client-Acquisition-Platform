"""Models for storage operations."""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field


class StorageProviderType(str, Enum):
    """Supported storage provider types."""
    LOCAL = "LOCAL"
    S3 = "S3"
    MOCK = "MOCK"


class StorageUploadRequest(BaseModel):
    """Request payload to initiate or perform an upload."""
    tenant_id: str
    workspace_id: str
    filename: str
    content_type: str
    size_bytes: int
    classification: Optional[str] = "GENERAL"
    metadata: Dict[str, str] = Field(default_factory=dict)


class StorageUploadResult(BaseModel):
    """Result of a storage upload operation."""
    storage_key: str
    provider: StorageProviderType
    checksum_sha256: str
    size_bytes: int
    content_type: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
