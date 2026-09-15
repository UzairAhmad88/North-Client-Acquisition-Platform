"""Connector Registry, Discovery, and Factory for Phase 65."""

from typing import Any, Dict, List, Optional, Type
from datetime import datetime, timezone
from backend.app.services.data.connectors.base import BaseConnector
from backend.app.services.data.connectors.database_connector import DatabaseConnector
from backend.app.services.data.connectors.api_connector import ApiConnector
from backend.app.services.data.connectors.files_connector import FilesConnector
from backend.app.services.data.connectors.cloud_connector import CloudConnector
from backend.app.services.data.connectors.applications_connector import ApplicationsConnector
from backend.app.services.data.connectors.analytics_connector import AnalyticsConnector
from backend.app.services.data.connectors.messaging_connector import MessagingConnector
from backend.app.services.data.connectors.documents_connector import DocumentsConnector
from backend.app.services.data.connectors.github_connector import GithubConnector
from backend.app.services.data.connectors.crm_connector import CrmConnector
from backend.app.services.data.connectors.finance_connector import FinanceConnector
from backend.app.services.data.connectors.engineering_connector import EngineeringConnector
from backend.app.services.data.connectors.custom_connector import CustomConnector


CONNECTOR_REGISTRY_MAP: Dict[str, Type[BaseConnector]] = {
    "database": DatabaseConnector,
    "api": ApiConnector,
    "files": FilesConnector,
    "cloud": CloudConnector,
    "applications": ApplicationsConnector,
    "analytics": AnalyticsConnector,
    "messaging": MessagingConnector,
    "documents": DocumentsConnector,
    "github": GithubConnector,
    "crm": CrmConnector,
    "finance": FinanceConnector,
    "engineering": EngineeringConnector,
    "custom": CustomConnector,
}


class ConnectorRegistry:
    """Central registry and lifecycle manager for all data connectors."""

    def __init__(self):
        self._instances: Dict[str, BaseConnector] = {}

    def get_supported_types(self) -> List[str]:
        return list(CONNECTOR_REGISTRY_MAP.keys())

    def create_connector(
        self, connector_type: str, connector_id: str, name: str, config: Optional[Dict[str, Any]] = None
    ) -> BaseConnector:
        normalized_type = connector_type.lower()
        connector_cls = CONNECTOR_REGISTRY_MAP.get(normalized_type, CustomConnector)
        instance = connector_cls(connector_id=connector_id, name=name, config=config or {})
        self._instances[connector_id] = instance
        return instance

    def get_connector(self, connector_id: str) -> Optional[BaseConnector]:
        return self._instances.get(connector_id)

    def list_connectors(self) -> List[Dict[str, Any]]:
        results = []
        for cid, conn in self._instances.items():
            results.append({
                "connector_id": cid,
                "name": conn.name,
                "is_connected": conn.is_connected,
                "last_sync": conn.last_sync_time.isoformat() if conn.last_sync_time else None,
            })
        return results

    def health_check_all(self) -> List[Dict[str, Any]]:
        return [conn.health_check() for conn in self._instances.values()]
