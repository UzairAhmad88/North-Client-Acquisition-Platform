"""In-memory mock storage provider for isolated tests."""

import hashlib
from datetime import datetime, timezone
from typing import BinaryIO, Dict, Optional

from integrations.storage.base import BaseStorageProvider, StorageObjectMetadata


class MockStorageProvider(BaseStorageProvider):
    """In-memory storage provider."""

    def __init__(self) -> None:
        self._store: Dict[str, bytes] = {}
        self._metadata: Dict[str, Dict[str, str]] = {}
        self._content_types: Dict[str, str] = {}

    def upload(
        self,
        storage_key: str,
        data: bytes | BinaryIO,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None,
    ) -> StorageObjectMetadata:
        if isinstance(data, (bytes, bytearray)):
            byte_content = bytes(data)
        else:
            byte_content = data.read()

        checksum = hashlib.sha256(byte_content).hexdigest()
        self._store[storage_key] = byte_content
        self._metadata[storage_key] = metadata or {}
        self._content_types[storage_key] = content_type

        return StorageObjectMetadata(
            storage_key=storage_key,
            size_bytes=len(byte_content),
            content_type=content_type,
            checksum_sha256=checksum,
            created_at=datetime.now(timezone.utc),
            etag=f'"{checksum}"',
            custom_metadata=metadata or {},
        )

    def download(self, storage_key: str) -> bytes:
        if storage_key not in self._store:
            raise FileNotFoundError(f"Mock storage key not found: {storage_key}")
        return self._store[storage_key]

    def delete(self, storage_key: str) -> bool:
        if storage_key in self._store:
            del self._store[storage_key]
            self._metadata.pop(storage_key, None)
            self._content_types.pop(storage_key, None)
            return True
        return False

    def exists(self, storage_key: str) -> bool:
        return storage_key in self._store

    def generate_private_url(
        self, storage_key: str, expires_in_seconds: int = 3600, download_filename: Optional[str] = None
    ) -> str:
        filename_param = f"&filename={download_filename}" if download_filename else ""
        return f"mock://storage/private/{storage_key}?expires={expires_in_seconds}{filename_param}"

    def copy(self, source_key: str, destination_key: str) -> StorageObjectMetadata:
        if source_key not in self._store:
            raise FileNotFoundError(f"Source key not found: {source_key}")
        data = self._store[source_key]
        return self.upload(
            destination_key,
            data,
            content_type=self._content_types.get(source_key, "application/octet-stream"),
            metadata=self._metadata.get(source_key, {}),
        )

    def move(self, source_key: str, destination_key: str) -> StorageObjectMetadata:
        meta = self.copy(source_key, destination_key)
        self.delete(source_key)
        return meta
