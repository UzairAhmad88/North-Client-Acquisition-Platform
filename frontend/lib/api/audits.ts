import { api } from "./client";

export interface AuditJob {
  id: string;
  business_id: string;
  user_id?: string | null;
  target_url?: string | null;
  status: "PENDING" | "RUNNING" | "COMPLETED" | "PARTIAL" | "FAILED" | "CANCELLED";
  requested_categories: string[];
  pages_requested: number;
  pages_analyzed: number;
  findings_count: number;
  warnings_count: number;
  errors_count: number;
  started_at?: string | null;
  completed_at?: string | null;
  error_message?: string | null;
  created_at: string;
  updated_at: string;
}

export interface AuditFinding {
  id: string;
  audit_id: string;
  code: string;
  category: string;
  severity: "INFO" | "LOW" | "MEDIUM" | "HIGH";
  confidence: "HIGH" | "MEDIUM" | "LOW";
  title: string;
  description: string;
  evidence: Record<string, any>;
  affected_page?: string | null;
  created_at: string;
}

export interface AuditPage {
  id: string;
  audit_id: string;
  url: string;
  status_code: number;
  response_time_ms: number;
  title?: string | null;
  content_type?: string | null;
  meta_description?: string | null;
  is_homepage: boolean;
  has_contact_form: boolean;
  created_at: string;
}

export interface BusinessAudit {
  id: string;
  business_id: string;
  research_record_id?: string | null;
  audit_job_id?: string | null;
  target_url?: string | null;
  audit_version: string;
  status: "AVAILABLE" | "UNAVAILABLE" | "TIMEOUT" | "REDIRECT_ERROR" | "BLOCKED" | "INVALID" | "NO_WEBSITE";
  overall_health: "HEALTHY" | "FAIR" | "NEEDS_ATTENTION" | "LIMITED_DATA";
  summary?: string | null;
  categories: Record<string, any>;
  findings: AuditFinding[];
  metrics: Record<string, any>;
  warnings: string[];
  errors: string[];
  started_at?: string | null;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface BusinessAuditHistory {
  business_id: string;
  total_audits: number;
  latest_audit?: BusinessAudit | null;
  audits: BusinessAudit[];
}

export interface AuditJobCreateInput {
  business_id: string;
  target_url?: string;
  requested_categories?: string[];
  pages_requested?: number;
}

export async function createAuditJob(data: AuditJobCreateInput): Promise<AuditJob> {
  const response = await api<{ data: AuditJob }>("/audits/jobs", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return response.data;
}

export async function listAuditJobs(params: {
  page?: number;
  page_size?: number;
  business_id?: string;
  status?: string;
} = {}): Promise<{ data: AuditJob[]; total: number }> {
  const query = new URLSearchParams();
  if (params.page) query.set("page", params.page.toString());
  if (params.page_size) query.set("page_size", params.page_size.toString());
  if (params.business_id) query.set("business_id", params.business_id);
  if (params.status) query.set("status", params.status);

  const response = await api<{ data: AuditJob[]; pagination: { total: number } }>(
    `/audits/jobs?${query.toString()}`
  );
  return { data: response.data, total: response.pagination.total };
}

export async function runAuditJob(jobId: string, runnerType: string = "MOCK"): Promise<AuditJob> {
  const response = await api<{ data: AuditJob }>(`/audits/jobs/${jobId}/run?runner_type=${runnerType}`, {
    method: "POST",
  });
  return response.data;
}

export async function runAuditAgentJob(jobId: string): Promise<AuditJob> {
  const response = await api<{ data: AuditJob }>(`/audits/jobs/${jobId}/run-agent`, {
    method: "POST",
  });
  return response.data;
}

export async function cancelAuditJob(jobId: string): Promise<AuditJob> {
  const response = await api<{ data: AuditJob }>(`/audits/jobs/${jobId}/cancel`, {
    method: "POST",
  });
  return response.data;
}

export async function getLatestBusinessAudit(businessId: string): Promise<BusinessAudit> {
  const response = await api<{ data: BusinessAudit }>(`/audits/businesses/${businessId}`);
  return response.data;
}

export async function getBusinessAuditHistory(businessId: string, limit: number = 20): Promise<BusinessAuditHistory> {
  const response = await api<{ data: BusinessAuditHistory }>(`/audits/businesses/${businessId}/history?limit=${limit}`);
  return response.data;
}

export async function listAuditFindings(
  businessId: string,
  category?: string,
  severity?: string
): Promise<AuditFinding[]> {
  const query = new URLSearchParams();
  if (category) query.set("category", category);
  if (severity) query.set("severity", severity);

  const response = await api<{ data: AuditFinding[] }>(`/audits/businesses/${businessId}/findings?${query.toString()}`);
  return response.data;
}
