"use client";

import React from "react";
import { MarketingRisk, MarketingFatigue } from "@/lib/api/marketing";

interface Props {
  risks: MarketingRisk[];
  fatigue: MarketingFatigue[];
}

export const MarketingRiskFatigueRadar: React.FC<Props> = ({ risks, fatigue }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Marketing Risks */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-slate-200">Marketing & Commercial Growth Risks</h3>
          <span className="text-xs bg-rose-950 text-rose-400 border border-rose-800 px-2 py-0.5 rounded-full">
            {risks.length} Tracked
          </span>
        </div>

        <div className="space-y-3">
          {risks.map((r) => (
            <div key={r.id} className="bg-slate-800/40 border border-slate-700/60 rounded-lg p-3.5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-200">{r.risk_category}</span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded font-semibold ${
                    r.severity === "HIGH"
                      ? "bg-rose-950 text-rose-400 border border-rose-850"
                      : "bg-amber-950 text-amber-400 border border-amber-800"
                  }`}
                >
                  {r.severity}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1.5">{r.description}</p>
              <div className="mt-2 text-[11px] text-slate-300 bg-slate-900/60 p-2 rounded border border-slate-700/40">
                <strong className="text-emerald-400 font-medium">Mitigation:</strong> {r.mitigation_strategy}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Audience Communication Frequency & Fatigue */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-slate-200">Audience Frequency & Fatigue Radar</h3>
          <span className="text-xs bg-cyan-950 text-cyan-400 border border-cyan-800 px-2 py-0.5 rounded-full">
            Consent & Cadence Protection
          </span>
        </div>

        <div className="space-y-3">
          {fatigue.map((f) => (
            <div key={f.id} className="bg-slate-800/40 border border-slate-700/60 rounded-lg p-3.5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-100">{f.channel}</span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded font-mono ${
                    f.fatigue_level === "CRITICAL"
                      ? "bg-rose-950 text-rose-400 border border-rose-800"
                      : f.fatigue_level === "ELEVATED"
                      ? "bg-amber-950 text-amber-400 border border-amber-800"
                      : "bg-emerald-950 text-emerald-400 border border-emerald-800"
                  }`}
                >
                  {f.fatigue_level}
                </span>
              </div>

              <div className="grid grid-cols-3 gap-2 mt-3 text-xs text-slate-300">
                <div>
                  <span className="text-slate-400 text-[10px] block">Weekly Freq</span>
                  <span className="font-mono">{f.weekly_frequency}x/wk</span>
                </div>
                <div>
                  <span className="text-slate-400 text-[10px] block">Unsubscribe Rate</span>
                  <span className="font-mono">{f.unsubscribe_rate_pct}%</span>
                </div>
                <div>
                  <span className="text-slate-400 text-[10px] block">Engagement Decay</span>
                  <span className="font-mono text-amber-400">{f.engagement_decay_pct}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
