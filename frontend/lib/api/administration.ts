import { api } from './client';

export interface AdminHealthReport {
  status: 'HEALTHY' | 'STABLE' | 'AT_RISK' | 'CRITICAL';
  configuration_validity_score: number;
  policy_consistency_score: number;
  integration_health_score: number;
  drift_count: number;
  pending_approvals_count: number;
  active_kill_switches_count: number;
  active_maintenance_mode: string;
  details: Record<string, any>;
  computed_at: string;
}

export interface ConfigItem {
  key: string;
  display_name: string;
  description: string;
  config_type: string;
  category: string;
  scope: string;
  default_value: any;
  current_value: any;
  validation_rules: Record<string, any>;
  sensitive: boolean;
  mutable: boolean;
  restart_required: boolean;
  policy_controlled: boolean;
  version: number;
  status: string;
}

export interface AdminChangeRequest {
  change_id: string;
  config_key: string;
  old_value: any;
  new_value: any;
  reason: string;
  requested_by: string;
  reviewed_by?: string;
  approved_by?: string;
  risk_level: string;
  status: string;
  effective_at?: string;
  created_at: string;
}

export interface PolicyRule {
  rule_id: string;
  name: string;
  condition: string;
  action: 'ALLOW' | 'REVIEW' | 'BLOCK';
  reason: string;
  is_mandatory_security: boolean;
}

export interface PolicyItem {
  policy_id: string;
  name: string;
  domain: string;
  description: string;
  scope: string;
  priority: number;
  version: number;
  status: string;
  rules: PolicyRule[];
  approval_required: boolean;
  created_by: string;
}

export interface FeatureFlagItem {
  key: string;
  name: string;
  description: string;
  status: 'ENABLED' | 'DISABLED' | 'CANARY' | 'SUNSET';
  rollout_type: 'BOOLEAN' | 'PERCENTAGE' | 'TENANT_TIER' | 'USER_LIST';
  rollout_percentage: number;
  allowed_tiers: string[];
  environment: string;
  owner: string;
  version: number;
}

export interface EnvironmentDefinition {
  env_id: string;
  name: string;
  env_type: string;
  is_production: boolean;
  requires_approval_for_changes: boolean;
  allow_mock_providers: boolean;
  allow_chaos_testing: boolean;
  allow_real_financial_execution: boolean;
  status: string;
  active_version: string;
}

export interface ProviderConfiguration {
  provider_id: string;
  name: string;
  category: string;
  base_url: string;
  secret_reference: string;
  timeout_seconds: number;
  max_retries: number;
  rate_limit_rpm: number;
  is_active: boolean;
  health_status: string;
  latency_ms: number;
  error_rate_percentage: number;
  last_health_check: string;
}

export interface KillSwitchItem {
  switch_id: string;
  name: string;
  level: string;
  target_identifier: string;
  state: 'ARMED' | 'DISARMED' | 'ACTIVE';
  reason?: string;
  activated_by?: string;
  activated_at?: string;
}

export interface MaintenanceState {
  current_mode: string;
  is_mutation_allowed: boolean;
  active_window?: {
    window_id: string;
    title: string;
    description: string;
    mode: string;
    is_active: boolean;
    internal_banner: string;
    client_portal_banner: string;
    initiated_by: string;
    affected_services: string[];
    start_time: string;
  };
}

export interface DriftItem {
  drift_id: string;
  key: string;
  expected_value: any;
  actual_value: any;
  severity: string;
  environment: string;
  detected_at: string;
  resolved: boolean;
}

export interface AdminOverview {
  health: AdminHealthReport;
  configs_count: number;
  policies_count: number;
  feature_flags_count: number;
  providers_count: number;
  environments_count: number;
  kill_switches_count: number;
  maintenance_mode: string;
}

export const administrationApi = {
  // Overview & Health
  getOverview: () => api.get<AdminOverview>('/administration/overview'),
  getHealth: () => api.get<AdminHealthReport>('/administration/health'),

  // Configurations
  listConfigs: (category?: string) => api.get<ConfigItem[]>('/administration/configs', { params: { category } }),
  registerConfig: (data: Partial<ConfigItem>) => api.post<ConfigItem>('/administration/configs', data),
  submitChangeRequest: (data: { key: string; new_value: any; reason: string; risk_level?: string }) =>
    api.post<AdminChangeRequest>('/administration/configs/change-request', data),
  approveChange: (changeId: string) => api.post<ConfigItem>(`/administration/configs/approve/${changeId}`),
  rollbackConfig: (data: { key: string; target_version: number; reason: string }) =>
    api.post<ConfigItem>('/administration/configs/rollback', data),
  getConfigDiff: (key: string, vFrom: number, vTo: number) =>
    api.get<Record<string, any>>('/administration/configs/diff', { params: { key, v_from: vFrom, v_to: vTo } }),

  // Policies
  listPolicies: (domain?: string) => api.get<PolicyItem[]>('/administration/policies', { params: { domain } }),
  registerPolicy: (data: Partial<PolicyItem>) => api.post<PolicyItem>('/administration/policies', data),
  evaluatePolicy: (data: { domain: string; action: string; actor_type?: string; context?: Record<string, any>; amount?: number }) =>
    api.post<{ action_result: string; reason: string }>('/administration/policies/evaluate', data),

  // Feature Flags
  listFeatureFlags: (environment?: string) => api.get<FeatureFlagItem[]>('/administration/feature-flags', { params: { environment } }),
  registerFeatureFlag: (data: Partial<FeatureFlagItem>) => api.post<FeatureFlagItem>('/administration/feature-flags', data),
  updateFlagStatus: (key: string, status: string) => api.post<FeatureFlagItem>(`/administration/feature-flags/${key}/status`, { status }),
  updateFlagRollout: (key: string, data: { rollout_type: string; rollout_percentage?: number; allowed_tiers?: string[] }) =>
    api.post<FeatureFlagItem>(`/administration/feature-flags/${key}/rollout`, data),

  // Environments
  listEnvironments: () => api.get<EnvironmentDefinition[]>('/administration/environments'),
  promoteEnvironmentConfig: (data: { source_env: string; target_env: string; keys: string[] }) =>
    api.post<any>('/administration/environments/promote', data),

  // Integrations
  listIntegrations: (category?: string) => api.get<ProviderConfiguration[]>('/administration/integrations', { params: { category } }),

  // System Controls
  listSystemControls: () => api.get<KillSwitchItem[]>('/administration/system-controls'),
  activateKillSwitch: (switchId: string, reason: string) =>
    api.post<KillSwitchItem>(`/administration/system-controls/${switchId}/activate`, { reason }),
  releaseKillSwitch: (switchId: string) =>
    api.post<KillSwitchItem>(`/administration/system-controls/${switchId}/release`),

  // Maintenance Mode
  getMaintenanceState: () => api.get<MaintenanceState>('/administration/maintenance'),
  startMaintenance: (data: { mode: string; title: string; description: string; internal_banner: string; client_banner?: string; affected_services?: string[] }) =>
    api.post<any>('/administration/maintenance/start', data),
  endMaintenance: () => api.post<{ status: string; current_mode: string }>('/administration/maintenance/end'),

  // Drift
  listDrifts: () => api.get<DriftItem[]>('/administration/drift'),
  resolveDrift: (driftId: string) => api.post<DriftItem>(`/administration/drift/${driftId}/resolve`),
};
