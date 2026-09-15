'use client';

import React from 'react';
import { Gauge, Zap, FormInput, Timer, Layers } from 'lucide-react';
import { EffortRecordItem } from '../../lib/api/customerExperience';

interface CustomerEffortGaugeProps {
  effortRecords: EffortRecordItem[];
}

export const CustomerEffortGauge: React.FC<CustomerEffortGaugeProps> = ({ effortRecords }) => {
  const latest = effortRecords[0] || {
    ces_score: 1.8,
    effort_tier: 'low_effort',
    step_count: 3,
    form_count: 1,
    repeated_info_instances: 0,
    waiting_time_minutes: 15,
  };

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'low_effort':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'moderate_effort':
        return 'text-blue-400 bg-blue-500/10 border-blue-500/20';
      case 'high_effort':
        return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      default:
        return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Gauge className="h-4 w-4 text-emerald-400" />
          Customer Effort Score (CES)
        </h3>
        <span className={`text-[10px] font-mono px-2 py-0.5 rounded border uppercase font-semibold ${getTierColor(latest.effort_tier)}`}>
          {latest.effort_tier.replace('_', ' ')}
        </span>
      </div>

      <div className="flex items-center justify-between p-4 rounded-lg bg-slate-800/40 border border-slate-800/60">
        <div>
          <div className="text-2xl font-bold font-mono text-emerald-400">
            {latest.ces_score.toFixed(1)} <span className="text-xs text-slate-500 font-normal">/ 5.0</span>
          </div>
          <p className="text-xs text-slate-400">Low Effort index indicates seamless user interactions</p>
        </div>
        <Zap className="h-8 w-8 text-emerald-400/60" />
      </div>

      <div className="grid grid-cols-3 gap-2 text-center text-xs">
        <div className="p-2.5 rounded-lg bg-slate-800/20 border border-slate-800/40">
          <div className="text-slate-400 text-[11px] mb-0.5 flex items-center justify-center gap-1">
            <Layers className="h-3 w-3 text-indigo-400" /> Steps
          </div>
          <div className="font-bold font-mono text-slate-200">{latest.step_count}</div>
        </div>
        <div className="p-2.5 rounded-lg bg-slate-800/20 border border-slate-800/40">
          <div className="text-slate-400 text-[11px] mb-0.5 flex items-center justify-center gap-1">
            <FormInput className="h-3 w-3 text-cyan-400" /> Repeated Info
          </div>
          <div className="font-bold font-mono text-slate-200">{latest.repeated_info_instances}</div>
        </div>
        <div className="p-2.5 rounded-lg bg-slate-800/20 border border-slate-800/40">
          <div className="text-slate-400 text-[11px] mb-0.5 flex items-center justify-center gap-1">
            <Timer className="h-3 w-3 text-amber-400" /> Wait Mins
          </div>
          <div className="font-bold font-mono text-slate-200">{latest.waiting_time_minutes}m</div>
        </div>
      </div>
    </div>
  );
};
