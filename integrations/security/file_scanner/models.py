"""Malware and File Security Scanner Models."""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field


class ScanStatus(str, Enum):
    """Status of file security scan."""
    CLEAN = "CLEAN"
    INFECTED = "INFECTED"
    SUSPICIOUS = "SUSPICIOUS"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


class ScanResult(BaseModel):
    """Detailed file scan result."""
    status: ScanStatus
    scanner_name: str
    threat_name: Optional[str] = None
    threat_category: Optional[str] = None
    confidence_score: float = 1.0
    scan_duration_ms: int = 0
    scanned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_output: Optional[str] = None
    details: Dict[str, str] = Field(default_factory=dict)
