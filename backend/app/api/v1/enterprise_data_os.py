"""FastAPI Router for Phase 62: Unified Enterprise Data Operating System."""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.enterprise_data_os.service import EnterpriseDataOperatingSystemService
    from backend.app.schemas.enterprise_data_os import (
        DataDomainCreateRequest,
        DataSourceCreateRequest,
        DataPipelineCreateRequest,
        DataLakehouseDatasetCreateRequest,
        DataContractCreateRequest,
        DataProductCreateRequest,
        SemanticMetricCreateRequest,
        DataAccessGrantRequest,
        DataCopilotQueryRequest,
        SandboxedSqlQueryRequest,
    )
except ImportError:
    from app.services.enterprise_data_os.service import EnterpriseDataOperatingSystemService
    from app.schemas.enterprise_data_os import (
        DataDomainCreateRequest,
        DataSourceCreateRequest,
        DataPipelineCreateRequest,
        DataLakehouseDatasetCreateRequest,
        DataContractCreateRequest,
        DataProductCreateRequest,
        SemanticMetricCreateRequest,
        DataAccessGrantRequest,
        DataCopilotQueryRequest,
        SandboxedSqlQueryRequest,
    )

router = APIRouter(prefix="/data-os", tags=["enterprise-data-os"])
_service_instance = EnterpriseDataOperatingSystemService()


def get_service() -> EnterpriseDataOperatingSystemService:
    return _service_instance


@router.get("/overview")
async def get_overview(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    return dict(service.get_enterprise_data_overview(tenant_id))


@router.get("/domains")
async def list_domains(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.sources_service._domains.values())


@router.post("/domains")
async def create_domain(
    req: DataDomainCreateRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    res = service.sources_service.create_data_domain(
        tenant_id=req.tenant_id,
        name=req.name,
        slug=req.slug,
        owner_team=req.owner_team,
        lead_steward_email=req.lead_steward_email,
        description=req.description or "",
    )
    return dict(res)


@router.get("/sources")
async def list_sources(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.sources_service._sources.values())


@router.post("/sources")
async def register_source(
    req: DataSourceCreateRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    res = service.sources_service.register_data_source(
        tenant_id=req.tenant_id,
        name=req.name,
        source_type=req.source_type,
        provider=req.provider,
        domain_id=req.domain_id,
        connection_endpoint=req.connection_endpoint,
        auth_type=req.auth_type,
        data_classification=req.data_classification,
    )
    return dict(res)


@router.get("/pipelines")
async def list_pipelines(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.pipelines_service._pipelines.values())


@router.post("/pipelines")
async def create_pipeline(
    req: DataPipelineCreateRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    res = service.pipelines_service.create_data_pipeline(
        tenant_id=req.tenant_id,
        name=req.name,
        source_datasets=req.source_datasets,
        target_dataset=req.target_dataset,
        schedule_type=req.schedule_type,
        sla_minutes=req.sla_minutes,
        owner_team=req.owner_team,
    )
    return dict(res)


@router.get("/datasets")
async def list_datasets(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.pipelines_service._datasets.values())


@router.post("/datasets")
async def register_dataset(
    req: DataLakehouseDatasetCreateRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    res = service.pipelines_service.register_lakehouse_dataset(
        tenant_id=req.tenant_id,
        domain_id=req.domain_id,
        name=req.name,
        layer=req.layer,
        format_type=req.format_type,
        storage_uri=req.storage_uri,
        partition_keys=req.partition_keys,
        record_count=req.record_count,
        size_mb=req.size_mb,
    )
    return dict(res)


@router.get("/contracts")
async def list_contracts(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.schemas_service._contracts.values())


@router.post("/contracts")
async def create_contract(
    req: DataContractCreateRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    res = service.schemas_service.create_data_contract(
        tenant_id=req.tenant_id,
        producer_team=req.producer_team,
        consumer_team=req.consumer_team,
        dataset_id=req.dataset_id,
        schema_version=req.schema_version,
        freshness_sla_minutes=req.freshness_sla_minutes,
        quality_threshold_pct=req.quality_threshold_pct,
    )
    return dict(res)


@router.get("/products")
async def list_products(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.schemas_service._products.values())


@router.post("/products")
async def publish_product(
    req: DataProductCreateRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    res = service.schemas_service.publish_data_product(
        tenant_id=req.tenant_id,
        domain_id=req.domain_id,
        name=req.name,
        purpose=req.purpose,
        owner_team=req.owner_team,
        underlying_datasets=req.underlying_datasets,
    )
    return dict(res)


@router.get("/catalog")
async def list_catalog_assets(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.catalog_service._assets.values())


@router.get("/glossary")
async def list_glossary_terms(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.catalog_service._glossary.values())


@router.get("/metrics")
async def list_semantic_metrics(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.catalog_service._semantic_metrics.values())


@router.post("/metrics")
async def define_semantic_metric(
    req: SemanticMetricCreateRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    res = service.catalog_service.define_semantic_metric(
        tenant_id=req.tenant_id,
        name=req.name,
        definition=req.definition,
        formula_sql=req.formula_sql,
        dimensions=req.dimensions,
        source_table=req.source_table,
        owner_team=req.owner_team,
    )
    return dict(res)


@router.get("/quality/rules")
async def list_quality_rules(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.quality_service._rules.values())


@router.get("/lineage")
async def list_lineage_edges(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.governance_service._lineage_edges.values())


@router.post("/access/grants")
async def create_access_grant(
    req: DataAccessGrantRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    res = service.governance_service.grant_data_access(
        tenant_id=req.tenant_id,
        principal_id=req.principal_id,
        dataset_id=req.dataset_id,
        access_level=req.access_level,
        row_filter_expression=req.row_filter_expression,
        masked_columns=req.masked_columns,
        approved_by=req.approved_by,
    )
    return dict(res)


@router.get("/features")
async def list_features(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.features_service._features.values())


@router.get("/finops/spend")
async def list_finops_spend(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.finops_service._finops_records.values())


@router.get("/incidents")
async def list_incidents(
    tenant_id: str = Query("default_tenant"),
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> List[Dict[str, Any]]:
    return list(service.finops_service._incidents.values())


@router.post("/sql/execute")
async def execute_sql(
    req: SandboxedSqlQueryRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    res = service.features_service.execute_sandboxed_sql_query(
        tenant_id=req.tenant_id,
        sql_query=req.sql_query,
        read_only=req.read_only,
    )
    return dict(res)


@router.post("/copilot/query")
async def query_data_copilot(
    req: DataCopilotQueryRequest,
    service: EnterpriseDataOperatingSystemService = Depends(get_service),
) -> Dict[str, Any]:
    return service.copilot_service.query_data_copilot(
        tenant_id=req.tenant_id,
        query=req.query,
    )
