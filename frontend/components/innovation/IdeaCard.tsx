'use client';

import React from 'react';
import { Lightbulb, Sparkles, TrendingUp, ShieldCheck, ArrowRight } from 'lucide-react';
import { InnovationIdea } from '../../lib/api/innovation';

interface IdeaCardProps {
  idea: InnovationIdea;
  onSelect?: (id: string) => void;
}

export const IdeaCard: React.FC<IdeaCardProps> = ({ idea, onSelect }) => {
  const getOriginBadge = (origin: string) => {
    switch (origin?.toUpperCase()) {
      case 'AI_WORKER':
        return { label: 'AI Worker Synthesis', color: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30' };
      case 'CLIENT':
      case 'SUPPORT_TICKET':
        return { label: 'Customer Signal', color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' };
      case 'RESEARCH':
      case 'COMPETITOR_ANALYSIS':
        return { label: 'Market Research', color: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30' };
      default:
        return { label: 'Human Generated', color: 'bg-amber-500/10 text-amber-400 border-amber-500/30' };
    }
  };

  const origin = getOriginBadge(idea.origin_source);

  return (
    <div
      onClick={() => onSelect && onSelect(idea.id)}
      className="p-5 rounded-xl border border-slate-800 bg-slate-900/60 hover:border-indigo-500/50 hover:bg-slate-900/90 transition-all cursor-pointer backdrop-blur-sm"
    >
      <div className="flex items-start justify-between gap-3 mb-2">
        <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${origin.color}`}>
          {origin.label}
        </span>
        <div className="text-right shrink-0">
          <span className="text-[10px] text-slate-500 block">11-Factor Score</span>
          <span className="text-xs font-bold font-mono text-emerald-400">
            {Math.round(idea.composite_score * 100)}%
          </span>
        </div>
      </div>

      <h4 className="text-sm font-bold text-white mb-1.5">{idea.title}</h4>
      <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
        {idea.description}
      </p>

      {/* 3 Key Factor Meters */}
      <div className="grid grid-cols-3 gap-2 text-center text-[10px] mb-3">
        <div className="p-1.5 rounded bg-slate-950/40 border border-slate-800">
          <span className="text-slate-500 block">Customer</span>
          <span className="text-indigo-300 font-mono font-bold">
            {Math.round(idea.customer_value_score * 100)}%
          </span>
        </div>
        <div className="p-1.5 rounded bg-slate-950/40 border border-slate-800">
          <span className="text-slate-500 block">Strategic Fit</span>
          <span className="text-cyan-300 font-mono font-bold">
            {Math.round(idea.strategic_fit_score * 100)}%
          </span>
        </div>
        <div className="p-1.5 rounded bg-slate-950/40 border border-slate-800">
          <span className="text-slate-500 block">Feasibility</span>
          <span className="text-emerald-300 font-mono font-bold">
            {Math.round(idea.technical_feasibility_score * 100)}%
          </span>
        </div>
      </div>

      <div className="flex items-center justify-between text-[10px] text-slate-500 pt-2 border-t border-slate-800/80">
        <span className="uppercase font-mono font-semibold text-slate-400">{idea.status}</span>
        <span className="flex items-center gap-1 text-indigo-400 font-medium">
          View Hypotheses <ArrowRight className="h-3 w-3" />
        </span>
      </div>
    </div>
  );
};
