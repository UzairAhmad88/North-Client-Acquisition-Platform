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

export async function getDashboardSummary(): Promise<DashboardSummaryData> {
  const response = await api<{ data: DashboardSummaryData }>("/dashboard/summary");
  return response.data;
}
