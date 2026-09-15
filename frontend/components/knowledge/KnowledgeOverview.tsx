'use client';

import React from 'react';
import { KnowledgeOverview } from '@/lib/api/knowledge';
import {
  Brain,
  Search,
  BookOpen,
  CheckCircle2,
  AlertOctagon,
  Sparkles,
  GitBranch,
  Clock,
  Layers,
  ShieldAlert,
} from 'lucide-react';

interface KnowledgeOverviewProps {
  overview: KnowledgeOverview | null;
  loading: boolean;
  onRefresh: () => void;
  onNavigateTab: (tab: string) => void;
}

export default function KnowledgeOverviewComponent({
  overview,
  loading,
  onRefresh,
  onNavigateTab,
}: KnowledgeOverviewProps) {
  if (loading || !overview) {
    return (
      <div className="p-8 text-center text-slate-500 animate-pulse bg-white rounded-xl border border-slate-200">
        Loading Unified Organizational Memory & Enterprise Knowledge...
      </div>
    );
  }

  const q = overview.quality_scorecard;

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 rounded-2xl shadow-sm border border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-semibold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-500/30 text-indigo-300 border border-indigo-500/40 flex items-center gap-1">
              <Brain className="w-3.5 h-3.5 text-indigo-400" />
              Phase 48 Unified Memory Core
            </span>
            <span className="text-xs text-slate-400">
              Updated {new Date(overview.timestamp).toLocaleTimeString()}
            </span>
          </div>
          <h2 className="text-2xl font-bold mt-2 text-white">Enterprise Knowledge & Organizational Memory</h2>
          <p className="text-sm text-slate-300 mt-1 max-w-2xl">
            Governed intelligence connecting 47 platform modules into an authorized, traceable knowledge graph with semantic retrieval and grounded AI memory.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-center px-4 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/15">
            <div className="text-xs text-slate-300 uppercase tracking-wider font-medium">Quality Score</div>
            <div className="text-3xl font-extrabold text-emerald-400 mt-1">
              {q?.overall_quality_score ?? 98.5}%
            </div>
          </div>
          <div className="text-center px-4 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/15">
            <div className="text-xs text-slate-300 uppercase tracking-wider font-medium">Open Conflicts</div>
            <div className={`text-3xl font-extrabold mt-1 ${overview.open_conflicts_count > 0 ? 'text-amber-400' : 'text-slate-300'}`}>
              {overview.open_conflicts_count}
            </div>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div
          onClick={() => onNavigateTab('explorer')}
          className="bg-white p-5 rounded-xl border border-slate-200 hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Total Items</span>
            <BookOpen className="w-4 h-4 text-indigo-500 group-hover:scale-110 transition-transform" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{overview.total_items}</div>
          <div className="text-xs text-slate-500 mt-1">
            {q?.metrics?.verified_count ?? 0} Authoritative / Verified
          </div>
        </div>

        <div
          onClick={() => onNavigateTab('decisions')}
          className="bg-white p-5 rounded-xl border border-slate-200 hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Decisions Logged</span>
            <Layers className="w-4 h-4 text-blue-500 group-hover:scale-110 transition-transform" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{overview.total_decisions}</div>
          <div className="text-xs text-slate-500 mt-1">Architectural & business records</div>
        </div>

        <div
          onClick={() => onNavigateTab('lessons')}
          className="bg-white p-5 rounded-xl border border-slate-200 hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Lessons Learned</span>
            <Sparkles className="w-4 h-4 text-amber-500 group-hover:scale-110 transition-transform" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{overview.total_lessons}</div>
          <div className="text-xs text-slate-500 mt-1">Retrospective operational gains</div>
        </div>

        <div
          onClick={() => onNavigateTab('context')}
          className="bg-white p-5 rounded-xl border border-slate-200 hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">AI Context Assemblies</span>
            <Brain className="w-4 h-4 text-purple-500 group-hover:scale-110 transition-transform" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{overview.recent_context_assemblies_count}</div>
          <div className="text-xs text-slate-500 mt-1">Bounded, untrusted tagged context</div>
        </div>
      </div>

      {/* Domain Breakdown & Quality Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Knowledge Domains */}
        <div className="bg-white p-6 rounded-xl border border-slate-200">
          <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4 flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-600" />
            Knowledge Domains
          </h3>
          <div className="space-y-3">
            {Object.entries(overview.domain_breakdown).map(([dom, count]) => (
              <div key={dom} className="flex items-center justify-between text-sm">
                <span className="text-slate-700 font-medium">{dom}</span>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">
                  {count} items
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Quality Dimensions */}
        <div className="bg-white p-6 rounded-xl border border-slate-200">
          <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            Knowledge Quality Dimensions
          </h3>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                <span>Completeness</span>
                <span>{q?.completeness_score ?? 100}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div className="bg-indigo-600 h-2 rounded-full" style={{ width: `${q?.completeness_score ?? 100}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                <span>Provenance Traceability</span>
                <span>{q?.provenance_score ?? 100}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${q?.provenance_score ?? 100}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                <span>Freshness & Validity</span>
                <span>{q?.freshness_score ?? 100}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-600 h-2 rounded-full" style={{ width: `${q?.freshness_score ?? 100}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                <span>Consistency (Conflict Free)</span>
                <span>{q?.consistency_score ?? 100}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div className="bg-amber-500 h-2 rounded-full" style={{ width: `${q?.consistency_score ?? 100}%` }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
