'use client';

import React from 'react';
import { Award, AlertOctagon, CheckCircle2, MessageSquare, ShieldAlert, Cpu } from 'lucide-react';
import { AIConsensusResult } from '../../lib/api/workforce';

interface ConsensusViewProps {
  consensusResult: AIConsensusResult | null;
}

export const ConsensusView: React.FC<ConsensusViewProps> = ({ consensusResult }) => {
  if (!consensusResult) {
    return (
      <div className="p-10 text-center rounded-xl border border-dashed border-slate-700/60 bg-slate-900/40 text-slate-500 text-xs">
        <Cpu className="mx-auto h-8 w-8 text-slate-500 mb-2" />
        <span>No active multi-worker consensus evaluations. Run consensus to adjudicate high-impact findings.</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="p-5 rounded-xl border border-indigo-500/20 bg-slate-900/60 backdrop-blur-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <span className="text-[10px] font-mono text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
              {consensusResult.consensus_code}
            </span>
            <h3 className="text-base font-bold text-white mt-1">{consensusResult.topic}</h3>
          </div>
          <div className="text-right">
            <div className="text-xs text-slate-400">Consensus Score</div>
            <div className="text-xl font-black text-emerald-400">
              {Math.round(consensusResult.consensus_score * 100)}%
            </div>
          </div>
        </div>

        <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-300 leading-relaxed">
          <span className="font-semibold text-indigo-300">Synthesized Finding: </span>
          {consensusResult.synthesized_conclusion}
        </div>

        {/* Participating Workers */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="text-slate-500 font-semibold">Participating Specialists:</span>
          {consensusResult.participating_workers.map((w, idx) => (
            <span key={idx} className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 text-[11px]">
              {w}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};
