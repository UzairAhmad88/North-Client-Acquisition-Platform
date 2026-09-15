import { api } from './client';

export interface RiskFinding {
  id: string;
  rule_id: string;
  category: string;
  severity: 'INFO' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  message: string;
  evidence_reference?: string;
  remediation?: string;
}

export interface QualityCheck {
  id: string;
  check_type: string;
  status: 'PASS' | 'WARNING' | 'FAIL';
  score: number;
  details: Record<string, any>;
}

export interface RiskAssessment {
  id: string;
  artifact_id: string;
  artifact_type: string;
  business_id?: string;
  lead_id?: string;
  decision: 'PASS' | 'REVIEW' | 'BLOCK';
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'BLOCKED';
  quality_score: number;
  evidence_coverage: number;
  confidence: string;
  engine_version: string;
  policy_version: string;
  content_hash: string;
  artifact_version: number;
  is_stale: boolean;
  status: string;
  human_override_decision?: string;
  human_override_reason?: string;
  human_override_by_id?: string;
  human_override_at?: string;
  created_at: string;
  updated_at: string;
  findings: RiskFinding[];
  quality_checks: QualityCheck[];
}

export async function checkRisk(artifactId: string, artifactType = 'OUTREACH'): Promise<RiskAssessment> {
  const res = await api<{ data: RiskAssessment }>('/risk/check', {
    method: 'POST',
    body: JSON.stringify({ artifact_id: artifactId, artifact_type: artifactType }),
  });
  return res.data;
}

export async function getRiskAssessment(assessmentId: string): Promise<RiskAssessment> {
  const res = await api<{ data: RiskAssessment }>(`/risk/assessments/${assessmentId}`);
  return res.data;
}

export async function getOutreachDraftRisk(draftId: string): Promise<RiskAssessment> {
  const res = await api<{ data: RiskAssessment }>(`/outreach/drafts/${draftId}/risk`);
  return res.data;
}

export async function overrideRiskAssessment(
  assessmentId: string,
  decision: 'ACCEPTED' | 'REJECTED',
  reason: string
): Promise<RiskAssessment> {
  const res = await api<{ data: RiskAssessment }>(`/risk/assessments/${assessmentId}/override`, {
    method: 'POST',
    body: JSON.stringify({ decision, reason }),
  });
  return res.data;
}
