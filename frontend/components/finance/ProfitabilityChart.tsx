'use client';

import React from 'react';
import { ProjectProfitabilityAnalysis } from '@/lib/api/finance';

export function ProfitabilityChart({ analysis }: { analysis: ProjectProfitabilityAnalysis }) {
  const summary = analysis.financial_summary;
  const costs = analysis.cost_breakdown;
  const metrics = analysis.profitability_metrics;
  const health = analysis.commercial_health;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6 text-slate-100">
      {/* Header & Health Badge */}
      <div className="flex justify-between items-center pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white">Project Profitability & Commercial Health</h2>
          <p className="text-xs text-slate-400 mt-1">Project ID: {analysis.project_id}</p>
        </div>
        {health && (
          <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
            health.status === 'highly_profitable' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
            health.status === 'profitable' ? 'bg-teal-950 text-teal-300 border border-teal-800' :
            health.status === 'at_risk' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
            'bg-rose-950 text-rose-300 border border-rose-800'
          }`}>
            {health.badge} ({health.status.replace('_', ' ')})
          </span>
        )}
      </div>

      {/* Margins Summary Grid */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/50">
            <span className="text-xs text-slate-400 uppercase">Estimated Margin</span>
            <div className="text-2xl font-bold text-white mt-1">{metrics.estimated_margin_pct}%</div>
            <span className="text-xs text-slate-500 mt-1 block">${parseFloat(metrics.estimated_gross_profit).toFixed(2)} target profit</span>
          </div>
          <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/50">
            <span className="text-xs text-slate-400 uppercase">Invoiced Margin</span>
            <div className="text-2xl font-bold text-cyan-400 mt-1">{metrics.invoiced_margin_pct}%</div>
            <span className="text-xs text-slate-500 mt-1 block">${parseFloat(metrics.invoiced_gross_profit).toFixed(2)} invoiced profit</span>
          </div>
          <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/50">
            <span className="text-xs text-slate-400 uppercase">Realized Margin</span>
            <div className="text-2xl font-bold text-emerald-400 mt-1">{metrics.realized_margin_pct}%</div>
            <span className="text-xs text-slate-500 mt-1 block">${parseFloat(metrics.realized_gross_profit).toFixed(2)} cash profit</span>
          </div>
        </div>
      )}

      {/* Cost Rollup Breakdown */}
      {costs && (
        <div className="space-y-3">
          <h3 className="text-sm font-semibold uppercase text-slate-400 tracking-wider">Direct Cost Rollup</h3>
          <div className="bg-slate-800/40 rounded-xl p-4 border border-slate-800 divide-y divide-slate-800 text-sm">
            <div className="flex justify-between py-2">
              <span className="text-slate-400">Direct Labor ({costs.labor_hours_logged} hrs)</span>
              <span className="font-mono text-white">${parseFloat(costs.direct_labor_cost).toFixed(2)}</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-400">AI Tokens & Inference</span>
              <span className="font-mono text-white">${parseFloat(costs.ai_token_cost).toFixed(2)}</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-400">Infrastructure & Hosting</span>
              <span className="font-mono text-white">${parseFloat(costs.infrastructure_cost).toFixed(2)}</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-400">Subcontractors & Other</span>
              <span className="font-mono text-white">${(parseFloat(costs.subcontractor_cost) + parseFloat(costs.other_expenses)).toFixed(2)}</span>
            </div>
            <div className="flex justify-between py-2 font-bold text-base border-t border-slate-700">
              <span className="text-white">Actual Total Cost</span>
              <span className="font-mono text-rose-400">${parseFloat(costs.actual_total_cost).toFixed(2)}</span>
            </div>
          </div>
        </div>
      )}

      {/* AI Advisory Insights */}
      {analysis.agent_insights && analysis.agent_insights.length > 0 && (
        <div className="p-4 bg-indigo-950/40 border border-indigo-800/80 rounded-xl space-y-2">
          <h4 className="text-xs font-bold uppercase text-indigo-400 flex items-center gap-1.5">
            <span>🧠</span> Financial Intelligence Advisory
          </h4>
          <ul className="text-xs text-indigo-200 space-y-1 list-disc list-inside">
            {analysis.agent_insights.map((insight, idx) => (
              <li key={idx}>{insight}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
