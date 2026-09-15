"use client";

import React from "react";
import { ContentAsset, ContentGap } from "@/lib/api/marketing";

interface Props {
  content: ContentAsset[];
  gaps: ContentGap[];
}

export const ContentCommandCenter: React.FC<Props> = ({ content, gaps }) => {
  return (
    <div className="space-y-6">
      {/* High-Priority Content Gaps */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-200">High-Priority Content Gaps (Demand Driven)</h3>
            <p className="text-xs text-slate-400 mt-0.5">Identified missing content across Buyer Journey × Revenue Potential</p>
          </div>
          <span className="text-xs bg-amber-950 text-amber-400 border border-amber-800 px-2 py-0.5 rounded-full">
            {gaps.length} Actionable Gaps
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {gaps.map((gap) => (
            <div key={gap.id} className="bg-slate-800/40 border border-amber-500/20 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[10px] bg-indigo-950 text-indigo-400 border border-indigo-800 px-2 py-0.5 rounded font-mono">
                    {gap.journey_stage}
                  </span>
                  <h4 className="text-sm font-medium text-slate-100 mt-2">{gap.topic}</h4>
                </div>
                <div className="text-right">
                  <div className="text-xs font-semibold text-emerald-400">+${gap.revenue_potential_usd.toLocaleString()}</div>
                  <span className="text-[10px] text-slate-400">Est. Pipeline</span>
                </div>
              </div>

              <div className="flex items-center justify-between mt-4 pt-3 border-t border-slate-700/40 text-xs">
                <span className="text-slate-400">Audience: <strong className="text-slate-200">{gap.target_audience}</strong></span>
                <span className="text-amber-400 font-medium">Priority: {gap.priority_score}/10</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Content Asset Inventory & Verified Claims */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-slate-200">Content Inventory & Governance State</h3>
          <span className="text-xs bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-full font-mono">
            {content.length} Published Assets
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-800/60 text-slate-400 uppercase text-[10px] tracking-wider">
              <tr>
                <th className="p-3">Title</th>
                <th className="p-3">Type</th>
                <th className="p-3">Journey Stage</th>
                <th className="p-3">Version</th>
                <th className="p-3">Governance Status</th>
                <th className="p-3">Primary CTA</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {content.map((item) => (
                <tr key={item.id} className="hover:bg-slate-800/30 transition">
                  <td className="p-3 font-medium text-slate-100">{item.title}</td>
                  <td className="p-3">
                    <span className="bg-slate-800 text-slate-300 px-2 py-0.5 rounded text-[10px]">
                      {item.content_type}
                    </span>
                  </td>
                  <td className="p-3 text-cyan-400">{item.journey_stage}</td>
                  <td className="p-3 font-mono text-slate-400">v{item.current_version}</td>
                  <td className="p-3">
                    <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded text-[10px] font-medium">
                      {item.status}
                    </span>
                  </td>
                  <td className="p-3 text-slate-400">{item.primary_cta || "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
