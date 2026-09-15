import React from 'react';
import { AiFactoryOverviewMetrics } from '@/lib/api/aiModelFactory';

interface Props {
  metrics: AiFactoryOverviewMetrics | null;
  loading: boolean;
}

export const AiFactoryOverviewMetricsView: React.FC<Props> = ({ metrics, loading }) => {
  if (loading || !metrics) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 animate-pulse">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-24 bg-slate-800/50 rounded-xl border border-slate-700/50" />
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: 'Production Models',
      value: `${metrics.production_models} / ${metrics.total_models}`,
      sub: `${metrics.total_projects} Active AI Projects`,
      color: 'text-indigo-400',
      bg: 'bg-indigo-500/10 border-indigo-500/20',
    },
    {
      title: 'Active Deployments',
      value: metrics.total_deployments,
      sub: 'Canary & Blue/Green Active',
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10 border-emerald-500/20',
    },
    {
      title: 'Evaluation & Prompts',
      value: `${metrics.evaluation_suites} Suites`,
      sub: `${metrics.governed_prompts} Governed Prompts`,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10 border-purple-500/20',
    },
    {
      title: 'Monthly AI FinOps Spend',
      value: `$${metrics.total_finops_cost_usd.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      sub: `${metrics.active_gpu_jobs} GPU Nodes Allocated`,
      color: 'text-cyan-400',
      bg: 'bg-cyan-500/10 border-cyan-500/20',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {cards.map((card, idx) => (
        <div key={idx} className={`p-4 rounded-xl border ${card.bg} backdrop-blur-sm`}>
          <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{card.title}</p>
          <p className={`text-2xl font-bold mt-1 ${card.color}`}>{card.value}</p>
          <p className="text-xs text-slate-500 mt-1">{card.sub}</p>
        </div>
      ))}
    </div>
  );
};
