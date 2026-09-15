'use client';

import React, { useEffect, useState } from 'react';
import {
  InboxItem,
  InboxState,
  NotificationPriority,
  communicationApi,
} from '@/lib/api/communication';

export const UnifiedInboxViewer: React.FC = () => {
  const [items, setItems] = useState<InboxItem[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState<'ALL' | 'UNREAD' | 'PINNED' | 'ARCHIVED'>('ALL');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadInbox = async () => {
    setLoading(true);
    setError(null);
    try {
      let state: InboxState | undefined = undefined;
      let isRead: boolean | undefined = undefined;
      let isPinned: boolean | undefined = undefined;

      if (activeTab === 'UNREAD') {
        isRead = false;
        state = 'ACTIVE';
      } else if (activeTab === 'PINNED') {
        isPinned = true;
      } else if (activeTab === 'ARCHIVED') {
        state = 'ARCHIVED';
      } else {
        state = 'ACTIVE';
      }

      const res = await communicationApi.listInbox({
        state,
        is_read: isRead,
        is_pinned: isPinned,
      });
      setItems(res || []);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch inbox items');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInbox();
  }, [activeTab]);

  const handleToggleSelect = (id: string) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleSelectAll = () => {
    if (selectedIds.length === items.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(items.map((i) => i.id));
    }
  };

  const handleBulkAction = async (action: 'READ' | 'ARCHIVE' | 'DELETE') => {
    if (selectedIds.length === 0) return;
    try {
      if (action === 'READ') {
        await communicationApi.bulkUpdateInbox({ item_ids: selectedIds, is_read: true });
      } else if (action === 'ARCHIVE') {
        await communicationApi.bulkUpdateInbox({ item_ids: selectedIds, state: 'ARCHIVED' });
      } else if (action === 'DELETE') {
        await communicationApi.bulkUpdateInbox({ item_ids: selectedIds, state: 'DELETED' });
      }
      setSelectedIds([]);
      loadInbox();
    } catch (err: any) {
      setError(err.message || 'Bulk operation failed');
    }
  };

  const handleTogglePin = async (item: InboxItem) => {
    try {
      await communicationApi.updateInboxItem(item.id, { is_pinned: !item.is_pinned });
      loadInbox();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleToggleStar = async (item: InboxItem) => {
    try {
      await communicationApi.updateInboxItem(item.id, { is_starred: !item.is_starred });
      loadInbox();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleMarkRead = async (item: InboxItem) => {
    try {
      await communicationApi.updateInboxItem(item.id, { is_read: true });
      loadInbox();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getPriorityBadgeClass = (priority: NotificationPriority) => {
    switch (priority) {
      case 'CRITICAL_SECURITY':
        return 'bg-red-500/20 text-red-400 border border-red-500/40 animate-pulse';
      case 'URGENT':
        return 'bg-amber-500/20 text-amber-300 border border-amber-500/40';
      case 'HIGH':
        return 'bg-orange-500/20 text-orange-300 border border-orange-500/40';
      case 'NORMAL':
        return 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
      case 'LOW':
      default:
        return 'bg-slate-700/50 text-slate-400 border border-slate-700';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
            Unified Inbox
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Aggregated notifications, conversation alerts, tasks, and system communications.
          </p>
        </div>

        {/* Tab Filters */}
        <div className="flex items-center space-x-1 bg-slate-800/80 p-1 rounded-lg border border-slate-700">
          {(['ALL', 'UNREAD', 'PINNED', 'ARCHIVED'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${
                activeTab === tab
                  ? 'bg-cyan-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-950/50 border border-red-800 rounded-lg text-red-200 text-sm">
          {error}
        </div>
      )}

      {/* Action Toolbar */}
      {selectedIds.length > 0 && (
        <div className="flex items-center justify-between bg-cyan-950/40 border border-cyan-800/50 p-3 rounded-lg">
          <span className="text-xs text-cyan-300 font-medium">
            {selectedIds.length} item(s) selected
          </span>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handleBulkAction('READ')}
              className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded border border-slate-600"
            >
              Mark Read
            </button>
            <button
              onClick={() => handleBulkAction('ARCHIVE')}
              className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded border border-slate-600"
            >
              Archive
            </button>
            <button
              onClick={() => handleBulkAction('DELETE')}
              className="px-3 py-1 bg-red-900/60 hover:bg-red-800 text-red-200 text-xs font-medium rounded border border-red-700"
            >
              Delete
            </button>
          </div>
        </div>
      )}

      {/* Inbox List */}
      <div className="space-y-2">
        {loading ? (
          <div className="text-center py-12 text-slate-500 text-sm animate-pulse">
            Loading inbox items...
          </div>
        ) : items.length === 0 ? (
          <div className="text-center py-12 text-slate-500 text-sm border border-dashed border-slate-800 rounded-lg">
            No communication items in this view.
          </div>
        ) : (
          items.map((item) => (
            <div
              key={item.id}
              className={`flex items-center justify-between p-4 rounded-lg border transition-all ${
                item.is_read
                  ? 'bg-slate-900/40 border-slate-800/60 text-slate-300'
                  : 'bg-slate-800/60 border-slate-700 text-slate-100 font-medium'
              } hover:border-cyan-600/50`}
            >
              <div className="flex items-center space-x-3 min-w-0">
                <input
                  type="checkbox"
                  checked={selectedIds.includes(item.id)}
                  onChange={() => handleToggleSelect(item.id)}
                  className="rounded border-slate-700 bg-slate-800 text-cyan-500 focus:ring-0 focus:ring-offset-0"
                />
                <button
                  onClick={() => handleToggleStar(item)}
                  className={`text-sm ${item.is_starred ? 'text-amber-400' : 'text-slate-600 hover:text-slate-400'}`}
                >
                  ★
                </button>
                <button
                  onClick={() => handleTogglePin(item)}
                  className={`text-sm ${item.is_pinned ? 'text-cyan-400' : 'text-slate-600 hover:text-slate-400'}`}
                >
                  📌
                </button>
                <div className="min-w-0">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-semibold truncate">{item.title}</span>
                    <span
                      className={`text-[10px] font-mono px-2 py-0.5 rounded-full uppercase ${getPriorityBadgeClass(
                        item.priority
                      )}`}
                    >
                      {item.priority}
                    </span>
                    <span className="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded border border-slate-700 font-mono">
                      {item.item_type}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 truncate mt-0.5">{item.summary}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3 ml-4 flex-shrink-0">
                <span className="text-[11px] text-slate-500 font-mono">
                  {new Date(item.created_at).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </span>
                {!item.is_read && (
                  <button
                    onClick={() => handleMarkRead(item)}
                    className="text-xs text-cyan-400 hover:text-cyan-300 underline"
                  >
                    Mark read
                  </button>
                )}
                {item.action_url && (
                  <a
                    href={item.action_url}
                    className="px-2.5 py-1 bg-cyan-700/40 hover:bg-cyan-600/60 text-cyan-200 text-xs rounded border border-cyan-600/50"
                  >
                    Open ↗
                  </a>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
