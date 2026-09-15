import { api } from './client';

export interface StrategicObjective {
  id?: string;
  objective_id?: string;
  objective_code: string;
  name: string;
  description?: string;
  strategic_pillar: string;
  owner: string;
  priority: string;
  start_date: string;
  target_date: string;
  baseline_value: number;
  target_value: number;
  current_value: number;
  unit: string;
  status: string;
  confidence_score: number;
  confidence?: number;
  progress_percentage: number;
  evidence_summary?: string;
  version: number;
}

export interface KeyResult {
  id?: string;
  kr_code: string;
  objective_id: string;
  name: string;
  baseline_value: number;
  target_value: number;
  current_value: number;
  unit: string;
  progress_percentage: number;
  measurement_method: string;
  source_metric?: string;
  owner: string;
  confidence: number;
  deadline: string;
}

export interface StrategicInitiative {
  id?: string;
  initiative_code: string;
  title: string;
  description?: string;
  category: string;
  owner: string;
  status: string;
  expected_value_usd: number;
  estimated_cost_usd: number;
  required_fte_capacity: number;
  estimated_duration_weeks: number;
  priority_score: number;
  risk_score: number;
  feasibility_score: number;
  is_funded: boolean;
  version: number;
}

export interface OptimizationResult {
  run_code: string;
  status: string;
  runtime_seconds: number;
  budget_limit_usd: number;
  allocated_budget_usd: number;
  budget_utilization_percentage: number;
  capacity_limit_fte: number;
  allocated_capacity_fte: number;
  capacity_utilization_percentage: number;
  total_expected_value_usd: number;
  net_expected_benefit_usd: number;
  selected_initiatives: Array<{
    code: string;
    title: string;
    expected_value_usd: number;
    cost_usd: number;
    fte: number;
  }>;
  binding_constraints: string[];
  explanation: string;
}

export type OptimizationRun = OptimizationResult;

export interface ParetoPlan {
  plan_code: string;
  title: string;
  growth_score: number;
  profitability_score: number;
  risk_score: number;
  selected_initiatives: string[];
  total_cost_usd: number;
  expected_net_benefit_usd: number;
  is_pareto_optimal: boolean;
}

export interface ParetoFrontier {
  frontier_id?: string;
  frontier_packages?: any[];
  pareto_front_plans?: ParetoPlan[];
  trade_off_notes?: string;
}

export interface StrategicDecisionRecord {
  id: string;
  decision_id?: string;
  title?: string;
  decision?: string;
  rationale?: string;
  date?: string;
  author?: string;
  status?: string;
  question?: string;
  created_at?: string;
  selected_option?: any;
  decided_by?: string;
  impact_rating?: string;
}

export interface FeasibilityItem {
  objective_code: string;
  objective_name: string;
  feasibility_level: string;
  feasibility_score: number;
  required_growth_percentage: number;
  historical_growth_rate_pct: number;
  capacity_factor: number;
  confidence: number;
  rationale: string;
}

export interface GapItem {
  objective_code: string;
  objective_name: string;
  strategic_pillar: string;
  current_value: number;
  target_value: number;
  gap_value: number;
  gap_percentage: number;
  estimated_budget_needed_usd: number;
  estimated_fte_needed: number;
  urgency: string;
}

export interface Scorecard {
  scorecard_code: string;
  period: string;
  composite_health_score: number;
  composite_health_percentage: number;
  dimensions: Record<string, number>;
  evaluation_time: string;
}

export interface StrategyOverview {
  status: string;
  tenant_id: string;
  composite_health_score: number;
  composite_health_percentage: number;
  total_active_objectives: number;
  total_active_initiatives: number;
  active_plans?: any;
  scorecard: Scorecard;
}

export type StrategicPlanOverview = StrategyOverview;

export interface StrategyCopilotResponse {
  query: string;
  intent: string;
  explanation: string;
  recommendations: string[];
  confidence: number;
  governance_notice: string;
  answer?: string;
  evidence?: any[];
  assumptions?: any[];
  suggested_actions?: string[];
}

export type StrategyCopilotQueryResponse = StrategyCopilotResponse;

export const strategyApi = {
  getOverview: (tenantId: string = 'default_tenant') =>
    api.get<StrategyOverview>('/api/v1/strategy/overview', { params: { tenant_id: tenantId } }),

  listObjectives: (pillar?: string) =>
    api.get<StrategicObjective[]>('/api/v1/strategy/objectives', { params: { pillar } }),

  getObjectives: (pillar?: string) =>
    api.get<StrategicObjective[]>('/api/v1/strategy/objectives', { params: { pillar } }),

  createObjective: (payload: {
    name: string;
    target_value: number;
    unit?: string;
    baseline_value?: number;
    strategic_pillar?: string;
    owner?: string;
    priority?: string;
    description?: string;
  }) =>
    api.post<StrategicObjective>('/api/v1/strategy/objectives', payload),

  updateObjectiveProgress: (code: string, payload: { current_value: number; evidence_summary?: string }) =>
    api.patch<StrategicObjective>(`/api/v1/strategy/objectives/${code}/progress`, payload),

  createKeyResult: (payload: {
    objective_id: string;
    name: string;
    target_value: number;
    unit?: string;
    baseline_value?: number;
    owner?: string;
  }) =>
    api.post<KeyResult>('/api/v1/strategy/key-results', payload),

  listInitiatives: () =>
    api.get<StrategicInitiative[]>('/api/v1/strategy/initiatives'),

  getInitiatives: () =>
    api.get<StrategicInitiative[]>('/api/v1/strategy/initiatives'),

  createInitiative: (payload: {
    title: string;
    owner: string;
    category?: string;
    expected_value_usd?: number;
    estimated_cost_usd?: number;
    required_fte_capacity?: number;
    estimated_duration_weeks?: number;
    description?: string;
  }) =>
    api.post<StrategicInitiative>('/api/v1/strategy/initiatives', payload),

  runOptimization: (payload: {
    plan_id?: string;
    budget_limit_usd?: number;
    capacity_limit_fte?: number;
    budget_ceiling?: number;
    fte_ceiling?: number;
    fte_capacity_ceiling?: number;
    weights?: any;
    objective_weights?: any;
    solver_type?: string;
    max_acceptable_risk?: number;
  }) =>
    api.post<OptimizationResult>('/api/v1/strategy/optimization', payload),

  getParetoFrontier: (budget: number = 100000, capacity: number = 8) =>
    api.get<ParetoPlan[]>('/api/v1/strategy/pareto', { params: { budget, capacity } }),

  getParetoAnalysis: async (budget: number = 100000, capacity: number = 8): Promise<ParetoFrontier> => {
    const plans = await api.get<ParetoPlan[]>('/api/v1/strategy/pareto', { params: { budget, capacity } });
    return { frontier_id: 'frontier-001', frontier_packages: Array.isArray(plans) ? plans : [], pareto_front_plans: Array.isArray(plans) ? plans : [] };
  },

  getFeasibility: () =>
    api.get<FeasibilityItem[]>('/api/v1/strategy/feasibility'),

  getGaps: () =>
    api.get<GapItem[]>('/api/v1/strategy/gaps'),

  getScorecard: (period: string = 'CURRENT_QUARTER') =>
    api.get<Scorecard>('/api/v1/strategy/scorecard', { params: { period } }),

  checkDrift: (payload: {
    metric_name?: string;
    expected_value: number;
    actual_value: number;
    drift_tolerance_pct?: number;
  }) =>
    api.post<{ has_drift: boolean; drift_event?: any }>('/api/v1/strategy/drift/check', payload),

  getDecisions: async () => [],
  approveDecision: async (id: string, rationale?: string) => ({}),
  rejectDecision: async (id: string, reason?: string) => ({}),

  recordDecision: (payload: {
    question: string;
    context_summary: string;
    selected_option: Record<string, any>;
    rationale: string;
    decision_owner: string;
    rejected_options?: Array<Record<string, any>>;
  }) =>
    api.post<any>('/api/v1/strategy/decisions', payload),

  queryCopilot: (query: string, tenantId: string = 'default_tenant') =>
    api.post<StrategyCopilotResponse>('/api/v1/strategy/copilot', { query, tenant_id: tenantId }),
};
