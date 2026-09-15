import { api } from './client';

export interface SupportRequestVersion {
  id: string;
  support_request_id: string;
  version_number: number;
  description: string;
  content_hash: string;
  created_by: string;
  created_at: string;
}

export interface SupportRequestEvent {
  id: string;
  support_request_id: string;
  event_type: string;
  actor_id: string;
  actor_type: string;
  event_data?: Record<string, any>;
  created_at: string;
}

export interface SupportRequestEvidence {
  id: string;
  support_request_id: string;
  file_name: string;
  file_path: string;
  file_type: string;
  sha256_hash: string;
  file_size_bytes: number;
  uploaded_by: string;
  created_at: string;
}

export interface SupportRequest {
  id: string;
  request_number: string;
  project_id: string;
  business_id?: string;
  client_account_id?: string;
  contract_id?: string;
  release_version_id?: string;
  requester: string;
  requester_email?: string;
  title: string;
  description: string;
  category: string;
  classification: string;
  priority: string;
  severity: string;
  status: string;
  warranty_status: string;
  maintenance_status: string;
  sla_status: string;
  assigned_to?: string;
  resolution_summary?: string;
  resolved_at?: string;
  closed_at?: string;
  created_at: string;
  updated_at: string;
  versions?: SupportRequestVersion[];
  events?: SupportRequestEvent[];
  evidences?: SupportRequestEvidence[];
}

export interface IncidentTimeline {
  id: string;
  incident_id: string;
  milestone: string;
  description: string;
  recorded_by: string;
  recorded_at: string;
}

export interface Incident {
  id: string;
  incident_number: string;
  project_id: string;
  title: string;
  description: string;
  severity: string;
  status: string;
  affected_service: string;
  impact_summary?: string;
  root_cause?: string;
  mitigation_steps?: string;
  postmortem?: string;
  detected_at: string;
  acknowledged_at?: string;
  mitigated_at?: string;
  resolved_at?: string;
  closed_at?: string;
  created_at: string;
  timelines?: IncidentTimeline[];
}

export interface Warranty {
  id: string;
  project_id: string;
  contract_id?: string;
  title: string;
  terms?: string;
  exclusions?: string;
  start_date: string;
  end_date?: string;
  status: string;
  created_at: string;
}

export interface MaintenanceWorkOrder {
  id: string;
  maintenance_plan_id: string;
  project_id: string;
  task_name: string;
  category: string;
  priority: string;
  status: string;
  scheduled_at: string;
  executed_at?: string;
  executed_by?: string;
  result_summary?: string;
  created_at: string;
}

export interface MaintenancePlan {
  id: string;
  project_id: string;
  title: string;
  plan_type: string;
  scope_description: string;
  frequency: string;
  status: string;
  start_date: string;
  end_date?: string;
  created_at: string;
  work_orders?: MaintenanceWorkOrder[];
}

export interface KnowledgeArticle {
  id: string;
  project_id?: string;
  title: string;
  content: string;
  article_type: string;
  visibility: string;
  status: string;
  author: string;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface ClientHealthSnapshot {
  id: string;
  project_id: string;
  business_id?: string;
  health_score: number;
  health_status: string;
  open_tickets_count: number;
  incident_count: number;
  satisfaction_score?: number;
  recommendations?: any;
  evaluated_at: string;
}

export interface SupportOpportunity {
  id: string;
  project_id: string;
  business_id?: string;
  support_request_id?: string;
  title: string;
  description: string;
  opportunity_type: string;
  estimated_value?: number;
  confidence: number;
  status: string;
  created_at: string;
}

export const supportApi = {
  // Support Requests
  createRequest: (data: {
    project_id: string;
    title: string;
    description: string;
    requester?: string;
    requester_email?: string;
    category?: string;
  }) =>
    api<SupportRequest>('/support/requests', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  listRequests: (params?: {
    project_id?: string;
    client_account_id?: string;
    business_id?: string;
    classification?: string;
    status?: string;
  }) => {
    const query = new URLSearchParams();
    if (params?.project_id) query.append('project_id', params.project_id);
    if (params?.classification) query.append('request_type', params.classification);
    if (params?.status) query.append('status', params.status);
    const qs = query.toString();
    return api<SupportRequest[]>(`/support/requests${qs ? `?${qs}` : ''}`);
  },

  getRequestDetail: (id: string) => api<SupportRequest>(`/support/requests/${id}`),

  updateStatus: (id: string, data: { status: string; notes?: string; rejection_reason?: string }) =>
    api<SupportRequest>(`/support/requests/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  addEvidence: (id: string, data: {
    evidence_type: string;
    title: string;
    file_path?: string;
    file_size_bytes?: number;
    mime_type?: string;
  }) =>
    api<SupportRequestEvidence>(`/support/requests/${id}/evidence`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  troubleshoot: (id: string, logs?: string[]) =>
    api<{
      possible_root_causes: string[];
      suggested_steps: string[];
      confidence: number;
      prevention_tips: string[];
    }>(`/support/requests/${id}/troubleshoot`, {
      method: 'POST',
      body: JSON.stringify({ logs: logs || [] }),
    }),

  evaluateWarranty: (id: string, data?: { approve_warranty: boolean; exclusion_reason?: string }) =>
    api<any>(`/support/requests/${id}/evaluate-warranty`, {
      method: 'POST',
      body: JSON.stringify(data || {}),
    }),

  routeToChange: (id: string, data: { change_request_id?: string; notes?: string }) =>
    api<SupportRequest>(`/support/requests/${id}/route-to-change`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Incidents
  createIncident: (data: {
    title: string;
    summary: string;
    severity: string;
    project_id?: string;
    lead_incident_commander?: string;
  }) =>
    api<Incident>('/support/incidents', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  listIncidents: (params?: { project_id?: string; severity?: string; status?: string }) => {
    const query = new URLSearchParams();
    if (params?.project_id) query.append('project_id', params.project_id);
    if (params?.severity) query.append('severity', params.severity);
    if (params?.status) query.append('status', params.status);
    const qs = query.toString();
    return api<Incident[]>(`/support/incidents${qs ? `?${qs}` : ''}`);
  },

  getIncidentDetail: (id: string) => api<Incident>(`/support/incidents/${id}`),

  updateIncidentStatus: (id: string, data: { status: string; message: string; root_cause?: string; resolution_summary?: string }) =>
    api<Incident>(`/support/incidents/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  // Warranties
  createWarranty: (data: Partial<Warranty>) =>
    api<Warranty>('/support/warranties', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getProjectWarranty: (projectId: string) => api<Warranty>(`/support/projects/${projectId}/warranty`),

  listWarranties: (params?: { client_account_id?: string; status?: string }) =>
    api<Warranty[]>('/support/warranties'),

  // Maintenance Plans & Work Orders
  createMaintenancePlan: (data: Partial<MaintenancePlan>) =>
    api<MaintenancePlan>('/support/maintenance-plans', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  listMaintenancePlans: (params?: { project_id?: string; client_account_id?: string; status?: string }) =>
    api<MaintenancePlan[]>('/support/maintenance-plans'),

  getMaintenancePlanDetail: (id: string) => api<MaintenancePlan>(`/support/maintenance-plans/${id}`),

  scheduleWorkOrder: (planId: string, data: { title: string; scheduled_for: string; project_id?: string }) =>
    api<MaintenanceWorkOrder>(`/support/maintenance-plans/${planId}/work-orders`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  listWorkOrders: (params?: { plan_id?: string; project_id?: string; status?: string }) =>
    api<MaintenanceWorkOrder[]>('/support/work-orders'),

  completeWorkOrder: (orderId: string, data: { execution_notes: string; checklist_results?: any[] }) =>
    api<MaintenanceWorkOrder>(`/support/work-orders/${orderId}/complete`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Knowledge Articles
  createKnowledgeArticle: (data: Partial<KnowledgeArticle>) =>
    api<KnowledgeArticle>('/support/knowledge-articles', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  listKnowledgeArticles: (params?: { business_id?: string; category?: string; is_published?: boolean }) =>
    api<KnowledgeArticle[]>('/support/knowledge-articles'),

  // Client Health & Opportunities
  getClientHealth: (clientAccountId: string, params?: { open_tickets?: number; incidents?: number }) =>
    api<ClientHealthSnapshot>(`/support/clients/${clientAccountId}/health`),

  listOpportunities: (params?: { client_account_id?: string; project_id?: string; status?: string }) =>
    api<SupportOpportunity[]>('/support/opportunities'),

  detectOpportunities: (clientAccountId: string, data?: { project_id?: string; ticket_summaries?: string[] }) =>
    api<SupportOpportunity[]>(`/support/clients/${clientAccountId}/detect-opportunities`, {
      method: 'POST',
      body: JSON.stringify(data || {}),
    }),
};
