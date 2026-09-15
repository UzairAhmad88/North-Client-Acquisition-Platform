"use client";

import React from "react";
import { AdversarialReview as AdversarialReviewType, DecisionTradeoff } from "@/lib/api/decision_rooms";
import { AlertTriangle, ShieldAlert, ArrowRightLeft, Check, X } from "lucide-react";

interface Props {
  reviews: AdversarialReviewType[];
  tradeoffs: DecisionTradeoff[];
}

export const AdversarialReviewPanel: React.FC<Props> = ({ reviews, tradeoffs }) => {
  return (
    <div className="space-y-6">
      {/* Trade-off Matrix */}
      <div>
        <h3 className="text-lg font-bold text-white mb-1 flex items-center gap-2">
          <ArrowRightLeft className="w-5 h-5 text-indigo-400" />
          Trade-off Engine
        </h3>
        <p className="text-xs text-slate-400 mb-4">Explicit analysis of gains and sacrifices when choosing between alternatives.</p>

        <div className="space-y-3">
          {tradeoffs.map((t) => (
            <div key={t.id} className="bg-slate-900 border border-slate-800 rounded-lg p-4 space-y-3">
              <p className="text-sm font-semibold text-indigo-300">
                {t.tradeoff_summary}
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                <div className="bg-emerald-950/20 border border-emerald-800/30 rounded p-3">
                  <div className="text-xs font-bold text-emerald-400 mb-1 flex items-center gap-1">
                    <Check className="w-3.5 h-3.5" /> GAINS / ADVANTAGES
                  </div>
                  <ul className="text-xs text-slate-300 space-y-1">
                    {t.gains_in_a.map((g, idx) => (
                      <li key={idx}>• {g}</li>
                    ))}
                  </ul>
                </div>

                <div className="bg-rose-950/20 border border-rose-800/30 rounded p-3">
                  <div className="text-xs font-bold text-rose-400 mb-1 flex items-center gap-1">
                    <X className="w-3.5 h-3.5" /> SACRIFICES / DRAWBACKS
                  </div>
                  <ul className="text-xs text-slate-300 space-y-1">
                    {t.sacrifices_in_a.map((s, idx) => (
                      <li key={idx}>• {s}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Adversarial Review Critiques */}
      <div>
        <h3 className="text-lg font-bold text-white mb-1 flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-amber-400" />
          Adversarial Challenge Mode & Critiques
        </h3>
        <p className="text-xs text-slate-400 mb-4">Independent red-team critique identifying weak assumptions, hidden costs, and second-order risks.</p>

        <div className="space-y-4">
          {reviews.map((rev) => (
            <div key={rev.id} className="bg-slate-900 border border-amber-500/20 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                  {rev.reviewer_role}
                </span>
              </div>

              <p className="text-slate-200 text-sm font-medium">
                "{rev.critique_summary}"
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
                {rev.weak_assumptions.length > 0 && (
                  <div className="bg-slate-800/60 rounded p-2.5">
                    <span className="font-semibold text-amber-400 block mb-1">Challenged Assumptions:</span>
                    <ul className="text-slate-300 space-y-1">
                      {rev.weak_assumptions.map((wa, idx) => (
                        <li key={idx}>• {wa}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {rev.hidden_costs.length > 0 && (
                  <div className="bg-slate-800/60 rounded p-2.5">
                    <span className="font-semibold text-rose-400 block mb-1">Hidden Costs / Frictions:</span>
                    <ul className="text-slate-300 space-y-1">
                      {rev.hidden_costs.map((hc, idx) => (
                        <li key={idx}>• {hc}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
