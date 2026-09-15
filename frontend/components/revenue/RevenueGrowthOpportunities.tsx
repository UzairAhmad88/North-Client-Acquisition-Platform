'use client';

import React from 'react';
import { Sparkles, TrendingUp, ArrowUpRight, Target } from 'lucide-react';
import { GrowthOpportunityItem } from '../../lib/api/revenueGrowth';

interface RevenueGrowthOpportunitiesProps {
  opportunities: GrowthOpportunityItem[];
}

export const RevenueGrowthOpportunities: React.FC<RevenueGrowthOpportunitiesProps> = ({ opportunities }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-purple-400" />
          Revenue Growth Opportunities & Expansion Vectors
        </h3>
        <span className="text-xs text-slate-400 font-mono">Total Potential: ${(opportunities.reduce((s, o) => s + o.estimated_arr_potential_usd, 0) / 1000).toFixed(0)}k</span>
      </div>

      <div className="space-y-3">
        {opportunities.map((opp) => (
          <div key={opp.id} className="p-3.5 rounded-lg border border-slate-800/80 bg-slate-800/30 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-100">{opp.title}</span>
              <span className="text-xs font-mono font-bold text-emerald-400">
                +${(opp.estimated_arr_potential_usd / 1000).toFixed(0)}k ARR
              </span>
            </div>
            {opp.description && <p className="text-xs text-slate-400">{opp.description}</p>}
            <div className="flex justify-between items-center text-[11px] text-slate-400 pt-1 border-t border-slate-800/60">
              <span>Segment: {opp.target_segment || 'Enterprise'}</span>
              <span className="font-mono text-purple-400">Confidence: {Math.round(opp.confidence * 100)}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
