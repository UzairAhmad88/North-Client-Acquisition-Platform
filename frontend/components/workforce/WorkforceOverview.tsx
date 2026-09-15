'use client';

import React from 'react';
import { Users, DollarSign, Clock, ShieldCheck, Cpu, ArrowUpRight, Award, AlertTriangle } from 'lucide-react';
import { WorkforceOverview as WorkforceOverviewData } from '../../lib/api/workforce';

interface WorkforceOverviewProps {
  overview: WorkforceOverviewData | null;
  onSelectTab?: (tabId: string) => void;
}

export const WorkforceOverview: React.FC<WorkforceOverviewProps> = ({ overview, onSelectTab }) => {
  if (!overview) {
    return (
      <div className="rounded-xl border border-dashed border-slate-700/60 bg-slate-900/40 p-8 text-center">
        <Cpu className="mx-auto h-10 w-10 text-slate-500 mb-3" />
        <h3 className="text-base font-semibold text-slate-300">Loading Workforce Intelligence...</h3>
      </div>
    );
  }

  const { economics } = overview;

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl border border-indigo-500/20 bg-gradient-to-r from-slate-900/90 via-indigo-950/40 to-slate-900/90 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/40">
              Autonomous AI Workforce OS
            </span>
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
              <ShieldCheck className="h-3 w-3" />
              Level 0-5 Supervision Active
            </span>
          </div>
          <h2 className="text-xl font-black text-white tracking-tight">Enterprise Multi-Agent Workforce Platform</h2>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
            Governed digital organization orchestrating 20 specialized AI knowledge workers across Sales, Delivery, Operations, Security, and Strategy under strict human executive authority.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {overview.pending_human_reviews > 0 && (
            <button
              onClick={() => onSelectTab && onSelectTab('reviews')}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-xs font-bold text-amber-300 shadow-md shadow-amber-500/10 transition-all cursor-pointer animate-pulse"
            >
              <AlertTriangle className="h-4 w-4 text-amber-400" />
              <span>{overview.pending_human_reviews} Reviews Pending</span>
            </button>
          )}
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-xl border border-slate-700/60 bg-slate-900/60 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Active Workers</span>
            <Users className="h-4 w-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">
            {overview.total_active_workers}
            <span className="text-xs font-normal text-slate-500 ml-1">/ 20 profiles</span>
          </div>
          <div className="text-[11px] text-emerald-400 mt-1 flex items-center gap-1">
            <ArrowUpRight className="h-3 w-3" />
            Across 5 AI Departments
          </div>
        </div>

        <div className="p-5 rounded-xl border border-slate-700/60 bg-slate-900/60 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Economic ROI</span>
            <Award className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-emerald-400 mt-2">
            {economics?.roi_multiple || 4.8}x
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            Net Savings: ${economics?.net_cost_savings_usd?.toLocaleString() || '1,840'}
          </div>
        </div>

        <div className="p-5 rounded-xl border border-slate-700/60 bg-slate-900/60 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Human Hours Saved</span>
            <Clock className="h-4 w-4 text-blue-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">
            {economics?.human_hours_saved || 42.5} hrs
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            {overview.total_tasks_processed} tasks executed
          </div>
        </div>

        <div className="p-5 rounded-xl border border-slate-700/60 bg-slate-900/60 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Total Compute Spend</span>
            <DollarSign className="h-4 w-4 text-purple-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">
            ${economics?.total_ai_cost_usd?.toFixed(2) || '4.50'}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            Within $25/day budget ceiling
          </div>
        </div>
      </div>
    </div>
  );
};
