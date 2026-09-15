'use client';

import React, { useState } from 'react';
import { ConversationManager } from './ConversationManager';
import { DeliveryAuditExplorer } from './DeliveryAuditExplorer';
import { NotificationPreferencesManager } from './NotificationPreferencesManager';
import { RealtimeCollaborationPanel } from './RealtimeCollaborationPanel';
import { UnifiedInboxViewer } from './UnifiedInboxViewer';

export const CommunicationWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<
    'INBOX' | 'CONVERSATIONS' | 'PREFERENCES' | 'DELIVERIES' | 'REALTIME'
  >('INBOX');

  return (
    <div className="flex flex-col space-y-6 max-w-7xl mx-auto w-full p-4">
      {/* Top Banner Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center bg-slate-900/90 border border-slate-800 p-6 rounded-2xl backdrop-blur-md">
        <div>
          <div className="flex items-center space-x-3">
            <span className="text-2xl">📬</span>
            <h1 className="text-2xl font-black tracking-tight text-slate-100">
              Communication & Collaboration Hub
            </h1>
          </div>
          <p className="text-sm text-slate-400 mt-1 max-w-2xl">
            Phase 37 Unified Communication Engine: Inbox, multi-channel notifications, conversations,
            real-time presence, and audit-grade delivery tracking.
          </p>
        </div>

        {/* Workspace Navigation Tabs */}
        <div className="flex items-center space-x-1 bg-slate-950/80 p-1.5 rounded-xl border border-slate-800 mt-4 md:mt-0 overflow-x-auto">
          <button
            onClick={() => setActiveTab('INBOX')}
            className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${
              activeTab === 'INBOX'
                ? 'bg-cyan-600 text-white shadow-lg'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            📥 Inbox
          </button>
          <button
            onClick={() => setActiveTab('CONVERSATIONS')}
            className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${
              activeTab === 'CONVERSATIONS'
                ? 'bg-indigo-600 text-white shadow-lg'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            💬 Conversations
          </button>
          <button
            onClick={() => setActiveTab('PREFERENCES')}
            className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${
              activeTab === 'PREFERENCES'
                ? 'bg-emerald-600 text-white shadow-lg'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            ⚙️ Preferences
          </button>
          <button
            onClick={() => setActiveTab('DELIVERIES')}
            className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${
              activeTab === 'DELIVERIES'
                ? 'bg-orange-600 text-white shadow-lg'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            📊 Delivery Audit
          </button>
          <button
            onClick={() => setActiveTab('REALTIME')}
            className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${
              activeTab === 'REALTIME'
                ? 'bg-cyan-500 text-white shadow-lg'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            ⚡ Real-Time
          </button>
        </div>
      </div>

      {/* Main Workspace Body */}
      <div className="transition-all duration-200">
        {activeTab === 'INBOX' && <UnifiedInboxViewer />}
        {activeTab === 'CONVERSATIONS' && <ConversationManager />}
        {activeTab === 'PREFERENCES' && <NotificationPreferencesManager />}
        {activeTab === 'DELIVERIES' && <DeliveryAuditExplorer />}
        {activeTab === 'REALTIME' && <RealtimeCollaborationPanel />}
      </div>
    </div>
  );
};
