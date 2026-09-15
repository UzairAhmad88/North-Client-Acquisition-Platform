import { api } from "./client";

export interface AgentSpec {
  name: string;
  version: string;
  description: string;
  enabled: boolean;
  permissions: string[];
  max_steps: number;
  max_tool_calls: number;
  max_runtime_seconds: number;
}

export interface AgentEvent {
  id: string;
  agent_run_id: string;
  event_type: string;
  message: string;
  payload: Record<string, any>;
  timestamp: string;
}

export interface AgentRun {
  id: string;
  workflow_id: string;
  task_id: string;
  agent_run_id: string;
  agent_name: string;
  agent_version: string;
  user_id?: string | null;
  lead_id?: string | null;
  business_id?: string | null;
  status: "CREATED" | "RUNNING" | "WAITING_FOR_APPROVAL" | "PAUSED" | "COMPLETED" | "FAILED" | "CANCELLED";
  input_summary: Record<string, any>;
  output_summary: Record<string, any>;
  confidence: "HIGH" | "MEDIUM" | "LOW";
  tool_calls_count: number;
  steps_count: number;
  started_at?: string | null;
  completed_at?: string | null;
  error_message?: string | null;
  estimated_tokens: number;
  estimated_cost: number;
  created_at: string;
  updated_at: string;
}

export interface AgentRunDetail extends AgentRun {
  events: AgentEvent[];
}

export interface AgentRunListResponse {
  data: AgentRun[];
  pagination: {
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  };
}

export async function listAgents(): Promise<AgentSpec[]> {
  const response = await api<{ data: AgentSpec[] }>("/agents");
  return response.data;
}

export async function getAgentSpec(name: string): Promise<AgentSpec> {
  const response = await api<{ data: AgentSpec }>(`/agents/${name}`);
  return response.data;
}

export async function listAgentRuns(options?: {
  lead_id?: string;
  status?: string;
  page?: number;
  limit?: number;
}): Promise<AgentRunListResponse> {
  const params = new URLSearchParams();
  if (options?.lead_id) params.append("lead_id", options.lead_id);
  if (options?.status) params.append("status", options.status);
  if (options?.page) params.append("page", options.page.toString());
  if (options?.limit) params.append("limit", options.limit.toString());

  const queryStr = params.toString() ? `?${params.toString()}` : "";
  return await api<AgentRunListResponse>(`/agent-runs${queryStr}`);
}

export async function getAgentRunDetail(id: string): Promise<AgentRunDetail> {
  const response = await api<{ data: AgentRunDetail }>(`/agent-runs/${id}`);
  return response.data;
}

export async function cancelAgentRun(id: string): Promise<AgentRun> {
  const response = await api<{ data: AgentRun }>(`/agent-runs/${id}/cancel`, {
    method: "POST",
  });
  return response.data;
}

export async function triggerAgentRun(data: {
  agent_name: string;
  lead_id?: string;
  business_id?: string;
  input_data?: Record<string, any>;
}): Promise<AgentRun> {
  const response = await api<{ data: AgentRun }>("/agent-runs", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return response.data;
}
