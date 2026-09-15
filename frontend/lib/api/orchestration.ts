import { api } from './client';

export interface WorkflowTemplate {
  workflow_key: string;
  name: string;
  description: string;
  category: string;
  version: string;
  steps: Array<{
    step_key: string;
    name: string;
    step_type: string;
    config: Record<string, any>;
    timeout_seconds: number;
  }>;
  transitions: Array<{
    from_step_key: string;
    to_step_key: string;
    condition?: string;
    is_default: boolean;
  }>;
}

export interface WorkflowRunStep {
  id: string;
  step_key: string;
  step_type: string;
  status: string;
  attempt_count: number;
  duration_ms: number;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  error_code?: string;
  error_summary?: string;
  started_at?: string;
  completed_at?: string;
}

export interface WorkflowRun {
  id: string;
  tenant_id: string;
  workflow_key: string;
  workflow_version: string;
  trigger_type: string;
  trigger_reference?: string;
  status: string;
  current_step?: string;
  correlation_id: string;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  error_code?: string;
  error_summary?: string;
  started_at: string;
  completed_at?: string;
  paused_at?: string;
  failed_at?: string;
  cancelled_at?: string;
}

export interface DomainEventRecord {
  id: string;
  event_id: string;
  event_type: string;
  event_version: string;
  aggregate_type: string;
  aggregate_id: string;
  tenant_id: string;
  payload: Record<string, any>;
  correlation_id: string;
  causation_id?: string;
  status: string;
  attempt_count: number;
  created_at: string;
}

export interface HumanTask {
  id: string;
  tenant_id: string;
  workflow_run_id: string;
  step_key: string;
  title: string;
  description: string;
  task_type: string;
  priority: string;
  assigned_to?: string;
  status: string;
  deadline?: string;
  input_data: Record<string, any>;
  decision?: string;
  decision_reason?: string;
  created_at: string;
  completed_at?: string;
}

export interface AutomationRule {
  id: string;
  tenant_id: string;
  name: string;
  description: string;
  version: string;
  trigger_type: string;
  trigger_config: Record<string, any>;
  condition_config: Record<string, any>;
  action_config: Record<string, any>;
  priority: string;
  enabled: boolean;
  requires_human_approval: boolean;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface DeadLetterRecord {
  id: string;
  event_id: string;
  event_type: string;
  workflow_id?: string;
  consumer: string;
  attempt_count: number;
  failure_type: string;
  error_summary: string;
  payload: Record<string, any>;
  status: string;
  last_error_at: string;
  created_at: string;
}

export const orchestrationApi = {
  // Workflows
  getTemplates: async (): Promise<WorkflowTemplate[]> => {
    return api<WorkflowTemplate[]>('/workflows/templates');
  },
  listWorkflows: async (status?: string, workflow_key?: string): Promise<WorkflowRun[]> => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (workflow_key) params.append('workflow_key', workflow_key);
    const query = params.toString() ? `?${params.toString()}` : '';
    return api<WorkflowRun[]>(`/workflows${query}`);
  },
  getWorkflow: async (runId: string): Promise<WorkflowRun> => {
    return api<WorkflowRun>(`/workflows/${runId}`);
  },
  startWorkflow: async (data: {
    workflow_key: string;
    input_data?: Record<string, any>;
    trigger_type?: string;
    trigger_reference?: string;
  }): Promise<WorkflowRun> => {
    return api<WorkflowRun>('/workflows/start', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  pauseWorkflow: async (runId: string): Promise<WorkflowRun> => {
    return api<WorkflowRun>(`/workflows/${runId}/pause`, {
      method: 'POST',
    });
  },
  resumeWorkflow: async (runId: string): Promise<WorkflowRun> => {
    return api<WorkflowRun>(`/workflows/${runId}/resume`, {
      method: 'POST',
    });
  },
  cancelWorkflow: async (runId: string, reason?: string): Promise<WorkflowRun> => {
    return api<WorkflowRun>(`/workflows/${runId}/cancel?reason=${encodeURIComponent(reason || 'Cancelled by user')}`, {
      method: 'POST',
    });
  },

  // Events
  listEvents: async (event_type?: string): Promise<DomainEventRecord[]> => {
    const params = new URLSearchParams();
    if (event_type) params.append('event_type', event_type);
    const query = params.toString() ? `?${params.toString()}` : '';
    return api<DomainEventRecord[]>(`/events${query}`);
  },
  replayEvents: async (data: { event_type: string; replay_mode?: string }): Promise<any> => {
    return api<any>('/events/replay', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Human Tasks
  listTasks: async (status?: string): Promise<HumanTask[]> => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    const query = params.toString() ? `?${params.toString()}` : '';
    return api<HumanTask[]>(`/tasks${query}`);
  },
  completeTask: async (taskId: string, data: { decision: string; decision_reason: string; content_hash?: string }): Promise<HumanTask> => {
    return api<HumanTask>(`/tasks/${taskId}/complete`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Automations
  listAutomations: async (enabled_only?: boolean): Promise<AutomationRule[]> => {
    const params = new URLSearchParams();
    if (enabled_only) params.append('enabled_only', 'true');
    const query = params.toString() ? `?${params.toString()}` : '';
    return api<AutomationRule[]>(`/automations${query}`);
  },
  createAutomation: async (data: Partial<AutomationRule>): Promise<AutomationRule> => {
    return api<AutomationRule>('/automations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  toggleAutomation: async (ruleId: string, enabled: boolean): Promise<AutomationRule> => {
    return api<AutomationRule>(`/automations/${ruleId}/toggle?enabled=${enabled}`, {
      method: 'POST',
    });
  },

  // DLQ
  listDeadLetters: async (status?: string): Promise<DeadLetterRecord[]> => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    const query = params.toString() ? `?${params.toString()}` : '';
    return api<DeadLetterRecord[]>(`/dead-letter${query}`);
  },
  retryDeadLetter: async (dlqId: string): Promise<DeadLetterRecord> => {
    return api<DeadLetterRecord>(`/dead-letter/${dlqId}/retry`, {
      method: 'POST',
    });
  },
};
