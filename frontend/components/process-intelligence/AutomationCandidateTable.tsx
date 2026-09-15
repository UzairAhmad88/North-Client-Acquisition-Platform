'use client';

import React from 'react';
import { AutomationCandidate } from '@/lib/api/processIntelligence';
import { Zap, CheckCircle2, AlertCircle, Clock } from 'lucide-react';

interface Props {
  candidates: AutomationCandidate[];
}

export default function AutomationCandidateTable({ candidates }: Props) {
  if (candidates.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-400">
        <Zap className="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p className="text-lg font-medium text-white">No Automation Candidates Identified</p>
        <p className="text-sm text-slate-500 mt-1">High frequency, repetitive manual tasks will be surfaced here after evaluation.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-purple-400" /> Automation Opportunities & 8-Factor Scorecard
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            {candidates.length} tasks evaluated across repetition, determinism, risk, and reversibility
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-400">
          <thead className="bg-slate-950 text-slate-300 text-xs font-semibold uppercase">
            <tr>
              <th className="px-4 py-3">Task Name</th>
              <th className="px-4 py-3">Monthly Frequency</th>
              <th className="px-4 py-3">Avg Duration</th>
              <th className="px-4 py-3">Suitability Score</th>
              <th className="px-4 py-3">Classification</th>
              <th className="px-4 py-3">Est. Savings</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {candidates.map((c) => (
              <tr key={c.candidate_code} className="hover:bg-slate-800/40">
                <td className="px-4 py-3 font-medium text-white">{c.task_name}</td>
                <td className="px-4 py-3 font-mono">{c.frequency_per_month}/mo</td>
                <td className="px-4 py-3 font-mono">{c.average_duration_minutes} min</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-purple-400">{c.suitability_score}</span>
                    <div className="w-16 h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div style={{ width: `${c.suitability_score * 100}%` }} className="bg-purple-500 h-full"></div>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 text-xs rounded font-semibold ${
                    c.classification === 'LOW_RISK_AUTOMATION' ? 'bg-emerald-500/20 text-emerald-300' :
                    c.classification === 'REVIEW_REQUIRED' ? 'bg-amber-500/20 text-amber-300' : 'bg-red-500/20 text-red-300'
                  }`}>
                    {c.classification}
                  </span>
                </td>
                <td className="px-4 py-3 font-mono text-emerald-400 font-bold">{c.expected_savings_hours_month} hrs/mo</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 text-xs rounded bg-slate-800 text-slate-300 font-mono">
                    {c.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
