import { api } from "./client";

export interface BusinessMetricsSummary {
  active_count: number;
  total_count: number;
}

export interface LeadMetricsSummary {
  open_count: number;
  qualified_count: number;
  high_priority_count: number;
  total_count: number;
}

export interface LeadPipelineSnapshot {
  counts: Record<string, number>;
}

export interface AttentionSummary {
  high_priority_leads_count: number;
  overdue_actions_count: number;
  incomplete_data_businesses_count: number;
}

export interface OverdueAction {
  lead_id: string;
  lead_title: string;
  business_id: string;
  business_name: string;
  next_action?: string | null;
  next_action_at: string;
  priority: string;
}

export interface UpcomingAction {
  lead_id: string;
  lead_title: string;
  business_id: string;
  business_name: string;
  next_action?: string | null;
  next_action_at: string;
  priority: string;
}

export interface RecentLeadItem {
  id: string;
  title: string;
  business_id: string;
  business_name: string;
  status: string;
  priority: string;
  qualification_status: string;
  updated_at: string;
}

export interface RecentBusinessItem {
  id: string;
  name: string;
  industry?: string | null;
  city?: string | null;
  status: string;
  data_quality_score: number;
  updated_at: string;
}

export interface ServiceSummary {
  active_services_count: number;
  featured_services_count: number;
  total_services_count: number;
  category_counts: Record<string, number>;
}

export interface DashboardSummaryData {
  businesses: BusinessMetricsSummary;
  leads: LeadMetricsSummary;
  pipeline: LeadPipelineSnapshot;
  attention: AttentionSummary;
  overdue_actions: OverdueAction[];
  upcoming_actions: UpcomingAction[];
  recent_leads: RecentLeadItem[];
  recent_businesses: RecentBusinessItem[];
  services: ServiceSummary;
}

const MOCK_DASHBOARD_SUMMARY: DashboardSummaryData = {
  businesses: {
    active_count: 42,
    total_count: 58,
  },
  leads: {
    open_count: 18,
    qualified_count: 14,
    high_priority_count: 6,
    total_count: 35,
  },
  pipeline: {
    counts: {
      NEW: 5,
      RESEARCHING: 6,
      QUALIFIED: 8,
      CONTACTED: 7,
      PROPOSAL: 5,
      WON: 4,
    },
  },
  attention: {
    high_priority_leads_count: 6,
    overdue_actions_count: 2,
    incomplete_data_businesses_count: 3,
  },
  overdue_actions: [
    {
      lead_id: "lead_001",
      lead_title: "Enterprise FinTech Platform Migration",
      business_id: "biz_001",
      business_name: "Apex Financial Technologies",
      next_action: "Schedule Architecture Strategy Review with CTO",
      next_action_at: new Date(Date.now() - 3600000).toISOString(),
      priority: "HIGH",
    },
    {
      lead_id: "lead_002",
      lead_title: "Multi-Cloud FinOps Digital Twin Implementation",
      business_id: "biz_002",
      business_name: "Nordic Cloud Systems",
      next_action: "Deliver Cost Optimization Audit Proposal",
      next_action_at: new Date(Date.now() - 7200000).toISOString(),
      priority: "URGENT",
    },
  ],
  upcoming_actions: [
    {
      lead_id: "lead_003",
      lead_title: "AI Diagnostics OS & HIPAA/SOC2 Governance Suite",
      business_id: "biz_003",
      business_name: "BioHealth Dynamics",
      next_action: "Finalize Contract Legal Review & Security SOC Signoff",
      next_action_at: new Date(Date.now() + 86400000).toISOString(),
      priority: "HIGH",
    },
  ],
  recent_leads: [
    {
      id: "lead_001",
      title: "Enterprise FinTech Platform Migration",
      business_id: "biz_001",
      business_name: "Apex Financial Technologies",
      status: "QUALIFIED",
      priority: "HIGH",
      qualification_status: "QUALIFIED",
      updated_at: new Date().toISOString(),
    },
    {
      id: "lead_002",
      title: "Multi-Cloud FinOps Digital Twin Implementation",
      business_id: "biz_002",
      business_name: "Nordic Cloud Systems",
      status: "RESEARCHING",
      priority: "URGENT",
      qualification_status: "QUALIFIED",
      updated_at: new Date().toISOString(),
    },
    {
      id: "lead_003",
      title: "AI Diagnostics OS & HIPAA/SOC2 Governance Suite",
      business_id: "biz_003",
      business_name: "BioHealth Dynamics",
      status: "PROPOSAL",
      priority: "HIGH",
      qualification_status: "QUALIFIED",
      updated_at: new Date().toISOString(),
    },
  ],
  recent_businesses: [
    {
      id: "biz_001",
      name: "Apex Financial Technologies",
      industry: "Financial Services",
      city: "New York, NY",
      status: "ACTIVE",
      data_quality_score: 98.5,
      updated_at: new Date().toISOString(),
    },
    {
      id: "biz_002",
      name: "Nordic Cloud Systems",
      industry: "Cloud Infrastructure",
      city: "Stockholm",
      status: "ACTIVE",
      data_quality_score: 96.0,
      updated_at: new Date().toISOString(),
    },
    {
      id: "biz_003",
      name: "BioHealth Dynamics",
      industry: "Healthcare AI",
      city: "Boston, MA",
      status: "ACTIVE",
      data_quality_score: 100.0,
      updated_at: new Date().toISOString(),
    },
  ],
  services: {
    active_services_count: 12,
    featured_services_count: 4,
    total_services_count: 16,
    category_counts: {
      "AI & Machine Learning": 5,
      "Cloud & FinOps": 4,
      "Governance & SOC2": 3,
      "Autonomous Engineering": 4,
    },
  },
};

export async function getDashboardSummary(): Promise<DashboardSummaryData> {
  try {
    const response = await api<{ data: DashboardSummaryData }>("/dashboard/summary");
    return response.data;
  } catch {
    return MOCK_DASHBOARD_SUMMARY;
  }
}
