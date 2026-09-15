'use client';

import React from 'react';
import { ClientRenewal } from '@/lib/api/customer_success';

interface RenewalTableProps {
  renewals: ClientRenewal[];
}

export function RenewalTable({ renewals }: RenewalTableProps) {
  if (!renewals || renewals.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl text-center text-slate-500">
        No upcoming renewal cycles found.
      </div>
    );
  }

  const getStatusBadge = (st: string) => {
    switch (st.toUpperCase()) {
      case 'RENEWED':
        return <span className="px-2.5 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">RENEWED</span>;
      case 'UPCOMING':
      case 'PREPARATION':
        return <span className="px-2.5 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-semibold">UPCOMING</span>;
      case 'NEGOTIATION':
      case 'REVIEW':
        return <span className="px-2.5 py-0.5 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-full text-xs font-semibold">IN NEGOTIATION</span>;
      case 'AT_RISK':
        return <span className="px-2.5 py-0.5 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-full text-xs font-semibold">AT RISK</span>;
      default:
        return <span className="px-2.5 py-0.5 bg-slate-500/10 text-slate-400 border border-slate-500/20 rounded-full text-xs font-semibold">{st}</span>;
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white">Renewal & Contract Retainers</h3>
          <p className="text-xs text-slate-400 mt-0.5">Commercial renewal schedule, probability weighting, and contract values.</p>
        </div>
        <span className="text-xs text-slate-500 font-mono">{renewals.length} cycles active</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-950/60 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
            <tr>
              <th className="py-3 px-4">Renewal Date</th>
              <th className="py-3 px-4">Target Contract Value</th>
              <th className="py-3 px-4">Probability</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4">Notes</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {renewals.map((r, i) => {
              const val = parseFloat(r.contract_value || r.estimated_renewal_value || '0');
              const prob = parseFloat(r.probability_pct || r.renewal_probability || '50');
              const dateStr = r.expiration_date || r.renewal_date || r.current_period_end;
              return (
                <tr key={r.id || i} className="hover:bg-slate-950/40 transition">
                  <td className="py-3 px-4 font-mono font-medium text-white">
                    {dateStr
                      ? new Date(dateStr).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                        })
                      : '—'}
                  </td>
                  <td className="py-3 px-4 font-mono font-bold text-emerald-400">
                    ${val.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <div className="w-16 bg-slate-800 rounded-full h-1.5 overflow-hidden">
                        <div
                          className={`h-1.5 rounded-full ${prob >= 75 ? 'bg-emerald-500' : prob >= 50 ? 'bg-amber-500' : 'bg-rose-500'}`}
                          style={{ width: `${Math.min(100, Math.max(0, prob))}%` }}
                        />
                      </div>
                      <span className="font-mono text-[11px] text-slate-300">{prob.toFixed(0)}%</span>
                    </div>
                  </td>
                  <td className="py-3 px-4">{getStatusBadge(r.status)}</td>
                  <td className="py-3 px-4 text-slate-400 max-w-xs truncate">{r.notes || '—'}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
