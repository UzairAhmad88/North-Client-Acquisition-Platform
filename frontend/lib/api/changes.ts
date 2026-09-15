import { api } from './client';

export interface ChangeImpact {
  id: string;
  impact_type: string;
  entity_type?: string;
  entity_id?: string;
  impact_action: string;
  impact_description: string;
  confidence: string;
  created_at: string;
}

export interface ChangeVersion {
  id: string;
  version_number: number;
  description: string;
  scope_summary?: string;
  commercial_summary?: string;
  schedule_summary?: string;
  impact_summary?: string;
  content_hash: string;
  created_at: string;
  impacts: ChangeImpact[];
}

export interface ChangeRequest {
  id: string;
  change_number: string;
  project_id: string;
  business_id?: string;
  title: string;
  description: string;
  category: string;
  classification: string;
  status: string;
  priority: string;
  source: string;
  requested_by: string;
  requested_at: string;
  impact_status: string;
  approval_status: string;
  client_approval_status: string;
  implementation_status: string;
  created_at: string;
  versions: ChangeVersion[];
}

export async function listProjectChanges(projectId: string) {
  return api<ChangeRequest[]>(`/projects/${projectId}/changes`);
}

export async function createChangeRequest(
  projectId: string,
  payload: { title: string; description: string; category?: string; source?: string; requested_by?: string }
) {
  return api<ChangeRequest>(`/projects/${projectId}/changes`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function getChangeDetail(changeId: string) {
  return api<ChangeRequest>(`/changes/${changeId}`);
}

export async function triageChange(changeId: string) {
  return api<ChangeRequest>(`/changes/${changeId}/triage`, {
    method: 'POST',
  });
}

export async function analyzeChangeImpact(changeId: string) {
  return api<any>(`/changes/${changeId}/analyze`, {
    method: 'POST',
  });
}

export async function approveInternalChange(changeId: string, approverId: string = 'North Operator') {
  return api<ChangeRequest>(`/changes/${changeId}/approve?approver_id=${encodeURIComponent(approverId)}`, {
    method: 'POST',
  });
}

export async function approveClientChange(
  changeId: string,
  payload: { approval_statement: string; signer_id?: string }
) {
  return api<ChangeRequest>(`/changes/${changeId}/client-approve`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateBaselineVersion(changeId: string) {
  return api<{ baseline_id: string; version: number; scope_hash: string }>(`/changes/${changeId}/baseline`, {
    method: 'POST',
  });
}

export async function implementChangeTasks(changeId: string) {
  return api<{ task_count: number; task_ids: string[] }>(`/changes/${changeId}/implement`, {
    method: 'POST',
  });
}
