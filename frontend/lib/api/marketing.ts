/**
 * Phase 59: Unified Marketing Intelligence, Demand Generation & Content Strategy API Client
 */

export interface MarketingOverviewMetrics {
  total_campaigns_active: number;
  total_leads_captured: number;
  total_mql_generated: number;
  total_content_assets: number;
  marketing_spend_usd: number;
  attributed_revenue_usd: number;
  overall_roas: number;
  avg_cac_usd: number;
  forecast_p50_leads: number;
  open_marketing_risks: number;
  status: string;
  as_of: string;
}

export interface MarketingAudience {
  id: string;
  name: string;
  description: string;
  target_icp: string;
  industry: string;
  company_size_tier: string;
  buying_context: string;
  primary_pain_points: string[];
  channel_preferences: string[];
  total_market_size: number;
  reachable_market_size: number;
  created_at: string;
}

export interface MarketingPositioning {
  id: string;
  audience_id: string;
  target_customer: string;
  problem_statement: string;
  alternative_solution: string;
  our_solution: string;
  key_differentiators: string[];
  value_statement: string;
  proof_points: string[];
  version: number;
  is_approved: boolean;
  approved_by?: string;
  created_at: string;
}

export interface ContentAsset {
  id: string;
  title: string;
  content_type: string;
  journey_stage: string;
  target_audience_id?: string;
  status: string;
  current_version: number;
  body_markdown: string;
  primary_cta?: string;
  revenue_influenced_usd: number;
  views_count: number;
  conversions_count: number;
  created_at: string;
  updated_at: string;
}

export interface ContentGap {
  id: string;
  topic: string;
  target_audience: string;
  journey_stage: string;
  demand_volume: string;
  revenue_potential_usd: number;
  effort_tier: string;
  priority_score: number;
  created_at: string;
}

export interface MarketingCampaign {
  id: string;
  name: string;
  campaign_type: string;
  status: string;
  target_audience_id?: string;
  allocated_budget_usd: number;
  actual_spend_usd: number;
  leads_generated: number;
  mql_generated: number;
  sql_generated: number;
  opportunities_influenced: number;
  pipeline_influenced_usd: number;
  revenue_attributed_usd: number;
  channels: string[];
  owner: string;
  is_governance_approved: boolean;
  created_at: string;
  updated_at: string;
}

export interface MarketingLead {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  company_name?: string;
  source_channel: string;
  first_touch_campaign?: string;
  fit_score: number;
  engagement_score: number;
  intent_score: number;
  composite_lead_score: number;
  qualification_stage: string;
  consent_obtained: boolean;
  is_suppressed: boolean;
  created_at: string;
}

export interface FunnelMetrics {
  id: string;
  period: string;
  impressions: number;
  visitors: number;
  leads: number;
  mql: number;
  sql: number;
  opportunities: number;
  deals_won: number;
  conversion_rate_lead_to_mql_pct: number;
  conversion_rate_mql_to_sql_pct: number;
  conversion_rate_sql_to_won_pct: number;
  avg_funnel_velocity_days: number;
  created_at: string;
}

export interface MarketingRoi {
  id: string;
  period: string;
  total_spend_usd: number;
  total_attributed_revenue_usd: number;
  cost_per_lead_usd: number;
  cost_per_mql_usd: number;
  cost_per_acquisition_usd: number;
  roas: number;
  roi_pct: number;
  created_at: string;
}

export interface MarketingForecast {
  id: string;
  period: string;
  scenario: string;
  p10_leads: number;
  p25_leads: number;
  p50_leads: number;
  p75_leads: number;
  p90_leads: number;
  p50_pipeline_usd: number;
  p50_revenue_usd: number;
  model_version: string;
  created_at: string;
}

export interface MarketingRisk {
  id: string;
  risk_category: string;
  description: string;
  severity: string;
  mitigation_strategy: string;
  status: string;
  created_at: string;
}

export interface MarketingFatigue {
  id: string;
  audience_id?: string;
  channel: string;
  weekly_frequency: number;
  unsubscribe_rate_pct: number;
  engagement_decay_pct: number;
  fatigue_level: string;
  created_at: string;
}

export interface CopilotResponse {
  query: string;
  answer: string;
  evidence: string[];
  uncertainty: string;
  timestamp: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const marketingApi = {
  getOverview: async (): Promise<MarketingOverviewMetrics> => {
    const res = await fetch(`${API_BASE}/marketing/overview`);
    return res.json();
  },
  getAudiences: async (): Promise<MarketingAudience[]> => {
    const res = await fetch(`${API_BASE}/marketing/audiences`);
    return res.json();
  },
  getPositioning: async (): Promise<MarketingPositioning[]> => {
    const res = await fetch(`${API_BASE}/marketing/positioning`);
    return res.json();
  },
  getContent: async (stage?: string): Promise<ContentAsset[]> => {
    const url = stage ? `${API_BASE}/marketing/content?stage=${stage}` : `${API_BASE}/marketing/content`;
    const res = await fetch(url);
    return res.json();
  },
  getContentGaps: async (): Promise<ContentGap[]> => {
    const res = await fetch(`${API_BASE}/marketing/content/gaps`);
    return res.json();
  },
  getCampaigns: async (status?: string): Promise<MarketingCampaign[]> => {
    const url = status ? `${API_BASE}/marketing/campaigns?status=${status}` : `${API_BASE}/marketing/campaigns`;
    const res = await fetch(url);
    return res.json();
  },
  getLeads: async (stage?: string): Promise<MarketingLead[]> => {
    const url = stage ? `${API_BASE}/marketing/leads?stage=${stage}` : `${API_BASE}/marketing/leads`;
    const res = await fetch(url);
    return res.json();
  },
  getFunnel: async (period: string = "2026-Q3"): Promise<FunnelMetrics> => {
    const res = await fetch(`${API_BASE}/marketing/funnel?period=${period}`);
    return res.json();
  },
  getRoi: async (period: string = "2026-Q3"): Promise<MarketingRoi> => {
    const res = await fetch(`${API_BASE}/marketing/roi?period=${period}`);
    return res.json();
  },
  getForecasts: async (): Promise<MarketingForecast[]> => {
    const res = await fetch(`${API_BASE}/marketing/forecasts`);
    return res.json();
  },
  getRisks: async (): Promise<MarketingRisk[]> => {
    const res = await fetch(`${API_BASE}/marketing/risks`);
    return res.json();
  },
  getFatigue: async (): Promise<MarketingFatigue[]> => {
    const res = await fetch(`${API_BASE}/marketing/fatigue`);
    return res.json();
  },
  askCopilot: async (query: string): Promise<CopilotResponse> => {
    const res = await fetch(`${API_BASE}/marketing/copilot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    return res.json();
  },
};
