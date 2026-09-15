"""Base types, enums, and utility structures for Phase 62 Enterprise Data Operating System."""

from enum import Enum
from typing import Any, Dict
import uuid


class DataDomainType(str, Enum):
    CUSTOMER = "CUSTOMER"
    PRODUCT = "PRODUCT"
    SALES = "SALES"
    MARKETING = "MARKETING"
    FINANCE = "FINANCE"
    OPERATIONS = "OPERATIONS"
    ENGINEERING = "ENGINEERING"
    SECURITY = "SECURITY"
    AI_ML = "AI_ML"
    HR = "HR"
    SUPPORT = "SUPPORT"
    GOVERNANCE = "GOVERNANCE"


class DataLayerType(str, Enum):
    BRONZE = "BRONZE"  # Raw immutable ingestion
    SILVER = "SILVER"  # Validated, cleansed, standardized
    GOLD = "GOLD"      # Business-ready curated data product


class IngestionMode(str, Enum):
    BATCH = "BATCH"
    MICRO_BATCH = "MICRO_BATCH"
    STREAMING = "STREAMING"
    CDC = "CDC"


class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class DataQualityDimension(str, Enum):
    COMPLETENESS = "COMPLETENESS"
    ACCURACY = "ACCURACY"
    CONSISTENCY = "CONSISTENCY"
    VALIDITY = "VALIDITY"
    UNIQUENESS = "UNIQUENESS"
    TIMELINESS = "TIMELINESS"


class DataIncidentSeverity(str, Enum):
    SEV0 = "SEV0"
    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"
    SEV4 = "SEV4"


def generate_data_id(prefix: str = "dat") -> str:
    """Generate unique deterministic identifier with domain prefix."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class AttrDict(dict):
    """Dictionary subclass supporting attribute-style read access and nested dictionary wrapping."""

    def __getattr__(self, name: str) -> Any:
        try:
            val = self[name]
            if isinstance(val, dict) and not isinstance(val, AttrDict):
                val = AttrDict(val)
                self[name] = val
            return val
        except KeyError:
            raise AttributeError(f"'AttrDict' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'AttrDict' object has no attribute '{name}'")
