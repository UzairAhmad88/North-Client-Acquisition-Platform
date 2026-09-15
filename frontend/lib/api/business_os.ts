import { api } from './client';

export interface KPISnapshot {
  kpi_id: string;
  name: string;
  category: string;
  value: number;
  previous_value?: number;
  target_value?: number;
  variance?: number;
  variance_pct?: number;
  unit: string;
  currency: string;
  source_domain: string;
  version: string;
  freshness_seconds: number;
  is_stale: boolean;
  status: 'EXCEEDING' | 'ON_TRACK' | 'AT_RISK' | 'OFF_TRACK';
  calculated_at: string;
}

export interface HealthDimension {
  dimension_name: string;
  score: number;
  weight_pct: number;
  status: 'HEALTHY' | 'STABLE' | 'WATCH' | 'AT_RISK' | 'CRITICAL';
  positive_drivers: string[];
  negative_drivers: string[];
  signals_count: number;
}

export interface BusinessHealthReport {
  overall_health_score: number;
  overall_status: 'HEALTHY' | 'STABLE' | 'WATCH' | 'AT_RISK' | 'CRITICAL';
  dimensions: Record<string, HealthDimension>;
  key_strengths: string[];
  critical_risks: string[];
  reconciliation_alerts: string[];
  evaluated_at: string;
}

export interface StrategicKeyResult {
  kr_id: string;
  objective_id: string;
  title: string;
  target_value: number;
  current_value: number;
  unit: string;
  status: string;
  progress_pct: number;
  owner?: string;
}

export interface StrategicInitiative {
  initiative_id: string;
  objective_id: string;
  title: string;
  owner: string;
  budget: number;
  priority: string;
  status: string;
  progress_pct: number;
  milestones: any[];
  dependencies: any[];
}

export interface StrategicObjective {
  objective_id: string;
  title: string;
  description?: string;
  timeframe: string;
  priority: string;
  status: string;
  owner: string;
  overall_progress_pct: number;
  key_results: StrategicKeyResult[];
  initiatives: StrategicInitiative[];
}

export interface DepartmentScorecard {
  department_name: string;
  category: string;
  overall_status: string;
  scorecard_items: Array<{
    kpi_id: string;
    name: string;
    category: string;
    target: number;
    actual: number;
    variance: number;
    variance_pct?: number;
    unit: string;
    currency: string;
    trend: string;
    status: string;
    owner: string;
  }>;
  generated_at: string;
}

export interface OrganizationalRisk {
  risk_id: string;
  title: string;
  description: string;
  category: string;
  probability: string;
  impact: string;
  risk_score: number;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  owner: string;
  status: string;
  identified_at: string;
  due_date?: string;
  evidence_signals: string[];
  mitigation_strategy: string;
  contingency_plan: string;
  last_reviewed_at: string;
}

export interface DecisionOption {
  option_id: string;
  title: string;
  description: string;
  expected_benefits: string[];
  expected_costs: string[];
  risks: string[];
  dependencies: string[];
  estimated_impact: string;
  confidence: string;
  evidence_references: string[];
}

export interface DecisionRecord {
  decision_id: string;
  title: string;
  business_question: string;
  context_summary: string;
  priority: string;
  status: string;
  candidate_options: DecisionOption[];
  ai_recommendation?: string;
  ai_recommendation_rationale?: string;
  chosen_option_id?: string;
  chosen_option_title?: string;
  decision_rationale?: string;
  decided_by?: string;
  decided_at?: string;
  evidence_signals: string[];
  expected_outcome: string;
  actual_outcome?: string;
  outcome_variance_analysis?: string;
  lessons_learned: string[];
  created_at: string;
  review_due_date?: string;
}

export interface ScenarioSimulationResult {
  scenario_id: string;
  scenario_name: string;
  scenario_type: string;
  simulated_revenue: number;
  simulated_profit: number;
  simulated_margin_pct: number;
  capacity_utilization_pct: number;
  cash_requirement: number;
  risk_level: string;
  assumptions_applied: Record<string, any>;
  sensitivity_rankings: Array<{
    variable: string;
    sensitivity_level: string;
    impact_description: string;
    elasticity_score: number;
  }>;
  generated_at: string;
  is_production_isolated: boolean;
}

export interface ExecutiveBriefing {
  briefing_id: string;
  frequency: string;
  title: string;
  summary_paragraph: string;
  key_metrics_snapshot: Record<string, any>;
  what_changed_summary: string[];
  top_decisions_required: any[];
  critical_risks: any[];
  upcoming_deadlines: any[];
  recommended_attention_areas: string[];
  generated_at: string;
}

export interface BusinessCalendarEvent {
  event_id: string;
  title: string;
  event_type: string;
  event_date: string;
  related_entity_id: string;
  related_entity_name: string;
  severity: string;
  owner: string;
  is_completed: boolean;
}

export interface CopilotResponse {
  query_id: string;
  user_query: string;
  intent: string;
  answer_markdown: string;
  confidence: string;
  evidence_sources: any[];
  suggested_followups: string[];
  action_prohibited: boolean;
  prohibited_reason?: string;
  answered_at: string;
}

export const businessOSApi = {
  getOverview: async () => {
    return api.get<any>('/executive/overview');
  },
  getHealth: async () => {
    return api.get<BusinessHealthReport>('/executive/health');
  },
  getBriefing: async (frequency: string = 'DAILY') => {
    return api.get<ExecutiveBriefing>(`/executive/briefings?frequency=${frequency}`);
  },
  getCalendar: async () => {
    return api.get<BusinessCalendarEvent[]>('/executive/calendar');
  },
  queryCopilot: async (query: string, user_role: string = 'EXECUTIVE') => {
    return api.post<CopilotResponse>('/executive/assistant/query', { query, user_role });
  },
  listObjectives: async () => {
    return api.get<StrategicObjective[]>('/strategy/objectives');
  },
  listScorecards: async () => {
    return api.get<DepartmentScorecard[]>('/strategy/scorecards');
  },
  listKPIs: async (category?: string) => {
    const url = category ? `/kpis?category=${category}` : '/kpis';
    return api.get<KPISnapshot[]>(url);
  },
  listRisks: async (category?: string, minSeverity?: string) => {
    let url = '/risks?';
    if (category) url += `category=${category}&`;
    if (minSeverity) url += `min_severity=${minSeverity}&`;
    return api.get<OrganizationalRisk[]>(url);
  },
  listDecisions: async (status?: string) => {
    const url = status ? `/decisions?status=${status}` : '/decisions';
    return api.get<DecisionRecord[]>(url);
  },
  recordDecision: async (decisionId: string, chosenOptionId: string, rationale: string, decidedBy: string) => {
    return api.post<DecisionRecord>(`/decisions/${decisionId}/decide`, {
      chosen_option_id: chosenOptionId,
      decision_rationale: rationale,
      decided_by: decidedBy,
    });
  },
  recordDecisionOutcome: async (decisionId: string, actualOutcome: string, varianceAnalysis: string, lessons: string[]) => {
    return api.post<DecisionRecord>(`/decisions/${decisionId}/outcome`, {
      actual_outcome: actualOutcome,
      outcome_variance_analysis: varianceAnalysis,
      lessons_learned: lessons,
    });
  },
  runScenario: async (payload: any) => {
    return api.post<ScenarioSimulationResult>('/scenarios/run', payload);
  },
};
