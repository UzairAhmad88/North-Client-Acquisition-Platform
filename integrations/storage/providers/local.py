"""Local filesystem storage provider implementation."""

import hashlib
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, Dict, Optional

from integrations.storage.base import BaseStorageProvider, StorageObjectMetadata


class LocalFileStorageProvider(BaseStorageProvider):
    """Local filesystem storage provider for development and testing."""

    def __init__(self, base_path: str = "./storage") -> None:
        self.base_path = Path(base_path).resolve()
        self.objects_dir = self.base_path / "objects"
        self.temp_dir = self.base_path / "temporary"
        self.previews_dir = self.base_path / "previews"
        self.quarantine_dir = self.base_path / "quarantine"

        for directory in [self.objects_dir, self.temp_dir, self.previews_dir, self.quarantine_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, storage_key: str) -> Path:
        """Resolve a safe path ensuring no directory traversal."""
        cleaned_key = storage_key.lstrip("/\\")
        target_path = (self.objects_dir / cleaned_key).resolve()
        if not str(target_path).startswith(str(self.objects_dir)):
            raise ValueError(f"Security error: Invalid storage path traversal '{storage_key}'")
        return target_path

    def upload(
        self,
        storage_key: str,
        data: bytes | BinaryIO,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None,
    ) -> StorageObjectMetadata:
        target_path = self._resolve_path(storage_key)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, (bytes, bytearray)):
            byte_content = bytes(data)
        else:
            byte_content = data.read()

        checksum = hashlib.sha256(byte_content).hexdigest()

        with open(target_path, "wb") as f:
            f.write(byte_content)

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
        target_path = self._resolve_path(storage_key)
        if not target_path.exists():
            raise FileNotFoundError(f"Storage object not found: {storage_key}")
        with open(target_path, "rb") as f:
            return f.read()

    def delete(self, storage_key: str) -> bool:
        target_path = self._resolve_path(storage_key)
        if target_path.exists():
            target_path.unlink()
            return True
        return False

    def exists(self, storage_key: str) -> bool:
        return self._resolve_path(storage_key).exists()

    def generate_private_url(
        self, storage_key: str, expires_in_seconds: int = 3600, download_filename: Optional[str] = None
    ) -> str:
        # In local mode, generate a private API proxy URL without exposing raw disk paths
        filename_param = f"&filename={download_filename}" if download_filename else ""
        return f"/api/v1/files/download?key={storage_key}&expires={expires_in_seconds}{filename_param}"

    def copy(self, source_key: str, destination_key: str) -> StorageObjectMetadata:
        src = self._resolve_path(source_key)
        dst = self._resolve_path(destination_key)
        if not src.exists():
            raise FileNotFoundError(f"Source object not found: {source_key}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        data = self.download(destination_key)
        checksum = hashlib.sha256(data).hexdigest()
        return StorageObjectMetadata(
            storage_key=destination_key,
            size_bytes=len(data),
            content_type="application/octet-stream",
            checksum_sha256=checksum,
            created_at=datetime.now(timezone.utc),
        )

    def move(self, source_key: str, destination_key: str) -> StorageObjectMetadata:
        meta = self.copy(source_key, destination_key)
        self.delete(source_key)
        return meta
