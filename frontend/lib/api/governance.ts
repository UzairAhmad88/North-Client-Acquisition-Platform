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
};
