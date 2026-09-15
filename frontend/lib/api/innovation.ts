/**
 * TypeScript API Client for Phase 55 — Unified Product & Innovation Intelligence, Idea Discovery, Validation & R&D Platform.
 */

export interface InnovationWorkspace {
  id: string;
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

export interface InnovationHypothesis {
  id: string;
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
};
