"use client";

import React from "react";
import { MarketingRoi } from "@/lib/api/marketing";

interface Props {
  roi: MarketingRoi | null;
}

export const AttributionRoiMatrix: React.FC<Props> = ({ roi }) => {
  if (!roi) return null;

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200">Marketing Economics & Multi-Touch Attribution ({roi.period})</h3>
          <p className="text-xs text-slate-400 mt-0.5">Closed-loop ROI, unit acquisition costs, and revenue efficiency</p>
        </div>
        <span className="text-xs bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-0.5 rounded-full font-mono">
          ROAS: {roi.roas}x
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-800/40 p-4 rounded-lg border border-slate-700/60">
          <span className="text-xs text-slate-400">Total Spend</span>
          <div className="text-xl font-bold text-slate-100 mt-1">${roi.total_spend_usd.toLocaleString()}</div>
        </div>
        <div className="bg-slate-800/40 p-4 rounded-lg border border-slate-700/60">
          <span className="text-xs text-slate-400">Attributed Revenue</span>
          <div className="text-xl font-bold text-emerald-400 mt-1">${roi.total_attributed_revenue_usd.toLocaleString()}</div>
        </div>
        <div className="bg-slate-800/40 p-4 rounded-lg border border-slate-700/60">
          <span className="text-xs text-slate-400">Cost Per Lead (CPL)</span>
          <div className="text-xl font-bold text-cyan-400 mt-1">${roi.cost_per_lead_usd}</div>
        </div>
        <div className="bg-slate-800/40 p-4 rounded-lg border border-slate-700/60">
          <span className="text-xs text-slate-400">Net Marketing ROI</span>
          <div className="text-xl font-bold text-purple-400 mt-1">+{roi.roi_pct}%</div>
        </div>
      </div>

      <div className="bg-slate-800/30 rounded-lg p-4 border border-slate-700/40 text-xs space-y-2">
        <div className="flex items-center justify-between text-slate-300">
          <span>Multi-Touch Attribution Model:</span>
          <strong className="text-indigo-400">Position-Based (W-Shaped: 30% First, 40% Middle, 30% Opportunity Creation)</strong>
        </div>
        <div className="flex items-center justify-between text-slate-300">
          <span>Cost Per Qualified Lead (CPQL):</span>
          <strong className="text-slate-200">${roi.cost_per_mql_usd}</strong>
        </div>
        <div className="flex items-center justify-between text-slate-300">
          <span>Customer Acquisition Cost (CAC):</span>
          <strong className="text-slate-200">${roi.cost_per_acquisition_usd}</strong>
        </div>
      </div>
    </div>
  );
};
