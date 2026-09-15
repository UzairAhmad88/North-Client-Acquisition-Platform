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
  return api<PaginatedLeadsResponse>(`/leads${queryString}`);
}

export async function getLead(id: string): Promise<{ data: Lead }> {
  return api<{ data: Lead }>(`/leads/${id}`);
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
