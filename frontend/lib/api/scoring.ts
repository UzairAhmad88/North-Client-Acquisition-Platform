import { api } from "./client";

export interface ComponentScore {
  component: string;
  score: number;
  weight: number;
  weighted_contribution: number;
  reasons: string[];
  evidence: string[];
  status: string;
}

export interface LeadScore {
  id: string;
  lead_id?: string | null;
  business_id: string;
  audit_id?: string | null;
  score_version: string;
  total_score: number;
  band: "HIGH" | "MEDIUM" | "LOW" | "VERY_LOW";
  website_need_score: number;
  online_presence_score: number;
  lead_capture_score: number;
  automation_potential_score: number;
  business_activity_score: number;
  contactability_score: number;
  service_fit_score: number;
  explanation: string;
  evidence: Record<string, any>;
  breakdown: Record<string, ComponentScore>;
  confidence: "HIGH" | "MEDIUM" | "LOW";
  is_stale: boolean;
  calculated_at: string;
  calculated_by?: string | null;
  created_at: string;
  updated_at: string;
}

export interface LeadScoreHistory {
  lead_id: string;
  total_scores: number;
  latest_score?: LeadScore | null;
  history: LeadScore[];
}

export async function calculateLeadScore(leadId: string): Promise<LeadScore> {
  const response = await api<{ data: LeadScore }>(`/scoring/leads/${leadId}/calculate`, {
    method: "POST",
  });
  return response.data;
}

export async function getLeadScore(leadId: string): Promise<LeadScore> {
  const response = await api<{ data: LeadScore }>(`/scoring/leads/${leadId}`);
  return response.data;
}

export async function getLeadScoreHistory(leadId: string, limit: number = 20): Promise<LeadScoreHistory> {
  const response = await api<{ data: LeadScoreHistory }>(`/scoring/leads/${leadId}/history?limit=${limit}`);
  return response.data;
}

export async function getBusinessScore(businessId: string): Promise<LeadScore> {
  const response = await api<{ data: LeadScore }>(`/scoring/businesses/${businessId}`);
  return response.data;
}
