"""
Phase 65: Autonomous Data AI Agents Package
"""

from agents.data.discovery_agent import DataDiscoveryAgent
from agents.data.ingestion_agent import DataIngestionAgent
from agents.data.quality_agent import DataQualityAgent
from agents.data.schema_agent import SchemaAgent
from agents.data.lineage_agent import LineageAgent
from agents.data.catalog_agent import CatalogAgent
from agents.data.metadata_agent import MetadataAgent
from agents.data.semantic_agent import SemanticAgent
from agents.data.graph_agent import GraphAgent
from agents.data.governance_agent import GovernanceAgent
from agents.data.privacy_agent import PrivacyAgent
from agents.data.anomaly_agent import AnomalyAgent
from agents.data.optimization_agent import OptimizationAgent
from agents.data.documentation_agent import DocumentationAgent
from agents.data.data_product_agent import DataProductAgent

__all__ = [
    "DataDiscoveryAgent",
    "DataIngestionAgent",
    "DataQualityAgent",
    "SchemaAgent",
    "LineageAgent",
    "CatalogAgent",
    "MetadataAgent",
    "SemanticAgent",
    "GraphAgent",
    "GovernanceAgent",
    "PrivacyAgent",
    "AnomalyAgent",
    "OptimizationAgent",
    "DocumentationAgent",
    "DataProductAgent",
]
