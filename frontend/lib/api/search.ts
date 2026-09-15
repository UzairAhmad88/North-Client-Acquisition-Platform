import { api } from './client';

export interface SearchResultItem {
  id: string;
  entity_type: string;
  entity_id: string;
  tenant_id: string;
  title: string;
  snippet: string;
  score: number;
  status?: string;
  priority?: string;
  action_url?: string;
  updated_at?: string;
  metadata?: Record<string, any>;
}

export interface SearchResponse {
  query: string;
  parsed_query: {
    search_type: string;
    entity_types: string[];
    status?: string;
    priority?: string;
  };
  total_count: number;
  results: SearchResultItem[];
  facets: Record<string, number>;
  latency_ms: number;
  index_freshness: string;
  index_version: number;
}

export interface SearchSuggestion {
  text: string;
  type: string;
  category?: string;
  entity_type?: string;
  entity_id?: string;
  query?: string;
}

export interface SavedSearch {
  id: string;
  tenant_id: string;
  user_id: string;
  name: string;
  query_text: string;
  filters_json: Record<string, any>;
  is_pinned: boolean;
  created_at: string;
}

export interface SearchPin {
  id: string;
  tenant_id: string;
  user_id: string;
  entity_type: string;
  entity_id: string;
  title: string;
  action_url: string;
  created_at: string;
}

export interface CommandDefinition {
  command_id: string;
  name: string;
  description: string;
  category: string;
  risk_level: string;
  requires_confirmation: boolean;
  requires_approval: boolean;
  parameters_schema: Record<string, any>;
}

export interface CommandResponse {
  request_id: string;
  command_id: string;
  category: string;
  risk_level: string;
  parameters: Record<string, any>;
  status: string;
  requires_confirmation: boolean;
  requires_approval: boolean;
  approval_reason?: string;
  execution_result?: Record<string, any>;
  error?: string;
  created_at: string;
}

export interface AssistantSource {
  entity_type: string;
  entity_id: string;
  title: string;
  action_url?: string;
  snippet?: string;
  confidence: number;
}

export interface AssistantQueryResponse {
  session_id: string;
  question: string;
  answer: string;
  answer_type: string;
  sources: AssistantSource[];
  suggested_actions: Array<{ label: string; command: string; url?: string }>;
  created_at: string;
  ai_trace_id?: string;
}

export const searchApi = {
  // Global Search
  search: (params: {
    q: string;
    entity_type?: string;
    status?: string;
    priority?: string;
    limit?: number;
    offset?: number;
  }) => {
    const query = new URLSearchParams();
    query.append('q', params.q);
    if (params.entity_type) query.append('entity_type', params.entity_type);
    if (params.status) query.append('status', params.status);
    if (params.priority) query.append('priority', params.priority);
    if (params.limit) query.append('limit', String(params.limit));
    if (params.offset) query.append('offset', String(params.offset));
    return api<SearchResponse>(`/search?${query.toString()}`);
  },

  getSuggestions: (q: string) =>
    api<SearchSuggestion[]>(`/search/suggestions?q=${encodeURIComponent(q)}`),

  listSavedSearches: () => api<SavedSearch[]>('/search/saved'),

  createSavedSearch: (payload: {
    name: string;
    query_text: string;
    filters_json?: Record<string, any>;
    is_pinned?: boolean;
  }) => api<SavedSearch>('/search/saved', { method: 'POST', body: JSON.stringify(payload) }),

  deleteSavedSearch: (id: string) =>
    api<any>(`/search/saved/${id}`, { method: 'DELETE' }),

  listPins: () => api<SearchPin[]>('/search/pins'),

  createPin: (payload: {
    entity_type: string;
    entity_id: string;
    title: string;
    action_url: string;
  }) => api<SearchPin>('/search/pins', { method: 'POST', body: JSON.stringify(payload) }),

  deletePin: (id: string) => api<any>(`/search/pins/${id}`, { method: 'DELETE' }),

  // Command Palette
  listCommands: () => api<CommandDefinition[]>('/command/registry'),

  parseCommand: (text: string) =>
    api<CommandResponse>('/command/parse', {
      method: 'POST',
      body: JSON.stringify({ text }),
    }),

  validateCommand: (commandId: string, parameters?: Record<string, any>) =>
    api<any>('/command/validate', {
      method: 'POST',
      body: JSON.stringify({ command_id: commandId, parameters: parameters || {} }),
    }),

  executeCommand: (payload: {
    command_id: string;
    parameters?: Record<string, any>;
    has_confirmation?: boolean;
    has_approval?: boolean;
  }) =>
    api<CommandResponse>('/command/execute', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  // Platform Assistant
  askAssistant: (payload: { question: string; session_id?: string }) =>
    api<AssistantQueryResponse>('/assistant/query', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  getSessionHistory: (sessionId: string) =>
    api<any[]>(`/assistant/sessions/${sessionId}/history`),
};
