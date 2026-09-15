/**
 * Phase 62: Unified Enterprise Data Operating System API Client
 */

export interface EnterpriseDataOverviewMetrics {
  tenant_id: string;
  domains_count: number;
  sources_count: number;
  pipelines_count: number;
  datasets_count: number;
  data_products_count: number;
  data_contracts_count: number;
  catalog_assets_count: number;
  semantic_metrics_count: number;
  composite_data_quality_pct: number;
  total_monthly_spend_usd: number;
  active_data_incidents_count: number;
  system_health: string;
  last_evaluated: string;
}

export interface DataDomainItem {
  domain_id: string;
  tenant_id: string;
  name: string;
  slug: string;
  owner_team: string;
  lead_steward_email: string;
  description: string;
  data_products_count: number;
  created_at: string;
}

export interface DataSourceItem {
  source_id: string;
  tenant_id: string;
  name: string;
  source_type: string;
  provider: string;
  domain_id?: string;
  connection_endpoint: string;
  auth_type: string;
  data_classification: string;
  status: string;
  reliability_score: number;
  registered_at: string;
}

export interface DataPipelineItem {
  pipeline_id: string;
  tenant_id: string;
  name: string;
  source_datasets: string[];
  target_dataset: string;
  schedule_type: string;
  sla_minutes: int;
  status: string;
  owner_team: string;
  last_run_status: string;
  created_at: string;
}

export interface LakehouseDatasetItem {
  dataset_id: string;
  tenant_id: string;
  domain_id: string;
  name: string;
  layer: string; // BRONZE, SILVER, GOLD
  format: string;
  storage_uri: string;
  partition_keys: string[];
  record_count: number;
  size_mb: number;
  classification: string;
  quality_status: string;
  created_at: string;
}

export interface DataContractItem {
  contract_id: string;
  tenant_id: string;
  producer_team: string;
  consumer_team: string;
  dataset_id: string;
  schema_version: string;
  freshness_sla_minutes: number;
  quality_threshold_pct: number;
  status: string;
  sla_compliance_pct: number;
  created_at: string;
}

export interface DataProductItem {
  product_id: string;
  tenant_id: string;
  domain_id: string;
  name: string;
  purpose: string;
  owner_team: string;
  underlying_datasets: string[];
  consumers_count: number;
  quality_score: number;
  health_status: string;
  published_at: string;
}

export interface DataCatalogAssetItem {
  asset_id: string;
  tenant_id: string;
  asset_name: string;
  asset_type: string;
  domain_name: string;
  owner_email: string;
  classification: string;
  quality_score: number;
  tags: string[];
  description: string;
  indexed_at: string;
}

export interface BusinessGlossaryTermItem {
  term_id: string;
  tenant_id: string;
  term_name: string;
  definition: string;
  domain_name: string;
  owner_email: string;
  synonyms: string[];
  related_metrics: string[];
  created_at: string;
}

export interface SemanticMetricItem {
  metric_id: string;
  tenant_id: string;
  name: string;
  definition: string;
  formula_sql: string;
  dimensions: string[];
  source_table: string;
  owner_team: string;
  is_authoritative: boolean;
  created_at: string;
}

export interface DataQualityRuleItem {
  rule_id: string;
  tenant_id: string;
  dataset_id: string;
  rule_type: string;
  dimension: string;
  severity: string;
  pass_rate_pct: number;
  is_active: boolean;
  last_evaluated_at: string;
}

export interface DataLineageEdgeItem {
  edge_id: string;
  tenant_id: string;
  source_asset_id: string;
  target_asset_id: string;
  relationship_type: string;
  transformation_name?: string;
  created_at: string;
}

export interface FeatureStoreItem {
  feature_id: string;
  tenant_id: string;
  name: string;
  entity_name: string;
  data_type: string;
  source_dataset_id: string;
  transformation_logic: string;
  freshness_minutes: number;
  is_online_ready: boolean;
  created_at: string;
}

export interface DataFinopsSpendItem {
  cost_id: string;
  tenant_id: string;
  domain_name: string;
  total_monthly_spend_usd: number;
  breakdown: {
    storage: number;
    compute: number;
    query: number;
    ai_rag: number;
  };
  waste_estimate_usd: number;
  optimization_recommendations: string[];
  recorded_at: string;
}

export interface DataIncidentItem {
  incident_id: string;
  tenant_id: string;
  title: string;
  severity: string;
  incident_type: string;
  affected_datasets: string[];
  status: string;
  declared_by: string;
  detected_at: string;
}

export interface DataCopilotResponse {
  query: string;
  facts: string[];
  inferences: string[];
  hypotheses: string[];
  recommendations: string[];
  confidence_score: number;
  governance_notice: string;
  timestamp: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchEnterpriseDataOverview(tenantId = "default_tenant"): Promise<EnterpriseDataOverviewMetrics> {
  const res = await fetch(`${API_BASE}/data-os/overview?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch Enterprise Data OS overview");
  return res.json();
}

export async function fetchDataDomains(tenantId = "default_tenant"): Promise<DataDomainItem[]> {
  const res = await fetch(`${API_BASE}/data-os/domains?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data domains");
  return res.json();
}

export async function fetchDataSources(tenantId = "default_tenant"): Promise<DataSourceItem[]> {
  const res = await fetch(`${API_BASE}/data-os/sources?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data sources");
  return res.json();
}

export async function fetchDataPipelines(tenantId = "default_tenant"): Promise<DataPipelineItem[]> {
  const res = await fetch(`${API_BASE}/data-os/pipelines?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data pipelines");
  return res.json();
}

export async function fetchLakehouseDatasets(tenantId = "default_tenant"): Promise<LakehouseDatasetItem[]> {
  const res = await fetch(`${API_BASE}/data-os/datasets?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch lakehouse datasets");
  return res.json();
}

export async function fetchDataContracts(tenantId = "default_tenant"): Promise<DataContractItem[]> {
  const res = await fetch(`${API_BASE}/data-os/contracts?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data contracts");
  return res.json();
}

export async function fetchDataProducts(tenantId = "default_tenant"): Promise<DataProductItem[]> {
  const res = await fetch(`${API_BASE}/data-os/products?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data products");
  return res.json();
}

export async function fetchDataCatalog(tenantId = "default_tenant"): Promise<DataCatalogAssetItem[]> {
  const res = await fetch(`${API_BASE}/data-os/catalog?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data catalog");
  return res.json();
}

export async function fetchBusinessGlossary(tenantId = "default_tenant"): Promise<BusinessGlossaryTermItem[]> {
  const res = await fetch(`${API_BASE}/data-os/glossary?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch business glossary");
  return res.json();
}

export async function fetchSemanticMetrics(tenantId = "default_tenant"): Promise<SemanticMetricItem[]> {
  const res = await fetch(`${API_BASE}/data-os/metrics?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch semantic metrics");
  return res.json();
}

export async function fetchDataQualityRules(tenantId = "default_tenant"): Promise<DataQualityRuleItem[]> {
  const res = await fetch(`${API_BASE}/data-os/quality/rules?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data quality rules");
  return res.json();
}

export async function fetchDataLineage(tenantId = "default_tenant"): Promise<DataLineageEdgeItem[]> {
  const res = await fetch(`${API_BASE}/data-os/lineage?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data lineage");
  return res.json();
}

export async function fetchFeatures(tenantId = "default_tenant"): Promise<FeatureStoreItem[]> {
  const res = await fetch(`${API_BASE}/data-os/features?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch feature store items");
  return res.json();
}

export async function fetchDataFinopsSpend(tenantId = "default_tenant"): Promise<DataFinopsSpendItem[]> {
  const res = await fetch(`${API_BASE}/data-os/finops/spend?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data FinOps spend");
  return res.json();
}

export async function fetchDataIncidents(tenantId = "default_tenant"): Promise<DataIncidentItem[]> {
  const res = await fetch(`${API_BASE}/data-os/incidents?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch data incidents");
  return res.json();
}

export async function queryDataCopilot(query: string, tenantId = "default_tenant"): Promise<DataCopilotResponse> {
  const res = await fetch(`${API_BASE}/data-os/copilot/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, tenant_id: tenantId }),
  });
  if (!res.ok) throw new Error("Failed to query Data Copilot");
  return res.json();
}
