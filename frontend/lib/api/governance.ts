import { api } from './client';

export interface GovernanceExecutiveSummary {
  governance_health: string;
  composite_compliance_score: number;
  critical_blockers: number;
  governance_debt_score: number;
  active_exceptions: number;
  advisory_recommendation: string;
  generated_at: string;
}

export interface GovernancePostureData {
  composite_compliance_score: number;
  overall_health: string;
  total_requirements: number;
  implemented_requirements: number;
  total_controls: number;
  healthy_controls: number;
  failing_controls: number;
  open_findings_count: number;
  critical_findings_count: number;
  active_exceptions_count: number;
  stale_evidence_count: number;
  domain_scores: Record<string, number>;
  technical_debt_score: number;
  captured_at: string;
}

export interface GovernanceFrameworkItem {
  framework_code: string;
  name: string;
  version: string;
  category: string;
  jurisdiction: string;
  description: string;
  status: string;
  owner: string;
}

export interface GovernanceRequirementItem {
  requirement_code: string;
  framework_code: string;
  title: string;
  description: string;
  category: string;
  priority: string;
  status: string;
}

export interface GovernanceControlItem {
  control_code: string;
  name: string;
  objective: string;
  domain: string;
  control_type: string;
  frequency: string;
  automation_level: string;
  owner_id: string;
  operator_id: string;
  health_status: string;
  implementations: string[];
}

export interface GovernanceEvidenceItem {
  evidence_id: string;
  evidence_type: string;
  source_subsystem: string;
  source_record_id: string;
  sha256_hash: string;
  provenance_uri: string;
  summary: string;
  collected_at: string;
  freshness_status: string;
}

export interface GovernanceRiskItem {
  risk_code: string;
  title: string;
  category: string;
  likelihood: number;
  impact: number;
  inherent_risk_score: number;
  residual_risk_score: number;
  risk_level: string;
  treatment: string;
  owner_id: string;
  status: string;
  mitigating_controls: string[];
}

export interface GovernanceExceptionItem {
  exception_code: string;
  title: string;
  control_code: string;
  reason: string;
  compensating_controls: string[];
  owner_id: string;
  requester_id: string;
  approver_id?: string;
  status: string;
  expiration_date: string;
}

export interface GovernanceFindingItem {
  finding_code: string;
  control_code: string;
  title: string;
  description: string;
  severity: string;
  root_cause?: string;
  owner_id: string;
  status: string;
  due_date: string;
}

export interface PrivacyRequestItem {
  request_code: string;
  subject_id: string;
  request_type: string;
  status: string;
  requested_at: string;
  due_date: string;
  assigned_to: string;
}

export interface VendorProfileItem {
  vendor_code: string;
  name: string;
  service_provided: string;
  criticality: string;
  data_access_level: string;
  security_risk: string;
  privacy_risk: string;
  owner_id: string;
  status: string;
  dependent_services: string[];
}

export interface CopilotAnswer {
  query: string;
  answer: string;
  evidence_citations: string[];
  disclaimer: string;
  uncertainty_score: number;
  timestamp: string;
}

export interface TraceEvent {
  id: string;
  name: string;
  span_type: string;
  status: string;
  timestamp?: string;
  created_at?: string;
  input_summary?: any;
  output_summary?: any;
  duration_ms?: number;
  tokens_consumed?: number;
  metadata?: Record<string, any>;
}

export interface AITrace {
  id: string;
  trace_id?: string;
  tenant_id?: string;
  started_at?: string;
  agent_id: string;
  task_name?: string;
  status: string;
  duration_ms?: number;
  tokens_used?: number;
  events?: TraceEvent[];
  created_at?: string;
  total_duration_ms?: number;
  agent_version?: string;
  workflow_id?: string;
  model_id?: string;
  model_version?: string;
  total_tokens?: number;
  estimated_cost?: number;
  prompt_version?: string;
}

export interface PromptItem {
  id: string;
  prompt_code?: string;
  name: string;
  version?: string;
  template?: string;
  status?: string;
  author?: string;
  created_at: string;
  tenant_id?: string;
  current_version?: string;
  purpose?: string;
  agent_target?: string;
  prompt_key?: string;
  versions?: any[];
}

export interface EvaluationDataset {
  id: string;
  dataset_code?: string;
  name: string;
  sample_count?: number;
  domain?: string;
  created_at: string;
  tenant_id?: string;
  dataset_key?: string;
  description?: string;
  cases?: any[];
  task_type?: string;
  is_golden?: boolean;
  version?: string;
}

export interface EvaluationRun {
  id: string;
  run_code?: string;
  dataset_id?: string;
  model_name?: string;
  pass_rate_pct?: number;
  latency_p99_ms?: number;
  status?: string;
  completed_at?: string;
  tenant_id?: string;
  agent_key?: string;
  agent_version?: string;
  prompt_version?: string;
  model_version?: string;
  overall_score?: number;
  passed_cases_count?: number;
  failed_cases_count?: number;
  regression_detected?: boolean;
  regression_details?: string | Record<string, any>;
  evaluation_type?: string;
}

export interface AIIncident {
  id: string;
  incident_code: string;
  title: string;
  severity: string;
  status: string;
  affected_agent_id: string;
  detected_at: string;
}

export interface KillSwitchEvent {
  id: string;
  switch_code: string;
  target_agent_id: string;
  reason: string;
  triggered_by: string;
  is_active: boolean;
  triggered_at: string;
  level?: string;
}

export const governanceApi = {
  getOverview: () => api<GovernanceExecutiveSummary>('/governance/overview'),
  getPosture: () => api<GovernancePostureData>('/governance/posture'),

  listFrameworks: () => api<GovernanceFrameworkItem[]>('/governance/frameworks'),
  listRequirements: (frameworkCode: string = 'SOC2_TYPE_II') =>
    api<GovernanceRequirementItem[]>(`/governance/requirements?framework_code=${frameworkCode}`),

  listControls: (domain?: string) =>
    api<GovernanceControlItem[]>(domain ? `/governance/controls?domain=${domain}` : '/governance/controls'),

  testControl: (controlCode: string, payload: { test_type: string; result: string; details: string; executed_by: string }) =>
    api<any>(`/governance/controls/${controlCode}/test`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  listRisks: (category?: string) =>
    api<GovernanceRiskItem[]>(category ? `/governance/risks?category=${category}` : '/governance/risks'),

  acceptRisk: (riskCode: string, approverId: string, justification: string) =>
    api<GovernanceRiskItem>(`/governance/risks/${riskCode}/accept`, {
      method: 'POST',
      body: JSON.stringify({ approver_id: approverId, justification }),
    }),

  listExceptions: () => api<GovernanceExceptionItem[]>('/governance/exceptions'),
  requestException: (payload: any) =>
    api<GovernanceExceptionItem>('/governance/exceptions', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  approveException: (exceptionCode: string, approverId: string) =>
    api<GovernanceExceptionItem>(`/governance/exceptions/${exceptionCode}/approve`, {
      method: 'POST',
      body: JSON.stringify({ approver_id: approverId }),
    }),

  listFindings: () => api<GovernanceFindingItem[]>('/governance/findings'),
  createRemediationPlan: (findingCode: string, planTitle: string, actions: any[], ownerId: string) =>
    api<any>(`/governance/findings/${findingCode}/remediation`, {
      method: 'POST',
      body: JSON.stringify({ plan_title: planTitle, actions, owner_id: ownerId }),
    }),

  verifyRemediation: (findingCode: string, verifierId: string, evidenceId: string, retestPassed: boolean) =>
    api<any>(`/governance/findings/${findingCode}/verify`, {
      method: 'POST',
      body: JSON.stringify({
        verifier_id: verifierId,
        verification_evidence_id: evidenceId,
        retest_passed: retestPassed,
      }),
    }),

  listPrivacyRequests: () => api<PrivacyRequestItem[]>('/governance/privacy/requests'),
  listVendors: () => api<VendorProfileItem[]>('/governance/vendors'),

  askCopilot: (query: string) =>
    api<CopilotAnswer>(`/governance/copilot/query?query=${encodeURIComponent(query)}`, {
      method: 'POST',
    }),

  listTraces: async (): Promise<AITrace[]> => [],
  listPrompts: async (): Promise<PromptItem[]> => [],
  listEvaluationDatasets: async (): Promise<EvaluationDataset[]> => [],
  listEvaluationRuns: async (): Promise<EvaluationRun[]> => [],
  listIncidents: async (): Promise<AIIncident[]> => [],
  getActiveKillSwitches: async (): Promise<KillSwitchEvent[]> => [],
  runEvaluationBenchmark: async (payload: any): Promise<any> => ({}),
  triggerKillSwitch: async (payload: any): Promise<any> => ({}),
  registerPrompt: async (payload: any): Promise<any> => ({}),
};
