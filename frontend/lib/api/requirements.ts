import { api } from './client';

export interface ClientRequirement {
  id: string;
  discovery_session_id: string;
  business_id: string;
  lead_id?: string;
  category: string;
  title: string;
  description: string;
  source_type: string;
  source_reference?: string;
  explicit: boolean;
  confidence: string;
  status: string;
  priority: string;
  version: number;
  confirmed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface DiscoveryQuestion {
  id: string;
  discovery_session_id: string;
  question: string;
  category: string;
  priority: string;
  reason?: string;
  status: string;
  answer_text?: string;
  answered_at?: string;
  created_at: string;
}

export interface ScopeItem {
  id: string;
  discovery_session_id: string;
  requirement_id?: string;
  scope_status: string;
  description: string;
  priority: string;
  confirmed: boolean;
  version: number;
}

export interface DiscoverySession {
  id: string;
  business_id: string;
  lead_id?: string;
  conversation_id?: string;
  status: string;
  started_at: string;
  completed_at?: string;
  readiness_stage: string;
  readiness_score: number;
  completeness_score: number;
  scope_complexity: string;
  version: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface DiscoverySessionDetail extends DiscoverySession {
  requirements: ClientRequirement[];
  questions: DiscoveryQuestion[];
  scope_items: ScopeItem[];
}

export async function getDiscoverySessions(status?: string): Promise<DiscoverySession[]> {
  const query = status ? `?status=${encodeURIComponent(status)}` : '';
  const res = await api<DiscoverySession[]>(`/discovery-sessions${query}`);
  return res;
}

export async function createDiscoverySession(payload: {
  business_id: string;
  lead_id?: string;
  conversation_id?: string;
  notes?: string;
}): Promise<DiscoverySession> {
  return await api<DiscoverySession>('/discovery-sessions', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function getDiscoverySessionDetail(id: string): Promise<DiscoverySessionDetail> {
  return await api<DiscoverySessionDetail>(`/discovery-sessions/${id}`);
}

export async function analyzeDiscoverySession(id: string): Promise<DiscoverySessionDetail> {
  return await api<DiscoverySessionDetail>(`/discovery-sessions/${id}/analyze`, {
    method: 'POST',
  });
}

export async function confirmRequirement(sessionId: string, reqId: string): Promise<ClientRequirement> {
  return await api<ClientRequirement>(`/discovery-sessions/${sessionId}/requirements/${reqId}/confirm`, {
    method: 'POST',
  });
}

export async function answerQuestion(sessionId: string, qId: string, answerText: string): Promise<DiscoveryQuestion> {
  return await api<DiscoveryQuestion>(`/discovery-sessions/${sessionId}/questions/${qId}/answer`, {
    method: 'POST',
    body: JSON.stringify({ answer_text: answerText }),
  });
}
