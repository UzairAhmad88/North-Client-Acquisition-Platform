"use client";

import React from "react";
import { AITrace, AIIncident } from "@/lib/api/governance";
import {
  Activity,
  AlertOctagon,
  CheckCircle2,
  Clock,
  DollarSign,
  Layers,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";

interface AIOperationsDashboardProps {
  traces: AITrace[];
  incidents: AIIncident[];
  loading: boolean;
  onRefresh: () => void;
}

export const AIOperationsDashboard: React.FC<AIOperationsDashboardProps> = ({
  traces,
  incidents,
  loading,
  onRefresh,
}) => {
  if (loading && traces.length === 0) {
    return (
      <div className="p-8 text-center text-zinc-400">
        <div className="inline-block animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mb-3" />
        <p>Loading AI Operations & Observability Metrics...</p>
      </div>
    );
  }

  const completedTraces = traces.filter((t) => t.status === "COMPLETED").length;
  const failedTraces = traces.filter((t) => t.status === "FAILED").length;
  const successRate = traces.length > 0 ? ((completedTraces / traces.length) * 100).toFixed(1) : "100.0";

  const totalCost = traces.reduce((acc, t) => acc + (t.estimated_cost || 0), 0);
  const totalTokens = traces.reduce((acc, t) => acc + (t.total_tokens || 0), 0);
  const avgLatency =
    traces.length > 0
      ? (traces.reduce((acc, t) => acc + (t.total_duration_ms || 0), 0) / traces.length).toFixed(0)
      : "0";

  const activeIncidents = incidents.filter((i) => i.status !== "RESOLVED").length;

  return (
    <div className="space-y-6">
      {/* 4 Metric KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400">AI Success Rate</span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
              <CheckCircle2 className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-bold text-zinc-100">{successRate}%</div>
            <div className="text-xs text-zinc-400 mt-1">
              {completedTraces} passed / {failedTraces} failed workflows
            </div>
          </div>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Estimated AI Spend</span>
            <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
              <DollarSign className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-bold text-zinc-100">${totalCost.toFixed(3)}</div>
            <div className="text-xs text-zinc-400 mt-1">{totalTokens.toLocaleString()} total tokens consumed</div>
          </div>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Average Workflow Latency</span>
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
              <Clock className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-bold text-zinc-100">{avgLatency} ms</div>
            <div className="text-xs text-zinc-400 mt-1">Across all registered agents</div>
          </div>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Active Incidents</span>
            <div className={`p-2 rounded-lg ${activeIncidents > 0 ? "bg-rose-500/10 text-rose-400" : "bg-zinc-800 text-zinc-400"}`}>
              <AlertOctagon className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-bold text-zinc-100">{activeIncidents}</div>
            <div className="text-xs text-zinc-400 mt-1">0 uncontained critical breaches</div>
          </div>
        </div>
      </div>

      {/* Recent Workflow Traces List */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-indigo-400" />
            <h3 className="text-lg font-bold text-zinc-100">Live AI Workflow Execution Streams</h3>
          </div>
          <span className="text-xs text-zinc-400">Zero Chain-of-Thought Storage Enforced</span>
        </div>

        <div className="divide-y divide-zinc-800/60 overflow-hidden">
          {traces.length === 0 ? (
            <div className="p-6 text-center text-zinc-500">No active AI traces recorded.</div>
          ) : (
            traces.slice(0, 5).map((trace) => (
              <div key={trace.id} className="py-3 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-zinc-200 text-sm">{trace.agent_id}</span>
                    <span className="px-2 py-0.5 rounded text-xs bg-zinc-800 text-zinc-300 font-mono">
                      {trace.agent_version}
                    </span>
                    <span
                      className={`px-2 py-0.5 rounded text-xs font-medium ${
                        trace.status === "COMPLETED"
                          ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                          : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                      }`}
                    >
                      {trace.status}
                    </span>
                  </div>
                  <div className="text-xs text-zinc-400 mt-0.5">
                    Workflow: <span className="font-mono">{trace.workflow_id}</span> • Model: {trace.model_id} (
                    {trace.model_version})
                  </div>
                </div>

                <div className="text-right text-xs text-zinc-400">
                  <div className="text-zinc-200 font-mono font-medium">{(trace.total_duration_ms || trace.duration_ms || 0).toFixed(0)} ms</div>
                  <div>{(trace.total_tokens || trace.tokens_used || 0)} tokens (${(trace.estimated_cost || 0).toFixed(4)})</div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default AIOperationsDashboard;
