import { api } from './client';

export interface ProposalItem {
  id: string;
  proposal_id: string;
  service_id?: string;
  deliverable_id?: string;
  description: string;
  quantity: number;
  unit: string;
  is_optional: boolean;
  price?: number;
  created_at: string;
}

export interface ProposalVersion {
  id: string;
  proposal_id: string;
  version: number;
  content_hash: string;
  sections_json: any[];
  created_by_id?: string;
  created_at: string;
}

export interface Proposal {
  id: string;
  solution_id: string;
  business_id: string;
  lead_id?: string;
  proposal_type: string;
  title: string;
  summary: string;
  status: string;
  pricing_status: string;
  version: number;
  content_hash?: string;
  created_by_id?: string;
  approved_by_id?: string;
  approved_at?: string;
  created_at: string;
  updated_at: string;
}

export interface ProposalDetail extends Proposal {
  items: ProposalItem[];
  versions: ProposalVersion[];
}

export async function getProposals(status?: string): Promise<Proposal[]> {
  const query = status ? `?status=${encodeURIComponent(status)}` : '';
  return await api<Proposal[]>(`/proposals${query}`);
}

export async function createProposal(payload: {
  solution_id: string;
  proposal_type?: string;
  title?: string;
}): Promise<Proposal> {
  return await api<Proposal>('/proposals', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function getProposalDetail(id: string): Promise<ProposalDetail> {
  return await api<ProposalDetail>(`/proposals/${id}`);
}

export async function generateProposal(id: string): Promise<ProposalDetail> {
  return await api<ProposalDetail>(`/proposals/${id}/generate`, {
    method: 'POST',
  });
}

export async function approveProposal(id: string): Promise<Proposal> {
  return await api<Proposal>(`/proposals/${id}/approve`, {
    method: 'POST',
  });
}
