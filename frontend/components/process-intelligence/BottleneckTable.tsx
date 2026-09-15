'use client';

import React from 'react';
import { BottleneckRecord } from '@/lib/api/processIntelligence';
import { AlertTriangle, Clock, Layers } from 'lucide-react';

interface Props {
  bottlenecks: BottleneckRecord[];
}

export default function BottleneckTable({ bottlenecks }: Props) {
  if (bottlenecks.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-400">
        <Clock className="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p className="text-lg font-medium text-white">No Bottlenecks Detected</p>
        <p className="text-sm text-slate-500 mt-1">Activities are executing within expected latency thresholds.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" /> Process Latency Bottlenecks
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            {bottlenecks.length} activities exceeding queue and wait duration thresholds
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-400">
          <thead className="bg-slate-950 text-slate-300 text-xs font-semibold uppercase">
            <tr>
              <th className="px-4 py-3">Code</th>
              <th className="px-4 py-3">Activity Name</th>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Avg Wait (s)</th>
              <th className="px-4 py-3">Avg Proc (s)</th>
              <th className="px-4 py-3">Affected Cases</th>
              <th className="px-4 py-3">Root Cause & Evidence</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {bottlenecks.map((b) => (
              <tr key={b.bottleneck_code} className="hover:bg-slate-800/40">
                <td className="px-4 py-3 font-mono font-medium text-amber-400">{b.bottleneck_code}</td>
                <td className="px-4 py-3 font-medium text-white">{b.activity_name}</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 text-xs rounded bg-slate-800 text-slate-300 font-mono">
                    {b.bottleneck_type}
                  </span>
                </td>
                <td className="px-4 py-3 font-mono text-amber-400 font-bold">{b.average_wait_seconds}s</td>
                <td className="px-4 py-3 font-mono">{b.average_processing_seconds}s</td>
                <td className="px-4 py-3 font-mono text-indigo-300">{b.affected_cases_count}</td>
                <td className="px-4 py-3 text-xs text-slate-300 max-w-xs">{b.root_cause_summary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
