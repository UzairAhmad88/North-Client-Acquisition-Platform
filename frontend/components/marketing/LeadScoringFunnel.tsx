"use client";

import React from "react";
import { MarketingLead, FunnelMetrics } from "@/lib/api/marketing";

interface Props {
  leads: MarketingLead[];
  funnel: FunnelMetrics | null;
}

export const LeadScoringFunnel: React.FC<Props> = ({ leads, funnel }) => {
  return (
    <div className="space-y-6">
      {/* Funnel Stage Conversion & Velocity */}
      {funnel && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-slate-200">Marketing Funnel & Conversion Velocity ({funnel.period})</h3>
              <p className="text-xs text-slate-400 mt-0.5">Average Funnel Velocity: {funnel.avg_funnel_velocity_days} days</p>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-6 gap-3 text-center">
            <div className="bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
              <span className="text-[10px] text-slate-400 uppercase">Visitors</span>
              <div className="text-base font-bold text-slate-200 mt-1">{funnel.visitors.toLocaleString()}</div>
            </div>
            <div className="bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
              <span className="text-[10px] text-slate-400 uppercase">Leads</span>
              <div className="text-base font-bold text-cyan-400 mt-1">{funnel.leads.toLocaleString()}</div>
            </div>
            <div className="bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
              <span className="text-[10px] text-slate-400 uppercase">MQL ({funnel.conversion_rate_lead_to_mql_pct}%)</span>
              <div className="text-base font-bold text-indigo-400 mt-1">{funnel.mql.toLocaleString()}</div>
            </div>
            <div className="bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
              <span className="text-[10px] text-slate-400 uppercase">SQL ({funnel.conversion_rate_mql_to_sql_pct}%)</span>
              <div className="text-base font-bold text-purple-400 mt-1">{funnel.sql.toLocaleString()}</div>
            </div>
            <div className="bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
              <span className="text-[10px] text-slate-400 uppercase">Opportunities</span>
              <div className="text-base font-bold text-amber-400 mt-1">{funnel.opportunities.toLocaleString()}</div>
            </div>
            <div className="bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
              <span className="text-[10px] text-slate-400 uppercase">Won ({funnel.conversion_rate_sql_to_won_pct}%)</span>
              <div className="text-base font-bold text-emerald-400 mt-1">{funnel.deals_won.toLocaleString()}</div>
            </div>
          </div>
        </div>
      )}

      {/* 3-Component Lead Scoring Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-200">Captured Leads & 3-Component Score Breakdown</h3>
            <p className="text-xs text-slate-400 mt-0.5">Fit (40%) + Engagement (35%) + Intent (25%)</p>
          </div>
          <span className="text-xs bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-full font-mono">
            {leads.length} Leads
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-800/60 text-slate-400 uppercase text-[10px] tracking-wider">
              <tr>
                <th className="p-3">Email / Company</th>
                <th className="p-3">Source Channel</th>
                <th className="p-3 text-center">Fit (40%)</th>
                <th className="p-3 text-center">Engagement (35%)</th>
                <th className="p-3 text-center">Intent (25%)</th>
                <th className="p-3 text-center">Composite Score</th>
                <th className="p-3">Qualification Stage</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {leads.map((lead) => (
                <tr key={lead.id} className="hover:bg-slate-800/30 transition">
                  <td className="p-3">
                    <div className="font-medium text-slate-100">{lead.email}</div>
                    <div className="text-[11px] text-slate-400">{lead.company_name || "Direct Inquiry"}</div>
                  </td>
                  <td className="p-3 text-slate-400">{lead.source_channel}</td>
                  <td className="p-3 text-center font-mono text-cyan-400">{lead.fit_score}</td>
                  <td className="p-3 text-center font-mono text-indigo-400">{lead.engagement_score}</td>
                  <td className="p-3 text-center font-mono text-amber-400">{lead.intent_score}</td>
                  <td className="p-3 text-center font-mono font-bold text-emerald-400">{lead.composite_lead_score}</td>
                  <td className="p-3">
                    <span className="bg-indigo-950 text-indigo-400 border border-indigo-800 px-2 py-0.5 rounded text-[10px] font-semibold">
                      {lead.qualification_stage}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
