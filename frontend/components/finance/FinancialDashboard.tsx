'use client';

import React, { useState, useEffect } from 'react';
import { financeApi, Invoice, Payment, CashFlowForecast } from '@/lib/api/finance';
import Link from 'next/link';

export function FinancialDashboard() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [forecast, setForecast] = useState<CashFlowForecast | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      setIsLoading(true);
      try {
        const [invRes, payRes, fcastRes] = await Promise.all([
          financeApi.listInvoices({ limit: 20 }),
          financeApi.listPayments(),
          financeApi.forecastCashFlow({ months_ahead: 3, projected_monthly_burn: '15000.00' }),
        ]);
        setInvoices(invRes || []);
        setPayments(payRes || []);
        setForecast(fcastRes);
      } catch (err) {
        console.error('Failed to load financial dashboard data', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadDashboardData();
  }, []);

  const totalInvoiced = invoices.reduce((acc, inv) => acc + parseFloat(inv.total_amount || '0'), 0);
  const totalCollected = payments
    .filter((p) => p.status === 'succeeded')
    .reduce((acc, p) => acc + parseFloat(p.amount || '0'), 0);
  const totalOutstanding = invoices
    .filter((inv) => ['issued', 'partially_paid', 'overdue'].includes(inv.status))
    .reduce((acc, inv) => acc + parseFloat(inv.balance_due || '0'), 0);

  return (
    <div className="space-y-6 text-slate-100">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <span>💳</span> Unified Commercial & Financial Operations
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Deterministic billing, invoice lifecycles, immutable ledger postings, and AI commercial intelligence.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/finance/invoices"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition"
          >
            Manage Invoices
          </Link>
          <Link
            href="/finance/payments"
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-sm font-medium border border-slate-700 transition"
          >
            Payment Transactions
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Invoiced</span>
          <div className="text-2xl font-bold text-white mt-2">${totalInvoiced.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
          <span className="text-xs text-slate-500 mt-1 block">Across all active contracts</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">Collected Revenue</span>
          <div className="text-2xl font-bold text-emerald-400 mt-2">${totalCollected.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
          <span className="text-xs text-slate-500 mt-1 block">Verified settlements</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs font-semibold text-amber-400 uppercase tracking-wider">Outstanding Receivables</span>
          <div className="text-2xl font-bold text-amber-400 mt-2">${totalOutstanding.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
          <span className="text-xs text-slate-500 mt-1 block">Uncollected balances</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">3-Month Projected Inflow</span>
          <div className="text-2xl font-bold text-cyan-400 mt-2">
            ${forecast ? parseFloat(forecast.projected_inflows.total_expected_inflow).toLocaleString('en-US', { minimumFractionDigits: 2 }) : '0.00'}
          </div>
          <span className="text-xs text-slate-500 mt-1 block">Receivables + Retainers</span>
        </div>
      </div>

      {/* Quick Invoices & Recent Payments Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Invoices */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">Recent Invoices</h2>
            <Link href="/finance/invoices" className="text-xs text-indigo-400 hover:underline">View All →</Link>
          </div>
          {invoices.length === 0 ? (
            <p className="text-sm text-slate-500 py-6 text-center">No invoices recorded yet.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 text-xs">
                    <th className="pb-2 font-medium">Invoice #</th>
                    <th className="pb-2 font-medium">Status</th>
                    <th className="pb-2 font-medium">Total</th>
                    <th className="pb-2 font-medium">Balance</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {invoices.slice(0, 5).map((inv) => (
                    <tr key={inv.id} className="hover:bg-slate-800/40">
                      <td className="py-2.5 font-mono text-xs text-indigo-300">
                        <Link href={`/finance/invoices/${inv.id}`} className="hover:underline">{inv.invoice_number}</Link>
                      </td>
                      <td className="py-2.5">
                        <span className={`px-2 py-0.5 rounded text-[11px] font-semibold uppercase ${
                          inv.status === 'paid' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                          inv.status === 'draft' ? 'bg-slate-800 text-slate-300' :
                          inv.status === 'issued' ? 'bg-blue-950 text-blue-300 border border-blue-800' :
                          'bg-amber-950 text-amber-300 border border-amber-800'
                        }`}>
                          {inv.status}
                        </span>
                      </td>
                      <td className="py-2.5 font-medium">${parseFloat(inv.total_amount).toFixed(2)}</td>
                      <td className="py-2.5 text-slate-400">${parseFloat(inv.balance_due).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Recent Payment Transactions */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">Payment Settlements</h2>
            <Link href="/finance/payments" className="text-xs text-indigo-400 hover:underline">View All →</Link>
          </div>
          {payments.length === 0 ? (
            <p className="text-sm text-slate-500 py-6 text-center">No payment transactions recorded.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 text-xs">
                    <th className="pb-2 font-medium">Payment ID</th>
                    <th className="pb-2 font-medium">Provider</th>
                    <th className="pb-2 font-medium">Amount</th>
                    <th className="pb-2 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {payments.slice(0, 5).map((p) => (
                    <tr key={p.id} className="hover:bg-slate-800/40">
                      <td className="py-2.5 font-mono text-xs text-slate-300">{p.id.slice(0, 8)}...</td>
                      <td className="py-2.5 uppercase text-xs text-slate-400">{p.provider_type}</td>
                      <td className="py-2.5 font-medium text-emerald-400">${parseFloat(p.amount).toFixed(2)}</td>
                      <td className="py-2.5">
                        <span className={`px-2 py-0.5 rounded text-[11px] font-semibold uppercase ${
                          p.status === 'succeeded' ? 'bg-emerald-950 text-emerald-300' : 'bg-rose-950 text-rose-300'
                        }`}>
                          {p.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
