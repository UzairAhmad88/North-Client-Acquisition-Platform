import { api } from "./client";

export interface ClaimItem {
  statement: string;
  classification: "VERIFIED" | "INFERRED" | "GENERAL";
  is_supported: boolean;
  evidence_ids?: string[];
  risk_notes?: string | null;
}

export interface OutreachDraft {
  id: string;
  lead_id: string;
  business_id: string;
  user_id?: string | null;
  agent_run_id?: string | null;
  channel: "EMAIL" | "WHATSAPP" | "SMS" | "LINKEDIN" | "OTHER";
  tone: "PROFESSIONAL" | "FRIENDLY" | "CONCISE" | "CONSULTATIVE" | "LOCAL_BUSINESS";
  language: string;
  personalization_depth: "LIGHT" | "STANDARD" | "DEEP";
  objective: string;
  subject?: string | null;
  body: string;
  primary_angle: Record<string, any>;
  personalization_profile: Record<string, any>;
  claims: ClaimItem[];
  evidence: Record<string, any>[];
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "BLOCKED";
  outreach_readiness: "READY" | "NEEDS_MANUAL_REVIEW" | "NOT_RECOMMENDED" | "OUTREACH_BLOCKED";
  approval_status: "PENDING_APPROVAL" | "APPROVED" | "REJECTED" | "SENT" | "DELIVERED" | "BOUNCED" | "FAILED";
  rejection_reason?: string | null;
  version: number;
  content_hash?: string | null;
  is_stale: boolean;
  created_at: string;
  updated_at: string;
}

export interface OutreachEventItem {
  id: string;
  outreach_id: string;
  lead_id: string;
  business_id: string;
  user_id?: string | null;
  event_type: string;
  details: Record<string, any>;
  created_at: string;
}

export interface DncEntry {
  id: string;
  scope: string;
  target_value: string;
  reason?: string | null;
  is_active: boolean;
  created_at: string;
}

export async function runPersonalizationAgent(
  leadId: string,
  payload?: any
): Promise<OutreachDraft> {
  const response = await api<{ data: OutreachDraft }>(`/leads/${leadId}/personalization/run`, {
    method: "POST",
    body: JSON.stringify(payload || {}),
  });
  return response.data;
}

export async function getLatestPersonalization(leadId: string): Promise<OutreachDraft> {
  const response = await api<{ data: OutreachDraft }>(`/leads/${leadId}/personalization`);
  return response.data;
}

export async function getOutreachDraft(draftId: string): Promise<OutreachDraft> {
  const response = await api<{ data: OutreachDraft }>(`/outreach/drafts/${draftId}`);
  return response.data;
}

export async function updateOutreachDraft(
  draftId: string,
  payload: { subject?: string; body?: string; tone?: string; channel?: string }
): Promise<OutreachDraft> {
  const response = await api<{ data: OutreachDraft }>(`/outreach/drafts/${draftId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
  return response.data;
}

export async function approveOutreachDraft(draftId: string): Promise<OutreachDraft> {
  const response = await api<{ data: OutreachDraft }>(`/outreach/drafts/${draftId}/approve`, {
    method: "POST",
  });
  return response.data;
}

export async function rejectOutreachDraft(draftId: string, reason: string): Promise<OutreachDraft> {
  const response = await api<{ data: OutreachDraft }>(`/outreach/drafts/${draftId}/reject`, {
    method: "POST",
    body: JSON.stringify({ reason }),
  });
  return response.data;
}

export async function sendOutreachDraft(draftId: string): Promise<OutreachDraft> {
  const response = await api<{ data: OutreachDraft }>(`/outreach/drafts/${draftId}/send`, {
    method: "POST",
  });
  return response.data;
}

export async function getOutreachEvents(draftId: string): Promise<OutreachEventItem[]> {
  const response = await api<{ data: OutreachEventItem[] }>(`/outreach/drafts/${draftId}/events`);
  return response.data;
}

export async function listOutreachDrafts(
  approvalStatus?: string
): Promise<{ data: OutreachDraft[]; pagination: any }> {
  const query = approvalStatus ? `?approval_status=${approvalStatus}` : "";
  const response = await api<{ data: OutreachDraft[]; pagination: any }>(`/outreach/drafts${query}`);
  return response;
}

export async function addDncEntry(scope: string, targetValue: string, reason?: string): Promise<DncEntry> {
  const response = await api<{ data: DncEntry }>(`/outreach/dnc`, {
    method: "POST",
    body: JSON.stringify({ scope, target_value: targetValue, reason }),
  });
  return response.data;
}

export async function listDncEntries(): Promise<{ data: DncEntry[]; pagination: any }> {
  const response = await api<{ data: DncEntry[]; pagination: any }>(`/outreach/dnc`);
  return response;
}
