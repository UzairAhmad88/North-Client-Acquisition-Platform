/**
 * Phase 63: Unified AI/ML Model Factory, MLOps, LLMOps, Evaluation & Production AI Operating System API Client
 */

export interface AiFactoryOverviewMetrics {
  total_projects: number;
  total_models: number;
  production_models: number;
  total_deployments: number;
  evaluation_suites: number;
  governed_prompts: number;
  active_drift_alerts: number;
  active_gpu_jobs: number;
  total_finops_cost_usd: number;
  platform_health_status: string;
  timestamp: string;
}

export interface AiProjectItem {
  id: string;
  tenant_id: string;
  name: string;
  description: string;
  owner: string;
  team: string;
  domain: string;
  objective: string;
  budget_allocated_usd: number;
  budget_spent_usd: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface AiDatasetVersionItem {
  id: string;
  tenant_id: string;
  project_id: string;
  dataset_name: string;
  version: string;
  source_lakehouse_dataset_id?: string;
  features_list: string[];
  label_column?: string;
  splits: Record<string, number>;
  row_count: number;
  bias_check_status: string;
  lineage_provenance: Record<string, any>;
  created_at: string;
}

export interface AiExperimentItem {
  id: string;
  tenant_id: string;
  project_id: string;
  name: string;
  description: string;
  model_type: string;
  framework: string;
  search_strategy: string;
  best_metric_name: string;
  best_metric_value?: number;
  status: string;
  created_at: string;
}

export interface AiExperimentRunItem {
  id: string;
  tenant_id: string;
  experiment_id: string;
  run_number: number;
  git_commit_hash?: string;
  dataset_version_id?: string;
  hyperparameters: Record<string, any>;
  metrics: Record<string, number>;
  hardware_specs: Record<string, any>;
  duration_seconds: number;
  cost_usd: number;
  artifacts_uri?: string;
  status: string;
  created_at: string;
}

export interface AiModelItem {
  id: string;
  tenant_id: string;
  project_id: string;
  name: string;
  description: string;
  model_type: string;
  framework: string;
  owner: string;
  steward?: string;
  current_stage: string;
  active_version: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface AiModelVersionItem {
  id: string;
  tenant_id: string;
  model_id: string;
  version: string;
  stage: string;
  training_run_id?: string;
  dataset_version_id?: string;
  artifacts_manifest: Record<string, any>;
  metrics_summary: Record<string, number>;
  supply_chain_sbom: Record<string, any>;
  is_signed: boolean;
  quality_gate_passed: boolean;
  security_scan_passed: boolean;
  governance_approved: boolean;
  created_at: string;
}

export interface AiEvaluationSuiteItem {
  id: string;
  tenant_id: string;
  name: string;
  suite_type: string;
  target_model_type: string;
  thresholds_config: Record<string, number>;
  test_cases_count: number;
  created_at: string;
}

export interface AiEvaluationResultItem {
  id: string;
  tenant_id: string;
  suite_id: string;
  model_version_id: string;
  evaluator_engine: string;
  judge_model?: string;
  passed: boolean;
  score: number;
  detailed_metrics: Record<string, any>;
  failure_reasons: string[];
  created_at: string;
}

export interface AiPromptItem {
  id: string;
  tenant_id: string;
  name: string;
  version: string;
  purpose: string;
  system_prompt: string;
  user_template: string;
  variables: string[];
  target_model_family: string;
  stage: string;
  token_budget_max: number;
  created_at: string;
}

export interface AiDeploymentItem {
  id: string;
  tenant_id: string;
  model_version_id: string;
  environment: string;
  strategy: string;
  traffic_weight_pct: number;
  endpoint_url?: string;
  min_replicas: number;
  max_replicas: number;
  current_replicas: number;
  status: string;
  rollback_target_version_id?: string;
  created_at: string;
}

export interface AiDriftEventItem {
  id: string;
  tenant_id: string;
  deployment_id: string;
  drift_type: string;
  metric_name: string;
  metric_value: number;
  threshold: number;
  is_breached: boolean;
  suggested_action: string;
  created_at: string;
}

export interface AiCopilotResponse {
  query: string;
  facts: string[];
  inferences: string[];
  hypotheses: string[];
  recommendations: string[];
  confidence_score: number;
  governance_notice: string;
  timestamp: string;
}

const API_BASE = '/api/v1/ai-factory';

export const aiModelFactoryApi = {
  getOverview: async (tenantId: string = 'default_tenant'): Promise<AiFactoryOverviewMetrics> => {
    const res = await fetch(`${API_BASE}/overview?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch AI platform overview');
    return res.json();
  },

  getProjects: async (tenantId: string = 'default_tenant'): Promise<AiProjectItem[]> => {
    const res = await fetch(`${API_BASE}/projects?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch AI projects');
    return res.json();
  },

  getModels: async (tenantId: string = 'default_tenant'): Promise<AiModelItem[]> => {
    const res = await fetch(`${API_BASE}/models?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch AI models');
    return res.json();
  },

  getExperiments: async (tenantId: string = 'default_tenant'): Promise<AiExperimentItem[]> => {
    const res = await fetch(`${API_BASE}/experiments?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch AI experiments');
    return res.json();
  },

  getDeployments: async (tenantId: string = 'default_tenant'): Promise<AiDeploymentItem[]> => {
    const res = await fetch(`${API_BASE}/deployments?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch AI deployments');
    return res.json();
  },

  getPrompts: async (tenantId: string = 'default_tenant'): Promise<AiPromptItem[]> => {
    const res = await fetch(`${API_BASE}/prompts?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch AI prompts');
    return res.json();
  },

  getDriftEvents: async (tenantId: string = 'default_tenant'): Promise<AiDriftEventItem[]> => {
    const res = await fetch(`${API_BASE}/drift?tenant_id=${encodeURIComponent(tenantId)}`);
    if (!res.ok) throw new Error('Failed to fetch AI drift events');
    return res.json();
  },

  queryCopilot: async (query: string, tenantId: string = 'default_tenant'): Promise<AiCopilotResponse> => {
    const res = await fetch(`${API_BASE}/copilot/query?tenant_id=${encodeURIComponent(tenantId)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    if (!res.ok) throw new Error('Failed to query AI Copilot');
    return res.json();
  },
};
