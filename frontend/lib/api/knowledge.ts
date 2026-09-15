import { api } from './client';

export interface KnowledgeOverview {
  tenant_id: string;
  total_items: number;
  total_facts: number;
  total_decisions: number;
  total_lessons: number;
  open_conflicts_count: number;
  quality_scorecard: {
    total_items: number;
    overall_quality_score: number;
    completeness_score: number;
    authority_score: number;
    freshness_score: number;
    provenance_score: number;
    consistency_score: number;
    uniqueness_score: number;
    metrics: {
      verified_count: number;
      human_confirmed_count: number;
      inferred_count: number;
      stale_count: number;
      expired_count: number;
      conflicted_count: number;
      missing_provenance_count: number;
      low_confidence_count: number;
      duplicate_candidate_count: number;
    };
  };
  domain_breakdown: Record<string, number>;
  authority_breakdown: Record<string, number>;
  recent_context_assemblies_count: number;
  status: string;
  timestamp: string;
}

export interface KnowledgeItem {
  knowledge_code: string;
  tenant_id: string;
  title: string;
  content: string;
  summary?: string;
  domain: string;
  item_type: string;
  provenance: string;
  authority: string;
  confidence: number;
  classification: string;
  freshness_status: string;
  version: number;
  status: string;
  owner_id: string;
  content_hash: string;
  created_at: string;
  updated_at: string;
}

export interface SearchResult {
  knowledge_code: string;
  title: string;
  snippet: string;
  domain: string;
  item_type: string;
  authority: string;
  provenance: string;
  freshness: string;
  score: number;
  relevance_factors: Record<string, number>;
}

export interface ContextBundle {
  request_code: string;
  agent_id: string;
  task_intent: string;
  budget_tokens: number;
  consumed_tokens: number;
  items_count: number;
  citations: string[];
  encapsulated_context: string;
  uncertainty_disclosures: string[];
  assembled_at: string;
}

export interface KnowledgeConflict {
  conflict_code: string;
  tenant_id: string;
  source_a_code: string;
  source_b_code: string;
  description: string;
  status: string;
  detected_at: string;
  resolved_by?: string;
  resolved_at?: string;
  resolution_notes?: string;
}

export interface DecisionRecord {
  decision_code: string;
  tenant_id: string;
  title: string;
  question: string;
  context_background: string;
  options_considered: Array<{ option: string; pros: string; cons: string }>;
  decision_outcome: string;
  rationale: string;
  owner_id: string;
  approver_ids: string[];
  evidence_references: string[];
  status: string;
  decided_at: string;
}

export interface LessonItem {
  lesson_code: string;
  tenant_id: string;
  title: string;
  context_scope: string;
  problem: string;
  root_cause: string;
  what_worked: string;
  what_failed: string;
  recommendation: string;
  applicability_domain: string;
  owner_id: string;
  confidence: number;
}

export interface KnowledgeGraphData {
  nodes: Array<{ id: string; name: string; type: string; domain: string }>;
  edges: Array<{ source: string; target: string; type: string; confidence: number }>;
}

export async function getKnowledgeOverview(tenantId = 'default_tenant'): Promise<KnowledgeOverview> {
  const { data } = await api.get<KnowledgeOverview>(`/api/v1/knowledge/overview?tenant_id=${tenantId}`);
  return data;
}

export async function listKnowledgeItems(domain?: string, tenantId = 'default_tenant'): Promise<KnowledgeItem[]> {
  const url = domain
    ? `/api/v1/knowledge/items?domain=${domain}&tenant_id=${tenantId}`
    : `/api/v1/knowledge/items?tenant_id=${tenantId}`;
  const { data } = await api.get<KnowledgeItem[]>(url);
  return data;
}

export async function createKnowledgeItem(payload: {
  knowledge_code: string;
  title: string;
  content: string;
  domain?: string;
  item_type?: string;
  authority?: string;
  provenance?: string;
  confidence?: number;
  classification?: string;
  is_ai_generated?: boolean;
}): Promise<KnowledgeItem> {
  const { data } = await api.post<KnowledgeItem>('/api/v1/knowledge/items', payload);
  return data;
}

export async function searchKnowledge(payload: {
  query: string;
  domain?: string;
  strategy?: string;
  top_k?: number;
}): Promise<SearchResult[]> {
  const { data } = await api.post<SearchResult[]>('/api/v1/knowledge/search', payload);
  return data;
}

export async function assembleAiContext(payload: {
  task_intent: string;
  agent_id?: string;
  budget_tokens?: number;
  domain?: string;
}): Promise<ContextBundle> {
  const { data } = await api.post<ContextBundle>('/api/v1/knowledge/context', payload);
  return data;
}

export async function processDocument(payload: {
  document_id: string;
  title: string;
  content: string;
  doc_type?: string;
}): Promise<any> {
  const { data } = await api.post('/api/v1/knowledge/documents/process', payload);
  return data;
}

export async function getKnowledgeGraph(rootCode?: string, maxHops = 2): Promise<KnowledgeGraphData> {
  const url = rootCode
    ? `/api/v1/knowledge/graph?root_code=${rootCode}&max_hops=${maxHops}`
    : `/api/v1/knowledge/graph?max_hops=${maxHops}`;
  const { data } = await api.get<KnowledgeGraphData>(url);
  return data;
}

export async function listConflicts(): Promise<KnowledgeConflict[]> {
  const { data } = await api.get<KnowledgeConflict[]>('/api/v1/knowledge/conflicts');
  return data;
}

export async function resolveConflict(conflictCode: string, payload: {
  resolved_by: string;
  resolution_notes: string;
}): Promise<KnowledgeConflict> {
  const { data } = await api.post<KnowledgeConflict>(`/api/v1/knowledge/conflicts/${conflictCode}/resolve`, payload);
  return data;
}

export async function listDecisions(): Promise<DecisionRecord[]> {
  const { data } = await api.get<DecisionRecord[]>('/api/v1/knowledge/decisions');
  return data;
}

export async function listLessons(): Promise<LessonItem[]> {
  const { data } = await api.get<LessonItem[]>('/api/v1/knowledge/lessons');
  return data;
}

export async function getKnowledgeQuality(): Promise<any> {
  const { data } = await api.get('/api/v1/knowledge/quality');
  return data;
}

export async function submitSearchFeedback(payload: {
  query: string;
  result_code: string;
  is_helpful: boolean;
  feedback_text?: string;
}): Promise<any> {
  const { data } = await api.post('/api/v1/knowledge/feedback', payload);
  return data;
}
