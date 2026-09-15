/**
 * Phase 64: Autonomous Engineering Operating System & AI Software Factory API Client
 */

export interface EngineeringFactoryOverviewMetrics {
  active_projects_count: number;
  requirements_count: number;
  tasks_count: number;
  open_pull_requests_count: number;
  total_build_runs_count: number;
  test_suites_count: number;
  sbom_packages_count: number;
  deployments_count: number;
  services_count: number;
  healthy_services_count: number;
  active_incidents_count: number;
  self_healing_runbooks_count: number;
  total_finops_spend_usd: number;
  status: string;
}

export interface EngineeringProjectItem {
  id: string;
  tenant_id: string;
  name: string;
  description?: string;
  owner: string;
  team: string;
  repository_url?: string;
  tech_stack: string[];
  budget_allocated_usd: number;
  budget_spent_usd: number;
  status: string;
  created_at: string;
}

export interface EngineeringRequirementItem {
  id: string;
  tenant_id: string;
  project_id: string;
  title: string;
  description: string;
  requirement_type: string;
  priority: string;
  owner: string;
  status: string;
  ambiguity_score: number;
  dependencies: string[];
  created_at: string;
}

export interface ArchitectureComponentItem {
  id: string;
  tenant_id: string;
  project_id: string;
  name: string;
  component_type: string;
  owner_team: string;
  runtime_environment: string;
  slo_target_latency_p95_ms: number;
  slo_target_availability_pct: number;
  dependencies_json: string[];
  created_at: string;
}

export interface EngineeringTaskItem {
  id: string;
  tenant_id: string;
  requirement_id?: string;
  title: string;
  description: string;
  task_type: string;
  priority: string;
  assigned_agent: string;
  status: string;
  branch_name?: string;
  tokens_consumed: number;
  created_at: string;
}

export interface PullRequestItem {
  id: string;
  tenant_id: string;
  repository_id: string;
  title: string;
  source_branch: string;
  target_branch: string;
  author: string;
  status: string;
  risk_score_composite: number;
  risk_breakdown_json: Record<string, number>;
  ci_pipeline_status: string;
  is_merged: boolean;
  created_at: string;
}

export interface CiBuildRunItem {
  id: string;
  tenant_id: string;
  pipeline_id: string;
  commit_sha: string;
  branch: string;
  build_number: number;
  duration_seconds: number;
  status: string;
  logs_uri?: string;
  artifacts_generated: string[];
  created_at: string;
}

export interface TestSuiteItem {
  id: string;
  tenant_id: string;
  repository_id: string;
  suite_name: string;
  suite_type: string;
  total_tests_count: number;
  passed_tests_count: number;
  failed_tests_count: number;
  flaky_rate_pct: number;
  duration_seconds: number;
  last_run_at: string;
}

export interface SbomPackageItem {
  id: string;
  tenant_id: string;
  repository_id: string;
  package_name: string;
  version: string;
  license_type: string;
  is_license_compliant: boolean;
  vulnerabilities_count: number;
  scanned_at: string;
}

export interface AutonomousDeploymentItem {
  id: string;
  tenant_id: string;
  service_name: string;
  environment: string;
  strategy: string;
  version: string;
  traffic_weight_pct: number;
  verification_status: string;
  status: string;
  rollback_target_version?: string;
  created_at: string;
}

export interface ServiceCatalogItem {
  id: string;
  tenant_id: string;
  name: string;
  owner_team: string;
  slo_target_availability_pct: number;
  current_availability_pct: number;
  error_budget_remaining_pct: number;
  p95_latency_ms: number;
  status: string;
  created_at: string;
}

export interface EngineeringIncidentItem {
  id: string;
  tenant_id: string;
  service_name: string;
  severity: string;
  title: string;
  description?: string;
  correlated_root_cause_hypothesis?: string;
  remediation_status: string;
  mitigation_action_taken?: string;
  created_at: string;
}

export interface SelfHealingRunbookItem {
  id: string;
  tenant_id: string;
  name: string;
  trigger_condition: string;
  target_service: string;
  action_type: string;
  is_autonomous_approved: boolean;
  executions_count: number;
  success_rate_pct: number;
  created_at: string;
}

export interface CopilotQueryResponse {
  query: string;
  category: string;
  answer: string;
  citations: string[];
  answered_at: string;
}

const API_BASE = '/api/v1/engineering-factory';

export const autonomousEngineeringOsApi = {
  getOverview: async (tenantId: string = 'default_tenant'): Promise<EngineeringFactoryOverviewMetrics> => {
    const res = await fetch(`${API_BASE}/overview?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch Engineering Command Center metrics');
    return res.json();
  },

  getProjects: async (tenantId: string = 'default_tenant'): Promise<EngineeringProjectItem[]> => {
    const res = await fetch(`${API_BASE}/projects?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch projects');
    return res.json();
  },

  getRequirements: async (tenantId: string = 'default_tenant'): Promise<EngineeringRequirementItem[]> => {
    const res = await fetch(`${API_BASE}/requirements?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch requirements');
    return res.json();
  },

  getArchitectureComponents: async (tenantId: string = 'default_tenant'): Promise<ArchitectureComponentItem[]> => {
    const res = await fetch(`${API_BASE}/architecture/components?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch architecture components');
    return res.json();
  },

  getTasks: async (tenantId: string = 'default_tenant'): Promise<EngineeringTaskItem[]> => {
    const res = await fetch(`${API_BASE}/tasks?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch tasks');
    return res.json();
  },

  getPullRequests: async (tenantId: string = 'default_tenant'): Promise<PullRequestItem[]> => {
    const res = await fetch(`${API_BASE}/pull-requests?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch pull requests');
    return res.json();
  },

  getBuildRuns: async (tenantId: string = 'default_tenant'): Promise<CiBuildRunItem[]> => {
    const res = await fetch(`${API_BASE}/ci-cd/build-runs?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch build runs');
    return res.json();
  },

  getTestSuites: async (tenantId: string = 'default_tenant'): Promise<TestSuiteItem[]> => {
    const res = await fetch(`${API_BASE}/testing/suites?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch test suites');
    return res.json();
  },

  getSbomPackages: async (tenantId: string = 'default_tenant'): Promise<SbomPackageItem[]> => {
    const res = await fetch(`${API_BASE}/security/sbom-packages?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch SBOM packages');
    return res.json();
  },

  getDeployments: async (tenantId: string = 'default_tenant'): Promise<AutonomousDeploymentItem[]> => {
    const res = await fetch(`${API_BASE}/deployments?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch deployments');
    return res.json();
  },

  getServiceCatalog: async (tenantId: string = 'default_tenant'): Promise<ServiceCatalogItem[]> => {
    const res = await fetch(`${API_BASE}/service-catalog?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch service catalog');
    return res.json();
  },

  getIncidents: async (tenantId: string = 'default_tenant'): Promise<EngineeringIncidentItem[]> => {
    const res = await fetch(`${API_BASE}/incidents?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch incidents');
    return res.json();
  },

  getSelfHealingRunbooks: async (tenantId: string = 'default_tenant'): Promise<SelfHealingRunbookItem[]> => {
    const res = await fetch(`${API_BASE}/self-healing/runbooks?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch runbooks');
    return res.json();
  },

  queryCopilot: async (query: string, tenantId: string = 'default_tenant'): Promise<CopilotQueryResponse> => {
    const res = await fetch(`${API_BASE}/copilot/query?tenant_id=${encodeURIComponent(tenantId)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    if (!res.ok) throw new Error('Failed to query Software Factory Copilot');
    return res.json();
  },
};
