/**
 * Phase 61: Unified Engineering, SDLC, DevOps, CI/CD & Technical Operations OS API Client
 */

export interface EngineeringOverviewMetrics {
  tenant_id: string;
  organizations_count: number;
  teams_count: number;
  projects_count: number;
  repositories_count: number;
  open_pull_requests_count: number;
  services_count: number;
  healthy_services_pct: number;
  active_pipelines_count: number;
  open_incidents_count: number;
  sev0_sev1_incidents_count: number;
  dora_metrics: {
    deployment_frequency_per_day: number;
    lead_time_for_changes_hours: number;
    time_to_restore_service_hours: number;
    change_failure_rate_pct: number;
    dora_tier: string;
  };
  total_cloud_cost_monthly_usd: number;
  open_vulnerabilities_count: number;
  technical_debt_items_count: number;
  high_risk_changes_count: number;
  system_health: string;
  last_evaluated: string;
}

export interface EngineeringRepository {
  repository_id: string;
  tenant_id: string;
  name: string;
  provider: string;
  organization_name: string;
  default_branch: string;
  language: string;
  framework: string;
  owner_team: string;
  security_state: string;
  production_state: string;
  branch_protection_enabled: boolean;
  code_quality_score: number;
  updated_at: string;
}

export interface EngineeringPullRequest {
  pr_id: string;
  tenant_id: string;
  repository_id: string;
  repository_name: string;
  title: string;
  author: string;
  source_branch: string;
  target_branch: string;
  status: string;
  checks_passing: boolean;
  risk_level: string;
  review_verdicts: any[];
  linked_requirements: string[];
  linked_issues: string[];
  created_at: string;
}

export interface ServiceCatalogItem {
  service_id: string;
  tenant_id: string;
  name: string;
  owner_team: string;
  repository_id: string;
  runtime: string;
  environment: string;
  health_state: string;
  slo_target_pct: number;
  current_slo_pct: number;
  error_budget_remaining_pct: number;
  burn_rate_1h: number;
  monthly_cost_usd: number;
  dependencies: string[];
}

export interface CicdPipelineRecord {
  pipeline_id: string;
  tenant_id: string;
  repository_id: string;
  name: string;
  trigger_type: string;
  current_status: string;
  last_run_duration_sec: number;
  stages: {
    stage_name: string;
    status: string;
    duration_sec: number;
  }[];
  last_run_at: string;
}

export interface DeploymentRecord {
  deployment_id: string;
  tenant_id: string;
  service_id: string;
  application_name: string;
  version: string;
  environment: string;
  strategy: string;
  status: string;
  operator: string;
  approval_status: string;
  is_active: boolean;
  rollback_target_version?: string;
  started_at: string;
  completed_at?: string;
}

export interface ReleaseReadinessCheck {
  release_id: string;
  version: string;
  ready_for_production: boolean;
  readiness_score_pct: number;
  gate_checklist: {
    code_complete: boolean;
    tests_passing: boolean;
    coverage_acceptable: boolean;
    security_scans_clear: boolean;
    dependencies_vetted: boolean;
    documentation_updated: boolean;
    monitoring_configured: boolean;
    rollback_plan_verified: boolean;
    support_briefed: boolean;
    human_approval_obtained: boolean;
  };
  blockers: string[];
}

export interface IncidentRecord {
  incident_id: string;
  tenant_id: string;
  title: string;
  severity: string;
  status: string;
  affected_services: string[];
  customer_impact: string;
  mitigation_strategy?: string;
  timeline_events: any[];
  responders: string[];
  postmortem_completed: boolean;
  detected_at: string;
  resolved_at?: string;
}

export interface ChangeManagementRecord {
  change_id: string;
  tenant_id: string;
  title: string;
  reason: string;
  risk_level: string;
  risk_score: number;
  affected_systems: string[];
  requires_human_approval: boolean;
  approval_status: string;
  implementation_state: string;
  rollback_plan: string;
}

export interface DependencyVulnerabilityItem {
  vulnerability_id: string;
  tenant_id: string;
  cve_id: string;
  package_name: string;
  current_version: string;
  fixed_version: string;
  severity: string;
  exploitability: string;
  remediation_status: string;
  sla_deadline: string;
}

export interface TechnicalDebtItem {
  debt_id: string;
  tenant_id: string;
  title: string;
  category: string;
  component: string;
  principal_effort_days: number;
  interest_risk_level: string;
  annual_cost_usd: number;
  remediation_priority: string;
  status: string;
}

export interface FinOpsCostSummary {
  tenant_id: string;
  total_monthly_spend_usd: number;
  breakdown_by_category: {
    compute: number;
    storage: number;
    network: number;
    database: number;
    observability: number;
    ai_inference: number;
  };
  monthly_waste_estimate_usd: number;
  optimization_recommendations: {
    type: string;
    description: string;
    potential_savings_monthly_usd: number;
  }[];
}

export interface DeveloperCopilotResponse {
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

export async function fetchEngineeringOverview(tenantId = "default_tenant"): Promise<EngineeringOverviewMetrics> {
  const res = await fetch(`${API_BASE}/engineering-os/overview?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch Engineering OS overview");
  return res.json();
}

export async function fetchRepositories(tenantId = "default_tenant"): Promise<EngineeringRepository[]> {
  const res = await fetch(`${API_BASE}/engineering-os/repositories?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch repositories");
  return res.json();
}

export async function fetchPullRequests(tenantId = "default_tenant"): Promise<EngineeringPullRequest[]> {
  const res = await fetch(`${API_BASE}/engineering-os/pull-requests?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch pull requests");
  return res.json();
}

export async function fetchServices(tenantId = "default_tenant"): Promise<ServiceCatalogItem[]> {
  const res = await fetch(`${API_BASE}/engineering-os/services?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch services");
  return res.json();
}

export async function fetchPipelines(tenantId = "default_tenant"): Promise<CicdPipelineRecord[]> {
  const res = await fetch(`${API_BASE}/engineering-os/pipelines?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch CI/CD pipelines");
  return res.json();
}

export async function fetchDeployments(tenantId = "default_tenant"): Promise<DeploymentRecord[]> {
  const res = await fetch(`${API_BASE}/engineering-os/deployments?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch deployments");
  return res.json();
}

export async function fetchReleaseReadiness(releaseId = "rel_v2_4_0", tenantId = "default_tenant"): Promise<ReleaseReadinessCheck> {
  const res = await fetch(`${API_BASE}/engineering-os/releases/readiness?release_id=${releaseId}&tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch release readiness");
  return res.json();
}

export async function fetchIncidents(tenantId = "default_tenant"): Promise<IncidentRecord[]> {
  const res = await fetch(`${API_BASE}/engineering-os/incidents?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch incidents");
  return res.json();
}

export async function fetchChanges(tenantId = "default_tenant"): Promise<ChangeManagementRecord[]> {
  const res = await fetch(`${API_BASE}/engineering-os/changes?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch changes");
  return res.json();
}

export async function fetchVulnerabilities(tenantId = "default_tenant"): Promise<DependencyVulnerabilityItem[]> {
  const res = await fetch(`${API_BASE}/engineering-os/vulnerabilities?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch vulnerabilities");
  return res.json();
}

export async function fetchTechnicalDebt(tenantId = "default_tenant"): Promise<TechnicalDebtItem[]> {
  const res = await fetch(`${API_BASE}/engineering-os/technical-debt?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch technical debt");
  return res.json();
}

export async function fetchFinopsCosts(tenantId = "default_tenant"): Promise<FinOpsCostSummary> {
  const res = await fetch(`${API_BASE}/engineering-os/finops/costs?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch FinOps costs");
  return res.json();
}

export async function queryDeveloperCopilot(query: string, tenantId = "default_tenant"): Promise<DeveloperCopilotResponse> {
  const res = await fetch(`${API_BASE}/engineering-os/copilot/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, tenant_id: tenantId }),
  });
  if (!res.ok) throw new Error("Failed to query Developer Copilot");
  return res.json();
}
