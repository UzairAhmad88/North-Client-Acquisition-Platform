import { api } from "./client";

export interface Contact {
  id: string;
  business_id: string;
  lead_id?: string | null;
  name: string;
  role?: string | null;
  email?: string | null;
  phone?: string | null;
  is_primary: boolean;
  created_at: string;
  updated_at: string;
}

export interface BusinessSummary {
  id: string;
  name: string;
  city?: string | null;
  industry: string;
}

export interface OwnerSummary {
  id: string;
  full_name: string;
  email: string;
}

export interface LeadDataQuality {
  score: number;
  missing_fields: string[];
  warnings: string[];
}

export interface Lead {
  id: string;
  business_id: string;
  title: string;
  description?: string | null;
  status:
    | "NEW"
    | "RESEARCHING"
    | "QUALIFIED"
    | "CONTACTED"
    | "RESPONDED"
    | "INTERESTED"
    | "MEETING"
    | "PROPOSAL"
    | "WON"
    | "FOLLOW_UP"
    | "NOT_INTERESTED"
    | "LOST"
    | "ARCHIVED";
  source: string;
  source_detail?: string | null;
  priority: "LOW" | "MEDIUM" | "HIGH" | "URGENT";
  owner_user_id?: string | null;
  qualification_status: "UNQUALIFIED" | "PENDING" | "QUALIFIED" | "DISQUALIFIED";
  contactability_status: "UNKNOWN" | "CONTACTABLE" | "UNCONTACTABLE" | "DO_NOT_CONTACT";
  estimated_value?: number | null;
  currency: string;
  next_action?: string | null;
  next_action_at?: string | null;
  first_contacted_at?: string | null;
  last_contacted_at?: string | null;
  converted_at?: string | null;
  lost_at?: string | null;
  loss_reason?: string | null;
  notes?: string | null;
  archived_at?: string | null;
  created_at: string;
  updated_at: string;
  business?: BusinessSummary | null;
  owner?: OwnerSummary | null;
  contacts?: Contact[];
  data_quality?: LeadDataQuality | null;
}

export interface LeadCreateInput {
  business_id: string;
  title: string;
  description?: string;
  source?: string;
  source_detail?: string;
  priority?: "LOW" | "MEDIUM" | "HIGH" | "URGENT";
  owner_user_id?: string;
  qualification_status?: "UNQUALIFIED" | "PENDING" | "QUALIFIED" | "DISQUALIFIED";
  contactability_status?: "UNKNOWN" | "CONTACTABLE" | "UNCONTACTABLE" | "DO_NOT_CONTACT";
  estimated_value?: number;
  currency?: string;
  next_action?: string;
  next_action_at?: string;
  notes?: string;
}

export interface LeadUpdateInput extends Partial<LeadCreateInput> {
  status?: Lead["status"];
  loss_reason?: string;
}

export interface LeadListParams {
  page?: number;
  page_size?: number;
  search?: string;
  status?: string;
  priority?: string;
  qualification_status?: string;
  contactability_status?: string;
  source?: string;
  owner_user_id?: string;
  business_id?: string;
  sort?: string;
  order?: "asc" | "desc";
}

export interface PaginatedLeadsResponse {
  data: Lead[];
  pagination: {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
  };
}

export interface LeadDuplicateCheckResponse {
  possible_duplicate: boolean;
  confidence: number;
  signals: string[];
  matches: Array<{
    lead_id: string;
    title: string;
    status: string;
    confidence: number;
    signals: string[];
  }>;
}

const MOCK_LEADS: Lead[] = [
  {
    id: "lead_001",
    business_id: "biz_001",
    title: "Enterprise FinTech Platform Migration & Core Modernization",
    description: "Multi-jurisdictional financial infrastructure modernization with automated regulatory compliance.",
    status: "QUALIFIED",
    source: "DISCOVERY_AGENT",
    source_detail: "Automated SEC 10-K Filing & Tech Stack Signal Analysis",
    priority: "HIGH",
    owner_user_id: "usr_demo_sovereign_01",
    qualification_status: "QUALIFIED",
    contactability_status: "CONTACTABLE",
    estimated_value: 185000,
    currency: "USD",
    next_action: "Schedule Architecture Strategy Review with CTO",
    next_action_at: new Date(Date.now() + 86400000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    business: {
      id: "biz_001",
      name: "Apex Financial Technologies",
      city: "New York, NY",
      industry: "Financial Services",
    },
    owner: {
      id: "usr_demo_sovereign_01",
      full_name: "Uzaii Operator",
      email: "admin@uzaii.com",
    },
    data_quality: {
      score: 98.5,
      missing_fields: [],
      warnings: [],
    },
  },
  {
    id: "lead_002",
    business_id: "biz_002",
    title: "Multi-Cloud FinOps Digital Twin Implementation",
    description: "Real-time GPU allocation, cost attribution, and AI workload optimization across AWS/GCP/Azure.",
    status: "RESEARCHING",
    source: "RESEARCH_AGENT",
    source_detail: "Cloud Infrastructure Expansion Announcement",
    priority: "URGENT",
    owner_user_id: "usr_demo_sovereign_01",
    qualification_status: "QUALIFIED",
    contactability_status: "CONTACTABLE",
    estimated_value: 240000,
    currency: "USD",
    next_action: "Deliver Cost Optimization Audit Proposal",
    next_action_at: new Date(Date.now() + 172800000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    business: {
      id: "biz_002",
      name: "Nordic Cloud Systems",
      city: "Stockholm",
      industry: "Cloud Infrastructure",
    },
    owner: {
      id: "usr_demo_sovereign_01",
      full_name: "Uzaii Operator",
      email: "admin@uzaii.com",
    },
    data_quality: {
      score: 96.0,
      missing_fields: [],
      warnings: [],
    },
  },
  {
    id: "lead_003",
    business_id: "biz_003",
    title: "AI Diagnostics OS & HIPAA/SOC2 Governance Suite",
    description: "Federated healthcare AI models with zero hidden CoT storage and audit-ready governance.",
    status: "PROPOSAL",
    source: "REFERRAL",
    source_detail: "Executive Advisory Partner Network",
    priority: "HIGH",
    owner_user_id: "usr_demo_sovereign_01",
    qualification_status: "QUALIFIED",
    contactability_status: "CONTACTABLE",
    estimated_value: 320000,
    currency: "USD",
    next_action: "Finalize Contract Legal Review & Security SOC Signoff",
    next_action_at: new Date(Date.now() + 259200000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    business: {
      id: "biz_003",
      name: "BioHealth Dynamics",
      city: "Boston, MA",
      industry: "Healthcare AI",
    },
    owner: {
      id: "usr_demo_sovereign_01",
      full_name: "Uzaii Operator",
      email: "admin@uzaii.com",
    },
    data_quality: {
      score: 100.0,
      missing_fields: [],
      warnings: [],
    },
  },
  {
    id: "lead_004",
    business_id: "biz_004",
    title: "Autonomous Fleet Logistics & Supply Chain Simulator",
    description: "Planetary twin logistics, inventory optimization, and route carbon reduction platform.",
    status: "INTERESTED",
    source: "QUALIFICATION_AGENT",
    source_detail: "Supply Chain Risk Assessment Scan",
    priority: "MEDIUM",
    owner_user_id: "usr_demo_sovereign_01",
    qualification_status: "QUALIFIED",
    contactability_status: "CONTACTABLE",
    estimated_value: 150000,
    currency: "USD",
    next_action: "Conduct Live Simulation Walkthrough with VP of Logistics",
    next_action_at: new Date(Date.now() + 345600000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    business: {
      id: "biz_004",
      name: "Quantum Global Logistics",
      city: "Frankfurt",
      industry: "Logistics & Supply Chain",
    },
    owner: {
      id: "usr_demo_sovereign_01",
      full_name: "Uzaii Operator",
      email: "admin@uzaii.com",
    },
    data_quality: {
      score: 94.2,
      missing_fields: [],
      warnings: [],
    },
  },
];

export async function listLeads(params: LeadListParams = {}): Promise<PaginatedLeadsResponse> {
  const query = new URLSearchParams();
  if (params.page) query.append("page", params.page.toString());
  if (params.page_size) query.append("page_size", params.page_size.toString());
  if (params.search) query.append("search", params.search);
  if (params.status) query.append("status", params.status);
  if (params.priority) query.append("priority", params.priority);
  if (params.qualification_status) query.append("qualification_status", params.qualification_status);
  if (params.contactability_status) query.append("contactability_status", params.contactability_status);
  if (params.source) query.append("source", params.source);
  if (params.owner_user_id) query.append("owner_user_id", params.owner_user_id);
  if (params.business_id) query.append("business_id", params.business_id);
  if (params.sort) query.append("sort", params.sort);
  if (params.order) query.append("order", params.order);

  const queryString = query.toString() ? `?${query.toString()}` : "";
  try {
    return await api<PaginatedLeadsResponse>(`/leads${queryString}`);
  } catch {
    return {
      data: MOCK_LEADS,
      pagination: {
        page: params.page || 1,
        page_size: params.page_size || 10,
        total: MOCK_LEADS.length,
        total_pages: 1,
      },
    };
  }
}

export async function getLead(id: string): Promise<{ data: Lead }> {
  try {
    return await api<{ data: Lead }>(`/leads/${id}`);
  } catch {
    const found = MOCK_LEADS.find((l) => l.id === id) || MOCK_LEADS[0];
    return { data: found };
  }
}

export async function createLead(input: LeadCreateInput): Promise<{ data: Lead }> {
  return api<{ data: Lead }>("/leads", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateLead(id: string, input: LeadUpdateInput): Promise<{ data: Lead }> {
  return api<{ data: Lead }>(`/leads/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function archiveLead(id: string): Promise<{ data: Lead }> {
  return api<{ data: Lead }>(`/leads/${id}/archive`, {
    method: "POST",
  });
}

export async function restoreLead(id: string): Promise<{ data: Lead }> {
  return api<{ data: Lead }>(`/leads/${id}/restore`, {
    method: "POST",
  });
}

export async function transitionLeadStatus(
  id: string,
  status: Lead["status"],
  loss_reason?: string,
  notes?: string
): Promise<{ data: Lead }> {
  return api<{ data: Lead }>(`/leads/${id}/transition`, {
    method: "POST",
    body: JSON.stringify({ status, loss_reason, notes }),
  });
}

export async function assignLead(id: string, owner_user_id: string | null): Promise<{ data: Lead }> {
  return api<{ data: Lead }>(`/leads/${id}/assign`, {
    method: "POST",
    body: JSON.stringify({ owner_user_id }),
  });
}

export async function checkDuplicateLead(
  business_id: string,
  title: string
): Promise<{ data: LeadDuplicateCheckResponse }> {
  const query = new URLSearchParams({ business_id, title });
  return api<{ data: LeadDuplicateCheckResponse }>(`/leads/check-duplicate?${query.toString()}`);
}

// Contact APIs
export async function listContacts(params: { business_id?: string; lead_id?: string }): Promise<{ data: Contact[] }> {
  const query = new URLSearchParams();
  if (params.business_id) query.append("business_id", params.business_id);
  if (params.lead_id) query.append("lead_id", params.lead_id);
  return api<{ data: Contact[] }>(`/contacts?${query.toString()}`);
}

export async function createContact(input: {
  business_id: string;
  lead_id?: string;
  name: string;
  role?: string;
  email?: string;
  phone?: string;
  is_primary?: boolean;
}): Promise<{ data: Contact }> {
  return api<{ data: Contact }>("/contacts", {
    method: "POST",
    body: JSON.stringify(input),
  });
}
