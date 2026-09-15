'use client';

import React from 'react';
import { ClientOpportunity } from '@/lib/api/customer_success';

interface ClientOpportunitiesProps {
  opportunities: ClientOpportunity[];
}

export function ClientOpportunities({ opportunities }: ClientOpportunitiesProps) {
  if (!opportunities || opportunities.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl text-center text-slate-500">
        No expansion opportunities currently identified.
      </div>
    );
  }

  const getTypeBadge = (type: string) => {
    switch (type.toUpperCase()) {
      case 'EXPANSION':
        return <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded text-xs font-semibold">EXPANSION</span>;
      case 'CROSS_SELL':
        return <span className="px-2 py-0.5 bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 rounded text-xs font-semibold">CROSS-SELL</span>;
      case 'REFERRAL':
        return <span className="px-2 py-0.5 bg-purple-500/10 text-purple-400 border border-purple-500/30 rounded text-xs font-semibold">REFERRAL</span>;
      default:
        return <span className="px-2 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/30 rounded text-xs font-semibold">{type}</span>;
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white">Expansion & Growth Opportunities</h3>
          <p className="text-xs text-slate-400 mt-0.5">Value-expansion pipelines linked back to Estimation and Discovery lifecycles.</p>
        </div>
        <span className="text-xs px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full font-semibold">
          {opportunities.length} Identified
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        {opportunities.map((opp, idx) => {
          const val = parseFloat(opp.estimated_value || '0');
          return (
            <div key={opp.id || idx} className="p-4 bg-slate-950/60 border border-slate-800/80 rounded-xl space-y-2 hover:border-slate-700 transition flex flex-col justify-between">
              <div className="space-y-1.5">
                <div className="flex items-center justify-between gap-2">
                  {getTypeBadge(opp.opportunity_type)}
                  <span className="text-xs font-bold text-emerald-400 font-mono">
                    ${val.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </span>
                </div>
                <h4 className="text-sm font-semibold text-white mt-1">{opp.title}</h4>
                {opp.description ? <p className="text-xs text-slate-400 leading-relaxed">{opp.description}</p> : null}
              </div>
              <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-[11px] text-slate-500">
                <span>Confidence: {opp.confidence || opp.confidence_score || 'MEDIUM'}</span>
                <span className="capitalize font-medium text-slate-400">Status: {opp.status}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
