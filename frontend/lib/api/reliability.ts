import { api } from './client';

export interface ComponentHealth {
  component_name: string;
  component_type: string;
  status: 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY' | 'CRITICAL';
  latency_ms: number;
  is_critical: boolean;
  message?: string;
  details?: Record<string, any>;
  checked_at?: string;
}

export interface DeepHealthResult {
  status: 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY' | 'CRITICAL';
  active_circuit_breakers: number;
  open_incidents: number;
  components: Record<string, ComponentHealth>;
  timestamp: string;
}

export interface CircuitBreakerState {
  service_name: string;
  state: 'CLOSED' | 'OPEN' | 'HALF_OPEN';
  failure_count: number;
  success_count: number;
  failure_threshold: number;
  recovery_timeout: number;
  last_state_change?: string;
}

export interface SLOMetricSnapshot {
  slo_type: string;
  name: string;
  target_slo: number;
  current_sli: number;
  error_budget_remaining_pct: number;
  burn_rate_1h: number;
  burn_rate_24h: number;
  budget_status: 'HEALTHY' | 'WARNING' | 'EXHAUSTED' | 'BREACHED';
  total_events: number;
  bad_events: number;
  recorded_at: string;
}

export interface ErrorBudgetSummary {
  overall_status: string;
  slos: SLOMetricSnapshot[];
  generated_at: string;
}

export interface ReliabilityIncident {
  id: string;
  title: string;
  severity: 'SEV1_CRITICAL' | 'SEV2_MAJOR' | 'SEV3_MODERATE' | 'SEV4_LOW';
  status: 'TRIGGERED' | 'ACKNOWLEDGED' | 'INVESTIGATING' | 'MITIGATED' | 'RESOLVED' | 'CLOSED';
  affected_services: string[];
  lead_responder?: string;
  responders: string[];
  impact_summary: string;
  timeline_events: Array<{
    timestamp: string;
    description: string;
    actor: string;
  }>;
  mitigation_steps: Array<{
    step: string;
    completed: boolean;
  }>;
  started_at: string;
  acknowledged_at?: string;
  mitigated_at?: string;
  resolved_at?: string;
  created_at?: string;
}

export interface IncidentPostmortem {
  id: string;
  incident_id: string;
  summary: string;
  root_cause: string;
  five_whys: string[];
  timeline_events: Array<{
    timestamp: string;
    description: string;
    actor: string;
  }>;
  what_went_well: string[];
  what_could_improve: string[];
  action_items: Array<{
    task: string;
    owner: string;
    status: string;
    due_date?: string;
  }>;
  owner: string;
  created_at: string;
}

export interface BackupRecord {
  id: string;
  backup_type: string;
  status: string;
  size_bytes: number;
  storage_location: string;
  checksum_sha256: string;
  verified: boolean;
  retention_days: number;
  started_at: string;
  completed_at?: string;
}

export interface RestoreVerificationTest {
  test_id: string;
  backup_id: string;
  environment: string;
  status: string;
  rto_achieved_seconds: number;
  data_integrity_passed: boolean;
  tables_restored_count: number;
  records_verified_count: number;
  logs: Array<Record<string, any>>;
  executed_at: string;
}

export interface DRPlan {
  plan_name: string;
  scenario: string;
  target_rpo_minutes: number;
  target_rto_minutes: number;
  primary_region: string;
  secondary_region: string;
  status: string;
  recovery_steps: Array<{
    step: number;
    name: string;
    action: string;
    expected_duration_seconds: number;
    automated: boolean;
  }>;
}

export interface DRDrill {
  drill_id: string;
  scenario: string;
  initiated_by: string;
  status: string;
  actual_rto_minutes: number;
  data_loss_minutes: number;
  step_results: Array<Record<string, any>>;
  observations: string;
  lessons_learned: string[];
  started_at: string;
  completed_at: string;
}

export interface DeploymentRecord {
  id: string;
  version: string;
  environment: string;
  deployed_by: string;
  git_commit_sha: string;
  status: string;
  smoke_tests_passed: boolean;
  migrations_applied: boolean;
  release_notes?: string;
  deployed_at: string;
}

export interface FeatureFlag {
  name: string;
  description?: string;
  enabled: boolean;
  percentage_rollout: number;
  allowed_tiers?: string[];
  tenant_whitelist?: string[];
  tenant_blacklist?: string[];
}

export const reliabilityApi = {
  // Health & Circuits
  getDeepHealth: () => api.get<DeepHealthResult>('/reliability/health'),
  listCircuits: () => api.get<CircuitBreakerState[]>('/reliability/circuits'),
  resetCircuit: (serviceName: string) => api.post('/reliability/circuits/reset', { service_name: serviceName }),

  // SLOs
  getSLODashboard: () => api.get<ErrorBudgetSummary>('/reliability/slos'),
  createSLO: (data: Partial<SLOMetricSnapshot>) => api.post('/reliability/slos', data),

  // Incidents & Postmortems
  listIncidents: (status?: string) => api.get<ReliabilityIncident[]>('/reliability/incidents', { params: { status } }),
  getIncident: (id: string) => api.get<ReliabilityIncident>(`/reliability/incidents/${id}`),
  declareIncident: (data: Partial<ReliabilityIncident>) => api.post<ReliabilityIncident>('/reliability/incidents', data),
  acknowledgeIncident: (id: string) => api.post<ReliabilityIncident>(`/reliability/incidents/${id}/acknowledge`),
  mitigateIncident: (id: string) => api.post<ReliabilityIncident>(`/reliability/incidents/${id}/mitigate`),
  resolveIncident: (id: string) => api.post<ReliabilityIncident>(`/reliability/incidents/${id}/resolve`),
  addIncidentTimeline: (id: string, description: string, actor: string) =>
    api.post<ReliabilityIncident>(`/reliability/incidents/${id}/timeline`, { description, actor }),
  createPostmortem: (data: Partial<IncidentPostmortem>) => api.post<IncidentPostmortem>('/reliability/postmortems', data),
  getPostmortem: (incidentId: string) => api.get<IncidentPostmortem>(`/reliability/postmortems/${incidentId}`),
  runIntegrityCheck: () => api.post<Record<string, any>>('/reliability/integrity-check'),

  // Disaster Recovery
  listBackups: () => api.get<BackupRecord[]>('/disaster-recovery/backups'),
  triggerBackup: (data?: { backup_type?: string; storage_location?: string; retention_days?: number }) =>
    api.post<BackupRecord>('/disaster-recovery/backups', data || {}),
  listRestoreTests: () => api.get<RestoreVerificationTest[]>('/disaster-recovery/restore-tests'),
  runRestoreTest: (backupId: string, environment?: string) =>
    api.post<RestoreVerificationTest>('/disaster-recovery/restore-tests', { backup_id: backupId, environment }),
  listDRPlans: () => api.get<DRPlan[]>('/disaster-recovery/plans'),
  getDRPlan: (scenario: string) => api.get<DRPlan>(`/disaster-recovery/plans/${scenario}`),
  listDRDrills: () => api.get<DRDrill[]>('/disaster-recovery/drills'),
  runDRDrill: (scenario: string, initiatedBy: string, planName?: string) =>
    api.post<DRDrill>('/disaster-recovery/drills', { scenario, initiated_by: initiatedBy, plan_name: planName }),

  // Operations: Deployments & Flags
  listDeployments: () => api.get<DeploymentRecord[]>('/operations/deployments'),
  recordDeployment: (data: Partial<DeploymentRecord>) => api.post<DeploymentRecord>('/operations/deployments', data),
  evaluateAndRollback: (data: {
    current_version: string;
    target_version: string;
    error_rate_pct: number;
    p99_latency_ms: number;
    smoke_tests_passed: boolean;
    initiated_by: string;
    reason?: string;
  }) => api.post('/operations/rollbacks', data),
  listFeatureFlags: () => api.get<FeatureFlag[]>('/operations/feature-flags'),
  setFeatureFlag: (data: FeatureFlag) => api.post('/operations/feature-flags', data),
  evaluateFeatureFlag: (flagName: string, tenantId?: string, tenantTier?: string) =>
    api.post<{ flag_name: string; is_enabled: boolean }>('/operations/feature-flags/evaluate', {
      flag_name: flagName,
      tenant_id: tenantId,
      tenant_tier: tenantTier,
    }),
};
