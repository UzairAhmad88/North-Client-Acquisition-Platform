'use client';

import React from 'react';
import { Layers, Building2, User, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';
import { SalesOpportunityItem } from '../../lib/api/revenueGrowth';

interface PipelineStageBoardProps {
  opportunities: SalesOpportunityItem[];
}

export const PipelineStageBoard: React.FC<PipelineStageBoardProps> = ({ opportunities }) => {
  const stages = [
    { key: 'qualified', label: 'Qualified' },
    { key: 'discovery', label: 'Discovery' },
    { key: 'solution', label: 'Solution' },
    { key: 'proposal', label: 'Proposal' },
    { key: 'negotiation', label: 'Negotiation' },
    { key: 'contract', label: 'Contract' },
  ];

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Layers className="h-4 w-4 text-indigo-400" />
            Enterprise Sales Pipeline Matrix
          </h3>
          <p className="text-xs text-slate-400">Total Active Opportunities: {opportunities.length}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {stages.map((stg) => {
          const stageOpps = opportunities.filter((o) => o.stage.toLowerCase() === stg.key);
          const stageTotal = stageOpps.reduce((sum, o) => sum + o.estimated_arr_value, 0);

          return (
            <div key={stg.key} className="p-3 rounded-lg border border-slate-800 bg-slate-950/40 space-y-3 flex flex-col">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                <span className="text-xs font-bold text-slate-200">{stg.label}</span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  {stageOpps.length}
                </span>
              </div>
              
              <div className="text-[11px] font-mono text-emerald-400">
                ${(stageTotal / 1000).toFixed(0)}k ARR
              </div>

              <div className="flex-1 space-y-2 overflow-y-auto max-h-64">
                {stageOpps.map((opp) => (
                  <div key={opp.id} className="p-2.5 rounded-lg border border-slate-800/80 bg-slate-900/80 space-y-1.5 hover:border-slate-700 transition-colors">
                    <div className="text-xs font-semibold text-slate-100 line-clamp-2">{opp.title}</div>
                    <div className="text-xs font-mono text-emerald-400 font-bold">
                      ${opp.estimated_arr_value.toLocaleString()}
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-slate-400 pt-1 border-t border-slate-800/60">
                      <span className="flex items-center gap-1">
                        <User className="h-3 w-3 text-slate-500" />
                        {opp.owner_name}
                      </span>
                      <span className="font-mono text-indigo-400">
                        {Math.round(opp.win_probability * 100)}% Win
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
