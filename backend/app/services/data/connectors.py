"""Connectors management service for Phase 65."""

from typing import Any, Dict, List, Optional
from backend.app.services.data.connectors.registry import ConnectorRegistry


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

    def list_connectors(self) -> List[Dict[str, Any]]:
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
        conn.connect()
        return conn.discover_schema()
