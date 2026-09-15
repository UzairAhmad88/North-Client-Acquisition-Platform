import { api } from './client';

export interface TaskItem {
  id: string;
  project_id: string;
  parent_task_id?: string;
  deliverable_id?: string;
  milestone_id?: string;
  task_number: string;
  name: string;
  description: string;
  status: string;
  priority: string;
  assignee_id?: string;
  planned_start?: string;
  planned_end?: string;
  actual_start?: string;
  actual_end?: string;
  estimated_hours: number;
  actual_hours: number;
  progress_percent: number;
  dependency_status: string;
  blocked_reason?: string;
  version: number;
  created_at: string;
}

export interface MilestoneItem {
  id: string;
  project_id: string;
  name: string;
  description: string;
  target_date?: string;
  status: string;
  progress_percent: number;
  created_at: string;
}

export interface DeliverableItem {
  id: string;
  project_id: string;
  name: string;
  description: string;
  source_baseline_item: string;
  acceptance_criteria: string[];
  status: string;
  target_date?: string;
  created_at: string;
}

export interface ProjectDetail {
  id: string;
  project_number: string;
  name: string;
  description: string;
  business_id: string;
  client_id?: string;
  contract_id: string;
  baseline_id: string;
  owner_id?: string;
  status: string;
  health: string;
  priority: string;
  planned_start?: string;
  planned_end?: string;
  actual_start?: string;
  actual_end?: string;
  progress_percent: number;
  total_estimated_hours: number;
  total_actual_hours: number;
  version: number;
  created_at: string;
  updated_at: string;
  tasks: TaskItem[];
  milestones: MilestoneItem[];
  deliverables: DeliverableItem[];
}

export interface ProjectHealthResponse {
  health: string;
  reasons: string[];
  schedule_variance_days: number;
  effort_variance_hours: number;
  overdue_task_count: number;
  blocked_task_count: number;
  unresolved_blocker_count: number;
}

export async function listProjects(params?: { status?: string; health?: string; skip?: number; limit?: number }) {
  const query = new URLSearchParams();
  if (params?.status) query.append('status', params.status);
  if (params?.health) query.append('health', params.health);
  if (params?.skip) query.append('skip', params.skip.toString());
  if (params?.limit) query.append('limit', params.limit.toString());

  return api<{ items: ProjectDetail[]; total: number }>(`/projects?${query.toString()}`);
}

export async function getProjectDetail(projectId: string) {
  return api<ProjectDetail>(`/projects/${projectId}`);
}

export async function updateProjectStatus(projectId: string, status: string) {
  return api<ProjectDetail>(`/projects/${projectId}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });
}

export async function createTask(projectId: string, payload: {
  name: string;
  description: string;
  priority?: string;
  estimated_hours?: number;
  parent_task_id?: string;
  deliverable_id?: string;
  milestone_id?: string;
}) {
  return api<TaskItem>(`/projects/${projectId}/tasks`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateTaskStatus(taskId: string, payload: {
  status: string;
  progress_percent?: number;
  blocked_reason?: string;
}) {
  return api<TaskItem>(`/projects/tasks/${taskId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}

export async function getProjectHealth(projectId: string) {
  return api<ProjectHealthResponse>(`/projects/${projectId}/health`);
}

export async function runProjectAgent(projectId: string, action: 'PLAN_WBS' | 'SUMMARIZE' | 'ANALYZE_RISKS_AND_SCOPE') {
  return api<any>(`/projects/${projectId}/run-agent?action=${action}`, {
    method: 'POST',
  });
}
