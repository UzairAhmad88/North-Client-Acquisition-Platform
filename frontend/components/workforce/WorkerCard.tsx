'use client';

import React from 'react';
import { UserCheck, Shield, Cpu, Activity, Zap, CheckCircle2 } from 'lucide-react';
import { AIWorker } from '../../lib/api/workforce';

interface WorkerCardProps {
  worker: AIWorker;
  onSelectWorker?: (workerCode: string) => void;
}

export const WorkerCard: React.FC<WorkerCardProps> = ({ worker, onSelectWorker }) => {
  const getSupervisionBadge = (level: number) => {
    switch (level) {
      case 0:
        return { label: 'L0: Deterministic', color: 'bg-slate-500/10 text-slate-300 border-slate-500/30' };
      case 1:
        return { label: 'L1: Read-Only', color: 'bg-blue-500/10 text-blue-400 border-blue-500/30' };
      case 2:
        return { label: 'L2: Draft Gen', color: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30' };
      case 3:
        return { label: 'L3: Bounded Action', color: 'bg-purple-500/10 text-purple-400 border-purple-500/30' };
      case 4:
        return { label: 'L4: Review Required', color: 'bg-amber-500/10 text-amber-400 border-amber-500/30' };
      case 5:
        return { label: 'L5: Explicit Approval', color: 'bg-rose-500/10 text-rose-400 border-rose-500/30' };
      default:
        return { label: `L${level}`, color: 'bg-slate-500/10 text-slate-400 border-slate-500/30' };
    }
  };

  const badge = getSupervisionBadge(worker.supervision_level);

  return (
    <div
      onClick={() => onSelectWorker && onSelectWorker(worker.worker_code)}
      className="flex flex-col justify-between rounded-xl border border-slate-700/60 bg-slate-900/60 p-5 backdrop-blur-sm transition-all hover:border-indigo-500/50 hover:bg-slate-900/90 hover:shadow-lg hover:shadow-indigo-500/5 cursor-pointer"
    >
      <div>
        <div className="flex items-start justify-between gap-2 mb-3">
          <div>
            <span className="text-[10px] font-mono text-indigo-400 font-bold px-2 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/20">
              {worker.worker_code}
            </span>
            <h3 className="text-sm font-bold text-white mt-1.5">{worker.name}</h3>
            <div className="text-xs text-slate-400">{worker.role}</div>
          </div>
          <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${badge.color}`}>
            {badge.label}
          </span>
        </div>

        <p className="text-xs text-slate-400 mb-4 line-clamp-2 leading-relaxed">
          {worker.description || 'Specialized AI knowledge worker operating under governed supervision boundaries.'}
        </p>

        {/* Capabilities Tags */}
        <div className="flex flex-wrap gap-1 mb-4">
          {worker.capabilities.slice(0, 4).map((cap, idx) => (
            <span
              key={idx}
              className="px-1.5 py-0.5 rounded text-[9px] font-medium bg-slate-800 text-slate-300 border border-slate-700"
            >
              {cap}
            </span>
          ))}
          {worker.capabilities.length > 4 && (
            <span className="text-[9px] text-slate-500 self-center">
              +{worker.capabilities.length - 4} more
            </span>
          )}
        </div>
      </div>

      {/* Footer Metrics */}
      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
        <div className="flex items-center gap-1">
          <Activity className="h-3 w-3 text-emerald-400" />
          <span>Grounding: {Math.round(worker.grounding_score * 100)}%</span>
        </div>
        <div>
          <span className="text-white font-semibold">{worker.total_tasks_completed}</span> tasks
        </div>
      </div>
    </div>
  );
};
