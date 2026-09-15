'use client';

import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, HelpCircle, Activity, ArrowUpRight, ShieldAlert, Cpu } from 'lucide-react';
import { StrategicObjective } from '../../lib/api/strategy';

interface FeasibilityItem {
  objective_id: string;
  name: string;
  feasibility_score: number;
  feasibility_level: 'FEASIBLE' | 'LIKELY' | 'UNCERTAIN' | 'CHALLENGING' | 'UNLIKELY' | 'INFEASIBLE' | 'INSUFFICIENT_DATA';
  confidence_score: number;
  strategic_gap: number;
  gap_percentage: number;
  limiting_factors: string[];
  mitigation_recommendations: string[];
  unit?: string;
  target_value?: number;
  current_value?: number;
}

interface FeasibilityPanelProps {
  feasibilityData: FeasibilityItem[];
  isLoading?: boolean;
}

export const FeasibilityPanel: React.FC<FeasibilityPanelProps> = ({ feasibilityData, isLoading = false }) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-400">
        <Activity className="h-6 w-6 animate-spin mr-2 text-indigo-400" />
        <span>Evaluating probabilistic goal feasibility & strategic gaps...</span>
      </div>
    );
  }

  if (!feasibilityData || feasibilityData.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-700/60 bg-slate-900/40 p-8 text-center">
        <Cpu className="mx-auto h-10 w-10 text-slate-500 mb-3" />
        <h3 className="text-base font-semibold text-slate-300">No Feasibility Data Computed</h3>
        <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
          Run strategic gap analysis and feasibility evaluation to assess mathematical realism against organizational capacity and digital twin constraints.
        </p>
      </div>
    );
  }

  const getFeasibilityBadge = (level: string) => {
    switch (level) {
      case 'FEASIBLE':
      case 'LIKELY':
        return {
          icon: <CheckCircle className="h-4 w-4 text-emerald-400" />,
          color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
          label: level,
        };
      case 'UNCERTAIN':
      case 'CHALLENGING':
        return {
          icon: <AlertTriangle className="h-4 w-4 text-amber-400" />,
          color: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
          label: level,
        };
      case 'UNLIKELY':
      case 'INFEASIBLE':
        return {
          icon: <XCircle className="h-4 w-4 text-rose-400" />,
          color: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
          label: level,
        };
      default:
        return {
          icon: <HelpCircle className="h-4 w-4 text-slate-400" />,
          color: 'bg-slate-500/10 text-slate-400 border-slate-500/30',
          label: 'INSUFFICIENT DATA',
        };
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Summary */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-xl border border-slate-700/60 bg-slate-900/60 backdrop-blur-sm">
        <div>
          <h2 className="text-lg font-bold text-white tracking-tight">Probabilistic Goal Feasibility & Gap Analysis</h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time evaluation of objective achievability against historical velocity, current FTE allocations, and financial capacity constraints.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/80 text-xs font-semibold text-slate-300">
            {feasibilityData.length} Evaluated Objectives
          </div>
        </div>
      </div>

      {/* Grid of Feasibility Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {feasibilityData.map((item) => {
          const badge = getFeasibilityBadge(item.feasibility_level);
          return (
            <div
              key={item.objective_id}
              className="rounded-xl border border-slate-700/60 bg-slate-900/50 p-5 space-y-4 hover:border-slate-600 transition-all"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-sm font-semibold text-white">{item.name}</h3>
                  <div className="text-xs text-slate-400 mt-0.5">Objective ID: {item.objective_id.slice(0, 8)}...</div>
                </div>
                <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium border ${badge.color}`}>
                  {badge.icon}
                  <span>{badge.label}</span>
                </div>
              </div>

              {/* Progress & Gap Metrics */}
              <div className="grid grid-cols-3 gap-3 p-3 rounded-lg bg-slate-950/60 border border-slate-800/80 text-center">
                <div>
                  <div className="text-[10px] uppercase text-slate-500 font-semibold">Feasibility</div>
                  <div className="text-sm font-bold text-indigo-400 mt-0.5">
                    {Math.round(item.feasibility_score * 100)}%
                  </div>
                </div>
                <div>
                  <div className="text-[10px] uppercase text-slate-500 font-semibold">Strategic Gap</div>
                  <div className="text-sm font-bold text-amber-400 mt-0.5">
                    {item.strategic_gap} {item.unit || ''}
                  </div>
                </div>
                <div>
                  <div className="text-[10px] uppercase text-slate-500 font-semibold">Confidence</div>
                  <div className="text-sm font-bold text-emerald-400 mt-0.5">
                    {Math.round(item.confidence_score * 100)}%
                  </div>
                </div>
              </div>

              {/* Limiting Factors */}
              {item.limiting_factors && item.limiting_factors.length > 0 && (
                <div>
                  <div className="text-xs font-semibold text-rose-300 flex items-center gap-1 mb-1.5">
                    <ShieldAlert className="h-3.5 w-3.5 text-rose-400" />
                    Binding Constraints & Bottlenecks:
                  </div>
                  <ul className="space-y-1">
                    {item.limiting_factors.map((factor, idx) => (
                      <li key={idx} className="text-xs text-slate-400 flex items-center gap-1.5">
                        <span className="h-1.5 w-1.5 rounded-full bg-rose-500/80" />
                        {factor}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Mitigation / Recommended Actions */}
              {item.mitigation_recommendations && item.mitigation_recommendations.length > 0 && (
                <div className="p-3 rounded-lg bg-indigo-950/20 border border-indigo-500/20 text-xs">
                  <div className="font-semibold text-indigo-300 flex items-center gap-1 mb-1">
                    <ArrowUpRight className="h-3.5 w-3.5 text-indigo-400" />
                    Strategic Lever:
                  </div>
                  <p className="text-indigo-200/80 leading-relaxed">
                    {item.mitigation_recommendations[0]}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
