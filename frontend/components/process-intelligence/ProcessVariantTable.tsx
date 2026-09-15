'use client';

import React from 'react';
import { ProcessVariant } from '@/lib/api/processIntelligence';
import { Layers, CheckCircle2, XCircle, ArrowRight } from 'lucide-react';

interface Props {
  variants: ProcessVariant[];
}

export default function ProcessVariantTable({ variants }: Props) {
  if (variants.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-400">
        <Layers className="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p className="text-lg font-medium text-white">No Variants Discovered</p>
        <p className="text-sm text-slate-500 mt-1">Event traces are needed to classify distinct execution paths.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-purple-400" /> Discovered Process Variants
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            {variants.length} distinct end-to-end execution paths identified
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-400">
          <thead className="bg-slate-950 text-slate-300 text-xs font-semibold uppercase">
            <tr>
              <th className="px-4 py-3">Variant Code</th>
              <th className="px-4 py-3">Execution Sequence</th>
              <th className="px-4 py-3">Frequency</th>
              <th className="px-4 py-3">Share (%)</th>
              <th className="px-4 py-3">Avg Cycle (s)</th>
              <th className="px-4 py-3">Conversion</th>
              <th className="px-4 py-3">Conformance</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {variants.map((v) => (
              <tr key={v.variant_code} className="hover:bg-slate-800/40">
                <td className="px-4 py-3 font-mono font-medium text-indigo-400">{v.variant_code}</td>
                <td className="px-4 py-3">
                  <div className="flex flex-wrap items-center gap-1.5">
                    {v.event_sequence.map((step, idx) => (
                      <React.Fragment key={idx}>
                        <span className="px-2 py-0.5 text-xs rounded bg-slate-800 text-slate-200 font-medium">
                          {step}
                        </span>
                        {idx < v.event_sequence.length - 1 && (
                          <ArrowRight className="w-3 h-3 text-slate-600" />
                        )}
                      </React.Fragment>
                    ))}
                  </div>
                </td>
                <td className="px-4 py-3 font-mono font-medium text-white">{v.frequency}</td>
                <td className="px-4 py-3 font-mono text-purple-400">{v.percentage}%</td>
                <td className="px-4 py-3 font-mono">{v.average_cycle_time_seconds}s</td>
                <td className="px-4 py-3 font-mono text-emerald-400">{v.conversion_rate}%</td>
                <td className="px-4 py-3">
                  {v.is_conforming ? (
                    <span className="inline-flex items-center gap-1 text-xs text-emerald-400">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Conforming
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-xs text-red-400">
                      <XCircle className="w-3.5 h-3.5" /> Deviant
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
