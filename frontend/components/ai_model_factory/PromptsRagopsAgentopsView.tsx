import React from 'react';
import { AiPromptItem } from '@/lib/api/aiModelFactory';

interface Props {
  prompts: AiPromptItem[];
}

export const PromptsRagopsAgentopsView: React.FC<Props> = ({ prompts }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Prompts Registry */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-100">Governed Prompt Registry</h3>
          <span className="text-xs px-2.5 py-1 rounded-full bg-purple-500/20 text-purple-300 font-mono">
            {prompts.length} Templates
          </span>
        </div>
        <div className="space-y-3">
          {prompts.map((p) => (
            <div key={p.id} className="p-3.5 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-2">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-sm font-semibold text-white">{p.name}</h4>
                  <p className="text-xs text-slate-400">{p.purpose}</p>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">
                  v{p.version}
                </span>
              </div>
              <div className="bg-slate-900/60 p-2 rounded border border-slate-800 text-[11px] font-mono text-slate-300">
                <p className="text-slate-500 text-[10px] uppercase">Template Preview:</p>
                <p className="truncate">{p.user_template}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* RAGOps & AgentOps Telemetry */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-100">RAGOps & AgentOps Telemetry</h3>
          <span className="text-xs px-2.5 py-1 rounded-full bg-cyan-500/20 text-cyan-300 font-mono">
            Live
          </span>
        </div>
        <div className="space-y-3">
          <div className="p-3.5 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-2">
            <h4 className="text-xs font-mono text-cyan-400 uppercase">RAG Pipeline Metrics (30-Day Rollup)</h4>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-900/50 p-2 rounded">
                <span className="text-slate-500 text-[10px]">Context Groundedness:</span>
                <p className="font-bold text-emerald-400">95.0%</p>
              </div>
              <div className="bg-slate-900/50 p-2 rounded">
                <span className="text-slate-500 text-[10px]">Citation Faithfulness:</span>
                <p className="font-bold text-emerald-400">98.2%</p>
              </div>
              <div className="bg-slate-900/50 p-2 rounded">
                <span className="text-slate-500 text-[10px]">Retrieval Recall:</span>
                <p className="font-bold text-slate-200">96.0%</p>
              </div>
              <div className="bg-slate-900/50 p-2 rounded">
                <span className="text-slate-500 text-[10px]">Avg Retrieval Latency:</span>
                <p className="font-bold text-slate-200">35 ms</p>
              </div>
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-2">
            <h4 className="text-xs font-mono text-indigo-400 uppercase">AgentOps Multi-Agent Accuracy</h4>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-900/50 p-2 rounded">
                <span className="text-slate-500 text-[10px]">Tool Selection Accuracy:</span>
                <p className="font-bold text-emerald-400">99.4%</p>
              </div>
              <div className="bg-slate-900/50 p-2 rounded">
                <span className="text-slate-500 text-[10px]">Human Escalation Rate:</span>
                <p className="font-bold text-slate-200">0.8%</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
