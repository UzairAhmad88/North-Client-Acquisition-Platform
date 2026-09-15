/**
 * TypeScript API Client for Phase 58: Unified Revenue Growth, Go-to-Market Intelligence & Optimization Platform.
 */

export interface GtmStrategyItem {
  id: string;
  name: string;
  target_market: string;
  sales_motion: string;
  positioning?: string;
  value_proposition?: string;
  status: string;
  channels?: string[];
  metrics_targets?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface TargetAccountItem {
  id: string;
  company_name: string;
  domain?: string;
  industry?: string;
  employee_count: number;
  estimated_annual_revenue: number;
  country?: string;
  icp_fit_score: number;
  priority_level: string;
  coverage_status: string;
  assigned_rep?: string;
  created_at: string;
  updated_at: string;
}

export interface SalesOpportunityItem {
  id: string;
  account_id: string;
  pipeline_id?: string;
  title: string;
  stage: string;
  estimated_arr_value: number;
  win_probability: number;
  weighted_value: number;
  expected_close_date?: string;
  owner_name: string;
  sales_motion: string;
  primary_need?: string;
  risk_status: string;
  created_at: string;
  updated_at: string;
}

export interface SalesForecastItem {
  id: string;
  forecast_period: string;
  model_version: string;
  scenario: string;
  pipeline_total_usd: number;
  weighted_pipeline_usd: number;
  p10_usd: number;
  p25_usd: number;
  p50_usd: number;
  p75_usd: number;
  p90_usd: number;
  assumptions?: Record<string, any>;
  generated_at: string;
}

export interface RevenueWaterfallItem {
  id: string;
  period: string;
  beginning_arr_usd: number;
  new_arr_usd: number;
  expansion_arr_usd: number;
  contraction_arr_usd: number;
  churn_arr_usd: number;
  ending_arr_usd: number;
  net_retention_pct: number;
  recorded_at: string;
}

export interface UnitEconomicsItem {
  id: string;
  period: string;
  blended_cac_usd: number;
  average_ltv_usd: number;
  ltv_to_cac_ratio: number;
  payback_period_months: number;
  gross_margin_pct: number;
  calculated_at: string;
}

export interface PricingTierItem {
  id: string;
  product_or_service: string;
  tier_name: string;
  list_price_usd: number;
  billing_frequency: string;
  average_discount_pct: number;
  target_gross_margin_pct: number;
}

export interface DiscountRequestItem {
  id: string;
  opportunity_id: string;
  requested_discount_pct: number;
  original_price_usd: number;
  proposed_price_usd: number;
  margin_impact_pct: number;
  justification: string;
  status: string;
  approver_name?: string;
  approval_notes?: string;
  created_at: string;
}

export interface DealRiskItem {
  id: string;
  opportunity_id: string;
  risk_category: string;
  severity: string;
  description: string;
  mitigation_strategy?: string;
  status: string;
  created_at: string;
}

export interface GrowthOpportunityItem {
  id: string;
  opportunity_type: string;
  title: string;
  description?: string;
  estimated_arr_potential_usd: number;
  target_segment?: string;
  confidence: number;
  status: string;
  created_at: string;
}

export interface MarketCoverageItem {
  id: string;
  segment: string;
  territory: string;
  accounts_discovered: number;
  accounts_researched: number;
  qualified_accounts: number;
  contacted_accounts: number;
  active_opportunities: number;
  won_accounts: number;
  coverage_percentage: number;
  recorded_at: string;
}

export interface RevenueOverviewMetrics {
  current_annual_run_rate_usd: number;
  target_annual_run_rate_usd: number;
  active_pipeline_total_usd: number;
  weighted_pipeline_usd: number;
  target_accounts_count: number;
  active_opportunities_count: number;
  win_rate_percentage: number;
  blended_cac_usd: number;
  ltv_to_cac_ratio: number;
  net_revenue_retention_pct: number;
  identified_growth_potential_arr_usd: number;
  last_calculated_at: string;
}

const API_BASE = "/api/v1/revenue";

export const revenueGrowthApi = {
  getOverview: async (): Promise<RevenueOverviewMetrics> => {
    const res = await fetch(`${API_BASE}/overview`);
    if (!res.ok) throw new Error("Failed to fetch revenue overview");
    return res.json();
  },

  listGtmStrategies: async (): Promise<GtmStrategyItem[]> => {
    const res = await fetch(`${API_BASE}/gtm`);
    if (!res.ok) throw new Error("Failed to list GTM strategies");
    return res.json();
  },

  listTargetAccounts: async (): Promise<TargetAccountItem[]> => {
    const res = await fetch(`${API_BASE}/accounts`);
    if (!res.ok) throw new Error("Failed to list target accounts");
    return res.json();
  },

  listOpportunities: async (stage?: string): Promise<SalesOpportunityItem[]> => {
    const url = stage ? `${API_BASE}/opportunities?stage=${stage}` : `${API_BASE}/opportunities`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to list opportunities");
    return res.json();
  },

  getForecasts: async (): Promise<SalesForecastItem[]> => {
    const res = await fetch(`${API_BASE}/forecasts`);
    if (!res.ok) throw new Error("Failed to fetch forecasts");
    return res.json();
  },

  getForecastScenarios: async (period: string = "Q4-2026"): Promise<SalesForecastItem[]> => {
    const res = await fetch(`${API_BASE}/forecasts/scenarios?period=${period}`);
    if (!res.ok) throw new Error("Failed to fetch forecast scenarios");
    return res.json();
  },

  getWaterfalls: async (): Promise<RevenueWaterfallItem[]> => {
    const res = await fetch(`${API_BASE}/waterfall`);
    if (!res.ok) throw new Error("Failed to fetch revenue waterfall");
    return res.json();
  },

  getUnitEconomics: async (period: string = "Q3-2026"): Promise<UnitEconomicsItem> => {
    const res = await fetch(`${API_BASE}/economics?period=${period}`);
    if (!res.ok) throw new Error("Failed to fetch unit economics");
    return res.json();
  },

  listPricingTiers: async (): Promise<PricingTierItem[]> => {
    const res = await fetch(`${API_BASE}/pricing`);
    if (!res.ok) throw new Error("Failed to fetch pricing tiers");
    return res.json();
  },

  listDiscounts: async (): Promise<DiscountRequestItem[]> => {
    const res = await fetch(`${API_BASE}/discounts`);
    if (!res.ok) throw new Error("Failed to fetch discount requests");
    return res.json();
  },

  listDealRisks: async (): Promise<DealRiskItem[]> => {
    const res = await fetch(`${API_BASE}/risks`);
    if (!res.ok) throw new Error("Failed to fetch deal risks");
    return res.json();
  },

  listGrowthOpportunities: async (): Promise<GrowthOpportunityItem[]> => {
    const res = await fetch(`${API_BASE}/growth-opportunities`);
    if (!res.ok) throw new Error("Failed to fetch growth opportunities");
    return res.json();
  },

  getMarketCoverage: async (): Promise<MarketCoverageItem[]> => {
    const res = await fetch(`${API_BASE}/coverage`);
    if (!res.ok) throw new Error("Failed to fetch market coverage");
    return res.json();
  },

  askCopilot: async (query: string): Promise<any> => {
    const res = await fetch(`${API_BASE}/copilot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    if (!res.ok) throw new Error("Failed to query Revenue Intelligence Copilot");
    return res.json();
  },
};
