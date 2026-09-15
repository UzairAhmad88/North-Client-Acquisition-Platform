'use client';

import React from 'react';
import { Layers, Plus, Minus, Equal, ArrowRight } from 'lucide-react';
import { RevenueWaterfallItem } from '../../lib/api/revenueGrowth';

interface RevenueWaterfallChartProps {
  waterfall: RevenueWaterfallItem;
}

export const RevenueWaterfallChart: React.FC<RevenueWaterfallChartProps> = ({ waterfall }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Layers className="h-4 w-4 text-purple-400" />
            Authoritative ARR Revenue Waterfall
          </h3>
          <p className="text-xs text-slate-400 font-mono">Period: {waterfall.period} | NRR: {waterfall.net_retention_pct}%</p>
        </div>
        <span className="text-sm font-mono font-bold text-emerald-400">
          Ending ARR: ${(waterfall.ending_arr_usd / 1000000).toFixed(2)}M
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-6 gap-2 text-center text-xs pt-2">
        <div className="p-3 rounded-lg bg-slate-800/40 border border-slate-800/80">
          <div className="text-slate-400 text-[10px] uppercase font-semibold mb-1">Beginning ARR</div>
          <div className="text-base font-bold font-mono text-slate-200">
            ${(waterfall.beginning_arr_usd / 1000).toFixed(0)}k
          </div>
        </div>

        <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
          <div className="text-emerald-400 text-[10px] uppercase font-semibold mb-1 flex items-center justify-center gap-0.5">
            <Plus className="h-3 w-3" /> New ARR
          </div>
          <div className="text-base font-bold font-mono text-emerald-400">
            +${(waterfall.new_arr_usd / 1000).toFixed(0)}k
          </div>
        </div>

        <div className="p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
          <div className="text-cyan-400 text-[10px] uppercase font-semibold mb-1 flex items-center justify-center gap-0.5">
            <Plus className="h-3 w-3" /> Expansion
          </div>
          <div className="text-base font-bold font-mono text-cyan-400">
            +${(waterfall.expansion_arr_usd / 1000).toFixed(0)}k
          </div>
        </div>

        <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20">
          <div className="text-amber-400 text-[10px] uppercase font-semibold mb-1 flex items-center justify-center gap-0.5">
            <Minus className="h-3 w-3" /> Contraction
          </div>
          <div className="text-base font-bold font-mono text-amber-400">
            -${(waterfall.contraction_arr_usd / 1000).toFixed(0)}k
          </div>
        </div>

        <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20">
          <div className="text-rose-400 text-[10px] uppercase font-semibold mb-1 flex items-center justify-center gap-0.5">
            <Minus className="h-3 w-3" /> Churn
          </div>
          <div className="text-base font-bold font-mono text-rose-400">
            -${(waterfall.churn_arr_usd / 1000).toFixed(0)}k
          </div>
        </div>

        <div className="p-3 rounded-lg bg-indigo-500/20 border border-indigo-500/40">
          <div className="text-indigo-300 text-[10px] uppercase font-semibold mb-1 flex items-center justify-center gap-0.5">
            <Equal className="h-3 w-3" /> Ending ARR
          </div>
          <div className="text-base font-bold font-mono text-white">
            ${(waterfall.ending_arr_usd / 1000).toFixed(0)}k
          </div>
        </div>
      </div>
    </div>
  );
};
