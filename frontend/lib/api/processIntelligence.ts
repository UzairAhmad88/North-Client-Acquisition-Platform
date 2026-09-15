import { api } from './client';

export interface ProcessOverview {
  total_monitored_processes: number;
  total_active_cases: number;
  total_active_bottlenecks: number;
  total_conformance_violations: number;
  automation_opportunities_count: number;
  top_bottlenecks: BottleneckRecord[];
  recent_violations: ConformanceViolation[];
  automation_candidates: AutomationCandidate[];
}

export interface ProcessDefinition {
  id: string;
  process_code: string;
  tenant_id: string;
  name: string;
  description?: string;
  domain: string;
  owner_id: string;
  version: number;
  status: string;
  scope: string;
  expected_outcome?: string;
  policy_requirements: string[];
  governance_controls: string[];
  kpis: Record<string, any>;
}

export interface ProcessEvent {
  id: string;
  event_code: string;
  process_id?: string;
  case_id?: string;
  activity: string;
  timestamp: string;
  actor: string;
  actor_type: string;
  resource?: string;
  status: string;
  duration_ms: number;
  attributes: Record<string, any>;
}

export interface ProcessVariant {
  id: string;
  process_id: string;
  variant_code: string;
  event_sequence: string[];
  sequence_hash: string;
  frequency: number;
  percentage: number;
  average_cycle_time_seconds: number;
  conversion_rate: number;
  failure_rate: number;
  rework_rate: number;
  is_conforming: boolean;
}

export interface ProcessMap {
  id: string;
  process_id: string;
  map_type: string;
  version_number: number;
  nodes: Array<{ id: string; label: string; frequency: number; average_duration_ms: number }>;
  edges: Array<{
    source_activity: string;
    target_activity: string;
    transition_frequency: number;
    average_latency_seconds: number;
    median_latency_seconds: number;
    failure_count: number;
  }>;
  metrics_summary: Record<string, any>;
}

export interface ConformanceViolation {
  id: string;
  process_id: string;
  case_id?: string;
  rule_id?: string;
  violation_code: string;
  violation_type: string;
  detected_at: string;
  activity_involved: string;
  severity: string;
  description: string;
  evidence_payload: Record<string, any>;
  status: string;
}

export interface BottleneckRecord {
  id: string;
  process_id: string;
  bottleneck_code: string;
  activity_name: string;
  bottleneck_type: string;
  average_wait_seconds: number;
  average_processing_seconds: number;
  queue_depth: number;
  frequency: number;
  affected_cases_count: number;
  root_cause_summary: string;
  business_impact: string;
  severity: string;
  recommendation?: string;
  evidence_payload: Record<string, any>;
}

export interface ReworkRecord {
  id: string;
  process_id: string;
  case_id?: string;
  activity_name: string;
  repetition_count: number;
  wasted_duration_seconds: number;
  probable_driver: string;
  evidence_payload: Record<string, any>;
}

export interface HandoffRecord {
  id: string;
  process_id: string;
  source_role: string;
  target_role: string;
  handoff_type: string;
  average_delay_seconds: number;
  handoff_count: number;
  friction_score: number;
  common_issues: string[];
}

export interface AutomationCandidate {
  id: string;
  candidate_code: string;
  process_id: string;
  task_name: string;
  frequency_per_month: number;
  average_duration_minutes: number;
  error_rate: number;
  reversibility: string;
  suitability_score: number;
  classification: string;
  expected_savings_hours_month: number;
  status: string;
}

export interface OptimizationProposal {
  id: string;
  proposal_code: string;
  process_id: string;
  title: string;
  current_version: number;
  proposed_version: number;
  problem_statement: string;
  evidence_summary: string;
  proposed_changes: Record<string, any>;
  tradeoff_scorecard: Record<string, any>;
  expected_benefits: Record<string, any>;
  expected_cost: number;
  risk_level: string;
  rollback_plan: string;
  owner_id: string;
  status: string;
}

export interface SimulationResult {
  simulation_code: string;
  process_id: string;
  scenario_type: string;
  iterations: number;
  predicted_throughput: number;
  predicted_cycle_time_seconds: number;
  predicted_cost: number;
  predicted_failure_rate: number;
  predicted_rework_rate: number;
  results_summary: Record<string, any>;
  assumptions: Record<string, any>;
}

export interface ProcessHealthReport {
  process_id: string;
  health_status: string;
  cycle_time_score: number;
  conformance_score: number;
  failure_score: number;
  rework_score: number;
  slo_compliance_rate: number;
  factors_summary: Record<string, any>;
}

export const processIntelligenceApi = {
  getOverview: async (tenantId = 'default_tenant'): Promise<ProcessOverview> => {
    return api.get<ProcessOverview>(`/process-intelligence/overview?tenant_id=${tenantId}`);
  },

  listProcesses: async (tenantId = 'default_tenant'): Promise<ProcessDefinition[]> => {
    return api.get<ProcessDefinition[]>(`/process-intelligence/processes?tenant_id=${tenantId}`);
  },

  createProcess: async (data: Partial<ProcessDefinition>, tenantId = 'default_tenant'): Promise<ProcessDefinition> => {
    return api.post<ProcessDefinition>(`/process-intelligence/processes?tenant_id=${tenantId}`, data);
  },

  getProcess: async (processId: string, tenantId = 'default_tenant'): Promise<ProcessDefinition> => {
    return api.get<ProcessDefinition>(`/process-intelligence/processes/${processId}?tenant_id=${tenantId}`);
  },

  getVariants: async (processId: string, tenantId = 'default_tenant'): Promise<ProcessVariant[]> => {
    return api.get<ProcessVariant[]>(`/process-intelligence/variants?process_id=${processId}&tenant_id=${tenantId}`);
  },

  getProcessMap: async (processId: string, mapType = 'OBSERVED', tenantId = 'default_tenant'): Promise<ProcessMap> => {
    return api.get<ProcessMap>(`/process-intelligence/maps/${processId}?map_type=${mapType}&tenant_id=${tenantId}`);
  },

  getConformanceViolations: async (processId: string, tenantId = 'default_tenant'): Promise<ConformanceViolation[]> => {
    return api.get<ConformanceViolation[]>(`/process-intelligence/conformance?process_id=${processId}&tenant_id=${tenantId}`);
  },

  getBottlenecks: async (processId: string, tenantId = 'default_tenant'): Promise<BottleneckRecord[]> => {
    return api.get<BottleneckRecord[]>(`/process-intelligence/bottlenecks?process_id=${processId}&tenant_id=${tenantId}`);
  },

  getReworkRecords: async (processId: string, tenantId = 'default_tenant'): Promise<ReworkRecord[]> => {
    return api.get<ReworkRecord[]>(`/process-intelligence/rework?process_id=${processId}&tenant_id=${tenantId}`);
  },

  getHandoffRecords: async (processId: string, tenantId = 'default_tenant'): Promise<HandoffRecord[]> => {
    return api.get<HandoffRecord[]>(`/process-intelligence/handoffs?process_id=${processId}&tenant_id=${tenantId}`);
  },

  getAutomationCandidates: async (processId: string, tenantId = 'default_tenant'): Promise<AutomationCandidate[]> => {
    return api.get<AutomationCandidate[]>(`/process-intelligence/automation?process_id=${processId}&tenant_id=${tenantId}`);
  },

  listOptimizationProposals: async (processId: string, tenantId = 'default_tenant'): Promise<OptimizationProposal[]> => {
    return api.get<OptimizationProposal[]>(`/process-intelligence/optimization?process_id=${processId}&tenant_id=${tenantId}`);
  },

  createOptimizationProposal: async (data: any, tenantId = 'default_tenant'): Promise<OptimizationProposal> => {
    return api.post<OptimizationProposal>(`/process-intelligence/optimization?tenant_id=${tenantId}`, data);
  },

  runSimulation: async (data: any, tenantId = 'default_tenant'): Promise<SimulationResult> => {
    return api.post<SimulationResult>(`/process-intelligence/simulations?tenant_id=${tenantId}`, data);
  },

  getProcessHealth: async (processId: string, tenantId = 'default_tenant'): Promise<ProcessHealthReport> => {
    return api.get<ProcessHealthReport>(`/process-intelligence/health?process_id=${processId}&tenant_id=${tenantId}`);
  },

  queryCopilot: async (data: { process_id: string; query: string }, tenantId = 'default_tenant'): Promise<any> => {
    return api.post<any>(`/process-intelligence/copilot/query?tenant_id=${tenantId}`, data);
  },
};
