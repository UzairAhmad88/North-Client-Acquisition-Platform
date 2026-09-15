"use client";

import React from "react";
import { MarketingOverviewMetrics } from "@/lib/api/marketing";

interface Props {
  metrics: MarketingOverviewMetrics | null;
}

export const MarketingOverviewMetricsView: React.FC<Props> = ({ metrics }) => {
  if (!metrics) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 animate-pulse">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-28 bg-slate-800/40 rounded-xl border border-slate-700/50" />
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: "Attributed Revenue",
      value: `$${metrics.attributed_revenue_usd.toLocaleString()}`,
      subtitle: `ROAS: ${metrics.overall_roas}x`,
      color: "text-emerald-400",
      badge: "Closed Loop",
    },
    {
      title: "MQL Demand Generated",
      value: metrics.total_mql_generated.toString(),
      subtitle: `From ${metrics.total_leads_captured} captured leads`,
      color: "text-cyan-400",
      badge: `${metrics.total_campaigns_active} Active Campaigns`,
    },
    {
      title: "Average CAC",
      value: `$${Math.round(metrics.avg_cac_usd).toLocaleString()}`,
      subtitle: `Spend: $${metrics.marketing_spend_usd.toLocaleString()}`,
      color: "text-indigo-400",
      badge: "Deterministic Unit Econ",
    },
    {
      title: "Q4 P50 Demand Forecast",
      value: `${metrics.forecast_p50_leads} Leads`,
      subtitle: `${metrics.open_marketing_risks} Open Risks Tracked`,
      color: "text-amber-400",
      badge: "Monte Carlo Model",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((c, idx) => (
        <div
          key={idx}
          className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-4 shadow-sm hover:border-slate-700 transition"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">{c.title}</span>
            <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
              {c.badge}
            </span>
          </div>
          <div className={`text-2xl font-bold tracking-tight ${c.color}`}>{c.value}</div>
          <div className="text-xs text-slate-400 mt-1">{c.subtitle}</div>
        </div>
      ))}
    </div>
  );
};
