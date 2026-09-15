"""Storage Provider Abstraction Layer."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, BinaryIO, Dict, List, Optional
from pydantic import BaseModel, Field


class StorageObjectMetadata(BaseModel):
    """Metadata for stored binary object."""
    storage_key: str
    size_bytes: int
    content_type: str
    checksum_sha256: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    etag: Optional[str] = None
    custom_metadata: Dict[str, str] = Field(default_factory=dict)


class BaseStorageProvider(ABC):
    """Abstract base class for object storage providers."""

    @abstractmethod
    def upload(
        self,
        storage_key: str,
        data: bytes | BinaryIO,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None,
    ) -> StorageObjectMetadata:
        """Upload a file or stream to storage."""
        pass

    @abstractmethod
    def download(self, storage_key: str) -> bytes:
        """Download binary content for the given storage key."""
        pass

    @abstractmethod
    def delete(self, storage_key: str) -> bool:
        """Delete an object from storage."""
        pass

    @abstractmethod
    def exists(self, storage_key: str) -> bool:
        """Check if an object exists in storage."""
        pass

    @abstractmethod
    def generate_private_url(
        self, storage_key: str, expires_in_seconds: int = 3600, download_filename: Optional[str] = None
    ) -> str:
        """Generate a secure signed or temporary URL to access the object."""
        pass

    @abstractmethod
    def copy(self, source_key: str, destination_key: str) -> StorageObjectMetadata:
        """Copy an object within storage."""
        pass

    @abstractmethod
    def move(self, source_key: str, destination_key: str) -> StorageObjectMetadata:
        """Move an object within storage."""
        pass
