import { api } from './client';

export interface Metric {
  id: string;
  tenant_id: string;
  metric_key: string;
  name: string;
  description: string;
  category: string;
  formula: string;
  source_tables: string[];
  dimensions: string[];
  time_window_default: string;
  version: string;
  owner: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface ExecutiveOverview {
  overview_timestamp: string;
  pipeline_win_rate_pct: number;
  active_projects_count: number;
  estimation_variance_pct: number;
  sla_compliance_pct: number;
  realized_revenue_usd: number;
  ai_cost_usd: number;
  top_insights_count: number;
  top_insights: Array<{
    id: string;
    title: string;
    category: string;
    confidence: string;
  }>;
}

export interface FunnelStage {
  stage: string;
  count: number;
  conversion_to_next_pct: number;
}

export interface SalesIntelligence {
  time_window: string;
  overall_win_rate_pct: number;
  funnel: FunnelStage[];
  score_calibration: Record<string, { count: number; won: number; conversion_pct: number }>;
  sample_size: number;
  freshness: string;
}

export interface DeliveryIntelligence {
  total_completed_projects: number;
  total_estimated_hours: number;
  total_actual_hours: number;
  average_variance_pct: number;
  mean_abs_error_pct: number;
  underestimated_projects_count: number;
  overestimated_projects_count: number;
  on_target_projects_count: number;
  service_variances: Array<{ service: string; avg_variance_pct: number; project_count: number }>;
  scope_changes_summary: {
    total_change_requests: number;
    avg_changes_per_project: number;
    primary_root_cause: string;
  };
  quality_summary: {
    total_defects_recorded: number;
    escaped_to_uat_or_support: number;
    leakage_rate_pct: number;
  };
}

export interface SupportIntelligence {
  time_window: string;
  total_requests: number;
  resolved_count: number;
  open_count: number;
  avg_resolution_hours: number;
  sla_compliance_pct: number;
  categories: Array<{ category: string; count: number; pct: number }>;
  reopen_rate_pct: number;
}

export interface AIOperationsIntelligence {
  total_invocations: number;
  total_tokens_consumed: number;
  total_estimated_cost_usd: number;
  cost_per_lead_usd: number;
  cost_per_project_usd: number;
  human_revision_rate_pct: number;
  breakdown_by_agent: Array<{ agent: string; cost_usd: number; invocations: number }>;
}

export interface FinancialIntelligence {
  authoritative_currency: string;
  revenue: {
    actual_realized: number;
    forecast_pipeline: number;
    estimated_proposals: number;
  };
  costs: {
    actual_direct_labor: number;
    actual_ai_tokens: number;
    actual_infrastructure: number;
    actual_total_cost: number;
  };
  contribution_margin_pct: number;
  governance_rule: string;
}

export interface InsightEvidence {
  id: string;
  source_type: string;
  sample_count: number;
  baseline_value?: number;
  observed_value?: number;
  variance_pct?: number;
  details: Record<string, any>;
  created_at: string;
}

export interface BusinessInsight {
  id: string;
  tenant_id: string;
  title: string;
  description: string;
  category: string;
  confidence: string;
  sample_size: number;
  time_window: string;
  affected_entities: Record<string, any>;
  recommended_action?: string;
  status: string;
  created_by: string;
  reviewed_by?: string;
  reviewed_at?: string;
  created_at: string;
  evidence_items?: InsightEvidence[];
}

export interface BusinessRecommendation {
  id: string;
  insight_id?: string;
  title: string;
  recommendation: string;
  reason: string;
  expected_benefit: string;
  potential_downside: string;
  confidence: string;
  affected_workflow: string;
  status: string;
  decision_reason?: string;
  reviewed_by?: string;
  reviewed_at?: string;
  created_at: string;
}

export interface Experiment {
  id: string;
  tenant_id: string;
  title: string;
  hypothesis: string;
  target_workflow: string;
  target_metric: string;
  baseline_value: number;
  target_value: number;
  sample_target: number;
  current_sample_count: number;
  status: string;
  created_by: string;
  started_at?: string;
  completed_at?: string;
  conclusion?: string;
  created_at: string;
  metrics?: Array<{
    id: string;
    metric_name: string;
    is_primary: boolean;
    baseline_value: number;
    current_value: number;
    unit: string;
  }>;
}

export interface SemanticQueryResult {
  query_key: string;
  intent: string;
  parameters: Record<string, any>;
  data: any;
  summary: string;
  evidence_notes: string[];
}

export const analyticsApi = {
  getOverview: (tenantId: string = 'default_tenant'): Promise<ExecutiveOverview> =>
    api<ExecutiveOverview>(`/analytics/overview?tenant_id=${tenantId}`),

  getSalesIntelligence: (tenantId: string = 'default_tenant', timeWindow: string = '30d'): Promise<SalesIntelligence> =>
    api<SalesIntelligence>(`/analytics/sales?tenant_id=${tenantId}&time_window=${timeWindow}`),

  getDeliveryIntelligence: (tenantId: string = 'default_tenant', timeWindow: string = '30d'): Promise<DeliveryIntelligence> =>
    api<DeliveryIntelligence>(`/analytics/delivery?tenant_id=${tenantId}&time_window=${timeWindow}`),

  getSupportIntelligence: (tenantId: string = 'default_tenant', timeWindow: string = '30d'): Promise<SupportIntelligence> =>
    api<SupportIntelligence>(`/analytics/support?tenant_id=${tenantId}&time_window=${timeWindow}`),

  getAIOperations: (tenantId: string = 'default_tenant'): Promise<AIOperationsIntelligence> =>
    api<AIOperationsIntelligence>(`/analytics/ai?tenant_id=${tenantId}`),

  getFinancial: (tenantId: string = 'default_tenant'): Promise<FinancialIntelligence> =>
    api<FinancialIntelligence>(`/analytics/financial?tenant_id=${tenantId}`),

  listMetrics: (tenantId: string = 'default_tenant', category?: string): Promise<Metric[]> => {
    const params = new URLSearchParams({ tenant_id: tenantId });
    if (category) params.append('category', category);
    return api<Metric[]>(`/analytics/metrics?${params.toString()}`);
  },

  executeSemanticQuery: (query: string, tenantId: string = 'default_tenant'): Promise<SemanticQueryResult> =>
    api<SemanticQueryResult>(`/analytics/query?tenant_id=${tenantId}`, {
      method: 'POST',
      body: JSON.stringify({ query }),
    }),

  runLearningCycle: (tenantId: string = 'default_tenant'): Promise<{ status: string; insights_generated: number; message: string }> =>
    api<{ status: string; insights_generated: number; message: string }>(`/analytics/learning-cycle?tenant_id=${tenantId}`, {
      method: 'POST',
    }),

  listInsights: (tenantId: string = 'default_tenant', category?: string, status?: string): Promise<BusinessInsight[]> => {
    const params = new URLSearchParams({ tenant_id: tenantId });
    if (category) params.append('category', category);
    if (status) params.append('status', status);
    return api<BusinessInsight[]>(`/insights?${params.toString()}`);
  },

  getInsight: (insightId: string): Promise<BusinessInsight> =>
    api<BusinessInsight>(`/insights/${insightId}`),

  reviewInsight: (insightId: string, action: string, reviewedBy: string = 'user'): Promise<BusinessInsight> =>
    api<BusinessInsight>(`/insights/${insightId}/review`, {
      method: 'POST',
      body: JSON.stringify({ action, reviewed_by: reviewedBy }),
    }),

  listRecommendations: (tenantId: string = 'default_tenant', status?: string): Promise<BusinessRecommendation[]> => {
    const params = new URLSearchParams({ tenant_id: tenantId });
    if (status) params.append('status', status);
    return api<BusinessRecommendation[]>(`/insights/recommendations?${params.toString()}`);
  },

  reviewRecommendation: (recId: string, action: string, reviewer: string = 'user', notes?: string): Promise<BusinessRecommendation> =>
    api<BusinessRecommendation>(`/insights/recommendations/${recId}/review`, {
      method: 'POST',
      body: JSON.stringify({ action, reviewer, notes }),
    }),

  listExperiments: (tenantId: string = 'default_tenant', status?: string): Promise<Experiment[]> => {
    const params = new URLSearchParams({ tenant_id: tenantId });
    if (status) params.append('status', status);
    return api<Experiment[]>(`/experiments?${params.toString()}`);
  },

  createExperiment: (data: {
    title: string;
    hypothesis: string;
    target_workflow: string;
    target_metric: string;
    baseline_value: number;
    target_value: number;
    sample_target: number;
  }, tenantId: string = 'default_tenant'): Promise<Experiment> =>
    api<Experiment>(`/experiments?tenant_id=${tenantId}`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  evaluateExperiment: (expId: string): Promise<any> =>
    api<any>(`/experiments/${expId}/evaluate`, {
      method: 'POST',
    }),
};
