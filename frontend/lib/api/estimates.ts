import { api } from './client';

export interface EstimateWorkItem {
  id: string;
  estimate_id: string;
  requirement_id?: string;
  feature_id?: string;
  name: string;
  category: string;
  description: string;
  complexity: string;
  optimistic_hours: number;
  most_likely_hours: number;
  pessimistic_hours: number;
  expected_hours: number;
  confidence: string;
  created_at: string;
}

export interface EstimateCostItem {
  id: string;
  estimate_id: string;
  cost_type: string;
  description: string;
  amount: number;
  currency: string;
  source: string;
  created_at: string;
}

export interface EstimateScenario {
  id: string;
  estimate_id: string;
  name: string;
  description: string;
  scope: string;
  estimated_hours: number;
  internal_cost?: number;
  external_cost?: number;
  recommended_min?: number;
  recommended_max?: number;
  risk_level: string;
  status: string;
  created_at: string;
}

export interface ProjectEstimate {
  id: string;
  solution_id: string;
  business_id: string;
  lead_id?: string;
  status: string;
  complexity: string;
  confidence: string;
  estimated_hours: number;
  minimum_hours: number;
  maximum_hours: number;
  risk_buffer_percent: number;
  internal_cost?: number;
  external_cost?: number;
  recommended_min?: number;
  recommended_max?: number;
  requirements_version: number;
  solution_version: number;
  pricing_policy_version: string;
  cost_model_version: string;
  content_hash?: string;
  version: number;
  created_by_id?: string;
  approved_by_id?: string;
  approved_at?: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectEstimateDetail extends ProjectEstimate {
  work_items: EstimateWorkItem[];
  costs: EstimateCostItem[];
  scenarios: EstimateScenario[];
}

export async function getEstimates(status?: string): Promise<ProjectEstimate[]> {
  const query = status ? `?status=${encodeURIComponent(status)}` : '';
  return await api<ProjectEstimate[]>(`/estimates${query}`);
}

export async function createEstimate(payload: { solution_id: string }): Promise<ProjectEstimate> {
  return await api<ProjectEstimate>('/estimates', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function getEstimateDetail(id: string): Promise<ProjectEstimateDetail> {
  return await api<ProjectEstimateDetail>(`/estimates/${id}`);
}

export async function calculateEstimate(id: string): Promise<ProjectEstimateDetail> {
  return await api<ProjectEstimateDetail>(`/estimates/${id}/calculate`, {
    method: 'POST',
  });
}

export async function approveEstimate(id: string): Promise<ProjectEstimate> {
  return await api<ProjectEstimate>(`/estimates/${id}/approve`, {
    method: 'POST',
  });
}
