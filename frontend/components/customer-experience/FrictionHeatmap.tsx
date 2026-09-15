'use client';

import React from 'react';
import { AlertCircle, ShieldAlert, CheckCircle, Info } from 'lucide-react';
import { FrictionPointItem } from '../../lib/api/customerExperience';

interface FrictionHeatmapProps {
  frictions: FrictionPointItem[];
}

export const FrictionHeatmap: React.FC<FrictionHeatmapProps> = ({ frictions }) => {
  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case 'critical':
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 uppercase font-semibold">Critical</span>;
      case 'high':
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase font-semibold">High</span>;
      case 'medium':
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 uppercase font-semibold">Medium</span>;
      default:
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-500/10 text-slate-400 border border-slate-500/20 uppercase font-semibold">Low</span>;
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <AlertCircle className="h-4 w-4 text-rose-400" />
          Friction Engine & Bottleneck Points
        </h3>
        <span className="text-xs text-slate-400 font-mono">Open Frictions: {frictions.length}</span>
      </div>

      {frictions.length === 0 ? (
        <div className="text-center py-6 text-slate-400 text-xs">Zero friction points detected. Smooth journey execution.</div>
      ) : (
        <div className="space-y-2.5">
          {frictions.map((f) => (
            <div key={f.id} className="p-3 rounded-lg border border-slate-800/80 bg-slate-800/30 space-y-1.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono uppercase text-indigo-400 bg-indigo-500/10 px-1.5 py-0.5 rounded">
                    {f.stage}
                  </span>
                  <span className="text-xs font-semibold text-slate-200 capitalize">
                    {f.friction_type.replace('_', ' ')}
                  </span>
                </div>
                {getSeverityBadge(f.severity)}
              </div>
              <p className="text-xs text-slate-300">{f.description}</p>
              <div className="flex items-center justify-between pt-1 text-[11px] text-slate-400 border-t border-slate-800/50">
                <span>Impact: {f.customer_impact}</span>
                <span className="font-mono">Confidence: {Math.round(f.confidence * 100)}%</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
