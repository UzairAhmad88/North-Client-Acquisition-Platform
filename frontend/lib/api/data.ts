import { api } from './client';

export type DataAuthority =
  | 'RAW_DATA'
  | 'NORMALIZED_DATA'
  | 'VERIFIED_DATA'
  | 'DERIVED_DATA'
  | 'AI_INFERENCE'
  | 'HUMAN_CONFIRMATION'
  | 'CONTRACTUAL_COMMITMENT'
  | 'SYSTEM_INTEGRATION';

export type DataClassification =
  | 'PUBLIC'
  | 'INTERNAL'
  | 'CONFIDENTIAL'
  | 'RESTRICTED';

export type KnowledgeLifecycle =
  | 'INGESTED'
  | 'INDEXED'
  | 'VERIFIED'
  | 'CANONICAL'
  | 'DEPRECATED'
  | 'ARCHIVED';

export interface DataSource {
  id: string;
  tenant_id: string;
  name: string;
  source_type: string;
  description?: string;
  is_authoritative: boolean;
  authority_level: DataAuthority;
  is_active: boolean;
  sync_schedule?: string;
  last_synced_at?: string;
  created_at: string;
  updated_at: string;
}

export interface DataCatalogItem {
  id: string;
  tenant_id: string;
  name: string;
  domain: string;
  table_or_entity_name: string;
  description?: string;
  classification: DataClassification;
  authority_level: DataAuthority;
  source_id?: string;
  schema_definition: Record<string, any>;
  data_owner?: string;
  data_steward?: string;
  is_active: boolean;
  sla_freshness_hours?: number;
  sla_quality_threshold?: number;
  created_at: string;
  updated_at: string;
}

export interface DataQualityRun {
  id: string;
  tenant_id: string;
  catalog_item_id?: string;
  rule_id?: string;
  overall_score: number;
  status: string;
  total_records_evaluated: number;
  passed_records: number;
  failed_records: number;
  dimension_scores: {
    completeness: number;
    accuracy: number;
    consistency: number;
    freshness: number;
    validity: number;
    uniqueness: number;
    provenance: number;
  };
  violations: Array<any>;
  executed_at: string;
}

export interface DataConflict {
  id: string;
  tenant_id: string;
  domain: string;
  entity_type: string;
  entity_id: string;
  conflict_type: string;
  conflicting_fields: string[];
  source_records: Array<any>;
  status: string;
  resolution_strategy?: string;
  detected_at: string;
  resolved_at?: string;
}

export interface LineageGraphResponse {
  entity_id: string;
  entity_type: string;
  upstream_nodes: Array<{
    id: string;
    type: string;
    relationship: string;
    transformation?: string;
    confidence_score: number;
  }>;
  downstream_nodes: Array<{
    id: string;
    type: string;
    relationship: string;
    transformation?: string;
    confidence_score: number;
  }>;
  edges: Array<{
    id: string;
    source_type: string;
    source_id: string;
    target_type: string;
    target_id: string;
    relationship: string;
    transformation_name?: string;
    confidence_score: number;
  }>;
}

export interface ProvenanceRecord {
  id: string;
  tenant_id: string;
  entity_type: string;
  entity_id: string;
  provenance_type: string;
  actor_id?: string;
  actor_type: string;
  source_system?: string;
  authority_level: DataAuthority;
  context_data: Record<string, any>;
  recorded_at: string;
}

export interface DocumentRecord {
  id: string;
  tenant_id: string;
  tracking_id: string;
  title: string;
  document_type: string;
  classification: DataClassification;
  authority_level: DataAuthority;
  status: string;
  current_version: number;
  latest_sha256: string;
  domain?: string;
  entity_type?: string;
  entity_id?: string;
  metadata_json: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface DocumentIntegrityVerification {
  document_id: string;
  version_number: number;
  expected_sha256: string;
  calculated_sha256: string;
  is_valid: boolean;
  verified_at: string;
}

export interface KnowledgeItem {
  id: string;
  tenant_id: string;
  canonical_key?: string;
  title: string;
  topic: string;
  domain: string;
  content: string;
  summary?: string;
  authority_level: DataAuthority;
  lifecycle_state: KnowledgeLifecycle;
  classification: DataClassification;
  confidence_score: number;
  provenance_source?: string;
  created_by?: string;
  verified_by?: string;
  verified_at?: string;
  created_at: string;
  updated_at: string;
}

export interface KnowledgeRetrievalResponse {
  query: string;
  results_count: number;
  items: Array<{
    id: string;
    title: string;
    topic: string;
    domain: string;
    content: string;
    authority_level: string;
    lifecycle_state: string;
    classification: string;
    confidence_score: number;
    provenance_source?: string;
  }>;
  retrieved_at: string;
}

export interface DataRetentionPolicy {
  id: string;
  tenant_id: string;
  domain: string;
  entity_type: string;
  classification?: DataClassification;
  retention_period_days: number;
  action_on_expiry: string;
  is_active: boolean;
  created_at: string;
}

export interface LegalHold {
  id: string;
  tenant_id: string;
  case_reference: string;
  reason: string;
  entity_type: string;
  entity_id: string;
  active: boolean;
  placed_by: string;
  placed_at: string;
  released_by?: string;
  released_at?: string;
  notes?: string;
}

// -------------------------------------------------------------
// API Client Functions
// -------------------------------------------------------------

export const dataApi = {
  // 1. Data Sources & Catalog
  listDataSources: () => api<DataSource[]>('/api/v1/data/sources'),
  createDataSource: (data: Partial<DataSource>) =>
    api<DataSource>('/api/v1/data/sources', { method: 'POST', body: JSON.stringify(data) }),
  listCatalogItems: (params?: { domain?: string; authority_level?: string; classification?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return api<DataCatalogItem[]>(`/api/v1/data/catalog${query ? `?${query}` : ''}`);
  },
  getCatalogItem: (id: string) => api<DataCatalogItem>(`/api/v1/data/catalog/${id}`),
  createCatalogItem: (data: Partial<DataCatalogItem>) =>
    api<DataCatalogItem>('/api/v1/data/catalog', { method: 'POST', body: JSON.stringify(data) }),

  // 2. Data Quality & Conflicts
  evaluateQuality: (payload: { records: any[]; schema_definition?: any; catalog_item_id?: string }) =>
    api<DataQualityRun>('/api/v1/data/quality/evaluate', { method: 'POST', body: JSON.stringify(payload) }),
  listQualityRuns: (catalog_item_id?: string) =>
    api<DataQualityRun[]>(`/api/v1/data/quality/runs${catalog_item_id ? `?catalog_item_id=${catalog_item_id}` : ''}`),
  listConflicts: (status?: string) =>
    api<DataConflict[]>(`/api/v1/data/conflicts${status ? `?status=${status}` : ''}`),
  detectConflicts: (payload: { domain: string; entity_type: string; entity_id: string; records: any[] }) =>
    api<DataConflict[]>('/api/v1/data/conflicts/detect', { method: 'POST', body: JSON.stringify(payload) }),

  // 3. Lineage & Provenance
  getLineageGraph: (entityType: string, entityId: string) =>
    api<LineageGraphResponse>(`/api/v1/data/lineage/${entityType}/${entityId}`),
  addLineageEdge: (edge: any) =>
    api<{ id: string; status: string }>('/api/v1/data/lineage/edges', { method: 'POST', body: JSON.stringify(edge) }),
  getProvenance: (entityType: string, entityId: string) =>
    api<ProvenanceRecord[]>(`/api/v1/data/provenance/${entityType}/${entityId}`),

  // 4. Documents & Integrity Verification
  listDocuments: (params?: { document_type?: string; status?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return api<DocumentRecord[]>(`/api/v1/data/documents${query ? `?${query}` : ''}`);
  },
  getDocument: (id: string) => api<DocumentRecord>(`/api/v1/data/documents/${id}`),
  createDocument: (data: { title: string; document_type: string; content: string; summary?: string; classification?: string; authority_level?: string; domain?: string; entity_type?: string; entity_id?: string }) =>
    api<DocumentRecord>('/api/v1/data/documents', { method: 'POST', body: JSON.stringify(data) }),
  verifyDocument: (documentId: string, content: string, versionNumber: number = 1) =>
    api<DocumentIntegrityVerification>(`/api/v1/data/documents/${documentId}/verify`, {
      method: 'POST',
      body: JSON.stringify({ content, version_number: versionNumber }),
    }),

  // 5. Knowledge Base & Context Retrieval
  listKnowledgeItems: (params?: { domain?: string; lifecycle_state?: string; authority_level?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return api<KnowledgeItem[]>(`/api/v1/data/knowledge${query ? `?${query}` : ''}`);
  },
  createKnowledgeItem: (data: Partial<KnowledgeItem>) =>
    api<KnowledgeItem>('/api/v1/data/knowledge', { method: 'POST', body: JSON.stringify(data) }),
  promoteKnowledgeItem: (itemId: string, targetLifecycle: string, notes?: string) =>
    api<KnowledgeItem>(`/api/v1/data/knowledge/${itemId}/promote`, {
      method: 'POST',
      body: JSON.stringify({ target_lifecycle: targetLifecycle, notes }),
    }),
  retrieveKnowledgeContext: (query: string, domain?: string, minAuthority?: string) =>
    api<KnowledgeRetrievalResponse>('/api/v1/data/knowledge/retrieve', {
      method: 'POST',
      body: JSON.stringify({ query, domain, min_authority: minAuthority }),
    }),

  // 6. Retention Policies & Legal Holds
  listRetentionPolicies: (domain?: string) =>
    api<DataRetentionPolicy[]>(`/api/v1/data/retention/policies${domain ? `?domain=${domain}` : ''}`),
  createRetentionPolicy: (data: Partial<DataRetentionPolicy>) =>
    api<DataRetentionPolicy>('/api/v1/data/retention/policies', { method: 'POST', body: JSON.stringify(data) }),
  listLegalHolds: (activeOnly: boolean = true) =>
    api<LegalHold[]>(`/api/v1/data/retention/legal-holds?active_only=${activeOnly}`),
  placeLegalHold: (data: { case_reference: string; reason: string; entity_type: string; entity_id: string; notes?: string }) =>
    api<LegalHold>('/api/v1/data/retention/legal-holds', { method: 'POST', body: JSON.stringify(data) }),
  releaseLegalHold: (holdId: string, notes?: string) =>
    api<LegalHold>(`/api/v1/data/retention/legal-holds/${holdId}/release`, {
      method: 'POST',
      body: JSON.stringify({ notes }),
    }),
  checkCanDelete: (entityType: string, entityId: string) =>
    api<{ can_delete: boolean; reason: string; message: string }>(
      `/api/v1/data/retention/check-delete/${entityType}/${entityId}`
    ),
};
