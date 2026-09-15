import { api } from './client';

export interface DigitalTwinOverview {
  status: string;
  tenant_id: string;
  twin_models_count: number;
  composite_health_score: number;
  latest_snapshot_code: string;
  latest_snapshot_timestamp: string;
  state_hash: string;
  commercial_state: Record<string, any>;
  financial_state: Record<string, any>;
  delivery_state: Record<string, any>;
  ai_state: Record<string, any>;
  reliability_state: Record<string, any>;
  risk_state: Record<string, any>;
}

export interface StateSnapshot {
  id?: string;
  snapshot_code: string;
  tenant_id: string;
  title: string;
  snapshot_timestamp: string;
  commercial_state: Record<string, any>;
  delivery_state: Record<string, any>;
  operational_state: Record<string, any>;
  financial_state: Record<string, any>;
  ai_state: Record<string, any>;
  reliability_state: Record<string, any>;
  risk_state: Record<string, any>;
  composite_health_score: number;
  state_hash: string;
  is_valid: boolean;
}

export interface Scenario {
  id?: string;
  scenario_code: string;
  tenant_id: string;
  twin_model_id: string;
  name: string;
  description?: string;
  scenario_type: string;
  time_horizon: string;
  simulation_method: string;
  parameter_overrides: Record<string, number>;
  assumptions: Array<{
    name: string;
    parameter_code: string;
    baseline_value: number;
    assumed_value: number;
    delta_percentage: number;
  }>;
  constraints: Array<Record<string, any>>;
  status: string;
  created_by: string;
  version: number;
}

export interface SimulationResult {
  simulation_code: string;
  scenario_id: string;
  method: string;
  iterations: number;
  runtime_seconds: number;
  metrics_summary: {
    horizon_months?: number;
    cumulative_revenue_usd?: number;
    cumulative_gross_profit_usd?: number;
    cumulative_net_profit_usd?: number;
    cumulative_ai_cost_usd?: number;
    average_gross_margin_percentage?: number;
    ending_active_clients?: number;
    final_capacity_utilization_percentage?: number;
  };
  uncertainty_distribution: Record<string, {
    expected: number;
    p10: number;
    p25: number;
    p50: number;
    p75: number;
    p90: number;
    min: number;
    max: number;
  }>;
  constraint_violations: string[];
  is_sandboxed: boolean;
  assumptions_applied: Array<{ code: string; name: string; delta: number }>;
}

export interface ScenarioComparison {
  baseline: {
    scenario_name: string;
    scenario_code: string;
    cumulative_revenue_usd: number;
    cumulative_net_profit_usd: number;
    capacity_utilization_percentage: number;
    simulation_result: SimulationResult;
  };
  alternatives: Array<{
    scenario_name: string;
    scenario_code: string;
    method: string;
    cumulative_revenue_usd: number;
    revenue_delta_usd: number;
    revenue_delta_percentage: number;
    cumulative_net_profit_usd: number;
    net_profit_delta_usd: number;
    capacity_utilization_percentage: number;
    constraint_violations: string[];
    simulation_result: SimulationResult;
  }>;
}

export interface SensitivityRanking {
  parameter_code: string;
  parameter_name: string;
  target_metric: string;
  sensitivity_score: number;
  impact_level: string;
  low_impact_value: number;
  high_impact_value: number;
}

export interface CounterfactualResult {
  counterfactual_code: string;
  historical_event_id: string;
  hypothetical_condition: string;
  historical_actual: Record<string, any>;
  simulated_alternative: Record<string, any>;
  divergence_summary: string;
  limitations: string;
}

export interface DecisionOption {
  id?: string;
  option_code: string;
  title: string;
  scenario_id: string;
  expected_benefit_usd: number;
  expected_cost_usd: number;
  risk_score: number;
  confidence_score: number;
  tradeoff_summary: string;
}

export interface DecisionRecord {
  id?: string;
  decision_code: string;
  question: string;
  selected_option_id?: string;
  rationale: string;
  decision_owner: string;
  approved_at: string;
  scenario_version: number;
  status: string;
}

export interface OutcomeRecord {
  id?: string;
  decision_id?: string;
  scenario_id?: string;
  observed_period: string;
  predicted_metrics: Record<string, any>;
  actual_metrics: Record<string, any>;
  variance_percentage: number;
  model_error: number;
}

export interface CalibrationReport {
  calibrations_count: number;
  parameter_updates: Array<{
    parameter_code: string;
    recommended_action: string;
    reason: string;
  }>;
  average_prediction_error: number;
  summary: string;
}

export interface CopilotResponse {
  query: string;
  intent: string;
  scenario_generated?: Record<string, any>;
  simulation_result?: SimulationResult;
  explanation: string;
  confidence: number;
  governance_notice: string;
}

export const digitalTwinApi = {
  getOverview: (tenantId: string = 'default_tenant') =>
    api.get<DigitalTwinOverview>('/api/v1/digital-twin/overview', { params: { tenant_id: tenantId } }),

  getState: (tenantId: string = 'default_tenant') =>
    api.get<StateSnapshot>('/api/v1/digital-twin/state', { params: { tenant_id: tenantId } }),

  createSnapshot: (title: string, tenantId: string = 'default_tenant') =>
    api.post<StateSnapshot>('/api/v1/digital-twin/state/snapshot', { title }, { params: { tenant_id: tenantId } }),

  getParameters: () =>
    api.get<{ status: string; parameters: Record<string, any> }>('/api/v1/digital-twin/parameters'),

  createScenario: (payload: {
    name: string;
    scenario_type?: string;
    time_horizon?: string;
    simulation_method?: string;
    parameter_overrides?: Record<string, number>;
  }, tenantId: string = 'default_tenant') =>
    api.post<Scenario>('/api/v1/digital-twin/scenarios', payload, { params: { tenant_id: tenantId } }),

  runSimulation: (payload: {
    scenario_name?: string;
    parameter_overrides?: Record<string, number>;
    simulation_method?: string;
    time_horizon?: string;
    iterations?: number;
    random_seed?: number;
  }, tenantId: string = 'default_tenant') =>
    api.post<SimulationResult>('/api/v1/digital-twin/simulations/run', payload, { params: { tenant_id: tenantId } }),

  compareScenarios: (payload: {
    baseline_scenario_name?: string;
    baseline_overrides?: Record<string, number>;
    scenarios: Array<{ name: string; parameter_overrides: Record<string, number> }>;
    iterations?: number;
  }, tenantId: string = 'default_tenant') =>
    api.post<ScenarioComparison>('/api/v1/digital-twin/compare', payload, { params: { tenant_id: tenantId } }),

  getSensitivity: (payload: {
    target_metric?: string;
    parameter_overrides?: Record<string, number>;
    sweep_percentage?: number;
  }, tenantId: string = 'default_tenant') =>
    api.post<SensitivityRanking[]>('/api/v1/digital-twin/sensitivity', payload, { params: { tenant_id: tenantId } }),

  runCounterfactual: (payload: {
    historical_event_id: string;
    hypothetical_condition: string;
    historical_actual_metrics: Record<string, any>;
    hypothetical_parameter_overrides: Record<string, number>;
  }) =>
    api.post<CounterfactualResult>('/api/v1/digital-twin/counterfactuals', payload),

  recordDecision: (payload: {
    question: string;
    rationale: string;
    decision_owner: string;
    selected_option_id?: string;
  }) =>
    api.post<DecisionRecord>('/api/v1/digital-twin/decisions', payload),

  recordOutcome: (payload: {
    observed_period: string;
    predicted_metrics: Record<string, any>;
    actual_metrics: Record<string, any>;
    decision_id?: string;
    scenario_id?: string;
  }) =>
    api.post<OutcomeRecord>('/api/v1/digital-twin/outcomes', payload),

  runCalibration: (outcomes: Array<{
    observed_period: string;
    predicted_metrics: Record<string, any>;
    actual_metrics: Record<string, any>;
  }>) =>
    api.post<CalibrationReport>('/api/v1/digital-twin/calibration', outcomes),

  queryCopilot: (query: string, tenantId: string = 'default_tenant') =>
    api.post<CopilotResponse>('/api/v1/digital-twin/copilot', { query, tenant_id: tenantId }),
};
