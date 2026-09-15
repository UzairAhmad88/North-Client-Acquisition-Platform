import { api } from './client';

export interface ContractSection {
  id: string;
  contract_id: string;
  title: string;
  section_type: string;
  content: string;
  order_index: number;
  created_at: string;
}

export interface ContractDiscrepancy {
  id: string;
  contract_id: string;
  discrepancy_type: string;
  description: string;
  severity: string;
  status: string;
  created_at: string;
}

export interface ContractBaseline {
  id: string;
  contract_id: string;
  contract_version: number;
  requirements_version: number;
  solution_version: number;
  estimate_version: number;
  proposal_version: number;
  scope_hash: string;
  commercial_hash: string;
  contract_hash: string;
  is_locked: boolean;
  locked_at: string;
  created_at: string;
}

export interface Contract {
  id: string;
  proposal_id: string;
  estimate_id: string;
  solution_id: string;
  business_id: string;
  lead_id?: string;
  contract_number: string;
  title: string;
  summary: string;
  status: string;
  pricing_status: string;
  risk_status: string;
  currency: string;
  total_amount?: number;
  version: number;
  content_hash?: string;
  is_stale: boolean;
  created_by_id?: string;
  approved_by_id?: string;
  approved_at?: string;
  created_at: string;
  updated_at: string;
}

export interface ContractDetail extends Contract {
  sections: ContractSection[];
  discrepancies: ContractDiscrepancy[];
  baselines: ContractBaseline[];
}

export async function getContracts(status?: string): Promise<Contract[]> {
  const query = status ? `?status=${encodeURIComponent(status)}` : '';
  return await api<Contract[]>(`/contracts${query}`);
}

export async function createContract(payload: {
  proposal_id: string;
  estimate_id: string;
  title?: string;
}): Promise<Contract> {
  return await api<Contract>('/contracts', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function getContractDetail(id: string): Promise<ContractDetail> {
  return await api<ContractDetail>(`/contracts/${id}`);
}

export async function generateContract(id: string): Promise<ContractDetail> {
  return await api<ContractDetail>(`/contracts/${id}/generate`, {
    method: 'POST',
  });
}

export async function approveContract(id: string): Promise<Contract> {
  return await api<Contract>(`/contracts/${id}/approve`, {
    method: 'POST',
  });
}

export async function acceptContract(id: string, payload: {
  client_email: string;
  acceptance_statement: string;
}): Promise<Contract> {
  return await api<Contract>(`/contracts/${id}/accept`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function signContract(id: string): Promise<Contract> {
  return await api<Contract>(`/contracts/${id}/sign`, {
    method: 'POST',
  });
}

export async function lockBaseline(id: string): Promise<ContractBaseline> {
  return await api<ContractBaseline>(`/contracts/${id}/baseline`, {
    method: 'POST',
  });
}
