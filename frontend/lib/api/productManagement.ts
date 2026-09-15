/**
 * TypeScript API Client for Phase 56 — Unified Product Lifecycle, Product Management & Continuous Delivery Intelligence Platform.
 */

export interface ProductItem {
  id: string;
  name: string;
  type: string;
  description?: string;
  target_market?: string;
  owner: string;
  team?: string;
  lifecycle_stage: string;
  health: string;
  status: string;
  version: string;
  workspace_id?: string;
  created_at: string;
  updated_at: string;
}

export interface ProductObjective {
  id: string;
  product_id: string;
  name: string;
  metric: string;
  baseline: number;
  target: number;
  time_window: string;
  owner: string;
  confidence: number;
  status: string;
}

export interface ProductMetric {
  id: string;
  product_id: string;
  name: string;
  definition: string;
  formula?: string;
  source: string;
  owner: string;
  current_value: number;
  target_value?: number;
  is_north_star: boolean;
}

export interface ProductFeedback {
  id: string;
  product_id: string;
  source: string;
  feedback_type: string;
  customer_segment: string;
  content: string;
  sentiment_score?: number;
  revenue_impact_usd?: number;
  created_at: string;
}

export interface FeedbackTheme {
  theme: string;
  frequency: number;
  sentiment_avg: number;
  revenue_impact_total: number;
  urgency_level: string;
}

export interface ProductRequirement {
  id: string;
  product_id: string;
  title: string;
  description: string;
  category: string;
  priority: string;
  acceptance_criteria: string[];
  source: string;
  problem_id?: string;
  objective_id?: string;
  is_traceable: boolean;
  version: number;
}

export interface TraceabilityMatrix {
  product_id: string;
  requirements: ProductRequirement[];
  orphaned_requirements: ProductRequirement[];
  traceability_score: number;
  unlinked_backlog_items: any[];
}

export interface ProductEpic {
  id: string;
  product_id: string;
  title: string;
  objective: string;
  problem_statement?: string;
  status: string;
}

export interface ProductFeature {
  id: string;
  product_id: string;
  epic_id?: string;
  requirement_id?: string;
  title: string;
  description?: string;
  acceptance_criteria: string[];
  status: string;
}

export interface ProductBacklogItem {
  id: string;
  product_id: string;
  epic_id?: string;
  feature_id?: string;
  requirement_id?: string;
  title: string;
  type: string;
  story_points: number;
  status: string;
  prioritization_score?: number;
  prioritization_framework?: string;
}

export interface ProductRoadmap {
  id: string;
  product_id: string;
  title: string;
  scenario: string;
  items: ProductRoadmapItem[];
}

export interface ProductRoadmapItem {
  id: string;
  roadmap_id: string;
  title: string;
  horizon: string;
  feature_id?: string;
  confidence: number;
  objective_link?: string;
}

export interface ProductSprint {
  id: string;
  product_id: string;
  name: string;
  status: string;
  capacity_points: number;
  start_date?: string;
  end_date?: string;
}

export interface ProductRelease {
  id: string;
  product_id: string;
  version: string;
  readiness_status: string;
  critical_defects: number;
  qa_passed: boolean;
  security_reviewed: boolean;
  performance_benchmarked: boolean;
  rollback_tested: boolean;
  launch_readiness_score: number;
  blocking_reasons: string[];
}

export interface ProductFeatureFlag {
  id: string;
  product_id: string;
  key: string;
  state: string;
  rollout_percentage: number;
  description?: string;
}

export interface ProductHealthDetail {
  product_id: string;
  composite_score: number;
  status: string;
  factors: {
    adoption: number;
    satisfaction: number;
    reliability: number;
    velocity: number;
    revenue: number;
    security: number;
  };
}

export interface ProductDashboardData {
  product: ProductItem;
  vision: any;
  objectives: ProductObjective[];
  metrics: ProductMetric[];
  feedback_count: number;
  requirements_count: number;
  backlog_count: number;
  roadmaps_count: number;
  sprints_count: number;
  releases_count: number;
  health: ProductHealthDetail;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

export const productApi = {
  async getPortfolio(): Promise<{ total_products: number; active_products: number; products: ProductItem[] }> {
    const res = await fetch(`${API_BASE}/api/v1/products/portfolio`);
    if (!res.ok) throw new Error("Failed to load product portfolio");
    const json = await res.json();
    return json.data;
  },

  async listProducts(stage?: string): Promise<ProductItem[]> {
    const url = stage ? `${API_BASE}/api/v1/products?stage=${stage}` : `${API_BASE}/api/v1/products`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to list products");
    const json = await res.json();
    return json.data;
  },

  async createProduct(payload: {
    name: string;
    type?: string;
    description?: string;
    target_market?: string;
    owner?: string;
    team?: string;
  }): Promise<ProductItem> {
    const res = await fetch(`${API_BASE}/api/v1/products`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create product");
    const json = await res.json();
    return json.data;
  },

  async getProductDashboard(id: string): Promise<ProductDashboardData> {
    const res = await fetch(`${API_BASE}/api/v1/products/${id}`);
    if (!res.ok) throw new Error(`Failed to load product ${id}`);
    const json = await res.json();
    return json.data;
  },

  async transitionLifecycle(id: string, new_stage: string, rationale?: string): Promise<ProductItem> {
    const res = await fetch(`${API_BASE}/api/v1/products/${id}/lifecycle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ new_stage, rationale }),
    });
    if (!res.ok) throw new Error("Failed to transition lifecycle stage");
    const json = await res.json();
    return json.data;
  },

  async setVision(id: string, payload: any): Promise<any> {
    const res = await fetch(`${API_BASE}/api/v1/products/${id}/vision`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to set vision");
    const json = await res.json();
    return json.data;
  },

  async getTraceability(id: string): Promise<TraceabilityMatrix> {
    const res = await fetch(`${API_BASE}/api/v1/products/${id}/traceability`);
    if (!res.ok) throw new Error("Failed to load traceability matrix");
    const json = await res.json();
    return json.data;
  },

  async createRequirement(id: string, payload: any): Promise<ProductRequirement> {
    const res = await fetch(`${API_BASE}/api/v1/products/${id}/requirements`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create requirement");
    const json = await res.json();
    return json.data;
  },

  async getBacklog(id: string): Promise<{ epics: ProductEpic[]; features: ProductFeature[]; items: ProductBacklogItem[] }> {
    const res = await fetch(`${API_BASE}/api/v1/products/${id}/backlog`);
    if (!res.ok) throw new Error("Failed to load backlog");
    const json = await res.json();
    return json;
  },

  async scoreBacklogItem(productId: string, itemId: string, framework: string, inputs: Record<string, number>): Promise<any> {
    const res = await fetch(`${API_BASE}/api/v1/products/${productId}/backlog/score/${itemId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ framework, inputs }),
    });
    if (!res.ok) throw new Error("Failed to score backlog item");
    const json = await res.json();
    return json.data;
  },

  async evaluateReleaseReadiness(productId: string, releaseId: string, checks: any): Promise<any> {
    const res = await fetch(`${API_BASE}/api/v1/products/${productId}/releases/${releaseId}/readiness`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(checks),
    });
    if (!res.ok) throw new Error("Failed to evaluate release readiness");
    const json = await res.json();
    return json.data;
  },

  async queryCopilot(productId: string, query: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/v1/products/${productId}/copilot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    if (!res.ok) throw new Error("Failed to query product copilot");
    const json = await res.json();
    return json.data;
  },
};
