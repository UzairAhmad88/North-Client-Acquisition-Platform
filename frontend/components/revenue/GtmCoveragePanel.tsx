'use client';

import React from 'react';
import { Compass, Target, Building2, MapPin, CheckCircle2 } from 'lucide-react';
import { MarketCoverageItem, TargetAccountItem } from '../../lib/api/revenueGrowth';

interface GtmCoveragePanelProps {
  coverage: MarketCoverageItem[];
  accounts: TargetAccountItem[];
}

export const GtmCoveragePanel: React.FC<GtmCoveragePanelProps> = ({ coverage, accounts }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Compass className="h-4 w-4 text-cyan-400" />
          Market Coverage & Target Account Density
        </h3>
        <span className="text-xs text-slate-400 font-mono">Accounts: {accounts.length}</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {coverage.map((cov) => (
          <div key={cov.id} className="p-3.5 rounded-lg border border-slate-800/80 bg-slate-800/30 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-100">{cov.segment}</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 uppercase font-semibold">
                Coverage: {Math.round(cov.coverage_percentage * 100)}%
              </span>
            </div>
            
            <div className="flex items-center gap-1.5 text-xs text-slate-400">
              <MapPin className="h-3.5 w-3.5 text-indigo-400" />
              <span>{cov.territory}</span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-center text-[11px] pt-1">
              <div className="p-2 rounded bg-slate-900/60 border border-slate-800">
                <div className="text-slate-500 text-[10px]">Discovered</div>
                <div className="font-bold font-mono text-slate-200">{cov.accounts_discovered}</div>
              </div>
              <div className="p-2 rounded bg-slate-900/60 border border-slate-800">
                <div className="text-slate-500 text-[10px]">Qualified</div>
                <div className="font-bold font-mono text-indigo-400">{cov.qualified_accounts}</div>
              </div>
              <div className="p-2 rounded bg-slate-900/60 border border-slate-800">
                <div className="text-slate-500 text-[10px]">Won</div>
                <div className="font-bold font-mono text-emerald-400">{cov.won_accounts}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
