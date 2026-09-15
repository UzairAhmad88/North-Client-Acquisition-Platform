import { api } from './client';

export interface TestCase {
  id: string;
  test_plan_id: string;
  code: string;
  title: string;
  description?: string;
  category: string;
  priority: string;
  execution_type: string;
  preconditions?: string;
  steps?: any[];
  expected_results: string;
  is_regression: boolean;
  requirement_id?: string;
  deliverable_id?: string;
  created_at: string;
}

export interface TestPlan {
  id: string;
  project_id: string;
  title: string;
  description?: string;
  plan_type: string;
  status: string;
  created_by: string;
  created_at: string;
  test_cases: TestCase[];
}

export interface TestRun {
  id: string;
  project_id: string;
  test_plan_id: string;
  name: string;
  environment: string;
  status: string;
  executed_by?: string;
  passed_count: number;
  failed_count: number;
  blocked_count: number;
  skipped_count: number;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface Defect {
  id: string;
  defect_number: string;
  project_id: string;
  title: string;
  description: string;
  severity: string;
  priority: string;
  status: string;
  classification: string;
  reported_by: string;
  assigned_to?: string;
  resolution_summary?: string;
  created_at: string;
}

export interface UATSession {
  id: string;
  project_id: string;
  client_account_id: string;
  title: string;
  scope_description?: string;
  status: string;
  approved_by_client: boolean;
  client_signoff_at?: string;
  created_at: string;
}

export interface ReleaseVersion {
  id: string;
  project_id: string;
  version_tag: string;
  target_environment: string;
  status: string;
  release_notes?: string;
  qa_approval_status: string;
  client_approval_status: string;
  created_at: string;
}

export interface HandoverChecklist {
  id: string;
  project_id: string;
  title: string;
  code_repository_transferred: boolean;
  documentation_delivered: boolean;
  credentials_transferred: boolean;
  training_completed: boolean;
  deployment_verified: boolean;
  status: string;
  signed_off_by_client: boolean;
  client_signoff_hash?: string;
  signed_off_at?: string;
}

// API functions
export async function listTestPlans(projectId: string) {
  return api<TestPlan[]>(`/projects/${projectId}/test-plans`);
}

export async function createTestPlan(projectId: string, payload: { title: string; description?: string; plan_type?: string }) {
  return api<TestPlan>(`/projects/${projectId}/test-plans`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function generateAITestCases(testPlanId: string) {
  return api<TestCase[]>(`/test-plans/${testPlanId}/generate-cases`, {
    method: 'POST',
  });
}

export async function listTestRuns(projectId: string) {
  return api<TestRun[]>(`/projects/${projectId}/test-runs`);
}

export async function createTestRun(projectId: string, payload: { test_plan_id: string; name: string; environment?: string }) {
  return api<TestRun>(`/projects/${projectId}/test-runs`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function recordTestResult(testRunId: string, payload: { test_case_id: string; status: string; actual_results?: string; execution_notes?: string }) {
  return api<{ result_id: string; status: string }>(`/test-runs/${testRunId}/results`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function listDefects(projectId: string) {
  return api<Defect[]>(`/projects/${projectId}/defects`);
}

export async function createDefect(projectId: string, payload: { title: string; description: string; reported_by?: string; is_against_spec?: boolean }) {
  return api<Defect>(`/projects/${projectId}/defects`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateDefectStatus(defectId: string, payload: { status: string; resolution_summary?: string }) {
  return api<Defect>(`/defects/${defectId}/status`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}

export async function listUATSessions(projectId: string) {
  return api<UATSession[]>(`/projects/${projectId}/uat-sessions`);
}

export async function createUATSession(projectId: string, payload: { client_account_id: string; title: string; scope_description?: string }) {
  return api<UATSession>(`/projects/${projectId}/uat-sessions`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function submitUATFeedback(uatSessionId: string, payload: { comments: string; feedback_type?: string; rating?: number; create_defect_if_issue?: boolean }) {
  return api<{ feedback_id: string; defect_id?: string }>(`/uat-sessions/${uatSessionId}/feedback`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function signoffUATSession(uatSessionId: string, payload: { client_signer_id: string; signoff_statement: string }) {
  return api<UATSession>(`/uat-sessions/${uatSessionId}/signoff`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function listReleases(projectId: string) {
  return api<ReleaseVersion[]>(`/projects/${projectId}/releases`);
}

export async function createReleaseVersion(projectId: string, payload: { version_tag: string; target_environment?: string; release_notes?: string }) {
  return api<ReleaseVersion>(`/projects/${projectId}/releases`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function evaluateReleaseGate(releaseId: string) {
  return api<{
    release_id: string;
    version_tag: string;
    status: string;
    qa_approval_status: string;
    readiness_score: number;
    is_ready_for_release: boolean;
    blocking_conditions: string[];
    recommendations: string[];
  }>(`/releases/${releaseId}/evaluate-gate`, {
    method: 'POST',
  });
}

export async function getHandoverChecklist(projectId: string) {
  return api<HandoverChecklist>(`/projects/${projectId}/handover`);
}

export async function completeHandover(projectId: string, payload: { client_signer_id: string; signoff_statement: string }) {
  return api<{ handover_checklist: HandoverChecklist; project_status: string; sha256_signoff_hash: string }>(`/projects/${projectId}/handover/complete`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
