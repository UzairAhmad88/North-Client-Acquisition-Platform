'use client';

import React from 'react';
import { StrategicObjective } from '@/lib/api/business_os';

interface StrategyProgressProps {
  objectives: StrategicObjective[];
}

export const StrategyProgress: React.FC<StrategyProgressProps> = ({ objectives }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span>🎯</span> Strategic Objectives & OKR Progress
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Evidence-based execution tracking connecting high-level strategy to delivery milestones.
          </p>
        </div>
        <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full text-xs font-semibold">
          {objectives.length} Active Strategic OKRs
        </span>
      </div>

      <div className="space-y-6">
        {objectives.map((obj) => (
          <div key={obj.objective_id} className="bg-slate-950/60 border border-slate-800 rounded-lg p-5">
            <div className="flex items-center justify-between mb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-xs font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
                    {obj.timeframe}
                  </span>
                  <h3 className="font-bold text-slate-100 text-sm">{obj.title}</h3>
                </div>
                <p className="text-xs text-slate-400 mt-1">{obj.description}</p>
              </div>
              <div className="text-right">
                <div className="text-xl font-bold text-emerald-400">{Number(obj.overall_progress_pct).toFixed(1)}%</div>
                <span className="text-[11px] text-slate-400">Overall Progress</span>
              </div>
            </div>

            {/* Key Results */}
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 mt-4">Key Results (OKRs)</h4>
            <div className="space-y-2">
              {obj.key_results.map((kr) => (
                <div key={kr.kr_id} className="bg-slate-900 border border-slate-800/80 rounded-md p-3 text-xs">
                  <div className="flex items-center justify-between font-semibold text-slate-200 mb-1">
                    <span>{kr.title}</span>
                    <span className="text-emerald-400">{Number(kr.progress_pct).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-950 rounded-full h-1.5 mt-1 overflow-hidden">
                    <div
                      className="bg-emerald-500 h-1.5 rounded-full"
                      style={{ width: `${Math.min(100, Number(kr.progress_pct))}%` }}
                    />
                  </div>
                  <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                    <span>Current: {Number(kr.current_value).toLocaleString()} {kr.unit}</span>
                    <span>Target: {Number(kr.target_value).toLocaleString()} {kr.unit}</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Initiatives */}
            {obj.initiatives.length > 0 && (
              <div className="mt-4">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">Supporting Initiatives</h4>
                <div className="space-y-2">
                  {obj.initiatives.map((init) => (
                    <div key={init.initiative_id} className="bg-slate-900 border border-slate-800/80 rounded-md p-3 text-xs">
                      <div className="flex items-center justify-between font-semibold text-slate-200 mb-1">
                        <span>{init.title} (Owner: {init.owner})</span>
                        <span className="text-indigo-400">{Number(init.progress_pct).toFixed(1)}%</span>
                      </div>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {init.milestones.map((m: any) => (
                          <span
                            key={m.id}
                            className={`px-2 py-0.5 rounded text-[10px] font-medium border ${
                              m.completed
                                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                                : 'bg-slate-950 text-slate-400 border-slate-800'
                            }`}
                          >
                            {m.completed ? '✓' : '○'} {m.title} ({m.due_date})
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
