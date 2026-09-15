'use client';

import React from 'react';
import { ArrowRight, FileCheck, Layers, ShieldCheck, Sparkles } from 'lucide-react';
import { AIHandoff } from '../../lib/api/workforce';

interface HandoffPanelProps {
  handoffs: AIHandoff[];
}

export const HandoffPanel: React.FC<HandoffPanelProps> = ({ handoffs }) => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-xl border border-indigo-500/20 bg-slate-900/60 backdrop-blur-sm">
        <div>
          <div className="flex items-center gap-2">
            <Layers className="h-5 w-5 text-indigo-400" />
            <h2 className="text-lg font-bold text-white tracking-tight">Inter-Worker Structured Handoffs</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Governed artifact transfers between specialized workers. Enforces explicit evidence, assumptions, and deliverables over opaque reasoning.
          </p>
        </div>
        <div className="px-3 py-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/30 text-xs font-bold text-indigo-300">
          {handoffs.length} Audited Handoffs
        </div>
      </div>

      {/* List */}
      {handoffs.length === 0 ? (
        <div className="p-10 text-center rounded-xl border border-dashed border-slate-700/60 bg-slate-900/40 text-slate-500 text-xs">
          No inter-worker handoffs recorded in this session.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {handoffs.map((h) => (
            <div
              key={h.handoff_code}
              className="p-5 rounded-xl border border-slate-700/60 bg-slate-900/50 hover:border-indigo-500/40 transition-all space-y-3"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="font-mono text-indigo-400 font-semibold">{h.handoff_code}</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {h.status}
                </span>
              </div>

              {/* Transfer Pathway */}
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-xs">
                <div className="font-semibold text-white">{h.from_worker_code}</div>
                <ArrowRight className="h-4 w-4 text-indigo-400" />
                <div className="font-semibold text-indigo-300">{h.to_worker_code}</div>
              </div>

              <div className="text-xs text-slate-300">
                <span className="text-slate-500 font-semibold">Context: </span>
                {h.context_summary}
              </div>

              <div className="p-2.5 rounded-lg bg-indigo-950/20 border border-indigo-500/20 text-xs">
                <div className="font-semibold text-indigo-300 mb-1">Expected Next Action:</div>
                <div className="text-indigo-200/80">{h.expected_next_action}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
