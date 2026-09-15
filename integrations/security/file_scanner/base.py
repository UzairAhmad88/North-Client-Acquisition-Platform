"""File Scanner Base Interface."""

from abc import ABC, abstractmethod
from typing import BinaryIO, Optional
from integrations.security.file_scanner.models import ScanResult


class BaseFileScanner(ABC):
    """Abstract base class for malware/virus security scanners."""

    @abstractmethod
    def scan_bytes(self, data: bytes, filename: Optional[str] = None) -> ScanResult:
        """Scan raw byte content for threats."""
        pass

    @abstractmethod
    def scan_file(self, file_path: str) -> ScanResult:
        """Scan file on filesystem for threats."""
        pass
