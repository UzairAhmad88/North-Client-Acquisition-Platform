/**
 * Phase 52: Unified Autonomous Knowledge Worker & Multi-Agent Workforce API Client.
 */

import { api } from './client';

export interface AIWorker {
  id?: string;
  worker_code: string;
  organization_id: string;
  name: string;
  description?: string;
  role: string;
  specialization: string;
  status: 'DRAFT' | 'TESTING' | 'APPROVED' | 'SHADOW' | 'ACTIVE' | 'PAUSED' | 'SUSPENDED' | 'DEPRECATED';
  supervision_level: number;
  agent_version: string;
  model_name: string;
  capabilities: string[];
  total_tasks_completed: number;
  grounding_score: number;
  version: number;
}

export interface AIDepartment {
  id?: string;
  department_code: string;
  name: string;
  description?: string;
  monthly_budget_usd: number;
  current_spend_usd: number;
  status: string;
}

export interface AITeam {
  id?: string;
  team_code: string;
  department_code: string;
  name: string;
  purpose?: string;
  workflow_template: string;
  status: string;
  budget_limit_usd: number;
  members: string[];
}

export interface AIWorkTask {
  id?: string;
  task_code: string;
  objective: string;
  description?: string;
  worker_code?: string;
  priority: string;
  status: string;
  supervision_level: number;
  risk_level: string;
  inputs: Record<string, any>;
  expected_output?: string;
  result_summary?: string;
  dependencies: string[];
  cost_usd: number;
  confidence_score: number;
}

export interface AIHandoff {
  id?: string;
  handoff_code: string;
  from_worker_code: string;
  to_worker_code: string;
  task_code: string;
  context_summary: string;
  artifacts: Array<Record<string, any>>;
  expected_next_action: string;
  confidence_score: number;
  status: string;
}

export interface AIConsensusResult {
  consensus_code: string;
  topic: string;
  participating_workers: string[];
  consensus_score: number;
  has_conflicts: boolean;
  synthesized_conclusion: string;
  dissenting_views: Array<Record<string, any>>;
}

export interface WorkforceOverview {
  status: string;
  total_active_workers: number;
  total_departments: number;
  total_tasks_processed: number;
  pending_human_reviews: number;
  economics: {
    total_tasks_completed: number;
    total_ai_cost_usd: number;
    human_hours_saved: number;
    equivalent_human_cost_usd: number;
    net_cost_savings_usd: number;
    roi_multiple: number;
  };
  active_kill_switches: number;
}

export interface WorkforceCopilotResponse {
  query: string;
  answer: string;
  evidence: string[];
  suggested_actions: string[];
  governance_notice: string;
}

export const workforceApi = {
  getOverview: async (): Promise<WorkforceOverview> => {
    return api.get<WorkforceOverview>('/workforce/overview');
  },

  getWorkers: async (specialization?: string, status?: string): Promise<AIWorker[]> => {
    return api.get<AIWorker[]>('/workforce/workers', {
      params: { specialization, status },
    });
  },

  registerWorker: async (data: {
    name: string;
    role: string;
    specialization: string;
    description?: string;
    supervision_level?: number;
    capabilities?: string[];
  }): Promise<AIWorker> => {
    return api.post<AIWorker>('/workforce/workers', data);
  },

  getDepartments: async (): Promise<AIDepartment[]> => {
    return api.get<AIDepartment[]>('/workforce/departments');
  },

  getTeams: async (departmentCode?: string): Promise<AITeam[]> => {
    return api.get<AITeam[]>('/workforce/teams', {
      params: { department_code: departmentCode },
    });
  },

  decomposeObjective: async (objective: string, domain?: string): Promise<AIWorkTask[]> => {
    return api.post<AIWorkTask[]>('/workforce/tasks/decompose', {
      objective,
      domain: domain || 'GROWTH_EXPANSION',
    });
  },

  getTasks: async (workerCode?: string, status?: string): Promise<AIWorkTask[]> => {
    return api.get<AIWorkTask[]>('/workforce/tasks', {
      params: { worker_code: workerCode, status },
    });
  },

  getPendingReviews: async (): Promise<any[]> => {
    return api.get<any[]>('/workforce/reviews/pending');
  },

  resolveReview: async (reviewId: string, approved: boolean, reviewerId: string, rationale: string): Promise<any> => {
    return api.post<any>(`/workforce/reviews/${reviewId}/resolve`, {
      approved,
      reviewer_id: reviewerId,
      rationale,
    });
  },

  createHandoff: async (data: {
    from_worker_code: string;
    to_worker_code: string;
    task_code: string;
    context_summary: string;
    artifacts: any[];
    expected_next_action: string;
  }): Promise<AIHandoff> => {
    return api.post<AIHandoff>('/workforce/handoffs', data);
  },

  evaluateConsensus: async (topic: string, workerEvaluations: any[]): Promise<AIConsensusResult> => {
    return api.post<AIConsensusResult>('/workforce/consensus', {
      topic,
      worker_evaluations: workerEvaluations,
    });
  },

  triggerKillSwitch: async (targetType: string, targetIdentifier: string, reason: string): Promise<any> => {
    return api.post<any>('/workforce/kill-switch', {
      target_type: targetType,
      target_identifier: targetIdentifier,
      reason,
      operator_id: 'security_admin',
    });
  },

  queryCopilot: async (query: string): Promise<WorkforceCopilotResponse> => {
    return api.post<WorkforceCopilotResponse>('/workforce/copilot/query', { query });
  },
};
