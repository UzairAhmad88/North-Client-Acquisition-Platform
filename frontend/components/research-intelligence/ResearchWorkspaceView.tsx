'use client';

import React, { useState } from 'react';
import { Layers, Globe, Database, CheckCircle2, Split, FileText, Bot, ArrowLeft } from 'lucide-react';
import { WorkspaceDetail } from '../../lib/api/research_intelligence';
import { SourceExplorer } from './SourceExplorer';
import { EvidenceGroundingBoard } from './EvidenceGroundingBoard';
import { VerificationPanel } from './VerificationPanel';
import { ResearchReportViewer } from './ResearchReportViewer';
import { ResearchCopilot } from './ResearchCopilot';

interface ResearchWorkspaceViewProps {
  workspaceDetail: WorkspaceDetail;
  onBack: () => void;
}

export const ResearchWorkspaceView: React.FC<ResearchWorkspaceViewProps> = ({
  workspaceDetail,
  onBack,
}) => {
  const [activeTab, setActiveTab] = useState<'sources' | 'facts' | 'verification' | 'reports' | 'copilot'>('sources');

  const { workspace, sources, facts, claims, conflicts, reports } = workspaceDetail;

  return (
    <div className="space-y-6">
      {/* Workspace Header */}
      <div className="flex items-start justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <button
            onClick={onBack}
            className="flex items-center gap-1.5 text-xs text-indigo-400 hover:text-indigo-300 mb-2 transition-colors"
          >
            <ArrowLeft className="h-3.5 w-3.5" />
            <span>Back to All Workspaces</span>
          </button>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-semibold">
              {workspace.research_type}
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-semibold">
              {workspace.status}
            </span>
          </div>
          <h1 className="text-xl font-bold text-white">{workspace.title}</h1>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Research Target: <span className="text-slate-200">"{workspace.research_question}"</span>
          </p>
        </div>
      </div>

      {/* Sub-navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-2">
        <button
          onClick={() => setActiveTab('sources')}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'sources'
              ? 'border-indigo-500 text-white bg-slate-900/40'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Globe className="h-4 w-4 text-cyan-400" />
          Sources ({sources.length})
        </button>

        <button
          onClick={() => setActiveTab('facts')}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'facts'
              ? 'border-indigo-500 text-white bg-slate-900/40'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Database className="h-4 w-4 text-emerald-400" />
          Evidence & Facts ({facts.length})
        </button>

        <button
          onClick={() => setActiveTab('verification')}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'verification'
              ? 'border-indigo-500 text-white bg-slate-900/40'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <CheckCircle2 className="h-4 w-4 text-indigo-400" />
          Claims & Conflicts ({claims.length})
        </button>

        <button
          onClick={() => setActiveTab('reports')}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'reports'
              ? 'border-indigo-500 text-white bg-slate-900/40'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileText className="h-4 w-4 text-amber-400" />
          Reports ({reports.length})
        </button>

        <button
          onClick={() => setActiveTab('copilot')}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'copilot'
              ? 'border-indigo-500 text-white bg-slate-900/40'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Bot className="h-4 w-4 text-rose-400" />
          Research Copilot
        </button>
      </div>

      {/* Tab Panels */}
      <div>
        {activeTab === 'sources' && <SourceExplorer sources={sources} />}
        {activeTab === 'facts' && <EvidenceGroundingBoard facts={facts} />}
        {activeTab === 'verification' && <VerificationPanel claims={claims} conflicts={conflicts} />}
        {activeTab === 'reports' && (
          <div className="space-y-6">
            {reports.length === 0 ? (
              <div className="text-center py-12 rounded-xl border border-slate-800 bg-slate-900/40 text-xs text-slate-500">
                No synthesis reports generated for this workspace yet.
              </div>
            ) : (
              reports.map((rep) => <ResearchReportViewer key={rep.id} report={rep} />)
            )}
          </div>
        )}
        {activeTab === 'copilot' && <ResearchCopilot workspaceId={workspace.id} />}
      </div>
    </div>
  );
};
