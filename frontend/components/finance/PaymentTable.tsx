'use client';

import React, { useState, useEffect } from 'react';
import { financeApi, Payment } from '@/lib/api/finance';

export function PaymentTable() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadPayments = async () => {
    setIsLoading(true);
    try {
      const data = await financeApi.listPayments();
      setPayments(data || []);
    } catch (err) {
      console.error('Failed to load payments', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadPayments();
  }, []);

  return (
    <div className="space-y-6 text-slate-100">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>💳</span> Payment Transactions & Settlements
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Review processed provider payments, fees, refunds, and reconciliation audit trails.
        </p>
      </div>

      {/* Payments List Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        {isLoading ? (
          <div className="p-8 text-center text-slate-400">Loading payments...</div>
        ) : payments.length === 0 ? (
          <div className="p-12 text-center text-slate-500">No payment transactions recorded.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-800/60 text-slate-400 text-xs uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-4">Payment ID</th>
                  <th className="py-3 px-4">Provider</th>
                  <th className="py-3 px-4">Method</th>
                  <th className="py-3 px-4">Amount</th>
                  <th className="py-3 px-4">Processing Fee</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {payments.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3 px-4 font-mono font-medium text-slate-300">{p.id.slice(0, 8)}...</td>
                    <td className="py-3 px-4 uppercase text-xs text-slate-400">{p.provider_type}</td>
                    <td className="py-3 px-4 capitalize text-slate-300">{p.payment_method.replace('_', ' ')}</td>
                    <td className="py-3 px-4 font-medium text-emerald-400">${parseFloat(p.amount).toFixed(2)}</td>
                    <td className="py-3 px-4 text-xs text-slate-500">${parseFloat(p.fee_amount).toFixed(2)}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-semibold uppercase ${
                        p.status === 'succeeded' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                        'bg-rose-950 text-rose-300 border border-rose-800'
                      }`}>
                        {p.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-500">
                      {new Date(p.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
