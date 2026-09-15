import { api } from "./client";

export interface Service {
  id: string;
  name: string;
  slug: string;
  short_description?: string | null;
  description?: string | null;
  category:
    | "WEB_DEVELOPMENT"
    | "SOFTWARE_DEVELOPMENT"
    | "BUSINESS_AUTOMATION"
    | "AI_SYSTEMS"
    | "DATA_ANALYTICS"
    | "UI_UX"
    | "MAINTENANCE"
    | "CONSULTING"
    | "OTHER";
  subcategory?: string | null;
  status: "DRAFT" | "ACTIVE" | "PAUSED" | "ARCHIVED";
  delivery_model:
    | "FIXED_PROJECT"
    | "CUSTOM_QUOTE"
    | "SUBSCRIPTION"
    | "RETAINER"
    | "HOURLY"
    | "CONSULTATION";
  pricing_model: "FIXED" | "STARTING_AT" | "RANGE" | "CUSTOM" | "NOT_SET";
  base_price?: number | null;
  price_min?: number | null;
  price_max?: number | null;
  currency: string;
  estimated_duration_days?: number | null;
  is_featured: boolean;
  is_active: boolean;
  features: string[];
  requirements: string[];
  target_business_types: string[];
  archived_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ServiceCreateInput {
  name: string;
  slug?: string;
  short_description?: string;
  description?: string;
  category: Service["category"];
  subcategory?: string;
  status?: Service["status"];
  delivery_model?: Service["delivery_model"];
  pricing_model?: Service["pricing_model"];
  base_price?: number;
  price_min?: number;
  price_max?: number;
  currency?: string;
  estimated_duration_days?: number;
  is_featured?: boolean;
  is_active?: boolean;
  features?: string[];
  requirements?: string[];
  target_business_types?: string[];
}

export interface ServiceUpdateInput extends Partial<ServiceCreateInput> {}

export interface LeadService {
  id: string;
  lead_id: string;
  service_id: string;
  relationship_type: "CONSIDERED" | "RECOMMENDED" | "SELECTED" | "REJECTED";
  source: "HUMAN" | "RULE" | "AI" | "IMPORT" | "OTHER";
  notes?: string | null;
  created_at: string;
  updated_at: string;
  service?: Service | null;
}

export interface ServiceListParams {
  page?: number;
  page_size?: number;
  search?: string;
  category?: string;
  status?: string;
  delivery_model?: string;
  pricing_model?: string;
  is_featured?: boolean;
  is_active?: boolean;
  sort?: string;
  order?: "asc" | "desc";
}

export interface PaginatedServicesResponse {
  data: Service[];
  pagination: {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
  };
}

export async function listServices(params: ServiceListParams = {}): Promise<PaginatedServicesResponse> {
  const query = new URLSearchParams();
  if (params.page) query.append("page", params.page.toString());
  if (params.page_size) query.append("page_size", params.page_size.toString());
  if (params.search) query.append("search", params.search);
  if (params.category) query.append("category", params.category);
  if (params.status) query.append("status", params.status);
  if (params.delivery_model) query.append("delivery_model", params.delivery_model);
  if (params.pricing_model) query.append("pricing_model", params.pricing_model);
  if (params.is_featured !== undefined) query.append("is_featured", params.is_featured.toString());
  if (params.is_active !== undefined) query.append("is_active", params.is_active.toString());
  if (params.sort) query.append("sort", params.sort);
  if (params.order) query.append("order", params.order);

  const queryString = query.toString() ? `?${query.toString()}` : "";
  return api<PaginatedServicesResponse>(`/services${queryString}`);
}

export async function getService(id: string): Promise<{ data: Service }> {
  return api<{ data: Service }>(`/services/${id}`);
}

export async function getServiceBySlug(slug: string): Promise<{ data: Service }> {
  return api<{ data: Service }>(`/services/slug/${slug}`);
}

export async function createService(input: ServiceCreateInput): Promise<{ data: Service }> {
  return api<{ data: Service }>("/services", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateService(id: string, input: ServiceUpdateInput): Promise<{ data: Service }> {
  return api<{ data: Service }>(`/services/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function archiveService(id: string): Promise<{ data: Service }> {
  return api<{ data: Service }>(`/services/${id}/archive`, {
    method: "POST",
  });
}

export async function restoreService(id: string): Promise<{ data: Service }> {
  return api<{ data: Service }>(`/services/${id}/restore`, {
    method: "POST",
  });
}

// Lead-Service APIs
export async function listLeadServices(leadId: string): Promise<{ data: LeadService[] }> {
  return api<{ data: LeadService[] }>(`/leads/${leadId}/services`);
}

export async function addServiceToLead(
  leadId: string,
  input: {
    service_id: string;
    relationship_type?: LeadService["relationship_type"];
    source?: LeadService["source"];
    notes?: string;
  }
): Promise<{ data: LeadService }> {
  return api<{ data: LeadService }>(`/leads/${leadId}/services`, {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function removeServiceFromLead(
  leadId: string,
  serviceId: string
): Promise<{ data: { success: boolean; message: string } }> {
  return api<{ data: { success: boolean; message: string } }>(`/leads/${leadId}/services/${serviceId}`, {
    method: "DELETE",
  });
}
