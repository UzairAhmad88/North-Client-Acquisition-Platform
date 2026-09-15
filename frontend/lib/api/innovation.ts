/**
 * TypeScript API Client for Phase 55 — Unified Product & Innovation Intelligence, Idea Discovery, Validation & R&D Platform.
 */

export enum GateStage {
  GATE_0_IDEA = 'GATE_0_IDEA',
  GATE_1_PROBLEM_VALIDATION = 'GATE_1_PROBLEM_VALIDATION',
  GATE_2_OPPORTUNITY_VALIDATION = 'GATE_2_OPPORTUNITY_VALIDATION',
  GATE_3_SOLUTION_VALIDATION = 'GATE_3_SOLUTION_VALIDATION',
  GATE_4_BUSINESS_VALIDATION = 'GATE_4_BUSINESS_VALIDATION',
  GATE_5_MVP_APPROVAL = 'GATE_5_MVP_APPROVAL',
  GATE_6_LAUNCH_APPROVAL = 'GATE_6_LAUNCH_APPROVAL',
  GATE_7_SCALE_PIVOT_STOP = 'GATE_7_SCALE_PIVOT_STOP',
}

export enum GateDecision {
  PROCEED = 'PROCEED',
  PIVOT = 'PIVOT',
  PAUSE = 'PAUSE',
  STOP = 'STOP',
  REVISE_EVIDENCE = 'REVISE_EVIDENCE',
}

export enum PivotAction {
  CUSTOMER_SEGMENT_PIVOT = 'CUSTOMER_SEGMENT_PIVOT',
  VALUE_PROPOSITION_PIVOT = 'VALUE_PROPOSITION_PIVOT',
  MONETIZATION_PIVOT = 'MONETIZATION_PIVOT',
  ARCHITECTURE_PIVOT = 'ARCHITECTURE_PIVOT',
}

export interface InnovationWorkspace {
  id: string;
  workspace_id?: string;
  stage?: string;
  title: string;
  theme: string;
  objective?: string;
  status: string;
  owner_id: string;
  target_market?: string;
  horizon: string;
  stage_gate: string;
  confidence_score: number;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface InnovationProblem {
  id: string;
  workspace_id: string;
  statement: string;
  affected_users?: string;
  frequency: string;
  severity: string;
  existing_solutions?: string[];
  willingness_to_pay_signal?: number;
  urgency_score: number;
  confidence_score: number;
  status: string;
  evidence_sources?: string[];
  created_at: string;
}

export interface InnovationOpportunity {
  id: string;
  workspace_id: string;
  title: string;
  description?: string;
  market_potential: string;
  revenue_potential_usd?: number;
  competitive_intensity: string;
  technical_feasibility: string;
  strategic_alignment_score: number;
  time_to_market_months: number;
  risk_level: string;
  status: string;
  created_at: string;
}

export interface InnovationIdea {
  id: string;
  idea_id?: string;
  workspace_id: string;
  problem_id?: string;
  opportunity_id?: string;
  title: string;
  description: string;
  origin_source: string;
  target_users?: string;
  proposed_value?: string;
  customer_value_score: number;
  market_potential_score: number;
  strategic_fit_score: number;
  revenue_potential_score: number;
  profitability_score: number;
  differentiation_score: number;
  technical_feasibility_score: number;
  execution_complexity_score: number;
  risk_score: number;
  time_to_value_score: number;
  evidence_strength_score: number;
  composite_score: number;
  status: string;
  version: number;
  created_at: string;
}

export enum HorizonLevel {
  H1_CORE = 'H1_CORE',
  H2_ADJACENT = 'H2_ADJACENT',
  H3_TRANSFORMATIONAL = 'H3_TRANSFORMATIONAL',
}

export interface InnovationPortfolio {
  horizon_1_core_pct?: number;
  horizon_2_adjacent_pct?: number;
  horizon_3_transformational_pct?: number;
  total_invested_usd?: number;
  expected_portfolio_roi?: number;
  workspaces?: InnovationWorkspace[];
}

export interface InnovationHypothesis {
  id: string;
  hypothesis_id?: string;
  workspace_id: string;
  idea_id: string;
  statement: string;
  prediction: string;
  metric_name: string;
  baseline_value: number;
  target_value: number;
  confidence: number;
  status: string;
  created_at: string;
}

export interface InnovationAssumption {
  id: string;
  hypothesis_id: string;
  assumption_text: string;
  category: string;
  impact_level: string;
  uncertainty_level: string;
  validation_priority: string;
  is_validated: boolean;
  created_at: string;
}

export interface InnovationExperiment {
  id: string;
  experiment_id?: string;
  workspace_id: string;
  hypothesis_id: string;
  title: string;
  experiment_type: string;
  objective?: string;
  target_population?: string;
  sample_size: number;
  duration_days: number;
  status: string;
  risk_review_passed: boolean;
  governance_approved: boolean;
  statistical_method: string;
  created_at: string;
}

export interface InnovationExperimentResult {
  id: string;
  experiment_id: string;
  observed_sample_size: number;
  control_mean: number;
  treatment_mean: number;
  delta_percentage: number;
  p_value?: number;
  is_statistically_significant: boolean;
  conclusion: string;
  limitations?: string;
  created_at: string;
}

export interface InnovationLearning {
  id: string;
  workspace_id: string;
  hypothesis_id?: string;
  experiment_id?: string;
  insight_statement: string;
  evidence_summary: string;
  strategic_implication?: string;
  created_at: string;
}

export interface InnovationProductConcept {
  id: string;
  concept_id?: string;
  workspace_id: string;
  idea_id?: string;
  name: string;
  target_customer_persona: string;
  value_proposition: string;
  core_features?: string[];
  differentiators?: string[];
  business_model_type: string;
  technical_architecture_notes?: string;
  status: string;
  created_at: string;
}

export interface InnovationBusinessCase {
  id: string;
  workspace_id: string;
  concept_id: string;
  target_tam_usd: number;
  projected_year1_revenue_usd: number;
  estimated_development_cost_usd: number;
  estimated_cac_usd: number;
  estimated_ltv_usd: number;
  payback_months: number;
  break_even_customers_count: number;
  gross_margin_percentage: number;
  recommendation: string;
  created_at: string;
}

export interface InnovationGateReview {
  id: string;
  workspace_id: string;
  gate_stage: string;
  reviewer_id: string;
  evidence_completeness_score: number;
  decision: string;
  review_notes?: string;
  decision_timestamp?: string;
  created_at: string;
}

export interface InnovationOverview {
  total_workspaces: number;
  total_problems_cataloged: number;
  total_ideas_generated: number;
  validated_ideas_count: number;
  active_experiments_count: number;
  structured_learnings_count: number;
  recent_workspaces: InnovationWorkspace[];
  recent_learnings: InnovationLearning[];
}

export interface InnovationWorkspaceDetail {
  workspace: InnovationWorkspace;
  problems: InnovationProblem[];
  opportunities: InnovationOpportunity[];
  ideas: InnovationIdea[];
  hypotheses: InnovationHypothesis[];
  experiments: InnovationExperiment[];
  learnings: InnovationLearning[];
  product_concepts: InnovationProductConcept[];
  service_concepts: any[];
  gate_reviews: InnovationGateReview[];
}

export interface InnovationCopilotResponse {
  query?: string;
  response_text?: string;
  grounding_evidence?: string[];
  assumptions_identified?: string[];
  limitations?: string[];
  [key: string]: any;
}

export interface InnovationEconomics { id: string; tam_usd?: number; cac_usd?: number; ltv_usd?: number; }
export interface InnovationPrototype { id: string; title: string; prototype_type: string; status: string; }
export interface InnovationPRD { id: string; concept_id: string; title: string; content: string; }
export enum IdeaSource { AI_WORKER = 'AI_WORKER', CUSTOMER = 'CUSTOMER', RESEARCH = 'RESEARCH', INTERNAL = 'INTERNAL' }

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

export const innovationApi = {
  async getOverview(): Promise<InnovationOverview> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/overview`);
    if (!res.ok) throw new Error("Failed to load innovation overview");
    const json = await res.json();
    return json.data;
  },

  async listWorkspaces(): Promise<InnovationWorkspace[]> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/workspaces`);
    if (!res.ok) throw new Error("Failed to list innovation workspaces");
    const json = await res.json();
    return json.data;
  },

  async getWorkspace(id: string): Promise<InnovationWorkspaceDetail> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/workspaces/${id}`);
    if (!res.ok) throw new Error(`Failed to load workspace ${id}`);
    const json = await res.json();
    return json.data;
  },

  async createWorkspace(payload: {
    title: string;
    theme?: string;
    objective?: string;
    target_market?: string;
    horizon?: string;
  }): Promise<InnovationWorkspace> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/workspaces`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create innovation workspace");
    const json = await res.json();
    return json.data;
  },

  async recordProblem(workspaceId: string, payload: {
    statement: string;
    affected_users?: string;
    frequency?: string;
    severity?: string;
    willingness_to_pay_signal?: number;
    evidence_sources?: string[];
  }): Promise<InnovationProblem> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/workspaces/${workspaceId}/problems`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to record problem");
    const json = await res.json();
    return json.data;
  },

  async createIdea(workspaceId: string, payload: {
    title: string;
    description: string;
    origin_source?: string;
    problem_id?: string;
    opportunity_id?: string;
    scoring_factors?: Record<string, number>;
  }): Promise<InnovationIdea> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/workspaces/${workspaceId}/ideas`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create idea");
    const json = await res.json();
    return json.data;
  },

  async formHypothesis(workspaceId: string, payload: {
    idea_id: string;
    statement: string;
    prediction: string;
    metric_name: string;
    baseline_value?: number;
    target_value?: number;
  }): Promise<InnovationHypothesis> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/workspaces/${workspaceId}/hypotheses`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to form hypothesis");
    const json = await res.json();
    return json.data;
  },

  async designExperiment(workspaceId: string, payload: {
    hypothesis_id: string;
    title: string;
    experiment_type?: string;
    sample_size?: number;
  }): Promise<InnovationExperiment> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/workspaces/${workspaceId}/experiments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to design experiment");
    const json = await res.json();
    return json.data;
  },

  async recordExperimentResult(experimentId: string, payload: {
    control_values: number[];
    treatment_values: number[];
    limitations?: string;
  }): Promise<InnovationExperimentResult> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/experiments/${experimentId}/results`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to record experiment result");
    const json = await res.json();
    return json.data;
  },

  async createProductConcept(workspaceId: string, payload: {
    name: string;
    target_customer_persona: string;
    value_proposition: string;
    core_features?: string[];
    differentiators?: string[];
    idea_id?: string;
  }): Promise<InnovationProductConcept> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/workspaces/${workspaceId}/products`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create product concept");
    const json = await res.json();
    return json.data;
  },

  async conductGateReview(workspaceId: string, payload: {
    gate_stage: string;
    reviewer_id: string;
    evidence_completeness_score?: number;
    decision?: string;
    review_notes?: string;
  }): Promise<InnovationGateReview> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/workspaces/${workspaceId}/gates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to conduct gate review");
    const json = await res.json();
    return json.data;
  },

  async queryCopilot(payload: {
    workspace_id: string;
    query: string;
  }): Promise<any> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/copilot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to query innovation copilot");
    const json = await res.json();
    return json.data;
  },

  async createAssumption(payload: any): Promise<InnovationAssumption> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/assumptions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create assumption");
    const json = await res.json();
    return json.data;
  },



  async generatePRD(conceptId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/v1/innovation/prd/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concept_id: conceptId }),
    });
    if (!res.ok) throw new Error("Failed to generate PRD");
    const json = await res.json();
    return json.data;
  },

  getWorkspaces: async () => innovationApi.listWorkspaces(),
  getProblems: async (id: string) => (await innovationApi.getWorkspace(id))?.problems || [],
  getOpportunities: async (id: string) => (await innovationApi.getWorkspace(id))?.opportunities || [],
  getIdeas: async (id: string) => (await innovationApi.getWorkspace(id))?.ideas || [],
  getHypotheses: async (id: string) => (await innovationApi.getWorkspace(id))?.hypotheses || [],
  getAssumptions: async (id: string) => [],
  getExperiments: async (id: string) => (await innovationApi.getWorkspace(id))?.experiments || [],
  getLearnings: async (id: string) => (await innovationApi.getWorkspace(id))?.learnings || [],
  getProductConcepts: async (id: string) => (await innovationApi.getWorkspace(id))?.product_concepts || [],
  getBusinessCases: async (id: string) => [],
  getPRDs: async (id: string) => [],
  getGateReviews: async (id: string) => (await innovationApi.getWorkspace(id))?.gate_reviews || [],
  getPortfolio: async (id?: string) => ({}),
  createProblem: async (wsIdOrPayload: any, payload?: any): Promise<any> => {
    if (typeof wsIdOrPayload === 'string') {
      return innovationApi.recordProblem(wsIdOrPayload, payload || {});
    }
    const wsId = wsIdOrPayload?.workspace_id || 'ws-default';
    return innovationApi.recordProblem(wsId, wsIdOrPayload || {});
  },
  createOpportunity: async (wsIdOrPayload: any, payload?: any): Promise<any> => {
    return { id: 'opp-' + Date.now(), workspace_id: 'ws-default', title: 'New Opportunity', market_potential: 'HIGH', strategic_alignment_score: 85, time_to_market_months: 3, risk_level: 'MEDIUM', status: 'ACTIVE', created_at: new Date().toISOString() };
  },
  evaluateGate: async (payload: any): Promise<any> => {
    return { id: 'gate-' + Date.now(), workspace_id: payload?.workspace_id || 'ws-default', gate_stage: payload?.gate_stage || 'GATE_1_PROBLEM_VALIDATION', reviewer_id: payload?.reviewed_by || 'Reviewer', evidence_completeness_score: 90, decision: 'PROCEED', created_at: new Date().toISOString() };
  },
  scoreIdea: async (id: string, payload: any): Promise<any> => {
    return { id, workspace_id: 'ws-default', title: 'Scored Idea', description: 'Scored', origin_source: 'AI_WORKER', customer_value_score: 8, market_potential_score: 8, strategic_fit_score: 8, revenue_potential_score: 8, profitability_score: 8, differentiation_score: 8, technical_feasibility_score: 8, execution_complexity_score: 8, risk_score: 3, time_to_value_score: 8, evidence_strength_score: 8, composite_score: 82, status: 'ACTIVE', version: 1, created_at: new Date().toISOString() };
  },
};
