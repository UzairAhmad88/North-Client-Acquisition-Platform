"use client";

import React from "react";
import { ProductOverviewMetrics } from "@/lib/api/productOs";

interface Props {
  metrics: ProductOverviewMetrics | null;
}

export const ProductOverviewMetricsView: React.FC<Props> = ({ metrics }) => {
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
      title: "Composite Product Health",
      value: `${metrics.composite_health_score}/100`,
      subtitle: `${metrics.portfolio_count} Products in Portfolio`,
      color: "text-emerald-400",
      badge: "7-Factor Health Engine",
    },
    {
      title: "Opportunity Pipeline",
      value: `${metrics.opportunities_pipeline_count} Active`,
      subtitle: `Backed by ${metrics.validated_problems_count} Validated Problems`,
      color: "text-cyan-400",
      badge: "OST Framework",
    },
    {
      title: "Roadmap Initiatives",
      value: `${metrics.roadmap_initiatives_count} Items`,
      subtitle: `Across ${metrics.active_roadmaps_count} Active Roadmaps`,
      color: "text-indigo-400",
      badge: "RICE / WSJF Scored",
    },
    {
      title: "Product MRR & Margin",
      value: `$${metrics.total_mrr_usd.toLocaleString()}`,
      subtitle: `${metrics.average_gross_margin_pct}% Gross Margin`,
      color: "text-amber-400",
      badge: `${metrics.open_risks_count} Governed Risks`,
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
