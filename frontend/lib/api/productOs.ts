/**
 * Phase 60: Unified Product Management, Product Intelligence, Roadmap & Lifecycle OS API Client
 */

export interface ProductOverviewMetrics {
  tenant_id: string;
  portfolio_count: number;
  validated_problems_count: number;
  opportunities_pipeline_count: number;
  active_roadmaps_count: number;
  roadmap_initiatives_count: number;
  composite_health_score: number;
  total_mrr_usd: number;
  average_gross_margin_pct: number;
  open_risks_count: number;
  lifecycle_breakdown: {
    RELEASED: number;
    BETA: number;
    DEVELOPMENT: number;
    DISCOVERY: number;
  };
  system_health: string;
  last_evaluated: string;
}

export interface ProductItem {
  product_id: string;
  tenant_id: string;
  name: string;
  product_line: string;
  code: string;
  lifecycle_state: string;
  target_icp: string;
  owner_email: string;
  description: string;
  created_at: string;
}

export interface ProductProblem {
  problem_id: string;
  tenant_id: string;
  product_id: string;
  title: string;
  reported_by_count: number;
  severity: string;
  validation_status: string;
  context: string;
  cost_of_inaction_usd: number;
  evidence_sources: string[];
}

export interface ProductOpportunity {
  opportunity_id: string;
  tenant_id: string;
  product_id: string;
  title: string;
  problem_id: string;
  customer_value_score: number;
  business_value_score: number;
  confidence_score: number;
  effort_score: number;
  strategic_fit_score: number;
  revenue_potential_usd: number;
  score: number;
}

export interface RoadmapBoard {
  tenant_id: string;
  total_initiatives: number;
  horizons: {
    NOW: any[];
    NEXT: any[];
    LATER: any[];
  };
  quarterly_initiatives: Record<string, any[]>;
}

export interface TraceabilityEntry {
  requirement_id: string;
  requirement_title: string;
  requirement_type: string;
  priority: string;
  status: string;
  problem: {
    problem_id: string;
    title: string;
    severity: string;
    validation_status: string;
  };
  opportunity: {
    opportunity_id: string;
    title: string;
    score: number;
  };
  roadmap_initiative: {
    initiative_id: string;
    title: string;
    horizon: string;
  };
  user_stories: {
    story_id: string;
    title: string;
    story_points: number;
    status: string;
    criteria_count: number;
  }[];
  is_orphaned: boolean;
  completeness_score: number;
}

export interface ProductHealthScorecard {
  scorecard_id: string;
  tenant_id: string;
  product_id: string;
  product_name: string;
  composite_score: number;
  health_state: string;
  breakdown: {
    adoption: number;
    retention: number;
    reliability: number;
    feedback_sentiment: number;
    support_efficiency: number;
    quality_defect: number;
    gross_margin: number;
  };
  risk_factors: string[];
  evaluated_at: string;
}

export interface UnitEconomicsRecord {
  economics_id: string;
  tenant_id: string;
  product_id: string;
  active_customers: number;
  mrr_usd: number;
  arr_usd: number;
  gross_profit_usd: number;
  gross_margin_pct: number;
  arpu_monthly: number;
  cost_per_customer: number;
  cac_usd: number;
  ltv_usd: number;
  cac_payback_months: number;
  ltv_to_cac_ratio: number;
  is_healthy_unit_economics: boolean;
}

export interface ProbabilisticForecast {
  forecast_id: string;
  metric_name: string;
  time_horizon_months: number;
  percentiles: {
    p10_pessimistic: number;
    p25_conservative: number;
    p50_median: number;
    p75_optimistic: number;
    p90_high_growth: number;
  };
  confidence_band_width_pct: number;
  assumptions: string[];
}

export interface ProductCopilotResponse {
  query: string;
  response: string;
  evidence_sources: string[];
  assumptions: string[];
  confidence: number;
  governance_notice: string;
  timestamp: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchProductOverview(tenantId = "default_tenant"): Promise<ProductOverviewMetrics> {
  const res = await fetch(`${API_BASE}/product-os/overview?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch Product OS overview");
  return res.json();
}

export async function fetchPortfolio(tenantId = "default_tenant"): Promise<ProductItem[]> {
  const res = await fetch(`${API_BASE}/product-os/portfolio?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch product portfolio");
  return res.json();
}

export async function createProduct(payload: any, tenantId = "default_tenant"): Promise<ProductItem> {
  const res = await fetch(`${API_BASE}/product-os/portfolio?tenant_id=${tenantId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create product");
  return res.json();
}

export async function fetchProblems(tenantId = "default_tenant"): Promise<ProductProblem[]> {
  const res = await fetch(`${API_BASE}/product-os/problems?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch customer problems");
  return res.json();
}

export async function fetchOpportunities(tenantId = "default_tenant"): Promise<ProductOpportunity[]> {
  const res = await fetch(`${API_BASE}/product-os/opportunities?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch product opportunities");
  return res.json();
}

export async function fetchRoadmapBoard(tenantId = "default_tenant"): Promise<RoadmapBoard> {
  const res = await fetch(`${API_BASE}/product-os/roadmaps?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch roadmap board");
  return res.json();
}

export async function fetchTraceabilityMatrix(tenantId = "default_tenant"): Promise<TraceabilityEntry[]> {
  const res = await fetch(`${API_BASE}/product-os/requirements/traceability?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch traceability matrix");
  return res.json();
}

export async function fetchHealthScorecards(tenantId = "default_tenant"): Promise<ProductHealthScorecard[]> {
  const res = await fetch(`${API_BASE}/product-os/health?tenant_id=${tenantId}`);
  if (!res.ok) throw new Error("Failed to fetch health scorecards");
  return res.json();
}

export async function queryProductCopilot(query: string, tenantId = "default_tenant"): Promise<ProductCopilotResponse> {
  const res = await fetch(`${API_BASE}/product-os/copilot/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, tenant_id: tenantId }),
  });
  if (!res.ok) throw new Error("Failed to query Product Copilot");
  return res.json();
}
