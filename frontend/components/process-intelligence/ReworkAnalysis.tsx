'use client';

import React from 'react';
import { ReworkRecord } from '@/lib/api/processIntelligence';
import { RefreshCw, Repeat, Layers } from 'lucide-react';

interface Props {
  reworkRecords: ReworkRecord[];
}

export default function ReworkAnalysis({ reworkRecords }: Props) {
  if (reworkRecords.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-400">
        <RefreshCw className="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p className="text-lg font-medium text-white">Zero Rework Loops Detected</p>
        <p className="text-sm text-slate-500 mt-1">Activities execute cleanly in single iterations without repeated loops.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Repeat className="w-5 h-5 text-amber-400" /> Rework & Loop Friction Analysis
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            {reworkRecords.length} repetitive activity loops detected across historical cases
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-400">
          <thead className="bg-slate-950 text-slate-300 text-xs font-semibold uppercase">
            <tr>
              <th className="px-4 py-3">Activity Name</th>
              <th className="px-4 py-3">Loop Repetitions</th>
              <th className="px-4 py-3">Wasted Duration</th>
              <th className="px-4 py-3">Probable Driver</th>
              <th className="px-4 py-3">Case ID</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {reworkRecords.map((r, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40">
                <td className="px-4 py-3 font-medium text-white">{r.activity_name}</td>
                <td className="px-4 py-3 font-mono text-amber-400 font-bold">{r.repetition_count}x</td>
                <td className="px-4 py-3 font-mono text-red-400">{r.wasted_duration_seconds}s</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 text-xs rounded bg-slate-800 text-slate-300 font-mono">
                    {r.probable_driver}
                  </span>
                </td>
                <td className="px-4 py-3 font-mono text-xs text-slate-400">{r.case_id || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
