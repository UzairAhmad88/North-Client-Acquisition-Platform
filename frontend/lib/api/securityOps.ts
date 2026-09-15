import { api } from './client';

export interface SecurityExecutiveOverview {
  brief_id: string;
  tenant_id: string;
  posture_grade: string;
  overall_health: string;
  composite_risk_score: number;
  open_critical_incidents: number;
  soc_metrics: {
    total_alerts: number;
    critical_high_alerts: number;
    open_incidents: number;
    closed_incidents: number;
    mttd_minutes: number;
    mttc_minutes: number;
    mttr_minutes: number;
    true_positive_rate: number;
    false_positive_rate: number;
    detection_coverage_pct: number;
    containment_success_rate: number;
  };
  domain_breakdown: {
    identity: number;
    ai: number;
    data: number;
    configuration: number;
    integrations: number;
    financial: number;
  };
  executive_recommendations: string[];
  generated_at: string;
}

export interface SecurityEventItem {
  security_event_id: string;
  event_type: string;
  event_category: string;
  timestamp: string;
  tenant_id: string;
  principal_id: string;
  principal_type: string;
  action: string;
  result: string;
  risk_level: string;
  source: string;
  resource_type?: string;
  resource_id?: string;
  ip_metadata: Record<string, any>;
  device_metadata: Record<string, any>;
  evidence: Record<string, any>;
  metadata: Record<string, any>;
}

export interface SecurityDetectionItem {
  detection_id: string;
  tenant_id: string;
  rule_id: string;
  rule_name: string;
  anomaly_type: string;
  severity: string;
  risk_score: number;
  confidence: number;
  mitre_technique_id?: string;
  mitre_tactic?: string;
  description: string;
  evidence_events: string[];
  metadata: Record<string, any>;
  detected_at: string;
}

export interface SecurityAlertItem {
  alert_id: string;
  tenant_id: string;
  title: string;
  description: string;
  severity: string;
  status: string;
  anomaly_type: string;
  mitre_technique_id?: string;
  mitre_tactic?: string;
  risk_score: number;
  confidence_score: number;
  affected_actor_id?: string;
  affected_target_id?: string;
  evidence: Record<string, any>;
  created_at: string;
}

export interface SecurityIncidentItem {
  incident_id: string;
  tenant_id: string;
  title: string;
  description: string;
  severity: string;
  status: string;
  category: string;
  detection_source: string;
  affected_tenants: string[];
  affected_users: string[];
  affected_services: string[];
  affected_resources: string[];
  timeline: Array<Record<string, any>>;
  evidence: Record<string, any>;
  root_cause?: string;
  containment_actions: string[];
  remediation_actions: string[];
  owner?: string;
  resolution?: string;
  created_at: string;
}

export interface InvestigationWorkspaceData {
  incident: SecurityIncidentItem;
  timeline: Array<{
    entry_id: string;
    timestamp: string;
    type: string;
    title: string;
    description: string;
    severity: string;
    source_id: string;
    category: string;
  }>;
  evidence_graph: {
    nodes: Array<{
      id: string;
      label: string;
      type: string;
      severity?: string;
      principal_type?: string;
      resource_type?: string;
    }>;
    edges: Array<{
      source: string;
      target: string;
      relationship: string;
    }>;
    node_count: number;
    edge_count: number;
  };
  hypotheses: Array<{
    id: string;
    title: string;
    confidence: number;
    status: string;
    supporting_evidence: string[];
    contradicting_evidence: string[];
    recommended_verification: string;
  }>;
  recommended_actions: Array<{
    action: string;
    label: string;
    risk: string;
  }>;
}

export interface BlastRadiusData {
  radius_id: string;
  incident_id?: string;
  tenant_id: string;
  overall_impact_score: number;
  affected_users: string[];
  affected_clients: string[];
  affected_tenants: string[];
  affected_services: string[];
  affected_projects: string[];
  affected_documents: string[];
  affected_financial_records: string[];
  affected_integrations: string[];
  affected_ai_agents: string[];
  affected_workflows: string[];
  narrative_summary: string;
  calculated_at: string;
}

export interface ThreatIndicatorItem {
  indicator_id: string;
  tenant_id: string;
  indicator_type: string;
  indicator_value: string;
  threat_category: string;
  severity: string;
  confidence: number;
  source: string;
  reputation: number;
  is_active: boolean;
  observed_at: string;
}

export interface RiskHeatmapItem {
  domain: string;
  category: string;
  risk_score: number;
  severity: string;
  probability: string;
  exposure: string;
  control_strength: string;
}

export interface RunbookItem {
  name: string;
  action_type: string;
  description: string;
}

export const securityOpsApi = {
  getOverview: async () => {
    const res = await api<{ data: SecurityExecutiveOverview }>('/security/overview');
    return res.data;
  },

  getPosture: async () => {
    const res = await api<{ data: any }>('/security/posture');
    return res.data;
  },

  getRisk: async () => {
    const res = await api<{ data: { assessment: any; heatmap: RiskHeatmapItem[] } }>('/security/risk');
    return res.data;
  },

  listEvents: async (limit = 50) => {
    const res = await api<{ data: SecurityEventItem[] }>(`/security/events?limit=${limit}`);
    return res.data;
  },

  ingestEvent: async (payload: {
    event_type: string;
    source: string;
    principal_id: string;
    action: string;
    status: string;
    resource_id?: string;
    ip_address?: string;
    metadata?: Record<string, any>;
  }) => {
    const res = await api<{ data: any }>('/security/events', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  listDetections: async () => {
    const res = await api<{ data: SecurityDetectionItem[] }>('/security/detections');
    return res.data;
  },

  listAlerts: async () => {
    const res = await api<{ data: SecurityAlertItem[] }>('/security/alerts');
    return res.data;
  },

  updateAlertStatus: async (alertId: string, status: string) => {
    const res = await api<{ data: any }>(`/security/alerts/${alertId}/status`, {
      method: 'POST',
      body: JSON.stringify({ status }),
    });
    return res.data;
  },

  listIncidents: async () => {
    const res = await api<{ data: SecurityIncidentItem[] }>('/security/incidents');
    return res.data;
  },

  createIncident: async (payload: {
    title: string;
    description: string;
    severity?: string;
    affected_users?: string[];
    affected_services?: string[];
  }) => {
    const res = await api<{ data: any }>('/security/incidents', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  getInvestigationWorkspace: async (incidentId: string) => {
    const res = await api<{ data: InvestigationWorkspaceData }>(`/security/investigations/${incidentId}`);
    return res.data;
  },

  getBlastRadius: async (incidentId: string) => {
    const res = await api<{ data: BlastRadiusData }>(`/security/blast-radius/${incidentId}`);
    return res.data;
  },

  listAttackChains: async () => {
    const res = await api<{ data: any[] }>('/security/attack-chains');
    return res.data;
  },

  listRunbooks: async () => {
    const res = await api<{ data: RunbookItem[] }>('/security/runbooks');
    return res.data;
  },

  executeRemediation: async (payload: {
    alert_id: string;
    action_name: string;
    requested_by: string;
    approved_by: string;
    parameters?: Record<string, any>;
  }) => {
    const res = await api<{ data: any }>('/security/remediation/execute', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  getEmergencyControls: async () => {
    const res = await api<{ data: Record<string, boolean> }>('/security/emergency-controls');
    return res.data;
  },

  toggleEmergencyControl: async (control: string, enable: boolean, operatorId: string, reason: string) => {
    const res = await api<{ data: any }>('/security/emergency-controls/toggle', {
      method: 'POST',
      body: JSON.stringify({ control, enable, operator_id: operatorId, reason }),
    });
    return res.data;
  },

  listThreatIndicators: async () => {
    const res = await api<{ data: ThreatIndicatorItem[] }>('/security/indicators');
    return res.data;
  },

  queryCopilot: async (query: string, contextId?: string) => {
    const res = await api<{ data: any }>('/security/copilot', {
      method: 'POST',
      body: JSON.stringify({ query, context_id: contextId }),
    });
    return res.data;
  },
};
