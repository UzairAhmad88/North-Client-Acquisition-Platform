'use client';

import React, { useState, useEffect } from 'react';
import { financeApi, Invoice } from '@/lib/api/finance';
import Link from 'next/link';

export function InvoiceTable() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);

  const loadInvoices = async () => {
    setIsLoading(true);
    try {
      const data = await financeApi.listInvoices({ status: statusFilter || undefined });
      setInvoices(data || []);
    } catch (err) {
      console.error('Failed to load invoices', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadInvoices();
  }, [statusFilter]);

  return (
    <div className="space-y-6 text-slate-100">
      {/* Header & Filter Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <span>📄</span> Invoices & Commercial Billing
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Track draft generation, approval chains, issuance, and collection balances.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-sm text-slate-200 rounded-lg px-3 py-2 outline-none focus:border-indigo-500"
          >
            <option value="">All Statuses</option>
            <option value="draft">Draft</option>
            <option value="pending_approval">Pending Approval</option>
            <option value="approved">Approved</option>
            <option value="issued">Issued</option>
            <option value="partially_paid">Partially Paid</option>
            <option value="paid">Paid</option>
            <option value="overdue">Overdue</option>
          </select>
        </div>
      </div>

      {/* Invoices List Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        {isLoading ? (
          <div className="p-8 text-center text-slate-400">Loading invoices...</div>
        ) : invoices.length === 0 ? (
          <div className="p-12 text-center text-slate-500">No invoices match the selected filter.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-800/60 text-slate-400 text-xs uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-4">Invoice #</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Terms</th>
                  <th className="py-3 px-4">Total Amount</th>
                  <th className="py-3 px-4">Amount Paid</th>
                  <th className="py-3 px-4">Balance Due</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {invoices.map((inv) => (
                  <tr key={inv.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3 px-4 font-mono font-medium text-indigo-300">
                      <Link href={`/finance/invoices/${inv.id}`} className="hover:underline">{inv.invoice_number}</Link>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-semibold uppercase ${
                        inv.status === 'paid' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                        inv.status === 'draft' ? 'bg-slate-800 text-slate-300' :
                        inv.status === 'approved' ? 'bg-indigo-950 text-indigo-300 border border-indigo-800' :
                        inv.status === 'issued' ? 'bg-blue-950 text-blue-300 border border-blue-800' :
                        'bg-amber-950 text-amber-300 border border-amber-800'
                      }`}>
                        {inv.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-400 uppercase">{inv.payment_terms}</td>
                    <td className="py-3 px-4 font-medium text-white">${parseFloat(inv.total_amount).toFixed(2)}</td>
                    <td className="py-3 px-4 text-emerald-400">${parseFloat(inv.amount_paid).toFixed(2)}</td>
                    <td className="py-3 px-4 text-amber-400 font-medium">${parseFloat(inv.balance_due).toFixed(2)}</td>
                    <td className="py-3 px-4 text-right">
                      <Link
                        href={`/finance/invoices/${inv.id}`}
                        className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs rounded border border-slate-700 transition"
                      >
                        View Details
                      </Link>
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
