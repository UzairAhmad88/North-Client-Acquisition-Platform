'use client';

import React, { useState, useEffect } from 'react';
import {
  Compass,
  Globe,
  Database,
  CheckCircle2,
  Bell,
  AlertTriangle,
  Plus,
  ArrowUpRight,
  TrendingUp,
  Activity,
  Layers,
  Search,
} from 'lucide-react';
import {
  ResearchOverview,
  ResearchWorkspace,
  WorkspaceDetail,
  researchIntelligenceApi,
} from '../../lib/api/research_intelligence';
import { ResearchWorkspaceView } from './ResearchWorkspaceView';
import { CompetitiveIntelligenceCard } from './CompetitiveIntelligenceCard';
import { ResearchCopilot } from './ResearchCopilot';

export const ResearchDashboard: React.FC = () => {
  const [overview, setOverview] = useState<ResearchOverview | null>(null);
  const [selectedWorkspaceId, setSelectedWorkspaceId] = useState<string | null>(null);
  const [workspaceDetail, setWorkspaceDetail] = useState<WorkspaceDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'workspaces' | 'events' | 'copilot'>('workspaces');

  // New Workspace Modal
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newQuestion, setNewQuestion] = useState('');
  const [newType, setNewType] = useState('MARKET');

  const fetchOverview = async () => {
    try {
      setLoading(true);
      const data = await researchIntelligenceApi.getOverview();
      setOverview(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load research overview');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectWorkspace = async (id: string) => {
    try {
      setLoading(true);
      const detail = await researchIntelligenceApi.getWorkspace(id);
      setWorkspaceDetail(detail);
      setSelectedWorkspaceId(id);
    } catch (err: any) {
      setError(err.message || 'Failed to load workspace details');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateWorkspace = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newQuestion.trim()) return;

    try {
      setLoading(true);
      const created = await researchIntelligenceApi.createWorkspace({
        title: newTitle,
        research_question: newQuestion,
        research_type: newType,
      });
      setShowCreateModal(false);
      setNewTitle('');
      setNewQuestion('');
      await fetchOverview();
      await handleSelectWorkspace(created.id);
    } catch (err: any) {
      setError(err.message || 'Failed to create workspace');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  if (selectedWorkspaceId && workspaceDetail) {
    return (
      <ResearchWorkspaceView
        workspaceDetail={workspaceDetail}
        onBack={() => {
          setSelectedWorkspaceId(null);
          setWorkspaceDetail(null);
          fetchOverview();
        }}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-bold">
              Phase 54
            </span>
            <span className="text-xs text-slate-400">Continuous Intelligence Engine</span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            Autonomous Research & Continuous Discovery
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Discover Broadly • Verify Carefully • Synthesize Explicitly • Track Uncertainty • Preserve Provenance
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white shadow-sm transition-all self-start sm:self-auto"
        >
          <Plus className="h-4 w-4" />
          <span>New Research Workspace</span>
        </button>
      </div>

      {/* Overview Metrics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
          <div className="text-[11px] text-slate-400 font-medium">Workspaces</div>
          <div className="text-xl font-bold font-mono text-white mt-1">
            {overview?.total_workspaces || 0}
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">
            {overview?.active_researching || 0} active researching
          </div>
        </div>

        <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
          <div className="text-[11px] text-slate-400 font-medium">Cataloged Sources</div>
          <div className="text-xl font-bold font-mono text-cyan-400 mt-1">
            {overview?.total_sources_cataloged || 0}
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">SSRF-isolated</div>
        </div>

        <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
          <div className="text-[11px] text-slate-400 font-medium">Verified Facts</div>
          <div className="text-xl font-bold font-mono text-emerald-400 mt-1">
            {overview?.verified_facts_count || 0}
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">Corroborated</div>
        </div>

        <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
          <div className="text-[11px] text-slate-400 font-medium">Watch Rules</div>
          <div className="text-xl font-bold font-mono text-indigo-400 mt-1">
            {overview?.active_monitoring_rules || 0}
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">Continuous scans</div>
        </div>

        <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
          <div className="text-[11px] text-slate-400 font-medium">24h Critical Events</div>
          <div className="text-xl font-bold font-mono text-rose-400 mt-1">
            {overview?.critical_events_24h || 0}
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">Significance high+</div>
        </div>

        <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
          <div className="text-[11px] text-slate-400 font-medium">Epistemic Trust</div>
          <div className="text-xl font-bold font-mono text-purple-400 mt-1">
            98.4%
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">Zero Hallucination</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-2">
        <button
          onClick={() => setActiveTab('workspaces')}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'workspaces'
              ? 'border-indigo-500 text-white bg-slate-900/40'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers className="h-4 w-4 text-indigo-400" />
          Research Workspaces ({overview?.recent_workspaces?.length || 0})
        </button>

        <button
          onClick={() => setActiveTab('events')}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'events'
              ? 'border-indigo-500 text-white bg-slate-900/40'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Bell className="h-4 w-4 text-amber-400" />
          Continuous Intelligence Feed ({overview?.recent_events?.length || 0})
        </button>

        <button
          onClick={() => setActiveTab('copilot')}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors ${
            activeTab === 'copilot'
              ? 'border-indigo-500 text-white bg-slate-900/40'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Search className="h-4 w-4 text-cyan-400" />
          Interactive Research Copilot
        </button>
      </div>

      {/* Tab Contents */}
      {activeTab === 'workspaces' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {(overview?.recent_workspaces || []).map((ws) => (
            <div
              key={ws.id}
              onClick={() => handleSelectWorkspace(ws.id)}
              className="group p-5 rounded-xl border border-slate-800 bg-slate-900/60 hover:border-indigo-500/50 hover:bg-slate-900/90 transition-all cursor-pointer backdrop-blur-sm"
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold uppercase">
                  {ws.research_type}
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  {ws.status}
                </span>
              </div>
              <h3 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors mb-1">
                {ws.title}
              </h3>
              <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
                "{ws.research_question}"
              </p>
              <div className="flex items-center justify-between text-[10px] text-slate-500 pt-3 border-t border-slate-800/80">
                <span>v{ws.version}.0</span>
                <span className="flex items-center gap-1 text-indigo-400 group-hover:translate-x-0.5 transition-transform font-medium">
                  Open Workspace <ArrowUpRight className="h-3 w-3" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'events' && (
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-3">
          {(overview?.recent_events || []).length === 0 ? (
            <div className="text-center py-10 text-xs text-slate-500">
              No continuous intelligence events detected in current period.
            </div>
          ) : (
            overview?.recent_events.map((evt) => (
              <div
                key={evt.id}
                className="p-3.5 rounded-lg border border-slate-800 bg-slate-950/40 flex items-start justify-between gap-4"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-bold text-white">{evt.entity_or_topic}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded border font-semibold ${
                      evt.significance === 'CRITICAL' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' : 'bg-blue-500/10 text-blue-400 border-blue-500/30'
                    }`}>
                      {evt.significance}
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono uppercase">{evt.event_type}</span>
                  </div>
                  <p className="text-xs text-slate-300">{evt.summary}</p>
                </div>
                <div className="text-[10px] text-slate-500 shrink-0 font-mono">
                  {evt.observed_at ? new Date(evt.observed_at).toLocaleTimeString() : 'Recent'}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'copilot' && <ResearchCopilot />}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-lg rounded-xl border border-slate-800 bg-slate-900 p-6 shadow-xl">
            <h2 className="text-base font-bold text-white mb-1">Create Research Workspace</h2>
            <p className="text-xs text-slate-400 mb-4">
              Define a focused research question, objective, and domain category.
            </p>

            <form onSubmit={handleCreateWorkspace} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Workspace Title
                </label>
                <input
                  type="text"
                  required
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Q4 Competitor AI Pricing Strategy"
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Research Question
                </label>
                <textarea
                  required
                  rows={3}
                  value={newQuestion}
                  onChange={(e) => setNewQuestion(e.target.value)}
                  placeholder="e.g. How are tier-1 enterprise SaaS providers pricing multi-agent workforce platforms?"
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Research Domain
                </label>
                <select
                  value={newType}
                  onChange={(e) => setNewType(e.target.value)}
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-indigo-500 focus:outline-none"
                >
                  <option value="MARKET">Market Intelligence</option>
                  <option value="COMPETITIVE">Competitive Intelligence</option>
                  <option value="TECHNOLOGY">Technology Research</option>
                  <option value="AI">AI Intelligence & Benchmarks</option>
                  <option value="SECURITY">Security Intelligence</option>
                  <option value="REGULATORY">Regulatory & Compliance</option>
                </select>
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-4 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white transition-colors"
                >
                  Launch Workspace
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
