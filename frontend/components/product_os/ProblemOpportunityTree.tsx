"use client";

import React from "react";
import { ProductProblem, ProductOpportunity } from "@/lib/api/productOs";

interface Props {
  problems: ProductProblem[];
  opportunities: ProductOpportunity[];
}

export const ProblemOpportunityTreeView: React.FC<Props> = ({ problems, opportunities }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-slate-100">Opportunity Solution Tree (OST)</h2>
        <p className="text-xs text-slate-400">
          Enforces semantic separation: Customer Request ≠ Requirement ≠ Opportunity ≠ Strategic Priority
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Validated Problems */}
        <div className="space-y-3">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Validated Customer Problems ({problems.length})
          </h3>
          <div className="space-y-2">
            {problems.map((prob) => (
              <div
                key={prob.problem_id}
                className="p-3 bg-slate-950/70 border border-slate-800/80 rounded-lg space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-200">{prob.title}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-rose-950/80 text-rose-400 border border-rose-800 font-mono">
                    {prob.severity}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400">{prob.context}</p>
                <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono pt-1">
                  <span>Reported by: {prob.reported_by_count} accounts</span>
                  <span>Cost of inaction: ${prob.cost_of_inaction_usd.toLocaleString()}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Scored Opportunities */}
        <div className="space-y-3">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Scored Product Opportunities ({opportunities.length})
          </h3>
          <div className="space-y-2">
            {opportunities.map((opp) => (
              <div
                key={opp.opportunity_id}
                className="p-3 bg-slate-950/70 border border-slate-800/80 rounded-lg space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-200">{opp.title}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800 font-mono">
                    Score: {opp.score}/10
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-2 text-[10px] text-slate-400 pt-1">
                  <div>Value: {opp.customer_value_score}/10</div>
                  <div>Confidence: {opp.confidence_score}/10</div>
                  <div>Effort: {opp.effort_score}/10</div>
                </div>
                <div className="text-[10px] text-indigo-400 font-mono pt-0.5">
                  Revenue Potential: ${opp.revenue_potential_usd.toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
