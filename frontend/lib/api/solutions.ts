import { api } from './client';

export interface SolutionFeature {
  id: string;
  solution_id: string;
  title: string;
  description: string;
  category: string;
  status: string;
  priority: string;
  created_at: string;
}

export interface SolutionDeliverable {
  id: string;
  solution_id: string;
  name: string;
  description: string;
  status: string;
  priority: string;
  created_at: string;
}

export interface SolutionIntegration {
  id: string;
  solution_id: string;
  purpose: string;
  provider: string;
  data_flow: string;
  status: string;
  created_at: string;
}

export interface SolutionAssumption {
  id: string;
  solution_id: string;
  assumption_text: string;
  status: string;
  risk_level: string;
  created_at: string;
}

export interface SolutionDesign {
  id: string;
  discovery_session_id: string;
  business_id: string;
  lead_id?: string;
  status: string;
  overview: string;
  architecture_summary: string;
  complexity_tier: string;
  version: number;
  created_by_id?: string;
  approved_by_id?: string;
  approved_at?: string;
  created_at: string;
  updated_at: string;
}

export interface SolutionDesignDetail extends SolutionDesign {
  features: SolutionFeature[];
  deliverables: SolutionDeliverable[];
  integrations: SolutionIntegration[];
  assumptions: SolutionAssumption[];
}

export async function getSolutionDesigns(status?: string): Promise<SolutionDesign[]> {
  const query = status ? `?status=${encodeURIComponent(status)}` : '';
  return await api<SolutionDesign[]>(`/solutions${query}`);
}

export async function createSolutionDesign(payload: {
  discovery_session_id: string;
  overview?: string;
}): Promise<SolutionDesign> {
  return await api<SolutionDesign>('/solutions', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function getSolutionDesignDetail(id: string): Promise<SolutionDesignDetail> {
  return await api<SolutionDesignDetail>(`/solutions/${id}`);
}

export async function analyzeSolutionDesign(id: string): Promise<SolutionDesignDetail> {
  return await api<SolutionDesignDetail>(`/solutions/${id}/analyze`, {
    method: 'POST',
  });
}

export async function approveSolutionDesign(id: string): Promise<SolutionDesign> {
  return await api<SolutionDesign>(`/solutions/${id}/approve`, {
    method: 'POST',
  });
}
