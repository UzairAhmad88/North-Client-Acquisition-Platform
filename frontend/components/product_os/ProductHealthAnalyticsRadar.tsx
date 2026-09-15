"use client";

import React from "react";
import { ProductHealthScorecard } from "@/lib/api/productOs";

interface Props {
  scorecards: ProductHealthScorecard[];
}

export const ProductHealthAnalyticsRadarView: React.FC<Props> = ({ scorecards }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-slate-100">Composite 7-Factor Product Health</h2>
        <p className="text-xs text-slate-400">
          Evaluates Adoption (15%), Retention (20%), Reliability (20%), Sentiment (15%), Support (10%), Quality (10%), Margin (10%)
        </p>
      </div>

      <div className="space-y-4">
        {scorecards.map((sc) => (
          <div
            key={sc.scorecard_id}
            className="p-4 bg-slate-950/70 border border-slate-800/90 rounded-lg space-y-3"
          >
            <div className="flex items-center justify-between">
              <div>
                <span className="font-semibold text-sm text-slate-200">{sc.product_name}</span>
                <span className="ml-2 text-xs text-slate-500 font-mono">({sc.product_id})</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-slate-400">Score: {sc.composite_score}/100</span>
                <span
                  className={`text-[10px] px-2.5 py-0.5 rounded font-mono font-semibold ${
                    sc.health_state === "HEALTHY"
                      ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                      : sc.health_state === "WATCH"
                      ? "bg-amber-950 text-amber-400 border border-amber-800"
                      : "bg-rose-950 text-rose-400 border border-rose-800"
                  }`}
                >
                  {sc.health_state}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 text-center text-xs">
              <div className="p-2 bg-slate-900/80 rounded border border-slate-800">
                <div className="text-[10px] text-slate-400">Adoption</div>
                <div className="font-semibold text-cyan-400">{sc.breakdown.adoption}%</div>
              </div>
              <div className="p-2 bg-slate-900/80 rounded border border-slate-800">
                <div className="text-[10px] text-slate-400">Retention</div>
                <div className="font-semibold text-indigo-400">{sc.breakdown.retention}%</div>
              </div>
              <div className="p-2 bg-slate-900/80 rounded border border-slate-800">
                <div className="text-[10px] text-slate-400">Reliability</div>
                <div className="font-semibold text-emerald-400">{sc.breakdown.reliability}%</div>
              </div>
              <div className="p-2 bg-slate-900/80 rounded border border-slate-800">
                <div className="text-[10px] text-slate-400">Sentiment</div>
                <div className="font-semibold text-purple-400">{sc.breakdown.feedback_sentiment}%</div>
              </div>
              <div className="p-2 bg-slate-900/80 rounded border border-slate-800">
                <div className="text-[10px] text-slate-400">Support Eff.</div>
                <div className="font-semibold text-amber-400">{sc.breakdown.support_efficiency}%</div>
              </div>
              <div className="p-2 bg-slate-900/80 rounded border border-slate-800">
                <div className="text-[10px] text-slate-400">Quality</div>
                <div className="font-semibold text-teal-400">{sc.breakdown.quality_defect}%</div>
              </div>
              <div className="p-2 bg-slate-900/80 rounded border border-slate-800">
                <div className="text-[10px] text-slate-400">Unit Margin</div>
                <div className="font-semibold text-emerald-400">{sc.breakdown.gross_margin}%</div>
              </div>
            </div>

            {sc.risk_factors?.length > 0 && (
              <div className="pt-1 text-[11px] text-rose-400 space-y-0.5 font-mono">
                {sc.risk_factors.map((rf, idx) => (
                  <div key={idx}>⚠ {rf}</div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
