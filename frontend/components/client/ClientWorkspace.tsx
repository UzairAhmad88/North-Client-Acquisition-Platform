'use client';

import React, { useState } from 'react';
import { DeliverableReviewPanel } from './DeliverableReviewPanel';
import { ClientThreadsPanel } from './ClientThreadsPanel';
import { ClientFilesPanel } from './ClientFilesPanel';
import { ClientActionItemsPanel } from './ClientActionItemsPanel';
import {
  LayoutDashboard,
  FileCheck,
  MessageSquare,
  FolderGit2,
  UserCheck,
  ShieldCheck,
  Building2,
  Clock,
  Sparkles,
} from 'lucide-react';

interface ClientWorkspaceProps {
  projectId: string;
  projectName?: string;
  clientName?: string;
}

export const ClientWorkspace: React.FC<ClientWorkspaceProps> = ({
  projectId,
  projectName = 'Enterprise Customer Portal System',
  clientName = 'Acme Global Corp',
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'deliverables' | 'threads' | 'files' | 'actions'>(
    'overview'
  );

  // Sample deliverable data for demonstration/integration
  const sampleDeliverable = {
    id: 'deliv-001',
    title: 'Phase 27 Technical Solution & Client Portal Architecture Spec',
    currentVersion: {
      version_number: 1,
      title: 'V1.0 Client Portal Architecture Spec',
      description: 'Defines permission boundaries, cryptographic SHA-256 deliverable sign-offs, and client discussion channels.',
      content_payload: JSON.stringify(
        {
          project: projectName,
          client: clientName,
          security_policy: 'INTERNAL_ONLY by default. Explicit CLIENT_VISIBLE required.',
          approval_protocol: 'SHA-256 content hash verification on sign-off submission.',
          prohibited_ai_actions: [
            'APPROVE_DELIVERABLE',
            'APPROVE_SCOPE_CHANGE',
            'MODIFY_CONTRACT',
            'CHANGE_PRICE',
          ],
        },
        null,
        2
      ),
      created_at: new Date().toISOString(),
      status: 'PENDING_REVIEW' as const,
    },
    versionHistory: [
      {
        version_number: 1,
        title: 'V1.0 Initial Draft',
        description: 'Initial draft published for review',
        content_payload: '{}',
        created_at: new Date(Date.now() - 86400000).toISOString(),
        status: 'PENDING_REVIEW' as const,
      },
    ],
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4 sm:p-6 text-slate-100">
      {/* Workspace Top Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-blue-600/10 border border-blue-500/20 rounded-xl text-blue-400">
              <Building2 className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-2xl font-black text-white tracking-tight">{projectName}</h1>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  Active Collaboration
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Client Organization: <strong className="text-slate-200">{clientName}</strong> • Project ID: <code className="text-slate-300">{projectId}</code>
              </p>
            </div>
          </div>
        </div>

        {/* Status Pill */}
        <div className="flex items-center space-x-3 bg-slate-950 px-4 py-2.5 rounded-xl border border-slate-800">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <div className="text-xs">
            <div className="font-semibold text-slate-200">North’s Secure Client Portal</div>
            <div className="text-[10px] text-slate-400">Restricted Data Visibility Filter Active</div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-800 pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('overview')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition ${
            activeTab === 'overview'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
              : 'bg-slate-900/60 text-slate-400 hover:bg-slate-800 hover:text-white border border-slate-800'
          }`}
        >
          <LayoutDashboard className="w-4 h-4" />
          <span>Overview</span>
        </button>

        <button
          onClick={() => setActiveTab('deliverables')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition ${
            activeTab === 'deliverables'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
              : 'bg-slate-900/60 text-slate-400 hover:bg-slate-800 hover:text-white border border-slate-800'
          }`}
        >
          <FileCheck className="w-4 h-4" />
          <span>Deliverables Sign-Off</span>
        </button>

        <button
          onClick={() => setActiveTab('threads')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition ${
            activeTab === 'threads'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
              : 'bg-slate-900/60 text-slate-400 hover:bg-slate-800 hover:text-white border border-slate-800'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span>Discussions</span>
        </button>

        <button
          onClick={() => setActiveTab('files')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition ${
            activeTab === 'files'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
              : 'bg-slate-900/60 text-slate-400 hover:bg-slate-800 hover:text-white border border-slate-800'
          }`}
        >
          <FolderGit2 className="w-4 h-4" />
          <span>Files</span>
        </button>

        <button
          onClick={() => setActiveTab('actions')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition ${
            activeTab === 'actions'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
              : 'bg-slate-900/60 text-slate-400 hover:bg-slate-800 hover:text-white border border-slate-800'
          }`}
        >
          <UserCheck className="w-4 h-4" />
          <span>Action Items</span>
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-1">
              <div className="text-xs text-slate-400 flex items-center justify-between">
                <span>Deliverables Ready</span>
                <FileCheck className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-2xl font-bold text-white">1 Version</div>
              <div className="text-[11px] text-amber-400 flex items-center space-x-1">
                <Clock className="w-3 h-3" />
                <span>Requires Sign-Off</span>
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-1">
              <div className="text-xs text-slate-400 flex items-center justify-between">
                <span>Active Discussions</span>
                <MessageSquare className="w-4 h-4 text-blue-400" />
              </div>
              <div className="text-2xl font-bold text-white">3 Threads</div>
              <div className="text-[11px] text-emerald-400">All Client-Sanitized</div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-1">
              <div className="text-xs text-slate-400 flex items-center justify-between">
                <span>Published Assets</span>
                <FolderGit2 className="w-4 h-4 text-purple-400" />
              </div>
              <div className="text-2xl font-bold text-white">4 Files</div>
              <div className="text-[11px] text-slate-400">Client-Visible</div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-1">
              <div className="text-xs text-slate-400 flex items-center justify-between">
                <span>Action Checklist</span>
                <UserCheck className="w-4 h-4 text-amber-400" />
              </div>
              <div className="text-2xl font-bold text-white">2 Pending</div>
              <div className="text-[11px] text-amber-400">Inputs Needed</div>
            </div>
          </div>

          {/* Quick Deliverables Review Preview */}
          <DeliverableReviewPanel
            deliverableId={sampleDeliverable.id}
            deliverableTitle={sampleDeliverable.title}
            currentVersion={sampleDeliverable.currentVersion}
            versionHistory={sampleDeliverable.versionHistory}
          />
        </div>
      )}

      {activeTab === 'deliverables' && (
        <DeliverableReviewPanel
          deliverableId={sampleDeliverable.id}
          deliverableTitle={sampleDeliverable.title}
          currentVersion={sampleDeliverable.currentVersion}
          versionHistory={sampleDeliverable.versionHistory}
        />
      )}

      {activeTab === 'threads' && <ClientThreadsPanel projectId={projectId} />}

      {activeTab === 'files' && <ClientFilesPanel projectId={projectId} />}

      {activeTab === 'actions' && <ClientActionItemsPanel />}
    </div>
  );
};
