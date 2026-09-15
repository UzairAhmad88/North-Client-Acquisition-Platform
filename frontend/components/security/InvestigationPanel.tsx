'use client';

import React from 'react';
import { InvestigationWorkspaceData } from '@/lib/api/securityOps';
import { Compass, Clock, GitBranch, Lightbulb, ShieldCheck, X } from 'lucide-react';

interface InvestigationPanelProps {
  data: InvestigationWorkspaceData | null;
  loading: boolean;
  onClose: () => void;
}

export default function InvestigationPanel({ data, loading, onClose }: InvestigationPanelProps) {
  if (loading || !data) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 text-center text-slate-500 animate-pulse">
        Compiling investigation workspace, evidence graph, and chronological timeline...
      </div>
    );
  }

  const { incident, timeline, evidence_graph, hypotheses, recommended_actions } = data;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-bold text-indigo-700 bg-indigo-50 px-2.5 py-0.5 rounded-md border border-indigo-200">
              {incident.incident_id}
            </span>
            <span className="text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-rose-100 text-rose-800 border border-rose-200">
              {incident.severity}
            </span>
            <span className="text-xs text-slate-400">
              Status: <span className="font-semibold text-slate-700">{incident.status.toUpperCase()}</span>
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mt-2">{incident.title}</h2>
          <p className="text-xs text-slate-600 mt-1">{incident.description}</p>
        </div>

        <button
          onClick={onClose}
          className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Column 1: Chronological Timeline (Section 21) */}
        <div className="lg:col-span-1 space-y-3">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Clock className="w-4 h-4 text-indigo-600" />
            Chronological Timeline ({timeline.length})
          </h3>
          <div className="border border-slate-100 rounded-xl p-3 bg-slate-50/50 max-h-96 overflow-y-auto space-y-3">
            {timeline.map((entry, idx) => (
              <div key={entry.entry_id || idx} className="text-xs relative pl-4 border-l-2 border-indigo-200 space-y-1">
                <div className="flex justify-between items-center text-[10px] text-slate-400">
                  <span>{new Date(entry.timestamp).toLocaleTimeString()}</span>
                  <span className="font-mono text-[9px] bg-white px-1.5 py-0.2 rounded border border-slate-200">
                    {entry.type}
                  </span>
                </div>
                <div className="font-semibold text-slate-800">{entry.title}</div>
                <div className="text-slate-500 text-[11px]">{entry.description}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Column 2: Evidence Graph & Hypotheses (Sections 20 & 22) */}
        <div className="lg:col-span-2 space-y-5">
          {/* Root-Cause Hypotheses */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Lightbulb className="w-4 h-4 text-amber-500" />
              Root-Cause Hypotheses (Section 20)
            </h3>
            <div className="space-y-2.5">
              {hypotheses.map((hyp) => (
                <div key={hyp.id} className="p-4 rounded-xl border border-amber-200 bg-amber-50/40 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-xs text-amber-900">{hyp.title}</span>
                    <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 border border-amber-200">
                      {Math.round(hyp.confidence * 100)}% Confidence ({hyp.status})
                    </span>
                  </div>
                  <div className="text-xs text-slate-700">
                    <span className="font-semibold text-slate-800">Verification: </span>
                    {hyp.recommended_verification}
                  </div>
                  {hyp.supporting_evidence.length > 0 && (
                    <div className="text-[11px] text-slate-600 bg-white/70 p-2 rounded-lg border border-amber-100">
                      <span className="font-medium text-slate-700">Supporting Evidence: </span>
                      {hyp.supporting_evidence.join('; ')}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Evidence Graph Structure */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <GitBranch className="w-4 h-4 text-indigo-600" />
              Evidence Graph ({evidence_graph.node_count} Nodes, {evidence_graph.edge_count} Edges)
            </h3>
            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-3">
              <div className="flex flex-wrap gap-2">
                {evidence_graph.nodes.map((node) => (
                  <span
                    key={node.id}
                    className="text-xs px-2.5 py-1 bg-white rounded-lg border border-slate-200 font-medium text-slate-800 shadow-2xs"
                  >
                    <span className="text-[10px] uppercase text-indigo-500 font-bold mr-1">[{node.type}]</span>
                    {node.label}
                  </span>
                ))}
              </div>
              <p className="text-[11px] text-slate-500">
                Connected by proven relational edges: ACCESSES, PERFORMS, SUPPORTS, and TRIGGERS.
              </p>
            </div>
          </div>

          {/* Recommended Containment Actions */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              Recommended Containment & Remediation Actions
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5">
              {recommended_actions.map((act, idx) => (
                <div key={idx} className="p-3 bg-white rounded-xl border border-slate-200 flex flex-col justify-between shadow-2xs">
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Playbook</span>
                    <div className="text-xs font-bold text-slate-900 mt-0.5">{act.label}</div>
                    <span className="text-[10px] text-indigo-600 font-mono">{act.action}</span>
                  </div>
                  <div className="mt-2 text-[10px] text-slate-500">Risk Level: <span className="font-semibold text-slate-700">{act.risk}</span></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
