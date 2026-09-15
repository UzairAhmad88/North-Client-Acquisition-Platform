/**
 * TypeScript API Client for Phase 57: Unified Customer Experience, Journey Intelligence & Optimization Platform.
 */

export interface Customer360Profile {
  customer_id: string;
  identity: {
    name: string;
    tenant_id: string;
    segment: string;
    lifecycle_status: string;
    account_executive: string;
    customer_success_manager: string;
  };
  organization: {
    industry: string;
    tier: string;
    employee_count: number;
    arr: number;
    contract_renewal_date: string;
  };
  journeys: CustomerJourneyItem[];
  active_journey_count: number;
  health_summary: {
    overall_score: number;
    state: string;
    churn_risk_pct: number;
    expansion_readiness_pct: number;
  };
  effort_summary: {
    ces_score: number;
    tier: string;
  };
  sentiment_summary: {
    overall: string;
    confidence: number;
  };
  last_touchpoint: {
    channel: string;
    occurred_at: string;
    outcome: string;
  };
  generated_at: string;
}

export interface CustomerJourneyItem {
  id: string;
  customer_id: string;
  customer_name?: string;
  journey_type: string;
  current_stage: string;
  lifecycle_status: string;
  health_status: string;
  completion_rate: number;
  effort_score: number;
  sentiment_score: number;
  stage_history?: Array<{
    stage: string;
    entered_at: string;
    status: string;
    notes?: string;
  }>;
  created_at: string;
  updated_at: string;
}

export interface JourneyStageItem {
  id: string;
  journey_id: string;
  stage_name: string;
  order_index: number;
  status: string;
  entered_at?: string;
  completed_at?: string;
  duration_seconds: number;
  dropoff_risk: number;
  touchpoint_count: number;
  notes?: string;
}

export interface FrictionPointItem {
  id: string;
  customer_id: string;
  journey_id?: string;
  stage: string;
  friction_type: string;
  severity: string;
  description: string;
  evidence?: any;
  customer_impact?: string;
  business_impact?: string;
  confidence: number;
  resolution_status: string;
  created_at: string;
}

export interface EffortRecordItem {
  id: string;
  customer_id: string;
  journey_id?: string;
  stage: string;
  ces_score: number;
  effort_tier: string;
  step_count: number;
  form_count: number;
  repeated_info_instances: number;
  waiting_time_minutes: number;
  support_contacts_count: number;
  created_at: string;
}

export interface ExperienceHealthItem {
  id: string;
  customer_id: string;
  overall_health_score: number;
  health_state: string;
  factor_breakdown: {
    engagement: number;
    product_adoption: number;
    support_health: number;
    customer_effort: number;
    satisfaction_sentiment: number;
  };
  churn_probability: number;
  expansion_readiness: number;
  explanation?: string;
  last_evaluated_at: string;
}

export interface ChurnPredictionItem {
  id: string;
  customer_id: string;
  churn_probability: number;
  risk_level: string;
  primary_drivers?: string[];
  recommended_interventions?: string[];
  confidence: number;
  predicted_at: string;
}

export interface VoiceThemeItem {
  id: string;
  theme_name: string;
  description?: string;
  frequency: number;
  severity: string;
  trend_direction: string;
  affected_stages?: string[];
  sample_quotes?: string[];
}

export interface ExpectationGapItem {
  id: string;
  customer_id: string;
  area: string;
  promised_capability: string;
  customer_expected: string;
  delivered_reality: string;
  gap_severity: string;
  evidence_source?: string;
  remediation_action?: string;
  status: string;
}

export interface OverviewMetrics {
  active_journeys_count: number;
  journey_completion_rate: number;
  avg_customer_effort_score: number;
  overall_experience_health: number;
  average_churn_probability: number;
  open_friction_points_count: number;
  active_goals_count: number;
  identified_expansion_arr_usd: number;
  active_alerts_count: number;
  top_voc_themes_count: number;
  last_calculated_at: string;
}

const API_BASE = "/api/v1/customer-experience";

export const customerExperienceApi = {
  getOverview: async (): Promise<OverviewMetrics> => {
    const res = await fetch(`${API_BASE}/overview`);
    if (!res.ok) throw new Error("Failed to fetch CX overview");
    return res.json();
  },

  getCustomer360: async (customerId: string = "cust-demo-001"): Promise<Customer360Profile> => {
    const res = await fetch(`${API_BASE}/customer-360/${customerId}`);
    if (!res.ok) throw new Error(`Failed to fetch 360 profile for ${customerId}`);
    return res.json();
  },

  listJourneys: async (customerId?: string): Promise<CustomerJourneyItem[]> => {
    const url = customerId ? `${API_BASE}/journeys?customer_id=${customerId}` : `${API_BASE}/journeys`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to list journeys");
    return res.json();
  },

  listFrictions: async (customerId?: string): Promise<FrictionPointItem[]> => {
    const url = customerId ? `${API_BASE}/friction?customer_id=${customerId}` : `${API_BASE}/friction`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to list friction points");
    return res.json();
  },

  listEfforts: async (customerId?: string): Promise<EffortRecordItem[]> => {
    const url = customerId ? `${API_BASE}/effort?customer_id=${customerId}` : `${API_BASE}/effort`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to list effort records");
    return res.json();
  },

  getHealth: async (customerId: string = "cust-demo-001"): Promise<ExperienceHealthItem> => {
    const res = await fetch(`${API_BASE}/health?customer_id=${customerId}`);
    if (!res.ok) throw new Error("Failed to fetch health score");
    return res.json();
  },

  listChurnPredictions: async (customerId?: string): Promise<ChurnPredictionItem[]> => {
    const url = customerId ? `${API_BASE}/churn?customer_id=${customerId}` : `${API_BASE}/churn`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to list churn predictions");
    return res.json();
  },

  getVoiceOfCustomer: async (): Promise<{ records: any[]; themes: VoiceThemeItem[] }> => {
    const res = await fetch(`${API_BASE}/voice-of-customer`);
    if (!res.ok) throw new Error("Failed to fetch Voice of Customer");
    return res.json();
  },

  listExpectationGaps: async (customerId?: string): Promise<ExpectationGapItem[]> => {
    const url = customerId ? `${API_BASE}/expectations?customer_id=${customerId}` : `${API_BASE}/expectations`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to list expectation gaps");
    return res.json();
  },

  askCopilot: async (query: string, customerId: string = "cust-demo-001"): Promise<any> => {
    const res = await fetch(`${API_BASE}/copilot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, customer_id: customerId }),
    });
    if (!res.ok) throw new Error("Failed to query Customer Experience Copilot");
    return res.json();
  },
};
