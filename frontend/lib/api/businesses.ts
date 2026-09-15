import { api } from "./client";

export interface BusinessDataQuality {
  score: number;
  missing_fields: string[];
  warnings: string[];
}

export interface Business {
  id: string;
  name: string;
  normalized_name: string;
  legal_name?: string | null;
  description?: string | null;
  business_type: string;
  industry: string;
  category?: string | null;
  subcategory?: string | null;
  phone?: string | null;
  normalized_phone?: string | null;
  email?: string | null;
  normalized_email?: string | null;
  website_url?: string | null;
  normalized_website?: string | null;
  address?: string | null;
  city?: string | null;
  state?: string | null;
  country?: string | null;
  postal_code?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  timezone?: string | null;
  status: "ACTIVE" | "INACTIVE" | "ARCHIVED";
  source: string;
  source_url?: string | null;
  external_id?: string | null;
  created_by_user_id?: string | null;
  archived_at?: string | null;
  created_at: string;
  updated_at: string;
  data_quality?: BusinessDataQuality | null;
}

export interface BusinessCreateInput {
  name: string;
  legal_name?: string;
  description?: string;
  business_type?: string;
  industry?: string;
  category?: string;
  subcategory?: string;
  phone?: string;
  email?: string;
  website_url?: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  postal_code?: string;
  source?: string;
  source_url?: string;
  external_id?: string;
}

export interface BusinessUpdateInput extends Partial<BusinessCreateInput> {
  status?: "ACTIVE" | "INACTIVE" | "ARCHIVED";
}

export interface BusinessDuplicateCheckResponse {
  possible_duplicate: boolean;
  confidence: number;
  signals: string[];
  matches: Array<{
    business_id: string;
    name: string;
    confidence: number;
    signals: string[];
  }>;
}

export interface BusinessListParams {
  page?: number;
  page_size?: number;
  search?: string;
  status?: string;
  industry?: string;
  business_type?: string;
  city?: string;
  country?: string;
  source?: string;
  sort?: string;
  order?: "asc" | "desc";
}

export interface PaginatedBusinessesResponse {
  data: Business[];
  pagination: {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
  };
}

export async function listBusinesses(params: BusinessListParams = {}): Promise<PaginatedBusinessesResponse> {
  const query = new URLSearchParams();
  if (params.page) query.append("page", params.page.toString());
  if (params.page_size) query.append("page_size", params.page_size.toString());
  if (params.search) query.append("search", params.search);
  if (params.status) query.append("status", params.status);
  if (params.industry) query.append("industry", params.industry);
  if (params.business_type) query.append("business_type", params.business_type);
  if (params.city) query.append("city", params.city);
  if (params.country) query.append("country", params.country);
  if (params.source) query.append("source", params.source);
  if (params.sort) query.append("sort", params.sort);
  if (params.order) query.append("order", params.order);

  const queryString = query.toString() ? `?${query.toString()}` : "";
  return api<PaginatedBusinessesResponse>(`/businesses${queryString}`);
}

export async function getBusiness(id: string): Promise<{ data: Business }> {
  return api<{ data: Business }>(`/businesses/${id}`);
}

export async function createBusiness(input: BusinessCreateInput): Promise<{ data: Business }> {
  return api<{ data: Business }>("/businesses", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateBusiness(id: string, input: BusinessUpdateInput): Promise<{ data: Business }> {
  return api<{ data: Business }>(`/businesses/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function archiveBusiness(id: string): Promise<{ data: Business }> {
  return api<{ data: Business }>(`/businesses/${id}/archive`, {
    method: "POST",
  });
}

export async function restoreBusiness(id: string): Promise<{ data: Business }> {
  return api<{ data: Business }>(`/businesses/${id}/restore`, {
    method: "POST",
  });
}

export async function checkDuplicateBusiness(name: string, extra: Record<string, string> = {}): Promise<{ data: BusinessDuplicateCheckResponse }> {
  const query = new URLSearchParams({ name, ...extra });
  return api<{ data: BusinessDuplicateCheckResponse }>(`/businesses/check-duplicate?${query.toString()}`);
}
