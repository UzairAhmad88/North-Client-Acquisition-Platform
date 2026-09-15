"use client";

import React from "react";
import { EngineeringOverviewMetrics } from "@/lib/api/engineeringOs";

interface Props {
  metrics: EngineeringOverviewMetrics | null;
}

export const EngineeringOverviewMetricsView: React.FC<Props> = ({ metrics }) => {
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
      title: "DORA Performance Tier",
      value: metrics.dora_metrics.dora_tier,
      subtitle: `${metrics.dora_metrics.deployment_frequency_per_day} deploys/day · ${metrics.dora_metrics.lead_time_for_changes_hours}h lead time`,
      color: "text-emerald-400",
      badge: "DORA Benchmarks",
    },
    {
      title: "Services & Reliability",
      value: `${metrics.services_count} Services`,
      subtitle: `${metrics.healthy_services_pct}% Healthy · MTTR: ${metrics.dora_metrics.time_to_restore_service_hours}h`,
      color: "text-cyan-400",
      badge: `${metrics.open_incidents_count} Open Incidents`,
    },
    {
      title: "Repositories & CI/CD",
      value: `${metrics.repositories_count} Repositories`,
      subtitle: `${metrics.open_pull_requests_count} Open PRs · ${metrics.active_pipelines_count} Pipelines`,
      color: "text-indigo-400",
      badge: "Supply Chain Vetted",
    },
    {
      title: "FinOps Spend & Tech Debt",
      value: `$${metrics.total_cloud_cost_monthly_usd.toLocaleString()}/mo`,
      subtitle: `${metrics.technical_debt_items_count} Debt Items · ${metrics.open_vulnerabilities_count} CVEs`,
      color: "text-amber-400",
      badge: `${metrics.high_risk_changes_count} High-Risk Changes`,
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
