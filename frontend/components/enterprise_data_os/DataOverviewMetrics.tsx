"use client";

import React from "react";
import { EnterpriseDataOverviewMetrics } from "@/lib/api/enterpriseDataOs";

interface Props {
  metrics: EnterpriseDataOverviewMetrics | null;
}

export const DataOverviewMetricsView: React.FC<Props> = ({ metrics }) => {
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
      title: "Data Quality Index",
      value: `${metrics.composite_data_quality_pct}%`,
      subtitle: "6-Dimension Quality (Completeness & Validity)",
      color: "text-emerald-400",
      badge: "Automated Checks",
    },
    {
      title: "Domains & Data Products",
      value: `${metrics.data_products_count} Gold Products`,
      subtitle: `Across ${metrics.domains_count} Business Domains · ${metrics.data_contracts_count} Contracts`,
      color: "text-cyan-400",
      badge: "SLA Compliant",
    },
    {
      title: "Lakehouse & Pipelines",
      value: `${metrics.datasets_count} Datasets`,
      subtitle: `${metrics.sources_count} Data Sources · ${metrics.pipelines_count} Active DAGs`,
      color: "text-indigo-400",
      badge: "Bronze / Silver / Gold",
    },
    {
      title: "Data FinOps Spend",
      value: `$${metrics.total_monthly_spend_usd.toLocaleString()}/mo`,
      subtitle: `${metrics.catalog_assets_count} Catalog Assets · ${metrics.semantic_metrics_count} Semantic Metrics`,
      color: "text-amber-400",
      badge: `${metrics.active_data_incidents_count} Active Incidents`,
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
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono">
              {c.badge}
            </span>
          </div>
          <div className={`text-2xl font-bold ${c.color} mb-1`}>{c.value}</div>
          <div className="text-xs text-slate-500">{c.subtitle}</div>
        </div>
      ))}
    </div>
  );
};
