'use client';

import React from 'react';
import { Target, TrendingUp, ShieldAlert, ArrowUpRight, DollarSign, Activity } from 'lucide-react';
import { ResearchCompetitorProfile } from '../../lib/api/research_intelligence';

interface CompetitiveIntelligenceCardProps {
  competitor: ResearchCompetitorProfile;
}

export const CompetitiveIntelligenceCard: React.FC<CompetitiveIntelligenceCardProps> = ({ competitor }) => {
  const getThreatBadge = (level: string) => {
    switch (level?.toUpperCase()) {
      case 'CRITICAL':
      case 'HIGH':
        return { label: level, color: 'bg-rose-500/10 text-rose-400 border-rose-500/30' };
      case 'MEDIUM':
        return { label: 'Medium Threat', color: 'bg-amber-500/10 text-amber-400 border-amber-500/30' };
      default:
        return { label: 'Low / Emerging', color: 'bg-blue-500/10 text-blue-400 border-blue-500/30' };
    }
  };

  const threat = getThreatBadge(competitor.threat_level || 'MEDIUM');

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm hover:border-slate-700 transition-all">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
            <Target className="h-4 w-4 text-indigo-400" />
            {competitor.competitor_name}
          </h3>
          <p className="text-xs text-slate-400">{competitor.market_segment || 'Enterprise SaaS / AI Solutions'}</p>
        </div>
        <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${threat.color}`}>
          {threat.label}
        </span>
      </div>

      {/* Product Offerings */}
      {competitor.product_portfolio && competitor.product_portfolio.length > 0 && (
        <div className="mb-3">
          <span className="text-[10px] font-medium text-slate-400 uppercase tracking-wider block mb-1">
            Core Products
          </span>
          <div className="flex flex-wrap gap-1">
            {competitor.product_portfolio.map((prod, idx) => (
              <span
                key={idx}
                className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700"
              >
                {prod}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-2 gap-2 text-[11px] mb-3">
        <div className="p-2.5 rounded bg-slate-950/40 border border-slate-800/80">
          <span className="text-emerald-400 font-semibold block mb-1">Strengths</span>
          <ul className="space-y-0.5 text-slate-300 text-[10px]">
            {(competitor.strengths || ['Enterprise distribution', 'Brand recognition']).slice(0, 2).map((s, i) => (
              <li key={i} className="truncate">• {s}</li>
            ))}
          </ul>
        </div>
        <div className="p-2.5 rounded bg-slate-950/40 border border-slate-800/80">
          <span className="text-amber-400 font-semibold block mb-1">Weaknesses</span>
          <ul className="space-y-0.5 text-slate-300 text-[10px]">
            {(competitor.weaknesses || ['High pricing tier', 'Legacy tech stack']).slice(0, 2).map((w, i) => (
              <li key={i} className="truncate">• {w}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="flex items-center justify-between text-[10px] text-slate-400 pt-2 border-t border-slate-800">
        <span className="flex items-center gap-1">
          <Activity className="h-3 w-3 text-cyan-400" />
          Public Signals Tracked
        </span>
        <span>{competitor.last_activity_date ? `Updated ${new Date(competitor.last_activity_date).toLocaleDateString()}` : 'Active Monitoring'}</span>
      </div>
    </div>
  );
};
