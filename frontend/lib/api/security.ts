import { api } from './client';

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
  role: string;
  roles: string[];
  created_at: string;
  last_login_at?: string;
}

export interface UserSession {
  id: string;
  user_id: string;
  tenant_id: string;
  ip_address?: string;
  user_agent?: string;
  is_mfa_authenticated: boolean;
  expires_at: string;
  last_seen_at: string;
  is_revoked: boolean;
}

export interface SystemRoleItem {
  name: string;
  description: string;
  is_internal: boolean;
  permissions: string[];
}

export interface SystemPermissionItem {
  name: string;
  resource: string;
  action: string;
  description: string;
  risk_level: string;
}

export interface APIKeyItem {
  id: string;
  name: string;
  key_prefix: string;
  scopes: string[];
  expires_at?: string;
  last_used_at?: string;
  is_revoked: boolean;
  created_at: string;
}

export interface APIKeyCreatedResponse {
  id: string;
  name: string;
  key_prefix: string;
  secret_key: string;
  scopes: string[];
  expires_at?: string;
}

export interface SecurityEventItem {
  id: string;
  event_type: string;
  severity: string;
  principal_id: string;
  principal_type: string;
  tenant_id: string;
  action?: string;
  resource?: string;
  resource_id?: string;
  result: string;
  reason_code: string;
  details: Record<string, any>;
  ip_address?: string;
  user_agent?: string;
  occurred_at: string;
}

export interface SecurityMetrics {
  active_sessions_count: number;
  users_count: number;
  security_events_last_24h: number;
  failed_logins_last_24h: number;
  mfa_enabled_users_count: number;
  api_keys_active_count: number;
}

export interface MFASetupData {
  secret: string;
  backup_codes: string[];
  qr_code_uri: string;
}

export const securityApi = {
  // Users
  listUsers: () => api<UserProfile[]>('/api/v1/security/users'),
  inviteUser: (data: { email: string; full_name: string; role: string }) =>
    api<UserProfile>('/api/v1/security/users/invite', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  suspendUser: (userId: string) =>
    api<UserProfile>(`/api/v1/security/users/${userId}/suspend`, { method: 'POST' }),
  activateUser: (userId: string) =>
    api<UserProfile>(`/api/v1/security/users/${userId}/activate`, { method: 'POST' }),

  // Sessions
  listSessions: () => api<UserSession[]>('/api/v1/security/sessions'),
  revokeSession: (sessionId: string) =>
    api<{ revoked: boolean }>('/api/v1/security/sessions/revoke', {
      method: 'POST',
      body: JSON.stringify({ session_id: sessionId }),
    }),
  revokeAllSessions: () =>
    api<{ revoked_count: number }>('/api/v1/security/sessions/revoke-all', { method: 'POST' }),

  // Roles & Permissions
  listRoles: () => api<SystemRoleItem[]>('/api/v1/security/roles'),
  listPermissions: () => api<SystemPermissionItem[]>('/api/v1/security/permissions'),

  // MFA
  setupMFA: () => api<MFASetupData>('/api/v1/security/mfa/setup', { method: 'POST' }),
  stepUpAuth: (data: { password: string }) =>
    api<{ step_up_token: string; expires_in_minutes: number }>('/api/v1/security/step-up', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // API Keys
  listAPIKeys: () => api<APIKeyItem[]>('/api/v1/security/api-keys'),
  createAPIKey: (data: { name: string; scopes: string[]; expires_in_days?: number }) =>
    api<APIKeyCreatedResponse>('/api/v1/security/api-keys', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  revokeAPIKey: (keyId: string) =>
    api<{ revoked: boolean }>(`/api/v1/security/api-keys/${keyId}`, { method: 'DELETE' }),

  // Security Metrics & Audit
  getMetrics: () => api<SecurityMetrics>('/api/v1/security/metrics'),
  listEvents: (limit: number = 50) =>
    api<SecurityEventItem[]>(`/api/v1/security/events?limit=${limit}`),
};

