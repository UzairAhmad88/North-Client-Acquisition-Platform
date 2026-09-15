"""Base connector interface for Phase 65 Autonomous Data & Knowledge OS."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


class BaseConnector(ABC):
    """Abstract Base Class for all standard enterprise data connectors.
    
    Every connector implements:
      - connect()
      - discover_schema()
      - extract()
      - validate()
      - load()
      - health_check()
      - disconnect()
    """

    def __init__(self, connector_id: str, name: str, config: Optional[Dict[str, Any]] = None):
        self.connector_id = connector_id
        self.name = name
        self.config = config or {}
        self.is_connected = False
        self.last_sync_time: Optional[datetime] = None

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection with external service/source."""
        pass

    @abstractmethod
    def discover_schema(self) -> Dict[str, Any]:
        """Inspect and return schema definition/types of the data source."""
        pass

    @abstractmethod
    def extract(self, query_or_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extract raw records from source."""
        pass

    @abstractmethod
    def validate(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate extracted records against constraints."""
        pass

    @abstractmethod
    def load(self, records: List[Dict[str, Any]], target_destination: str) -> Dict[str, Any]:
        """Load records into target lakehouse, warehouse, or mart."""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Verify connectivity, latency, and auth validity."""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Gracefully release connection handles."""
        pass
