"""Phase 65 Connectors Package & Service."""

from typing import Any, Dict, List, Optional
from backend.app.services.data.connectors.base import BaseConnector
from backend.app.services.data.connectors.registry import ConnectorRegistry, CONNECTOR_REGISTRY_MAP
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


class ConnectorsService:
    """Manages connector instances, registry, and live health monitoring."""

    def __init__(self, registry: Optional[ConnectorRegistry] = None):
        self.registry = registry or ConnectorRegistry()
        # Pre-seed default core connectors
        self.registry.create_connector("database", "conn_db_default", "Default Postgres Connector", {"db_type": "POSTGRES"})
        self.registry.create_connector("api", "conn_api_default", "Default REST API Connector", {})
        self.registry.create_connector("files", "conn_files_default", "Default Parquet Files Connector", {"format": "PARQUET"})
        self.registry.create_connector("cloud", "conn_cloud_default", "Default S3 Lakehouse Connector", {"provider": "AWS"})
        self.registry.create_connector("crm", "conn_crm_default", "Default CRM Connector", {})
        self.registry.create_connector("finance", "conn_fin_default", "Default Stripe Ledger Connector", {})
        self.registry.create_connector("documents", "conn_doc_default", "Default Documents Knowledge Connector", {})
        self.registry.create_connector("github", "conn_gh_default", "Default GitHub Repos Connector", {})

    def register_connector(self, connector_type: str, connector_id: str, name: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        conn = self.registry.create_connector(connector_type, connector_id, name, config)
        return {
            "connector_id": conn.connector_id,
            "name": conn.name,
            "type": connector_type,
            "status": "REGISTERED",
        }

    def list_connectors(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return self.registry.list_connectors()

    def test_connector(self, connector_id: str) -> Dict[str, Any]:
        conn = self.registry.get_connector(connector_id)
        if not conn:
            return {"connector_id": connector_id, "status": "NOT_FOUND", "passed": False}
        connected = conn.connect()
        health = conn.health_check()
        return {"connector_id": connector_id, "connected": connected, "health": health, "passed": connected}

    def discover_schema(self, connector_id: str) -> Dict[str, Any]:
        conn = self.registry.get_connector(connector_id)
        if not conn:
            return {"error": "Connector not found", "connector_id": connector_id}
        return conn.discover_schema()


__all__ = [
    "BaseConnector",
    "ConnectorRegistry",
    "CONNECTOR_REGISTRY_MAP",
    "DatabaseConnector",
    "ApiConnector",
    "FilesConnector",
    "CloudConnector",
    "ApplicationsConnector",
    "AnalyticsConnector",
    "MessagingConnector",
    "DocumentsConnector",
    "GithubConnector",
    "CrmConnector",
    "FinanceConnector",
    "EngineeringConnector",
    "CustomConnector",
    "ConnectorsService",
]
