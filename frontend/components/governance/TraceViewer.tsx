"use client";

import React, { useState } from "react";
import { AITrace, TraceEvent } from "@/lib/api/governance";
import {
  Clock,
  Layers,
  Search,
  CheckCircle,
  AlertTriangle,
  FileCode,
  ShieldCheck,
  Zap,
} from "lucide-react";

interface TraceViewerProps {
  traces: AITrace[];
  onRefresh: () => void;
}

export const TraceViewer: React.FC<TraceViewerProps> = ({ traces, onRefresh }) => {
  const [selectedTrace, setSelectedTrace] = useState<AITrace | null>(traces.length > 0 ? traces[0] : null);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredTraces = traces.filter(
    (t) =>
      t.agent_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.workflow_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Left List */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-zinc-100 text-sm">Execution Traces</h3>
          <span className="text-xs text-zinc-500">{filteredTraces.length} recorded</span>
        </div>

        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-zinc-500" />
          <input
            type="text"
            placeholder="Search by agent or workflow..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div className="space-y-2 max-h-[550px] overflow-y-auto pr-1">
          {filteredTraces.map((t) => (
            <button
              key={t.id}
              onClick={() => setSelectedTrace(t)}
              className={`w-full text-left p-3 rounded-lg border transition ${
                selectedTrace?.id === t.id
                  ? "bg-indigo-950/40 border-indigo-500/50 text-indigo-200"
                  : "bg-zinc-950/60 border-zinc-800/80 text-zinc-400 hover:border-zinc-700"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-xs text-zinc-200">{t.agent_id}</span>
                <span
                  className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${
                    t.status === "COMPLETED"
                      ? "bg-emerald-500/10 text-emerald-400"
                      : "bg-rose-500/10 text-rose-400"
                  }`}
                >
                  {t.status}
                </span>
              </div>
              <div className="text-[11px] text-zinc-500 mt-1 font-mono truncate">{t.workflow_id}</div>
              <div className="flex items-center justify-between text-[10px] text-zinc-500 mt-2">
                <span>{t.total_duration_ms.toFixed(0)} ms</span>
                <span>{t.total_tokens} tok</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Right Span Detail */}
      <div className="lg:col-span-2 bg-zinc-900/80 border border-zinc-800 rounded-xl p-6 space-y-6">
        {selectedTrace ? (
          <>
            <div>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-bold text-zinc-100">{selectedTrace.agent_id}</h3>
                  <span className="px-2 py-0.5 rounded text-xs bg-zinc-800 text-zinc-300 font-mono">
                    {selectedTrace.agent_version}
                  </span>
                </div>
                <div className="text-xs text-zinc-400 font-mono">Trace ID: {selectedTrace.id}</div>
              </div>
              <p className="text-xs text-zinc-400">
                Workflow: <span className="font-mono text-zinc-300">{selectedTrace.workflow_id}</span> • Model:{" "}
                {selectedTrace.model_id} ({selectedTrace.model_version}) • Prompt: {selectedTrace.prompt_version}
              </p>
            </div>

            {/* Structured Spans Timeline */}
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-3 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-indigo-400" />
                Execution Spans (No Hidden Chain-of-Thought)
              </h4>

              <div className="space-y-3">
                {selectedTrace.events && selectedTrace.events.length > 0 ? (
                  selectedTrace.events.map((span, idx) => (
                    <div key={span.id || idx} className="bg-zinc-950 border border-zinc-800 rounded-lg p-3 text-xs">
                      <div className="flex items-center justify-between mb-1.5">
                        <div className="flex items-center gap-2">
                          <span className="px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-300 text-[10px] font-mono">
                            {span.span_type}
                          </span>
                          <span className="font-semibold text-zinc-200">{span.name}</span>
                        </div>
                        <span className="text-zinc-500 font-mono">{span.duration_ms.toFixed(0)} ms</span>
                      </div>

                      <div className="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-zinc-850 text-[11px]">
                        <div>
                          <span className="text-zinc-500 block mb-0.5">Input Summary:</span>
                          <pre className="text-zinc-300 bg-zinc-900 p-1.5 rounded overflow-x-auto text-[10px]">
                            {JSON.stringify(span.input_summary, null, 2)}
                          </pre>
                        </div>
                        <div>
                          <span className="text-zinc-500 block mb-0.5">Output Summary:</span>
                          <pre className="text-zinc-300 bg-zinc-900 p-1.5 rounded overflow-x-auto text-[10px]">
                            {JSON.stringify(span.output_summary, null, 2)}
                          </pre>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="p-4 bg-zinc-950/60 rounded-lg text-center text-xs text-zinc-500">
                    Spans captured and aggregated at workflow boundary.
                  </div>
                )}
              </div>
            </div>
          </>
        ) : (
          <div className="p-12 text-center text-zinc-500">Select a trace to view structured spans.</div>
        )}
      </div>
    </div>
  );
};

export default TraceViewer;
