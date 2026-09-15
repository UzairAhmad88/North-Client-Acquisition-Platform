import { api } from "./client";

export interface RecommendationEvidence {
  source: string;
  source_id?: string | null;
  type: string;
  description: string;
  strength: number;
  confidence: string;
}

export interface ServiceRecommendation {
  id: string;
  lead_id: string;
  business_id: string;
  service_id: string;
  service_name?: string | null;
  service_slug?: string | null;
  recommendation_version: string;
  relevance_score: number;
  band: "STRONG" | "GOOD" | "POSSIBLE" | "WEAK";
  priority: "HIGH" | "MEDIUM" | "LOW";
  confidence: "HIGH" | "MEDIUM" | "LOW";
  status: "SUGGESTED" | "REVIEWED" | "ACCEPTED" | "REJECTED" | "STALE";
  reasons: string[];
  evidence: Record<string, any>[];
  limitations: string[];
  rejection_reason?: string | null;
  rejected_by?: string | null;
  rejected_at?: string | null;
  accepted_by?: string | null;
  accepted_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ServiceRecommendationListResponse {
  data: ServiceRecommendation[];
  pagination: {
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  };
}

export async function calculateLeadRecommendations(leadId: string): Promise<ServiceRecommendation[]> {
  const response = await api<{ data: ServiceRecommendation[] }>(`/leads/${leadId}/recommendations/calculate`, {
    method: "POST",
  });
  return response.data;
}

export async function getLeadRecommendations(
  leadId: string,
  options?: { status?: string; min_score?: number; limit?: number }
): Promise<ServiceRecommendationListResponse> {
  const params = new URLSearchParams();
  if (options?.status) params.append("status", options.status);
  if (options?.min_score !== undefined) params.append("min_score", options.min_score.toString());
  if (options?.limit) params.append("limit", options.limit.toString());

  const queryStr = params.toString() ? `?${params.toString()}` : "";
  const response = await api<ServiceRecommendationListResponse>(`/leads/${leadId}/recommendations${queryStr}`);
  return response;
}

export async function getRecommendation(id: string): Promise<ServiceRecommendation> {
  const response = await api<{ data: ServiceRecommendation }>(`/recommendations/${id}`);
  return response.data;
}

export async function acceptRecommendation(id: string): Promise<ServiceRecommendation> {
  const response = await api<{ data: ServiceRecommendation }>(`/recommendations/${id}/accept`, {
    method: "POST",
  });
  return response.data;
}

export async function rejectRecommendation(id: string, reason?: string): Promise<ServiceRecommendation> {
  const response = await api<{ data: ServiceRecommendation }>(`/recommendations/${id}/reject`, {
    method: "POST",
    body: JSON.stringify({ reason }),
  });
  return response.data;
}
