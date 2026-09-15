/**
 * TypeScript API Client for Phase 53 — Unified Human-AI Collaboration, Decision Room & Augmented Intelligence Platform.
 */

export interface DecisionRoom {
  id: string;
  title: string;
  question: string;
  objective?: string;
  decision_type: string;
  importance: string;
  status: string;
  owner_id: string;
  selected_option_id?: string;
  decision_summary?: string;
  decided_at?: string;
  decided_by?: string;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface DecisionEvidence {
  id: string;
  evidence_type: string;
  source: string;
  claim: string;
  provenance?: string;
  authority: string;
  statement_category: string;
  confidence: number;
  freshness: string;
}

export interface DecisionOption {
  id: string;
  name: string;
  description: string;
  benefits: string[];
  costs: number;
  risks: string[];
  uncertainty_level: string;
  reversibility: string;
  composite_score: number;
  version: number;
}

export interface DecisionTradeoff {
  id: string;
  option_a_id: string;
  option_b_id: string;
  tradeoff_summary: string;
  gains_in_a: string[];
  sacrifices_in_a: string[];
}

export interface SpecialistAnalysis {
  id: string;
  specialist_role: string;
  worker_id?: string;
  summary: string;
  recommendations: string[];
  key_findings: string[];
  confidence: number;
  facts: string[];
  inferences: string[];
}

export interface AdversarialReview {
  id: string;
  reviewer_role: string;
  target_option_id?: string;
  critique_summary: string;
  weak_assumptions: string[];
  unintended_consequences: string[];
  hidden_costs: string[];
  data_gaps: string[];
}

export interface DecisionDisagreement {
  id: string;
  topic: string;
  disagreement_category: string;
  party_a: string;
  view_a: string;
  party_b: string;
  view_b: string;
  status: string;
}

export interface DecisionApproval {
  id: string;
  step_name: string;
  required_role: string;
  approver_id?: string;
  status: string;
  decision_notes?: string;
  reviewed_at?: string;
}

export interface DecisionRoomOverview {
  room: DecisionRoom;
  context?: any;
  evidence: DecisionEvidence[];
  assumptions: any[];
  unknowns: any[];
  options: DecisionOption[];
  criteria: any[];
  tradeoffs: DecisionTradeoff[];
  scenarios: any[];
  risks: any[];
  analyses: SpecialistAnalysis[];
  reviews: AdversarialReview[];
  disagreements: DecisionDisagreement[];
  consensus: {
    consensus_pct: number;
    disagreement_pct: number;
    total_specialist_analyses: number;
    total_disagreements: number;
    primary_disagreement: string;
  };
  discussions: any[];
  approvals: DecisionApproval[];
  actions: any[];
  outcomes: any[];
  post_reviews: any[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const decisionRoomsApi = {
  async listRooms(status?: string, decisionType?: string): Promise<DecisionRoom[]> {
    const params = new URLSearchParams();
    if (status) params.append("status", status);
    if (decisionType) params.append("decision_type", decisionType);
    const res = await fetch(`${API_BASE}/api/v1/decision-rooms?${params.toString()}`);
    if (!res.ok) throw new Error("Failed to list decision rooms");
    const json = await res.json();
    return json.data;
  },

  async getRoomOverview(id: string): Promise<DecisionRoomOverview> {
    const res = await fetch(`${API_BASE}/api/v1/decision-rooms/${id}`);
    if (!res.ok) throw new Error(`Failed to load decision room ${id}`);
    const json = await res.json();
    return json.data;
  },

  async createRoom(payload: {
    title: string;
    question: string;
    owner_id?: string;
    decision_type?: string;
    importance?: string;
    objective?: string;
  }): Promise<DecisionRoom> {
    const res = await fetch(`${API_BASE}/api/v1/decision-rooms`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create decision room");
    const json = await res.json();
    return json.data;
  },

  async recordDecision(id: string, payload: { selected_option_id: string; decision_summary: string; decided_by?: string }): Promise<DecisionRoom> {
    const res = await fetch(`${API_BASE}/api/v1/decision-rooms/${id}/decide`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to record decision");
    const json = await res.json();
    return json.data;
  },

  async recordApproval(id: string, payload: { step_id: string; approver_id: string; status?: string; notes?: string }): Promise<any> {
    const res = await fetch(`${API_BASE}/api/v1/decision-rooms/${id}/approvals`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to record approval action");
    const json = await res.json();
    return json.data;
  },

  async queryCopilot(roomId: string, query: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/v1/decision-rooms/copilot/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ room_id: roomId, query }),
    });
    if (!res.ok) throw new Error("Failed to query collaboration copilot");
    const json = await res.json();
    return json.data;
  },
};
