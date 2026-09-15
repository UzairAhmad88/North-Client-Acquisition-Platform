'use client';

import React from 'react';
import { ClientHealthScore } from '@/lib/api/customer_success';

interface ClientHealthBreakdownProps {
  healthScore?: ClientHealthScore | null;
}

export function ClientHealthBreakdown({ healthScore }: ClientHealthBreakdownProps) {
  if (!healthScore) {
    return (
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl text-center text-slate-500">
        No calibrated health score recorded for this client.
      </div>
    );
  }

  const scoreNum = parseFloat(healthScore.overall_score || healthScore.composite_score || '0');
  const band = healthScore.health_band || 'INSUFFICIENT_DATA';

  const getBandBadge = (b: string) => {
    switch (b) {
      case 'EXCELLENT':
      case 'HEALTHY':
      case 'GOOD':
        return <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-full text-xs font-semibold">HEALTHY</span>;
      case 'STABLE':
        return <span className="px-3 py-1 bg-blue-500/10 border border-blue-500/30 text-blue-400 rounded-full text-xs font-semibold">STABLE</span>;
      case 'WATCH':
        return <span className="px-3 py-1 bg-amber-500/10 border border-amber-500/30 text-amber-400 rounded-full text-xs font-semibold">WATCH</span>;
      case 'AT_RISK':
      case 'CRITICAL':
        return <span className="px-3 py-1 bg-rose-500/10 border border-rose-500/30 text-rose-400 rounded-full text-xs font-semibold">AT RISK</span>;
      default:
        return <span className="px-3 py-1 bg-slate-500/10 border border-slate-500/30 text-slate-400 rounded-full text-xs font-semibold">INSUFFICIENT DATA</span>;
    }
  };

  const getTrendIcon = (t: string) => {
    if (t === 'IMPROVING') return <span className="text-emerald-400 flex items-center gap-1 text-xs">▲ Improving</span>;
    if (t === 'DECLINING') return <span className="text-rose-400 flex items-center gap-1 text-xs">▼ Declining</span>;
    return <span className="text-slate-400 flex items-center gap-1 text-xs">● Stable</span>;
  };

  const factors = [
    { name: 'Engagement & Collaboration', score: healthScore.engagement_score, weight: '15%' },
    { name: 'Project Delivery & Milestones', score: healthScore.project_score || healthScore.project_health_score, weight: '20%' },
    { name: 'Support SLA & Resolution', score: healthScore.support_score || healthScore.support_satisfaction_score, weight: '10%' },
    { name: 'Financial Operations & Payments', score: healthScore.finance_score || healthScore.financial_health_score, weight: '15%' },
    { name: 'CSAT / Satisfaction Sentiment', score: healthScore.satisfaction_score || healthScore.support_satisfaction_score, weight: '20%' },
    { name: 'Relationship & Stakeholders', score: healthScore.relationship_score || healthScore.relationship_health_score, weight: '10%' },
    { name: 'Strategic Goal Progress', score: healthScore.goal_score || healthScore.goal_progress_score, weight: '10%' },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h3 className="text-lg font-bold text-white">Client Health Score Breakdown</h3>
            {getBandBadge(band)}
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Multi-factor deterministic scoring with missing data safety protection.
          </p>
        </div>
        <div className="flex items-center gap-6">
          <div className="text-right">
            <div className="text-3xl font-extrabold text-white">{scoreNum.toFixed(1)}<span className="text-sm font-normal text-slate-400">/100</span></div>
            <div className="flex items-center justify-end gap-2 mt-1">
              {getTrendIcon(healthScore.trend || 'STABLE')}
              <span className="text-xs text-slate-500">| Confidence: {healthScore.confidence || healthScore.confidence_score || 'HIGH'}</span>
            </div>
          </div>
        </div>
      </div>

      {healthScore.explanation || healthScore.explanation_summary ? (
        <div className="p-3.5 bg-slate-950/60 border border-slate-800/80 rounded-xl text-xs text-slate-300">
          <span className="font-semibold text-slate-200">AI Diagnostic Summary: </span>
          {healthScore.explanation || healthScore.explanation_summary}
        </div>
      ) : null}

      {/* Factor Progress Bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {factors.map((f, i) => {
          const val = f.score ? parseFloat(f.score) : null;
          return (
            <div key={i} className="p-3.5 bg-slate-950/40 border border-slate-800/50 rounded-xl space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-medium text-slate-300">{f.name}</span>
                <span className="text-slate-400 font-mono">
                  {val !== null ? `${val.toFixed(0)}/100` : <span className="text-slate-600 italic">No Data</span>}
                  <span className="text-slate-500 text-[10px] ml-1">({f.weight})</span>
                </span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                <div
                  className={`h-2 rounded-full transition-all duration-500 ${
                    val === null
                      ? 'w-0'
                      : val >= 80
                      ? 'bg-emerald-500'
                      : val >= 60
                      ? 'bg-blue-500'
                      : val >= 40
                      ? 'bg-amber-500'
                      : 'bg-rose-500'
                  }`}
                  style={{ width: val !== null ? `${Math.min(100, Math.max(0, val))}%` : '0%' }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
