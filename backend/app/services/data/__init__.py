import importlib.util
import os

_data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data.py"))
if os.path.exists(_data_file):
    _spec = importlib.util.spec_from_file_location("app.services.data_legacy", _data_file)
    if _spec and _spec.loader:
        _data_module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_data_module)
        DataPlatformService = getattr(_data_module, "DataPlatformService", None)
else:
    DataPlatformService = None

from backend.app.services.data.sources import SourcesService, SourcesService as DataSourceService
from backend.app.services.data.connectors import ConnectorsService, ConnectorsService as DataConnectorService
from backend.app.services.data.ingestion import IngestionService, IngestionService as DataIngestionService
from backend.app.services.data.pipelines import PipelinesService, PipelinesService as DataPipelineService
from backend.app.services.data.orchestration import OrchestrationService, OrchestrationService as PipelineOrchestrationService
from backend.app.services.data.lake import LakeService, LakeService as DataLakeService
from backend.app.services.data.warehouse import WarehouseService, WarehouseService as DataWarehouseService
from backend.app.services.data.marts import MartsService, MartsService as DataMartService
from backend.app.services.data.products import ProductsService, ProductsService as DataProductService
from backend.app.services.data.contracts import ContractsService, ContractsService as DataContractService
from backend.app.services.data.schema_registry import SchemaRegistryService
from backend.app.services.data.quality import QualityService, QualityService as DataQualityService
from backend.app.services.data.observability import ObservabilityService, ObservabilityService as DataObservabilityService
from backend.app.services.data.incidents import IncidentsService, IncidentsService as DataIncidentService
from backend.app.services.data.lineage import LineageService, LineageService as DataLineageService
from backend.app.services.data.catalog import CatalogService, CatalogService as DataCatalogService
from backend.app.services.data.metadata import MetadataService
from backend.app.services.data.glossary import GlossaryService, GlossaryService as BusinessGlossaryService
from backend.app.services.data.semantic_layer import SemanticLayerService
from backend.app.services.data.metrics import MetricsService, MetricsService as MetricStoreService
from backend.app.services.data.master_data import MasterDataService
from backend.app.services.data.entity_resolution import EntityResolutionService
from backend.app.services.data.knowledge_graph import KnowledgeGraphService
from backend.app.services.data.documents import DocumentsService, DocumentsService as DocumentKnowledgeService
from backend.app.services.data.search import SearchService, SearchService as EnterpriseSearchService
from backend.app.services.data.memory import MemoryService, MemoryService as EnterpriseMemoryService
from backend.app.services.data.retrieval import RetrievalService, RetrievalService as KnowledgeRAGService
from backend.app.services.data.datasets import DatasetsService, DatasetsService as AIDatasetService
from backend.app.services.data.features import FeaturesService, FeaturesService as FeatureStoreService
from backend.app.services.data.ai_governance import AiDataGovernanceService, AiDataGovernanceService as AIDataGovernanceService
from backend.app.services.data.privacy import PrivacyService
from backend.app.services.data.classification import DataClassificationService
from backend.app.services.data.access_control import DataAccessControlService
from backend.app.services.data.masking import DataMaskingService
from backend.app.services.data.retention import DataRetentionService
from backend.app.services.data.deletion import DataDeletionService
from backend.app.services.data.sharing import DataSharingService
from backend.app.services.data.exports import DataExportService
from backend.app.services.data.analytics import AnalyticsService
from backend.app.services.data.alerts import DataAlertService
from backend.app.services.data.forecasting import DataForecastingService
from backend.app.services.data.simulation import DataSimulationService
from backend.app.services.data.costs import DataCostService
from backend.app.services.data.security import DataSecurityService
from backend.app.services.data.reliability import DataReliabilityService
from backend.app.services.data.recommendations import DataRecommendationService
from backend.app.services.data.validation import QueryValidationService
from backend.app.services.data.service import AutonomousDataKnowledgeOperatingSystemService

__all__ = [
    "SourcesService",
    "DataSourceService",
    "ConnectorsService",
    "DataConnectorService",
    "IngestionService",
    "DataIngestionService",
    "PipelinesService",
    "DataPipelineService",
    "OrchestrationService",
    "PipelineOrchestrationService",
    "LakeService",
    "DataLakeService",
    "WarehouseService",
    "DataWarehouseService",
    "MartsService",
    "DataMartService",
    "ProductsService",
    "DataProductService",
    "ContractsService",
    "DataContractService",
    "SchemaRegistryService",
    "QualityService",
    "DataQualityService",
    "ObservabilityService",
    "DataObservabilityService",
    "IncidentsService",
    "DataIncidentService",
    "LineageService",
    "DataLineageService",
    "CatalogService",
    "DataCatalogService",
    "MetadataService",
    "GlossaryService",
    "BusinessGlossaryService",
    "SemanticLayerService",
    "MetricsService",
    "MetricStoreService",
    "MasterDataService",
    "EntityResolutionService",
    "KnowledgeGraphService",
    "DocumentsService",
    "DocumentKnowledgeService",
    "SearchService",
    "EnterpriseSearchService",
    "MemoryService",
    "EnterpriseMemoryService",
    "RetrievalService",
    "KnowledgeRAGService",
    "DatasetsService",
    "AIDatasetService",
    "FeaturesService",
    "FeatureStoreService",
    "AiDataGovernanceService",
    "AIDataGovernanceService",
    "PrivacyService",
    "DataClassificationService",
    "DataAccessControlService",
    "DataMaskingService",
    "DataRetentionService",
    "DataDeletionService",
    "DataSharingService",
    "DataExportService",
    "AnalyticsService",
    "DataAlertService",
    "DataForecastingService",
    "DataSimulationService",
    "DataCostService",
    "DataSecurityService",
    "DataReliabilityService",
    "DataRecommendationService",
    "QueryValidationService",
    "AutonomousDataKnowledgeOperatingSystemService",
    "DataPlatformService",
]
