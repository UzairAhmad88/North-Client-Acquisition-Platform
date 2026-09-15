import { api } from './client';

export interface MessageItem {
  id: string;
  conversation_id: string;
  direction: 'INBOUND' | 'OUTBOUND';
  channel: string;
  subject?: string;
  body: string;
  status: string;
  provider_message_id?: string;
  sent_at?: string;
  created_at: string;
}

export interface ConversationAnalysis {
  id: string;
  conversation_id: string;
  latest_message_id?: string;
  primary_intent: string;
  all_intents: string[];
  intent_confidence: string;
  buying_signal_level: string;
  objection_type?: string;
  extracted_requirements: Array<{ category: string; item: string; is_explicit: boolean }>;
  missing_information: string[];
  conversation_stage: string;
  recommended_next_action: string;
  recommended_next_action_reason?: string;
  next_action_confidence: string;
  sentiment_signal: string;
  priority: string;
  human_correction?: Record<string, any>;
  human_correction_by_id?: string;
  human_correction_at?: string;
  created_at: string;
}

export interface ConversationDetail {
  id: string;
  lead_id: string;
  business_id: string;
  contact_id?: string;
  status: string;
  channel: string;
  current_intent?: string;
  conversation_stage: string;
  next_action?: string;
  priority: string;
  last_inbound_at?: string;
  created_at: string;
  updated_at: string;
  messages: MessageItem[];
  latest_analysis?: ConversationAnalysis;
}

export async function getConversations(status?: string): Promise<ConversationDetail[]> {
  const query = status ? `?status=${encodeURIComponent(status)}` : '';
  const res = await api<{ items: ConversationDetail[] }>(`/conversations${query}`);
  return res.items;
}

export async function getConversationDetail(id: string): Promise<ConversationDetail> {
  const res = await api<{ data: ConversationDetail }>(`/conversations/${id}`);
  return res.data;
}

export async function analyzeConversation(id: string): Promise<ConversationAnalysis> {
  const res = await api<{ data: ConversationAnalysis }>(`/conversations/${id}/analyze`, {
    method: 'POST',
  });
  return res.data;
}

export async function recordCorrection(
  id: string,
  correctedIntent?: string,
  correctedNextAction?: string,
  reason = 'Human operator correction'
): Promise<ConversationAnalysis> {
  const res = await api<{ data: ConversationAnalysis }>(`/conversations/${id}/correction`, {
    method: 'POST',
    body: JSON.stringify({
      corrected_intent: correctedIntent,
      corrected_next_action: correctedNextAction,
      reason,
    }),
  });
  return res.data;
}
