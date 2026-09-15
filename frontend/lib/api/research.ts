import { api } from "./client";

export interface ResearchJob {
  id: string;
  business_id: string;
  user_id?: string | null;
  status: "PENDING" | "RUNNING" | "COMPLETED" | "PARTIAL" | "FAILED" | "CANCELLED";
  requested_sections: string[];
  source_count: number;
  records_found: number;
  records_validated: number;
  records_rejected: number;
  started_at?: string | null;
  completed_at?: string | null;
  error_message?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ResearchRecord {
  id: string;
  business_id: string;
  research_job_id?: string | null;
  source_url?: string | null;
  source_trust: "OFFICIAL" | "HIGH_TRUST" | "MEDIUM_TRUST" | "LOW_TRUST" | "UNKNOWN";
  research_type:
    | "IDENTITY"
    | "CONTACT"
    | "LOCATION"
    | "SERVICES"
    | "WEBSITE"
    | "SOCIAL"
    | "HOURS"
    | "DESCRIPTION"
    | "PUBLIC_REVIEWS"
    | "GENERAL";
  field_name: string;
  raw_value?: string | null;
  normalized_value: string;
  confidence: "HIGH" | "MEDIUM" | "LOW";
  evidence_text?: string | null;
  observed_at: string;
  expires_at?: string | null;
  status: "VALIDATED" | "REJECTED" | "STALE" | "CONFLICT";
  meta_info?: Record<string, any> | null;
  created_at: string;
}

export interface ResearchConflict {
  id: string;
  business_id: string;
  field_name: string;
  competing_values: Array<{
    value: string;
    source_url?: string | null;
    confidence: string;
    observed_at?: string | null;
  }>;
  status: "NO_CONFLICT" | "CONFLICT" | "RESOLVED" | "REQUIRES_REVIEW";
  resolution_notes?: string | null;
  created_at: string;
  updated_at: string;
}

export interface BusinessResearchProfile {
  business_id: string;
  business_name: string;
  total_jobs: number;
  total_records: number;
  active_conflicts_count: number;
  last_researched_at?: string | null;
  confidence_score: number;
  records: ResearchRecord[];
  conflicts: ResearchConflict[];
}

export interface ResearchJobCreateInput {
  business_id: string;
  sections?: string[];
  provider_type?: "MOCK" | "WEB";
}

export async function createResearchJob(data: ResearchJobCreateInput): Promise<ResearchJob> {
  const response = await api<{ data: ResearchJob }>("/research/jobs", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return response.data;
}

export async function listResearchJobs(params: {
  page?: number;
  page_size?: number;
  business_id?: string;
  status?: string;
} = {}): Promise<{ data: ResearchJob[]; total: number }> {
  const query = new URLSearchParams();
  if (params.page) query.set("page", params.page.toString());
  if (params.page_size) query.set("page_size", params.page_size.toString());
  if (params.business_id) query.set("business_id", params.business_id);
  if (params.status) query.set("status", params.status);

  const response = await api<{ data: ResearchJob[]; pagination: { total: number } }>(
    `/research/jobs?${query.toString()}`
  );
  return { data: response.data, total: response.pagination.total };
}

export async function runResearchJob(jobId: string, providerType: string = "MOCK"): Promise<ResearchJob> {
  const response = await api<{ data: ResearchJob }>(`/research/jobs/${jobId}/run?provider_type=${providerType}`, {
    method: "POST",
  });
  return response.data;
}

export async function cancelResearchJob(jobId: string): Promise<ResearchJob> {
  const response = await api<{ data: ResearchJob }>(`/research/jobs/${jobId}/cancel`, {
    method: "POST",
  });
  return response.data;
}

export async function getBusinessResearchProfile(businessId: string): Promise<BusinessResearchProfile> {
  const response = await api<{ data: BusinessResearchProfile }>(`/research/businesses/${businessId}`);
  return response.data;
}

export async function runResearchAgentJob(jobId: string): Promise<ResearchJob> {
  const response = await api<{ data: ResearchJob }>(`/research/jobs/${jobId}/run-agent`, {
    method: "POST",
  });
  return response.data;
}
