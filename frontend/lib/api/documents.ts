import { api } from './client';

export interface FileItem {
  id: string;
  tenant_id: string;
  workspace_id: string;
  folder_id?: string;
  name: string;
  extension?: string;
  mime_type: string;
  size_bytes: number;
  checksum: string;
  storage_provider: string;
  storage_key: string;
  status: string;
  classification: string;
  sensitivity: string;
  visibility: string;
  owner_id?: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface FileUploadResponse {
  success: boolean;
  file_id?: string;
  tenant_id: string;
  workspace_id: string;
  filename: string;
  mime_type: string;
  size_bytes: number;
  checksum_sha256: string;
  storage_key?: string;
  status: string;
  classification: string;
  sensitivity: string;
  visibility: string;
  extracted_text?: string;
  chunks_count: number;
  preview?: Record<string, any>;
  validation_errors: string[];
}

export interface ManagedDocument {
  id: string;
  tenant_id: string;
  workspace_id: string;
  folder_id?: string;
  title: string;
  current_version_id?: string;
  current_version_number: number;
  status: string;
  classification: string;
  sensitivity: string;
  visibility: string;
  retention_status: string;
  legal_hold: boolean;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface ShareLinkResponse {
  link_id: string;
  token: string;
  document_id: string;
  permissions: string[];
  expires_at: string;
  created_by: string;
  access_url: string;
}

export const documentsApi = {
  // Files
  listFiles: (params?: { workspace_id?: string; folder_id?: string; classification?: string }) => {
    const query = new URLSearchParams();
    if (params?.workspace_id) query.append('workspace_id', params.workspace_id);
    if (params?.folder_id) query.append('folder_id', params.folder_id);
    if (params?.classification) query.append('classification', params.classification);
    return api<FileItem[]>(`/files?${query.toString()}`);
  },

  getFile: (id: string) => api<FileItem>(`/files/${id}`),

  uploadFile: async (formData: FormData) => {
    // Direct form upload
    return api<FileUploadResponse>('/files/upload', {
      method: 'POST',
      body: formData,
    });
  },

  // Documents
  listDocuments: (params?: { workspace_id?: string; classification?: string; status?: string }) => {
    const query = new URLSearchParams();
    if (params?.workspace_id) query.append('workspace_id', params.workspace_id);
    if (params?.classification) query.append('classification', params.classification);
    if (params?.status) query.append('status', params.status);
    return api<ManagedDocument[]>(`/documents?${query.toString()}`);
  },

  getDocument: (id: string) => api<ManagedDocument>(`/documents/${id}`),

  createDocument: (payload: {
    workspace_id: string;
    title: string;
    classification?: string;
    sensitivity?: string;
    visibility?: string;
    folder_id?: string;
  }) => api<ManagedDocument>('/documents', { method: 'POST', body: JSON.stringify(payload) }),

  submitForReview: (id: string, payload?: { reviewer_id?: string; notes?: string }) =>
    api<any>(`/documents/${id}/review`, { method: 'POST', body: JSON.stringify(payload || {}) }),

  approveDocument: (id: string, payload: { version_id: string; version_number: number; checksum: string; decision_notes?: string }) =>
    api<any>(`/documents/${id}/approve`, { method: 'POST', body: JSON.stringify(payload) }),

  generateShareLink: (id: string, payload: { expires_in_hours?: number; allow_download?: boolean; passcode?: string }) =>
    api<ShareLinkResponse>(`/documents/${id}/links`, { method: 'POST', body: JSON.stringify(payload) }),
};
