/**
 * TypeScript API Client for Phase 54 — Unified Autonomous Research, Intelligence & Continuous Discovery Engine.
 */

export interface ResearchWorkspace {
  id: string;
  title: string;
  research_question: string;
  objective?: string;
  research_type: string;
  status: string;
  scope_parameters?: Record<string, any>;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface ResearchSource {
  id: string;
  workspace_id: string;
  url?: string;
  title?: string;
  publisher?: string;
  source_type: string;
  trust_level: string;
  authority_score: number;
  reliability_score: number;
  content_hash?: string;
  status: string;
  created_at: string;
}

export interface ResearchFact {
  id: string;
  workspace_id: string;
  source_id?: string;
  entity_name?: string;
  fact_statement: string;
  fact_value?: string;
  observed_at?: string;
  status: string;
  confidence_score: number;
  created_at: string;
}

export interface ResearchClaim {
  id: string;
  workspace_id: string;
  claim_text: string;
  verification_status: string;
  supporting_source_ids?: string[];
  contradicting_source_ids?: string[];
  confidence_score: number;
  explanation?: string;
  created_at: string;
}

export interface ResearchConflict {
  id: string;
  workspace_id: string;
  claim_text: string;
  source_a_id?: string;
  source_b_id?: string;
  value_a?: string;
  value_b?: string;
  conflict_nature?: string;
  possible_explanation?: string;
  resolution_status: string;
  created_at: string;
}

export interface ResearchTrend {
  id: string;
  topic_or_entity: string;
  trend_type: string;
  direction: string;
  velocity_score: number;
  durability_assessment?: string;
  signals?: string[];
  first_observed?: string;
  last_updated?: string;
}

export interface ResearchCompetitorProfile {
  id: string;
  competitor_name: string;
  market_segment?: string;
  product_portfolio?: string[];
  pricing_signals?: Record<string, any>;
  strengths?: string[];
  weaknesses?: string[];
  threat_level?: string;
  last_activity_date?: string;
}

export interface ResearchMonitoringRule {
  id: string;
  target_name: string;
  target_type: string;
  keywords?: string[];
  frequency?: string;
  is_active: boolean;
  last_run_at?: string;
  created_at: string;
}

export interface ResearchIntelligenceEvent {
  id: string;
  rule_id?: string;
  event_type: string;
  entity_or_topic: string;
  significance: string;
  previous_state?: string;
  new_state?: string;
  summary: string;
  impact_analysis?: string;
  confidence_score: number;
  observed_at: string;
}

export interface ResearchReport {
  id: string;
  workspace_id: string;
  title: string;
  executive_summary?: string;
  methodology_scope?: string;
  key_findings?: string[];
  verified_claims_count: number;
  conflicts_analyzed_count: number;
  identified_gaps?: string[];
  recommendations?: string[];
  limitations?: string;
  version: number;
  created_at: string;
}

export interface ResearchOverview {
  total_workspaces: number;
  active_researching: number;
  total_sources_cataloged: number;
  verified_facts_count: number;
  active_monitoring_rules: number;
  critical_events_24h: number;
  recent_workspaces: ResearchWorkspace[];
  recent_events: ResearchIntelligenceEvent[];
}

export interface WorkspaceDetail {
  workspace: ResearchWorkspace;
  sources: ResearchSource[];
  facts: ResearchFact[];
  claims: ResearchClaim[];
  conflicts: ResearchConflict[];
  monitoring_rules: ResearchMonitoringRule[];
  reports: ResearchReport[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

export const researchIntelligenceApi = {
  async getOverview(): Promise<ResearchOverview> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/overview`);
    if (!res.ok) throw new Error("Failed to load research intelligence overview");
    const json = await res.json();
    return json.data;
  },

  async listWorkspaces(): Promise<ResearchWorkspace[]> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/workspaces`);
    if (!res.ok) throw new Error("Failed to list research workspaces");
    const json = await res.json();
    return json.data;
  },

  async getWorkspace(id: string): Promise<WorkspaceDetail> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/workspaces/${id}`);
    if (!res.ok) throw new Error(`Failed to load workspace ${id}`);
    const json = await res.json();
    return json.data;
  },

  async createWorkspace(payload: {
    title: string;
    research_question: string;
    objective?: string;
    research_type?: string;
    scope_parameters?: Record<string, any>;
  }): Promise<ResearchWorkspace> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/workspaces`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create research workspace");
    const json = await res.json();
    return json.data;
  },

  async addSource(payload: {
    workspace_id: string;
    url?: string;
    title?: string;
    publisher?: string;
    source_type?: string;
    raw_content?: string;
  }): Promise<ResearchSource> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/sources`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to register research source");
    const json = await res.json();
    return json.data;
  },

  async extractFacts(payload: {
    workspace_id: string;
    source_id?: string;
    raw_text: string;
  }): Promise<ResearchFact[]> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/facts/extract`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to extract facts");
    const json = await res.json();
    return json.data;
  },

  async verifyClaim(payload: {
    workspace_id: string;
    claim_text: string;
    candidate_source_ids?: string[];
  }): Promise<ResearchClaim> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/claims/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to verify claim");
    const json = await res.json();
    return json.data;
  },

  async createMonitoringRule(payload: {
    workspace_id?: string;
    target_name: string;
    target_type?: string;
    keywords?: string[];
    frequency?: string;
  }): Promise<ResearchMonitoringRule> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/monitoring`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create monitoring rule");
    const json = await res.json();
    return json.data;
  },

  async generateReport(payload: {
    workspace_id: string;
    title?: string;
  }): Promise<ResearchReport> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/reports/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to generate research report");
    const json = await res.json();
    return json.data;
  },

  async queryCopilot(payload: {
    workspace_id?: string;
    query: string;
  }): Promise<any> {
    const res = await fetch(`${API_BASE}/api/v1/research-intelligence/copilot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to query research copilot");
    const json = await res.json();
    return json.data;
  },
};
