'use client';

import React from 'react';
import { DollarSign, TrendingUp, ShieldCheck, ArrowRight } from 'lucide-react';

interface ChangeCommercialImpactProps {
  originalValue?: number;
  changeValue?: number;
  currency?: string;
  recommendation?: string;
}

export const ChangeCommercialImpact: React.FC<ChangeCommercialImpactProps> = ({
  originalValue = 500000.0,
  changeValue = 100000.0,
  currency = 'PKR',
  recommendation = 'ADDITIONAL_COST_REQUIRED',
}) => {
  const revisedValue = originalValue + changeValue;

  const formatMoney = (val: number) => {
    return `${currency} ${val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            <span>Commercial Delta & Value Adjustment</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Calculated via Phase 24 Cost Engine & Pricing Policy v1.0
          </p>
        </div>
        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center space-x-1">
          <TrendingUp className="w-3.5 h-3.5" />
          <span>{recommendation}</span>
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs text-slate-400">Committed Baseline Value</span>
          <div className="text-xl font-bold text-slate-200">{formatMoney(originalValue)}</div>
        </div>

        <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs text-slate-400">Change Proposal Adjustment</span>
          <div className="text-xl font-bold text-emerald-400">+{formatMoney(changeValue)}</div>
        </div>

        <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs text-slate-400">Revised Project Value</span>
          <div className="text-xl font-bold text-white">{formatMoney(revisedValue)}</div>
        </div>
      </div>

      <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 flex items-start space-x-3 text-xs text-slate-400">
        <ShieldCheck className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-200 block font-semibold">Pricing Policy Integrity Safeguard:</strong>
          Internal labor costs, hourly developer margins, and raw engineering multipliers are strictly protected. Only client-safe commercial totals are displayed.
        </div>
      </div>
    </div>
  );
};
