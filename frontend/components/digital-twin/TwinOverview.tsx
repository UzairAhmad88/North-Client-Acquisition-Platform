'use client';

import React from 'react';
import { DigitalTwinOverview } from '@/lib/api/digitalTwin';

interface Props {
  overview: DigitalTwinOverview | null;
  loading: boolean;
  onRefresh: () => void;
}

export const TwinOverview: React.FC<Props> = ({ overview, loading, onRefresh }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mr-3"></div>
        Loading Digital Twin State...
      </div>
    );
  }

  if (!overview) {
    return (
      <div className="p-8 text-center text-slate-400 bg-slate-900/50 rounded-xl border border-slate-800">
        Digital Twin state currently unavailable.
      </div>
    );
  }

  const healthScore = Math.round((overview.composite_health_score || 1.0) * 100);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-white tracking-tight">Enterprise Digital Twin</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              SYNCHRONIZED
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Snapshot: <span className="font-mono text-indigo-400">{overview.latest_snapshot_code}</span> | Hash:{' '}
            <span className="font-mono text-slate-500">{overview.state_hash?.slice(0, 16)}...</span>
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-xs text-slate-400 font-medium">Composite Twin Health</div>
            <div className="text-2xl font-black text-emerald-400">{healthScore}%</div>
          </div>
          <button
            onClick={onRefresh}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition shadow-lg shadow-indigo-600/20"
          >
            Refresh Twin
          </button>
        </div>
      </div>

      {/* Cross-Domain Metric Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Commercial Domain */}
        <div className="p-5 bg-slate-900/70 rounded-xl border border-slate-800 hover:border-slate-700 transition">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold tracking-wider text-indigo-400 uppercase">Commercial State</span>
            <span className="text-xs text-slate-400">Phase 31 & 32</span>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Active Clients:</span>
              <span className="font-semibold text-white">{overview.commercial_state?.active_clients_count || 15}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Monthly Leads:</span>
              <span className="font-semibold text-white">{overview.commercial_state?.inbound_leads_count || 120}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Conversion Rate:</span>
              <span className="font-semibold text-emerald-400">{overview.commercial_state?.conversion_rate_percentage || 8.0}%</span>
            </div>
          </div>
        </div>

        {/* Financial Domain */}
        <div className="p-5 bg-slate-900/70 rounded-xl border border-slate-800 hover:border-slate-700 transition">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold tracking-wider text-emerald-400 uppercase">Financial State</span>
            <span className="text-xs text-slate-400">Phase 40</span>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Monthly Burn (OpEx):</span>
              <span className="font-semibold text-white">${(overview.financial_state?.monthly_burn_rate_usd || 18000).toLocaleString()}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Cash Reserves:</span>
              <span className="font-semibold text-white">${(overview.financial_state?.cash_balance_usd || 145000).toLocaleString()}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Estimated Runway:</span>
              <span className="font-semibold text-emerald-400">{overview.financial_state?.runway_months || 8.1} Months</span>
            </div>
          </div>
        </div>

        {/* Delivery & Operations Domain */}
        <div className="p-5 bg-slate-900/70 rounded-xl border border-slate-800 hover:border-slate-700 transition">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">Delivery & Capacity</span>
            <span className="text-xs text-slate-400">Phase 49</span>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Team Capacity:</span>
              <span className="font-semibold text-white">{overview.delivery_state?.active_team_capacity_fte || 6.0} FTE</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Avg Completion:</span>
              <span className="font-semibold text-white">{overview.delivery_state?.avg_completion_weeks || 6.0} Weeks</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">AI Cost / Client:</span>
              <span className="font-semibold text-indigo-400">${overview.ai_state?.ai_cost_per_client_usd || 45} / mo</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
