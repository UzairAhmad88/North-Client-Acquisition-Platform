'use client';

import React from 'react';
import { Target, Compass, Sparkles, TrendingUp, CheckCircle2 } from 'lucide-react';
import { ProductObjective, ProductMetric } from '../../lib/api/productManagement';

interface VisionStrategyPanelProps {
  vision: any;
  objectives: ProductObjective[];
  metrics: ProductMetric[];
}

export const VisionStrategyPanel: React.FC<VisionStrategyPanelProps> = ({
  vision,
  objectives,
  metrics,
}) => {
  const northStar = metrics.find((m) => m.is_north_star) || metrics[0];

  return (
    <div className="space-y-6">
      {/* North Star Metric Card */}
      {northStar && (
        <div className="rounded-xl border border-indigo-500/30 bg-gradient-to-r from-indigo-950/40 via-purple-950/20 to-slate-900/60 p-5 backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="h-4 w-4 text-indigo-400" />
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-bold uppercase tracking-wider">
              North Star Metric
            </span>
          </div>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h3 className="text-lg font-bold text-white">{northStar.name}</h3>
              <p className="text-xs text-slate-300 mt-0.5">{northStar.definition}</p>
            </div>
            <div className="flex items-baseline gap-3 bg-slate-950/40 px-4 py-2.5 rounded-lg border border-slate-800">
              <span className="text-2xl font-black text-indigo-400">{northStar.current_value}</span>
              {northStar.target_value && (
                <span className="text-xs text-slate-400">Target: {northStar.target_value}</span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Vision Statement Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center gap-2 mb-3">
            <Compass className="h-4 w-4 text-cyan-400" />
            <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Value Proposition</h4>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/40 p-3 rounded-lg border border-slate-800">
            {vision?.value_proposition || 'Empowers cross-functional teams with continuous delivery intelligence, unified PRD traceability, and governed release gates.'}
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center gap-2 mb-3">
            <Target className="h-4 w-4 text-emerald-400" />
            <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Target Customer & Problem</h4>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/40 p-3 rounded-lg border border-slate-800">
            {vision?.problem_statement || 'Enterprises suffer from fragmented roadmaps, disconnected PRDs, orphaned requirements, and brittle manual release governance.'}
          </p>
        </div>
      </div>

      {/* Objectives / OKRs */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
        <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider mb-3 flex items-center gap-2">
          <TrendingUp className="h-4 w-4 text-indigo-400" />
          Strategic Objectives & Key Results ({objectives.length})
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {objectives.map((obj) => (
            <div key={obj.id} className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
              <div className="flex items-center justify-between text-xs font-bold text-white mb-1">
                <span>{obj.name}</span>
                <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">
                  {obj.status}
                </span>
              </div>
              <div className="text-[11px] text-slate-400 flex items-center justify-between mt-2">
                <span>Metric: {obj.metric}</span>
                <span>Target: {obj.target}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
