'use client';

import React, { useState, useEffect } from 'react';
import { financeApi, Invoice } from '@/lib/api/finance';
import Link from 'next/link';

export function InvoiceDetail({ invoiceId }: { invoiceId: string }) {
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const loadInvoice = async () => {
    setIsLoading(true);
    try {
      const data = await financeApi.getInvoice(invoiceId);
      setInvoice(data);
    } catch (err) {
      console.error('Failed to load invoice', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadInvoice();
  }, [invoiceId]);

  const handleApprove = async () => {
    if (!invoice) return;
    setIsProcessing(true);
    try {
      await financeApi.approveInvoice(invoice.id, 'approved', 'Approved via commercial portal');
      setActionMessage('Invoice approved successfully.');
      loadInvoice();
    } catch (err) {
      console.error(err);
      setActionMessage('Failed to approve invoice.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleIssue = async () => {
    if (!invoice) return;
    setIsProcessing(true);
    try {
      await financeApi.issueInvoice(invoice.id);
      setActionMessage('Invoice finalized and issued successfully.');
      loadInvoice();
    } catch (err) {
      console.error(err);
      setActionMessage('Failed to issue invoice.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleQuickPay = async () => {
    if (!invoice) return;
    setIsProcessing(true);
    try {
      await financeApi.chargePayment({
        invoice_id: invoice.id,
        amount: invoice.balance_due,
        currency: invoice.currency,
        payment_method: 'credit_card',
        provider_type: 'mock',
      });
      setActionMessage('Payment charged and settled successfully.');
      loadInvoice();
    } catch (err) {
      console.error(err);
      setActionMessage('Failed to process payment.');
    } finally {
      setIsProcessing(false);
    }
  };

  if (isLoading) {
    return <div className="p-8 text-center text-slate-400">Loading invoice details...</div>;
  }

  if (!invoice) {
    return <div className="p-8 text-center text-rose-400">Invoice not found.</div>;
  }

  return (
    <div className="space-y-6 text-slate-100 max-w-5xl mx-auto">
      {/* Top Breadcrumb & Actions */}
      <div className="flex items-center justify-between">
        <Link href="/finance/invoices" className="text-sm text-indigo-400 hover:underline">
          ← Back to Invoices
        </Link>
        <div className="flex items-center gap-2">
          {invoice.status === 'draft' && (
            <button
              onClick={handleApprove}
              disabled={isProcessing}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg shadow transition"
            >
              Approve Invoice
            </button>
          )}
          {['draft', 'approved'].includes(invoice.status) && (
            <button
              onClick={handleIssue}
              disabled={isProcessing}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg shadow transition"
            >
              Issue Invoice
            </button>
          )}
          {['issued', 'partially_paid'].includes(invoice.status) && (
            <button
              onClick={handleQuickPay}
              disabled={isProcessing}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg shadow transition"
            >
              Record Settlement (${parseFloat(invoice.balance_due).toFixed(2)})
            </button>
          )}
        </div>
      </div>

      {actionMessage && (
        <div className="p-3 bg-indigo-950/60 border border-indigo-800 text-indigo-200 text-xs rounded-lg">
          {actionMessage}
        </div>
      )}

      {/* Invoice Document Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center pb-6 border-b border-slate-800 gap-4">
          <div>
            <h1 className="text-3xl font-bold font-mono text-white">{invoice.invoice_number}</h1>
            <p className="text-xs text-slate-400 mt-1">Tenant ID: {invoice.tenant_id}</p>
          </div>
          <div className="text-right">
            <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
              invoice.status === 'paid' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
              invoice.status === 'issued' ? 'bg-blue-950 text-blue-300 border border-blue-800' :
              'bg-amber-950 text-amber-300 border border-amber-800'
            }`}>
              {invoice.status}
            </span>
            <div className="text-xs text-slate-400 mt-2">
              Payment Terms: <span className="uppercase text-slate-200">{invoice.payment_terms}</span>
            </div>
          </div>
        </div>

        {/* Line Items Table */}
        <div className="mt-8">
          <h2 className="text-sm font-semibold uppercase text-slate-400 tracking-wider mb-3">Line Items</h2>
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-800/60 text-slate-400 text-xs uppercase">
              <tr>
                <th className="py-2.5 px-3">Item</th>
                <th className="py-2.5 px-3 text-right">Qty</th>
                <th className="py-2.5 px-3 text-right">Unit Price</th>
                <th className="py-2.5 px-3 text-right">Subtotal</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {(invoice.items || []).map((itm, idx) => (
                <tr key={idx}>
                  <td className="py-3 px-3">
                    <div className="font-medium text-white">{itm.title}</div>
                    {itm.description && <div className="text-xs text-slate-400">{itm.description}</div>}
                  </td>
                  <td className="py-3 px-3 text-right font-mono">{parseFloat(itm.quantity).toFixed(2)}</td>
                  <td className="py-3 px-3 text-right font-mono">${parseFloat(itm.unit_price).toFixed(2)}</td>
                  <td className="py-3 px-3 text-right font-mono font-medium">${parseFloat(itm.subtotal || itm.unit_price).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Totals Summary */}
        <div className="mt-8 pt-6 border-t border-slate-800 flex justify-end">
          <div className="w-72 space-y-2 text-sm">
            <div className="flex justify-between text-slate-400">
              <span>Subtotal</span>
              <span className="font-mono text-white">${parseFloat(invoice.subtotal).toFixed(2)}</span>
            </div>
            {parseFloat(invoice.discount_amount) > 0 && (
              <div className="flex justify-between text-slate-400">
                <span>Discount</span>
                <span className="font-mono text-rose-400">-${parseFloat(invoice.discount_amount).toFixed(2)}</span>
              </div>
            )}
            {parseFloat(invoice.tax_amount) > 0 && (
              <div className="flex justify-between text-slate-400">
                <span>Tax ({invoice.tax_rate_pct}%)</span>
                <span className="font-mono text-white">${parseFloat(invoice.tax_amount).toFixed(2)}</span>
              </div>
            )}
            <div className="flex justify-between text-base font-bold text-white pt-2 border-t border-slate-800">
              <span>Total Amount</span>
              <span className="font-mono">${parseFloat(invoice.total_amount).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-emerald-400 text-sm">
              <span>Amount Paid</span>
              <span className="font-mono">${parseFloat(invoice.amount_paid).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-amber-400 text-sm font-semibold">
              <span>Balance Due</span>
              <span className="font-mono">${parseFloat(invoice.balance_due).toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
