import { api } from './client';

export type CommunicationType =
  | 'NOTIFICATION'
  | 'CONVERSATION_MESSAGE'
  | 'CLIENT_MESSAGE'
  | 'INTERNAL_NOTE'
  | 'OUTREACH_MESSAGE'
  | 'SYSTEM_ALERT'
  | 'SECURITY_ALERT'
  | 'WORKFLOW_UPDATE'
  | 'APPROVAL_REQUEST'
  | 'DOCUMENT_COMMENT';

export type NotificationPriority =
  | 'LOW'
  | 'NORMAL'
  | 'HIGH'
  | 'URGENT'
  | 'CRITICAL_SECURITY';

export type DeliveryChannel =
  | 'IN_APP'
  | 'EMAIL'
  | 'SMS'
  | 'WEBHOOK'
  | 'PUSH'
  | 'REALTIME_WS';

export type DeliveryStatus =
  | 'PENDING'
  | 'QUEUED'
  | 'SENT'
  | 'DELIVERED'
  | 'FAILED'
  | 'DEAD_LETTER'
  | 'SUPPRESSED'
  | 'SKIPPED_QUIET_HOURS';

export type InboxState =
  | 'ACTIVE'
  | 'READ'
  | 'ARCHIVED'
  | 'SNOOZED'
  | 'DELETED';

export type MessageVisibility =
  | 'CLIENT_VISIBLE'
  | 'INTERNAL';

export type ConversationType =
  | 'DIRECT'
  | 'GROUP'
  | 'PROJECT'
  | 'PROPOSAL'
  | 'CONTRACT'
  | 'SUPPORT_TICKET'
  | 'CHANGE_REQUEST';

export interface InboxItem {
  id: string;
  tenant_id: string;
  recipient_id: string;
  notification_id?: string;
  conversation_message_id?: string;
  item_type: CommunicationType;
  title: string;
  summary: string;
  priority: NotificationPriority;
  state: InboxState;
  is_read: boolean;
  is_starred: boolean;
  is_pinned: boolean;
  read_at?: string;
  snoozed_until?: string;
  action_url?: string;
  entity_type?: string;
  entity_id?: string;
  created_at: string;
  updated_at: string;
}

export interface InboxUnreadCount {
  unread_count: number;
  tenant_id: string;
  recipient_id: string;
}

export interface NotificationRecord {
  id: string;
  tenant_id: string;
  notification_type: CommunicationType;
  priority: NotificationPriority;
  title: string;
  body: string;
  source_module: string;
  source_event_id?: string;
  entity_type?: string;
  entity_id?: string;
  action_url?: string;
  actor_id?: string;
  idempotency_key?: string;
  metadata?: Record<string, any>;
  created_at: string;
}

export interface ConversationMember {
  id: string;
  conversation_id: string;
  user_id: string;
  role: string;
  joined_at: string;
  last_read_at?: string;
}

export interface ConversationAttachment {
  id: string;
  message_id: string;
  file_name: string;
  file_type: string;
  file_size_bytes: number;
  file_url: string;
  is_verified: boolean;
  created_at: string;
}

export interface ConversationMessage {
  id: string;
  conversation_id: string;
  sender_id: string;
  body: string;
  visibility: MessageVisibility;
  parent_id?: string;
  is_edited: boolean;
  edit_count: number;
  created_at: string;
  updated_at: string;
  attachments?: ConversationAttachment[];
}

export interface Conversation {
  id: string;
  tenant_id: string;
  title: string;
  conversation_type: ConversationType;
  entity_type?: string;
  entity_id?: string;
  created_by: string;
  is_closed: boolean;
  closed_at?: string;
  closed_by?: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ConversationDetail {
  conversation: Conversation;
  members: ConversationMember[];
  messages: ConversationMessage[];
}

export interface NotificationPreference {
  id: string;
  tenant_id: string;
  user_id: string;
  notification_type: CommunicationType;
  in_app_enabled: boolean;
  email_enabled: boolean;
  sms_enabled: boolean;
  webhook_enabled: boolean;
  push_enabled: boolean;
  quiet_hours_start?: string;
  quiet_hours_end?: string;
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface DeliveryRecord {
  id: string;
  tenant_id: string;
  notification_id?: string;
  recipient_id: string;
  channel: DeliveryChannel;
  status: DeliveryStatus;
  provider?: string;
  provider_message_id?: string;
  retry_count: number;
  max_retries: number;
  next_retry_at?: string;
  sent_at?: string;
  delivered_at?: string;
  failed_at?: string;
  error_details?: Record<string, any>;
  created_at: string;
}

export const communicationApi = {
  // Inbox API
  listInbox: (params?: {
    state?: InboxState;
    is_read?: boolean;
    is_pinned?: boolean;
    limit?: number;
    offset?: number;
  }) => {
    const query = new URLSearchParams();
    if (params?.state) query.append('state', params.state);
    if (params?.is_read !== undefined) query.append('is_read', String(params.is_read));
    if (params?.is_pinned !== undefined) query.append('is_pinned', String(params.is_pinned));
    if (params?.limit) query.append('limit', String(params.limit));
    if (params?.offset) query.append('offset', String(params.offset));
    const qs = query.toString();
    return api<InboxItem[]>(`/inbox${qs ? `?${qs}` : ''}`);
  },

  getUnreadCount: () => api<InboxUnreadCount>('/inbox/unread-count'),

  updateInboxItem: (
    itemId: string,
    payload: {
      state?: InboxState;
      is_read?: boolean;
      is_starred?: boolean;
      is_pinned?: boolean;
      snoozed_until?: string;
    }
  ) => api<InboxItem>(`/inbox/${itemId}`, { method: 'PATCH', body: JSON.stringify(payload) }),

  bulkUpdateInbox: (payload: {
    item_ids: string[];
    state?: InboxState;
    is_read?: boolean;
    is_starred?: boolean;
    is_pinned?: boolean;
    snoozed_until?: string;
  }) => api<{ updated_count: number; tenant_id: string; recipient_id: string }>('/inbox/bulk', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  }),

  // Notifications API
  listNotifications: (params?: {
    source_module?: string;
    priority?: NotificationPriority;
    limit?: number;
    offset?: number;
  }) => {
    const query = new URLSearchParams();
    if (params?.source_module) query.append('source_module', params.source_module);
    if (params?.priority) query.append('priority', params.priority);
    if (params?.limit) query.append('limit', String(params.limit));
    if (params?.offset) query.append('offset', String(params.offset));
    const qs = query.toString();
    return api<NotificationRecord[]>(`/notifications${qs ? `?${qs}` : ''}`);
  },

  createNotification: (payload: {
    notification_type: CommunicationType;
    priority?: NotificationPriority;
    title: string;
    body: string;
    source_module: string;
    source_event_id?: string;
    entity_type?: string;
    entity_id?: string;
    action_url?: string;
    recipients?: string[];
    channels?: DeliveryChannel[];
    idempotency_key?: string;
    metadata?: Record<string, any>;
  }) => api<any>('/notifications', { method: 'POST', body: JSON.stringify(payload) }),

  getNotification: (notificationId: string) =>
    api<NotificationRecord>(`/notifications/${notificationId}`),

  // Conversations API
  listConversations: (params?: {
    entity_type?: string;
    entity_id?: string;
    limit?: number;
    offset?: number;
  }) => {
    const query = new URLSearchParams();
    if (params?.entity_type) query.append('entity_type', params.entity_type);
    if (params?.entity_id) query.append('entity_id', params.entity_id);
    if (params?.limit) query.append('limit', String(params.limit));
    if (params?.offset) query.append('offset', String(params.offset));
    const qs = query.toString();
    return api<Conversation[]>(`/conversations${qs ? `?${qs}` : ''}`);
  },

  createConversation: (payload: {
    title: string;
    conversation_type: ConversationType;
    entity_type?: string;
    entity_id?: string;
    initial_members?: string[];
    metadata?: Record<string, any>;
  }) => api<any>('/conversations', { method: 'POST', body: JSON.stringify(payload) }),

  getConversation: (conversationId: string) =>
    api<ConversationDetail>(`/conversations/${conversationId}`),

  postMessage: (
    conversationId: string,
    payload: {
      body: string;
      visibility?: MessageVisibility;
      parent_id?: string;
      attachments?: Array<{
        file_name: string;
        file_type: string;
        file_size_bytes: number;
        file_url: string;
      }>;
      metadata?: Record<string, any>;
    }
  ) => api<any>(`/conversations/${conversationId}/messages`, {
    method: 'POST',
    body: JSON.stringify(payload),
  }),

  editMessage: (
    messageId: string,
    payload: {
      new_body: string;
      edit_reason?: string;
    }
  ) => api<any>(`/conversations/messages/${messageId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  }),

  // Preferences API
  listPreferences: () => api<NotificationPreference[]>('/notification-preferences'),

  updatePreference: (payload: {
    notification_type: CommunicationType;
    in_app_enabled?: boolean;
    email_enabled?: boolean;
    sms_enabled?: boolean;
    webhook_enabled?: boolean;
    push_enabled?: boolean;
    quiet_hours_start?: string;
    quiet_hours_end?: string;
    timezone?: string;
  }) => api<NotificationPreference>('/notification-preferences', {
    method: 'PUT',
    body: JSON.stringify(payload),
  }),

  // Delivery Audit API
  listDeliveries: (params?: {
    status?: DeliveryStatus;
    channel?: DeliveryChannel;
    limit?: number;
    offset?: number;
  }) => {
    const query = new URLSearchParams();
    if (params?.status) query.append('status', params.status);
    if (params?.channel) query.append('channel', params.channel);
    if (params?.limit) query.append('limit', String(params.limit));
    if (params?.offset) query.append('offset', String(params.offset));
    const qs = query.toString();
    return api<DeliveryRecord[]>(`/communication/deliveries${qs ? `?${qs}` : ''}`);
  },

  retryDelivery: (deliveryId: string) =>
    api<any>('/communication/deliveries/retry', {
      method: 'POST',
      body: JSON.stringify({ delivery_id: deliveryId }),
    }),
};
