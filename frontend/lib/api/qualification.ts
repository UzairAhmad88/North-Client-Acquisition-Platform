import { api } from "./client";

export interface QualificationFactor {
  name: string;
  status: "STRONG" | "MODERATE" | "WEAK" | "BLOCKED" | "UNKNOWN";
  assessment: string;
  confidence: "HIGH" | "MEDIUM" | "LOW";
  evidence?: any[];
}

export interface QualificationResult {
  id: string;
  lead_id: string;
  business_id: string;
  user_id?: string | null;
  agent_run_id?: string | null;
  decision: "QUALIFIED" | "POTENTIALLY_QUALIFIED" | "NEEDS_REVIEW" | "NOT_QUALIFIED" | "INSUFFICIENT_DATA";
  confidence: "HIGH" | "MEDIUM" | "LOW";
  summary?: string | null;
  factors: QualificationFactor[];
  reasons: string[];
  evidence: any[];
  risks: string[];
  missing_information: string[];
  limitations: string[];
  outreach_readiness: "READY" | "NEEDS_MANUAL_REVIEW" | "NOT_RECOMMENDED" | "OUTREACH_BLOCKED";
  recommended_internal_action?: string | null;
  qualification_version: string;
  is_stale: boolean;
  human_override_decision?: string | null;
  human_override_reason?: string | null;
  overridden_by_user_id?: string | null;
  overridden_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface HumanOverrideRequest {
  decision: "QUALIFIED" | "POTENTIALLY_QUALIFIED" | "NEEDS_REVIEW" | "NOT_QUALIFIED" | "INSUFFICIENT_DATA";
  reason: string;
}

export async function runLeadQualification(leadId: string): Promise<QualificationResult> {
  const response = await api<{ data: QualificationResult }>(`/leads/${leadId}/qualification`, {
    method: "POST",
  });
  return response.data;
}

export async function getLeadQualification(leadId: string): Promise<QualificationResult> {
  const response = await api<{ data: QualificationResult }>(`/leads/${leadId}/qualification`);
  return response.data;
}

export async function overrideLeadQualification(
  leadId: string,
  request: HumanOverrideRequest
): Promise<QualificationResult> {
  const response = await api<{ data: QualificationResult }>(`/leads/${leadId}/qualification/override`, {
    method: "POST",
    body: JSON.stringify(request),
  });
  return response.data;
}
