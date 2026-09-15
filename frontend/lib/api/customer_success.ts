import { api } from './client';

export interface ClientProfile {
  id: string;
  tenant_id: string;
  client_id?: string;
  client_account_id?: string;
  company_name?: string;
  business_name?: string;
  industry?: string;
  company_size?: string;
  lifecycle_stage: string;
  relationship_manager_id?: string;
  executive_sponsor?: string;
  communication_cadence?: string;
  client_timezone?: string;
  strategic_tier?: string;
  relationship_strength?: string;
  tags?: string[];
  custom_fields?: Record<string, any>;
  created_at: string;
  updated_at?: string;
}

export interface ClientRelationship {
  id: string;
  tenant_id: string;
  client_id: string;
  contact_name: string;
  contact_email?: string;
  contact_role?: string;
  role_title?: string;
  decision_role: string;
  influence_level?: string;
  relationship_strength: string;
  last_interaction_date?: string;
  notes?: string;
  is_primary_contact?: boolean;
  created_at: string;
}

export interface ClientTimelineEvent {
  id: string;
  tenant_id: string;
  client_id?: string;
  client_profile_id?: string;
  event_category?: string;
  event_type: string;
  title: string;
  summary?: string;
  description?: string;
  occurred_at: string;
  actor_id?: string;
  actor_name?: string;
  visibility?: string;
  metadata_payload?: Record<string, any>;
  payload?: Record<string, any>;
  created_at: string;
}

export interface ClientGoal {
  id: string;
  tenant_id: string;
  client_id?: string;
  title: string;
  description?: string;
  target_date?: string;
  status: string;
  progress_percentage?: string;
  metric_target?: string;
  metric_current?: string;
  created_at: string;
  updated_at?: string;
}

export interface ClientHealthScore {
  id: string;
  tenant_id: string;
  client_id?: string;
  composite_score?: string;
  overall_score?: string;
  health_band: string;
  engagement_score?: string;
  project_health_score?: string;
  project_score?: string;
  support_satisfaction_score?: string;
  support_score?: string;
  financial_health_score?: string;
  finance_score?: string;
  relationship_health_score?: string;
  relationship_score?: string;
  goal_progress_score?: string;
  goal_score?: string;
  confidence_score?: string;
  confidence?: string;
  trend: string;
  explanation_summary?: string;
  explanation?: string;
  calculation_breakdown?: Record<string, any>;
  calculated_at: string;
}

export interface ClientRisk {
  id: string;
  tenant_id: string;
  client_id?: string;
  category?: string;
  risk_category?: string;
  title: string;
  description?: string;
  severity: string;
  impact_summary?: string;
  mitigation_plan?: string;
  owner_id?: string;
  status: string;
  detected_by?: string;
  resolved_at?: string;
  created_at: string;
}

export interface ClientOpportunity {
  id: string;
  tenant_id: string;
  client_id?: string;
  opportunity_type: string;
  title: string;
  description?: string;
  estimated_value: string;
  confidence_score?: string;
  confidence?: string;
  status: string;
  target_service_id?: string;
  linked_lead_id?: string;
  created_at: string;
}

export interface ClientRenewal {
  id: string;
  tenant_id: string;
  client_id?: string;
  contract_id?: string;
  subscription_id?: string;
  current_period_end?: string;
  renewal_date?: string;
  expiration_date?: string;
  status: string;
  estimated_renewal_value?: string;
  contract_value?: string;
  renewal_probability?: string;
  probability_pct?: string;
  assigned_owner_id?: string;
  notes?: string;
  created_at: string;
}

export interface Client360Dossier {
  profile?: ClientProfile;
  relationships?: ClientRelationship[];
  latest_health?: ClientHealthScore;
  goals?: ClientGoal[];
  active_risks?: ClientRisk[];
  opportunities?: ClientOpportunity[];
  upcoming_renewals?: ClientRenewal[];
  recent_timeline?: ClientTimelineEvent[];
  account_plans?: any[];
  reviews?: any[];
}

export const customerSuccessApi = {
  // Profiles
  listProfiles: (params?: { lifecycle_stage?: string; limit?: number }) =>
    api.get<ClientProfile[]>('/customer-success/profiles', { params }),

  getProfile: (clientId: string) =>
    api.get<ClientProfile>(`/customer-success/profiles/${clientId}`),

  upsertProfile: (data: Partial<ClientProfile>) =>
    api.post<ClientProfile>('/customer-success/profiles', data),

  // Stakeholders
  listRelationships: (clientId: string) =>
    api.get<ClientRelationship[]>(`/customer-success/relationships/${clientId}`),

  createRelationship: (data: Partial<ClientRelationship>) =>
    api.post<ClientRelationship>('/customer-success/relationships', data),

  // Timeline
  getTimeline: (clientId: string, params?: { visibility?: string; limit?: number }) =>
    api.get<ClientTimelineEvent[]>(`/customer-success/timeline/${clientId}`, { params }),

  createTimelineEvent: (data: Partial<ClientTimelineEvent>) =>
    api.post<ClientTimelineEvent>('/customer-success/timeline', data),

  // Goals
  listGoals: (clientId: string) =>
    api.get<ClientGoal[]>(`/customer-success/goals/${clientId}`),

  createGoal: (data: Partial<ClientGoal>) =>
    api.post<ClientGoal>('/customer-success/goals', data),

  // Health
  calculateHealth: (data: Record<string, any>) =>
    api.post<any>('/customer-success/health/calculate', data),

  recordHealth: (clientId: string, data: Record<string, any>) =>
    api.post<ClientHealthScore>(`/customer-success/health/${clientId}/record`, data),

  getLatestHealth: (clientId: string) =>
    api.get<ClientHealthScore>(`/customer-success/health/${clientId}/latest`),

  getHealthHistory: (clientId: string, limit: number = 30) =>
    api.get<any[]>(`/customer-success/health/${clientId}/history`, { params: { limit } }),

  // Risks
  listRisks: (params?: { client_id?: string; status?: string }) =>
    api.get<ClientRisk[]>('/customer-success/risks', { params }),

  createRisk: (data: Partial<ClientRisk>) =>
    api.post<ClientRisk>('/customer-success/risks', data),

  // Opportunities
  listOpportunities: (params?: { client_id?: string }) =>
    api.get<ClientOpportunity[]>('/customer-success/opportunities', { params }),

  createOpportunity: (data: Partial<ClientOpportunity>) =>
    api.post<ClientOpportunity>('/customer-success/opportunities', data),

  // Renewals
  listRenewals: (params?: { client_id?: string }) =>
    api.get<ClientRenewal[]>('/customer-success/renewals', { params }),

  createRenewal: (data: Partial<ClientRenewal>) =>
    api.post<ClientRenewal>('/customer-success/renewals', data),

  // Client 360
  getClient360: (clientId: string) =>
    api.get<Client360Dossier>(`/customer-success/clients/${clientId}/360`),

  // Client Portal Transparent Success
  getPortalOverview: () =>
    api.get<any>('/portal/success/overview'),

  getPortalGoals: () =>
    api.get<ClientGoal[]>('/portal/success/goals'),

  getPortalTimeline: (limit: number = 20) =>
    api.get<ClientTimelineEvent[]>('/portal/success/timeline', { params: { limit } }),

  submitPortalSurvey: (data: { survey_id: string; score: number; answers?: Record<string, any>; feedback_text?: string }) =>
    api.post<any>('/portal/success/surveys/submit', data),
};
