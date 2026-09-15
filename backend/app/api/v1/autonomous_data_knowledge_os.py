"""
Phase 65: Autonomous Data & Knowledge Operating System FastAPI Router.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.services.data.service import AutonomousDataKnowledgeOperatingSystemService
from backend.app.schemas.autonomous_data_knowledge_os import (
    DataSourceCreate,
    DataConnectorCreate,
    DataIngestionJobCreate,
    DataPipelineCreate,
    DataProductCreate,
    DataContractCreate,
    DataQualityRuleCreate,
    DataQualityEvaluationRequest,
    DataIncidentCreate,
    DataLineageCreate,
    DataCatalogAssetCreate,
    BusinessTermCreate,
    SemanticModelCreate,
    MetricCreate,
    MasterEntityCreate,
    EntityResolutionRequest,
    KnowledgeNodeCreate,
    KnowledgeEdgeCreate,
    KnowledgeGraphQueryRequest,
    DocumentCreate,
    EnterpriseSearchRequest,
    EnterpriseMemoryCreate,
    KnowledgeRAGRequest,
    AIDatasetCreate,
    FeatureCreate,
    DataClassificationCreate,
    DataAccessPolicyCreate,
    DataAccessRequestCreate,
    DataRetentionPolicyCreate,
    LegalHoldCreate,
    DataDeletionRequestCreate,
    DataShareCreate,
    DataExportRequestCreate,
    DataAlertCreate,
    DataForecastCreate,
    DataSimulationCreate,
    DataCostCreate,
    DataBudgetCreate,
    DataSLOCreate,
    NaturalLanguageQueryRequest,
)

router = APIRouter(prefix="/data-knowledge-os", tags=["Autonomous Data & Knowledge Operating System"])


def get_service(db: Session = Depends(get_db)) -> AutonomousDataKnowledgeOperatingSystemService:
    return AutonomousDataKnowledgeOperatingSystemService(db)


# 1. Command Center Telemetry
@router.get("/command-center/summary", response_model=Dict[str, Any])
def get_command_center_summary(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.get_command_center_summary(tenant_id)


# 2. Autonomous Data Loop Execution
@router.post("/loop/run", response_model=Dict[str, Any])
def run_autonomous_data_loop(
    source_id: str,
    pipeline_id: str,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.run_autonomous_data_loop(tenant_id, source_id, pipeline_id)


# 3. Natural Language Query to Governed Data
@router.post("/query/nl", response_model=Dict[str, Any])
def execute_natural_language_query(
    payload: NaturalLanguageQueryRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.execute_natural_language_query(
        tenant_id=tenant_id,
        question=payload.question,
        user_id=payload.user_id,
        user_roles=payload.user_roles
    )


# 4. Data Sources & Connectors
@router.post("/sources", status_code=status.HTTP_201_CREATED)
def create_data_source(
    payload: DataSourceCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.sources.register_source(
        tenant_id=tenant_id,
        name=payload.name,
        source_type=payload.source_type,
        provider=payload.provider,
        owner=payload.owner,
        team=payload.team,
        environment=payload.environment,
        connection_url=payload.connection_url,
        refresh_rate=payload.refresh_rate,
        sensitivity=payload.sensitivity,
        classification=payload.classification
    )


@router.get("/sources")
def list_data_sources(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.sources.list_sources(tenant_id)


@router.post("/connectors", status_code=status.HTTP_201_CREATED)
def register_connector(
    payload: DataConnectorCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.connectors.register_connector(
        tenant_id=tenant_id,
        name=payload.name,
        connector_type=payload.connector_type,
        driver_module=payload.driver_module,
        configuration=payload.configuration
    )


@router.get("/connectors")
def list_connectors(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.connectors.list_connectors(tenant_id)


# 5. Ingestion Jobs & Pipelines
@router.post("/ingestion/jobs", status_code=status.HTTP_201_CREATED)
def create_ingestion_job(
    payload: DataIngestionJobCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.ingestion.create_ingestion_job(
        tenant_id=tenant_id,
        source_id=payload.source_id,
        job_type=payload.job_type
    )


@router.get("/ingestion/jobs")
def list_ingestion_jobs(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.ingestion.list_jobs(tenant_id)


@router.post("/pipelines", status_code=status.HTTP_201_CREATED)
def create_pipeline(
    payload: DataPipelineCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.pipelines.create_pipeline(
        tenant_id=tenant_id,
        name=payload.name,
        source_id=payload.source_id,
        destination_target=payload.destination_target,
        schedule_cron=payload.schedule_cron,
        trigger_type=payload.trigger_type,
        sla_minutes=payload.sla_minutes,
        owner=payload.owner
    )


@router.get("/pipelines")
def list_pipelines(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.pipelines.list_pipelines(tenant_id)


# 6. Data Lake & Warehouse & Marts
@router.get("/lake/assets")
def list_lake_assets(
    layer: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.lake.list_lake_assets(tenant_id, layer=layer)


@router.get("/warehouse/assets")
def list_warehouse_assets(
    asset_type: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.warehouse.list_warehouse_assets(tenant_id, asset_type=asset_type)


@router.get("/marts")
def list_data_marts(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.marts.list_marts(tenant_id)


# 7. Data Products & Contracts
@router.post("/products", status_code=status.HTTP_201_CREATED)
def create_data_product(
    payload: DataProductCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.products.create_product(
        tenant_id=tenant_id,
        name=payload.name,
        description=payload.description,
        owner=payload.owner,
        owner_team=payload.owner_team,
        tier=payload.tier,
        sla_tier=payload.sla_tier
    )


@router.get("/products")
def list_data_products(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.products.list_products(tenant_id)


@router.post("/contracts", status_code=status.HTTP_201_CREATED)
def create_data_contract(
    payload: DataContractCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.contracts.create_contract(
        tenant_id=tenant_id,
        name=payload.name,
        producer=payload.producer,
        consumer=payload.consumer,
        schema_definition=payload.schema_definition,
        quality_constraints=payload.quality_constraints,
        freshness_sla_minutes=payload.freshness_sla_minutes
    )


@router.get("/contracts")
def list_data_contracts(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.contracts.list_contracts(tenant_id)


# 8. Data Quality & Observability & Incidents
@router.post("/quality/rules", status_code=status.HTTP_201_CREATED)
def create_quality_rule(
    payload: DataQualityRuleCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.quality.create_quality_rule(
        tenant_id=tenant_id,
        rule_name=payload.rule_name,
        dataset_name=payload.dataset_name,
        dimension=payload.dimension,
        rule_type=payload.rule_type,
        expression=payload.expression,
        column_name=payload.column_name,
        severity=payload.severity
    )


@router.post("/quality/evaluate")
def evaluate_quality(
    payload: DataQualityEvaluationRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.quality.evaluate_dataset_quality(
        tenant_id=tenant_id,
        dataset_name=payload.dataset_name,
        sample_records=payload.sample_records
    )


@router.get("/quality/scores")
def list_quality_scores(
    dataset_name: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.quality.list_quality_scores(tenant_id, dataset_name=dataset_name)


@router.get("/incidents")
def list_incidents(
    status_filter: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.incidents.list_incidents(tenant_id, status=status_filter)


# 9. Lineage & Catalog & Glossary
@router.post("/lineage", status_code=status.HTTP_201_CREATED)
def record_lineage(
    payload: DataLineageCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.lineage.record_lineage(
        tenant_id=tenant_id,
        source_type=payload.source_type,
        source_id=payload.source_id,
        target_type=payload.target_type,
        target_id=payload.target_id,
        transformation_type=payload.transformation_type,
        transformation_logic=payload.transformation_logic
    )


@router.get("/lineage/graph")
def get_lineage_graph(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.lineage.get_full_lineage_graph(tenant_id)


@router.post("/catalog/assets", status_code=status.HTTP_201_CREATED)
def register_catalog_asset(
    payload: DataCatalogAssetCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.catalog.register_asset(
        tenant_id=tenant_id,
        name=payload.name,
        asset_type=payload.asset_type,
        description=payload.description,
        owner=payload.owner,
        domain=payload.domain,
        sensitivity=payload.sensitivity,
        tags=payload.tags
    )


@router.get("/catalog/assets")
def list_catalog_assets(
    domain: Optional[str] = None,
    search_query: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.catalog.list_assets(tenant_id, domain=domain, search_query=search_query)


@router.post("/glossary/terms", status_code=status.HTTP_201_CREATED)
def create_business_term(
    payload: BusinessTermCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.glossary.create_term(
        tenant_id=tenant_id,
        name=payload.name,
        definition=payload.definition,
        domain=payload.domain,
        owner=payload.owner,
        synonyms=payload.synonyms
    )


@router.get("/glossary/terms")
def list_glossary_terms(
    domain: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.glossary.list_terms(tenant_id, domain=domain)


# 10. Semantic Layer & Metric Store
@router.post("/semantic/models", status_code=status.HTTP_201_CREATED)
def create_semantic_model(
    payload: SemanticModelCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.semantic.create_model(
        tenant_id=tenant_id,
        name=payload.name,
        description=payload.description,
        source_table=payload.source_table,
        dimensions=payload.dimensions,
        measures=payload.measures,
        owner=payload.owner
    )


@router.get("/semantic/models")
def list_semantic_models(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.semantic.list_models(tenant_id)


@router.post("/metrics", status_code=status.HTTP_201_CREATED)
def create_metric(
    payload: MetricCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.metrics.create_metric(
        tenant_id=tenant_id,
        name=payload.name,
        definition=payload.definition,
        formula=payload.formula,
        source_entity=payload.source_entity,
        dimensions=payload.dimensions,
        owner=payload.owner,
        certification_status=payload.certification_status
    )


@router.get("/metrics")
def list_metrics(
    certification_status: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.metrics.list_metrics(tenant_id, status=certification_status)


# 11. Master Data & Entity Resolution
@router.post("/master-data/entities", status_code=status.HTTP_201_CREATED)
def create_master_entity(
    payload: MasterEntityCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.master_data.create_entity(
        tenant_id=tenant_id,
        entity_type=payload.entity_type,
        canonical_name=payload.canonical_name,
        attributes=payload.attributes
    )


@router.get("/master-data/entities")
def list_master_entities(
    entity_type: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.master_data.list_entities(tenant_id, entity_type=entity_type)


@router.post("/entity-resolution/match")
def resolve_entity(
    payload: EntityResolutionRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.entity_resolution.find_or_create_match(
        tenant_id=tenant_id,
        entity_type=payload.entity_type,
        incoming_name=payload.incoming_name,
        incoming_attributes=payload.incoming_attributes,
        auto_merge_threshold=payload.auto_merge_threshold
    )


# 12. Knowledge Graph
@router.post("/knowledge-graph/nodes", status_code=status.HTTP_201_CREATED)
def add_knowledge_node(
    payload: KnowledgeNodeCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.graph.add_node(
        tenant_id=tenant_id,
        node_type=payload.node_type,
        name=payload.name,
        properties=payload.properties,
        domain=payload.domain
    )


@router.post("/knowledge-graph/edges", status_code=status.HTTP_201_CREATED)
def add_knowledge_edge(
    payload: KnowledgeEdgeCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.graph.add_edge(
        tenant_id=tenant_id,
        source_node_id=payload.source_node_id,
        target_node_id=payload.target_node_id,
        relationship_type=payload.relationship_type,
        properties=payload.properties,
        confidence=payload.confidence
    )


@router.post("/knowledge-graph/query")
def query_knowledge_graph(
    payload: KnowledgeGraphQueryRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.graph.query_subgraph(
        tenant_id=tenant_id,
        root_node_id=payload.root_node_id,
        max_depth=payload.max_depth,
        relationship_types=payload.relationship_types
    )


@router.get("/knowledge-graph/stats")
def get_graph_stats(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.graph.get_graph_stats(tenant_id)


# 13. Documents & Enterprise Search & AI Memory & RAG
@router.post("/documents", status_code=status.HTTP_201_CREATED)
def register_document(
    payload: DocumentCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.documents.register_document(
        tenant_id=tenant_id,
        title=payload.title,
        file_type=payload.file_type,
        storage_path=payload.storage_path,
        text_content=payload.text_content,
        summary=payload.summary,
        entities=payload.entities,
        classification=payload.classification
    )


@router.get("/documents")
def list_documents(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.documents.list_documents(tenant_id)


@router.post("/search/hybrid")
def enterprise_search(
    payload: EnterpriseSearchRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.search.hybrid_search(
        tenant_id=tenant_id,
        query=payload.query,
        user_id=payload.user_id,
        limit=payload.limit
    )


@router.post("/memory", status_code=status.HTTP_201_CREATED)
def create_enterprise_memory(
    payload: EnterpriseMemoryCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.memory.create_memory(
        tenant_id=tenant_id,
        content=payload.content,
        memory_type=payload.memory_type,
        validation_status=payload.validation_status,
        entity_id=payload.entity_id,
        source_reference=payload.source_reference,
        confidence=payload.confidence,
        sensitivity=payload.sensitivity
    )


@router.get("/memory")
def list_enterprise_memories(
    memory_type: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.memory.list_memories(tenant_id, memory_type=memory_type)


@router.post("/rag/retrieve")
def execute_knowledge_rag(
    payload: KnowledgeRAGRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.rag.retrieve(
        tenant_id=tenant_id,
        query=payload.query,
        user_id=payload.user_id
    )


# 14. Governance & Privacy & Access Control
@router.post("/governance/classifications", status_code=status.HTTP_201_CREATED)
def create_classification(
    payload: DataClassificationCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.classification.create_classification(
        tenant_id=tenant_id,
        asset_id=payload.asset_id,
        classification_level=payload.classification_level,
        detected_categories=payload.detected_categories,
        confidence_score=payload.confidence_score,
        policy_tags=payload.policy_tags
    )


@router.get("/governance/classifications")
def list_classifications(
    level: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.classification.list_classifications(tenant_id, level=level)


@router.post("/access/policies", status_code=status.HTTP_201_CREATED)
def create_access_policy(
    payload: DataAccessPolicyCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.access_control.create_policy(
        tenant_id=tenant_id,
        name=payload.name,
        policy_type=payload.policy_type,
        resource_pattern=payload.resource_pattern,
        rules=payload.rules,
        row_level_filters=payload.row_level_filters,
        column_masks=payload.column_masks
    )


@router.get("/access/policies")
def list_access_policies(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.access_control.list_policies(tenant_id)


@router.post("/access/requests", status_code=status.HTTP_201_CREATED)
def create_access_request(
    payload: DataAccessRequestCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.access_control.create_request(
        tenant_id=tenant_id,
        requester_id=payload.requester_id,
        requester_type=payload.requester_type,
        target_resource=payload.target_resource,
        access_level=payload.access_level,
        business_justification=payload.business_justification,
        intended_purpose=payload.intended_purpose
    )


@router.get("/access/requests")
def list_access_requests(
    status_filter: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.access_control.list_requests(tenant_id, status=status_filter)


# 15. Retention & Deletion & Shares & Exports
@router.post("/retention/policies", status_code=status.HTTP_201_CREATED)
def create_retention_policy(
    payload: DataRetentionPolicyCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.retention.create_retention_policy(
        tenant_id=tenant_id,
        name=payload.name,
        dataset_pattern=payload.dataset_pattern,
        retention_days=payload.retention_days,
        action_after_expiry=payload.action_after_expiry,
        legal_basis=payload.legal_basis
    )


@router.post("/retention/legal-holds", status_code=status.HTTP_201_CREATED)
def create_legal_hold(
    payload: LegalHoldCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.retention.create_legal_hold(
        tenant_id=tenant_id,
        matter_name=payload.matter_name,
        custodian_id=payload.custodian_id,
        target_scope=payload.target_scope,
        placed_by=payload.placed_by,
        reason=payload.reason
    )


@router.post("/deletion/requests", status_code=status.HTTP_201_CREATED)
def submit_deletion_request(
    payload: DataDeletionRequestCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.deletion.submit_deletion_request(
        tenant_id=tenant_id,
        target_scope=payload.target_scope,
        deletion_type=payload.deletion_type,
        requested_by=payload.requested_by,
        reason=payload.reason
    )


@router.post("/sharing/shares", status_code=status.HTTP_201_CREATED)
def create_data_share(
    payload: DataShareCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.sharing.create_share(
        tenant_id=tenant_id,
        name=payload.name,
        shared_by=payload.shared_by,
        recipient_tenant_id=payload.recipient_tenant_id,
        recipient_email=payload.recipient_email,
        resource_ids=payload.resource_ids,
        share_type=payload.share_type
    )


@router.post("/exports/requests", status_code=status.HTTP_201_CREATED)
def request_data_export(
    payload: DataExportRequestCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.exports.request_export(
        tenant_id=tenant_id,
        user_id=payload.user_id,
        dataset_id=payload.dataset_id,
        format_type=payload.format_type,
        destination_target=payload.destination_target,
        purpose=payload.purpose
    )


# 16. Analytics & Alerts & FinOps Costs & SLOs
@router.post("/analytics/query")
def execute_self_service_analytics(
    data_product_id: Optional[str] = None,
    metrics: Optional[List[str]] = Query(None),
    dimensions: Optional[List[str]] = Query(None),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.analytics.execute_self_service_query(
        tenant_id=tenant_id,
        data_product_id=data_product_id,
        metric_names=metrics,
        dimensions=dimensions
    )


@router.post("/alerts", status_code=status.HTTP_201_CREATED)
def create_alert(
    payload: DataAlertCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.alerts.create_alert(
        tenant_id=tenant_id,
        name=payload.name,
        alert_type=payload.alert_type,
        target_resource=payload.target_resource,
        condition_expression=payload.condition_expression,
        severity=payload.severity,
        recipients=payload.recipients
    )


@router.post("/forecasting/generate", status_code=status.HTTP_201_CREATED)
def generate_forecast(
    payload: DataForecastCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.forecasting.generate_forecast(
        tenant_id=tenant_id,
        metric_name=payload.metric_name,
        horizon_days=payload.horizon_days,
        model_algorithm=payload.model_name
    )


@router.post("/simulation/run", status_code=status.HTTP_201_CREATED)
def run_simulation(
    payload: DataSimulationCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.simulation.run_simulation(
        tenant_id=tenant_id,
        scenario_name=payload.scenario_name,
        parameters=payload.parameters
    )


@router.post("/costs", status_code=status.HTTP_201_CREATED)
def record_cost(
    payload: DataCostCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.costs.record_cost(
        tenant_id=tenant_id,
        asset_id=payload.asset_id,
        cost_category=payload.cost_category,
        cost_amount=payload.cost_amount,
        billing_period=payload.billing_period,
        currency=payload.currency
    )


@router.get("/costs/summary")
def get_cost_summary(
    billing_period: str = Query(...),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.costs.get_cost_summary(tenant_id, billing_period)


@router.post("/slos", status_code=status.HTTP_201_CREATED)
def create_slo(
    payload: DataSLOCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.reliability.create_slo(
        tenant_id=tenant_id,
        asset_id=payload.asset_id,
        slo_type=payload.slo_type,
        target_percentage=payload.target_percentage,
        target_value=payload.target_value
    )


@router.get("/slos")
def list_slos(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDataKnowledgeOperatingSystemService = Depends(get_service)
):
    return service.reliability.list_slos(tenant_id)
