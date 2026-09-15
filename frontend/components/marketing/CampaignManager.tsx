"use client";

import React from "react";
import { MarketingCampaign } from "@/lib/api/marketing";

interface Props {
  campaigns: MarketingCampaign[];
}

export const CampaignManager: React.FC<Props> = ({ campaigns }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200">Marketing Campaigns & Multi-Channel Mix</h3>
          <p className="text-xs text-slate-400 mt-0.5">Governed stage progression and demand generation tracking</p>
        </div>
        <span className="text-xs bg-indigo-950 text-indigo-400 border border-indigo-800 px-2.5 py-0.5 rounded-full">
          {campaigns.length} Campaigns
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {campaigns.map((camp) => (
          <div key={camp.id} className="bg-slate-800/40 border border-slate-700/60 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="text-sm font-medium text-slate-100">{camp.name}</h4>
                <span className="text-[10px] text-slate-400 font-mono mt-0.5 block">Owner: {camp.owner}</span>
              </div>
              <span
                className={`text-[10px] px-2 py-0.5 rounded border font-semibold ${
                  camp.status === "ACTIVE"
                    ? "bg-emerald-950 text-emerald-400 border-emerald-800"
                    : "bg-slate-800 text-slate-300 border-slate-700"
                }`}
              >
                {camp.status}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-700/40 text-xs">
              <div>
                <span className="text-slate-400 block text-[10px]">Allocated Budget</span>
                <span className="font-semibold text-slate-200">${camp.allocated_budget_usd.toLocaleString()}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Leads / MQL</span>
                <span className="font-semibold text-cyan-400">{camp.leads_generated} / {camp.mql_generated}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Attributed Rev</span>
                <span className="font-semibold text-emerald-400">${camp.revenue_attributed_usd.toLocaleString()}</span>
              </div>
            </div>

            <div className="mt-3 flex items-center justify-between">
              <div className="flex flex-wrap gap-1">
                {camp.channels.map((chan, i) => (
                  <span key={i} className="text-[9px] bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded font-mono">
                    {chan}
                  </span>
                ))}
              </div>
              <span className="text-[10px] text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/60 font-medium">
                Governance: Approved
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
