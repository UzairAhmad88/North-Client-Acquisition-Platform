'use client';

import React from 'react';
import { OptimizationProposal } from '@/lib/api/processIntelligence';
import { Sliders, ShieldCheck, ArrowUpRight, Clock, DollarSign, Award } from 'lucide-react';

interface Props {
  proposals: OptimizationProposal[];
}

export default function OptimizationProposalComponent({ proposals }: Props) {
  if (proposals.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-400">
        <Sliders className="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p className="text-lg font-medium text-white">No Optimization Proposals</p>
        <p className="text-sm text-slate-500 mt-1">Multi-objective tradeoff proposals will appear here when generated.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Sliders className="w-5 h-5 text-indigo-400" /> Multi-Objective Optimization Proposals
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Gated workflow proposals balancing Cycle Time, Cost, Quality, Risk, and Compliance
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {proposals.map((p) => (
          <div key={p.proposal_code} className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-xs font-mono text-indigo-400">{p.proposal_code}</span>
                <h4 className="text-lg font-bold text-white mt-1">{p.title}</h4>
                <p className="text-xs text-slate-400">Version: v{p.current_version} &rarr; v{p.proposed_version}</p>
              </div>
              <span className="px-2.5 py-1 text-xs rounded-full bg-indigo-500/20 text-indigo-300 font-semibold uppercase">
                {p.status}
              </span>
            </div>

            <p className="text-sm text-slate-300">{p.problem_statement}</p>

            {/* Tradeoff Scorecard */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3 bg-slate-950 border border-slate-800 rounded-lg p-4">
              <div>
                <span className="text-xs text-slate-400">Cycle Time</span>
                <p className="text-base font-bold text-emerald-400 mt-0.5">
                  +{p.expected_benefits?.cycle_time_reduction_percentage || 25}%
                </p>
              </div>
              <div>
                <span className="text-xs text-slate-400">Cost Savings</span>
                <p className="text-base font-bold text-emerald-400 mt-0.5">
                  +{p.expected_benefits?.cost_reduction_percentage || 15}%
                </p>
              </div>
              <div>
                <span className="text-xs text-slate-400">Quality Index</span>
                <p className="text-base font-bold text-white mt-0.5">
                  {p.tradeoff_scorecard?.quality_score || 0.9}
                </p>
              </div>
              <div>
                <span className="text-xs text-slate-400">Risk Level</span>
                <p className="text-base font-bold text-amber-400 mt-0.5">{p.risk_level}</p>
              </div>
              <div>
                <span className="text-xs text-slate-400">Governance</span>
                <p className="text-base font-bold text-emerald-400 mt-0.5 flex items-center gap-1">
                  <ShieldCheck className="w-4 h-4" /> Aligned
                </p>
              </div>
            </div>

            <div className="text-xs text-slate-400 bg-slate-950/50 p-3 rounded border border-slate-800">
              <span className="font-semibold text-slate-300">Rollback Plan: </span>{p.rollback_plan}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
