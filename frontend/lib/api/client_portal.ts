import { api } from './client';

export interface ThreadMessage {
  id: string;
  thread_id: string;
  sender_id: string;
  sender_type: string;
  content: string;
  visibility: string;
  created_at: string;
}

export interface DiscussionThread {
  id: string;
  project_id: string;
  deliverable_id?: string;
  type: string;
  title: string;
  status: string;
  visibility: string;
  messages: ThreadMessage[];
  created_at: string;
}

export interface DeliverableApproval {
  id: string;
  deliverable_id: string;
  version_number: number;
  content_hash: string;
  approval_statement: string;
  signer_name: string;
  signer_email: string;
  approved_at: string;
}

export interface ProjectFileAsset {
  id: string;
  project_id: string;
  filename: string;
  mime_type: string;
  size_bytes: number;
  visibility: string;
  status: string;
  created_at: string;
}

export async function listProjectThreads(projectId: string) {
  return api<DiscussionThread[]>(`/client/projects/${projectId}/threads?is_client_view=true`);
}

export async function createThread(projectId: string, payload: { title: string; thread_type?: string; deliverable_id?: string }) {
  return api<DiscussionThread>(`/client/projects/${projectId}/threads`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function postMessage(threadId: string, payload: { content: string }) {
  return api<ThreadMessage>(`/client/threads/${threadId}/messages`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function approveDeliverable(deliverableId: string, payload: { version_number: number; approval_statement: string; content_payload: string }) {
  return api<DeliverableApproval>(`/client/deliverables/${deliverableId}/approve`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function listProjectFiles(projectId: string) {
  return api<ProjectFileAsset[]>(`/client/projects/${projectId}/files?is_client_view=true`);
}

export async function runClientAgent(projectId: string, action: 'CLASSIFY_REQUEST' | 'SUMMARIZE_FEEDBACK' | 'EXTRACT_ACTIONS' | 'EVALUATE_SCOPE') {
  return api<any>(`/client/projects/${projectId}/run-agent?action=${action}`, {
    method: 'POST',
  });
}
