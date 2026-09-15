'use client';

import React from 'react';
import { ProposalDetail } from '@/lib/api/proposals';

interface ProposalWorkspaceProps {
  proposalDetail: ProposalDetail;
  onGenerate?: () => void;
  onApprove?: () => void;
  isGenerating?: boolean;
}

export function ProposalWorkspace({
  proposalDetail,
  onGenerate,
  onApprove,
  isGenerating,
}: ProposalWorkspaceProps) {
  const isApproved = proposalDetail.status === 'APPROVED';

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-slate-100">{proposalDetail.title}</h2>
            <span className="rounded-full bg-indigo-500/20 px-3 py-1 text-xs font-semibold text-indigo-300 border border-indigo-500/30">
              v{proposalDetail.version}
            </span>
            <span
              className={`rounded-full px-3 py-1 text-xs font-semibold uppercase ${
                isApproved
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              }`}
            >
              {proposalDetail.status}
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Proposal ID: {proposalDetail.id} | Solution ID: {proposalDetail.solution_id}
          </p>
        </div>

        <div className="flex gap-3">
          {onGenerate && (
            <button
              onClick={onGenerate}
              disabled={isGenerating}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-indigo-500 disabled:opacity-50 transition-all"
            >
              {isGenerating ? 'Generating Proposal Draft...' : 'Generate Proposal Draft'}
            </button>
          )}

          {!isApproved && onApprove && (
            <button
              onClick={onApprove}
              className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-emerald-500 transition-all"
            >
              Approve Proposal Draft
            </button>
          )}
        </div>
      </div>

      {/* Pricing & Commercial Safety Status */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300">Commercial & Pricing Status</h3>
            <p className="mt-1 text-xs text-slate-400">{proposalDetail.summary}</p>
          </div>
          <span className="rounded bg-amber-500/20 px-3 py-1.5 text-xs font-bold uppercase text-amber-300 border border-amber-500/30">
            {proposalDetail.pricing_status.replace(/_/g, ' ')}
          </span>
        </div>
      </div>

      {/* Proposal Deliverables Items */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-md">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-300">
          Proposal Items & Scope ({proposalDetail.items?.length || 0})
        </h3>
        <div className="space-y-3">
          {proposalDetail.items?.map((item) => (
            <div key={item.id} className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950/40 p-4">
              <div>
                <h4 className="text-sm font-semibold text-slate-100">{item.description}</h4>
                <div className="mt-1 flex items-center gap-4 text-xs text-slate-400">
                  <span>Quantity: {item.quantity} {item.unit}</span>
                  <span>Optional: {item.is_optional ? 'Yes' : 'No'}</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-bold text-amber-400">
                  {item.price ? `$${item.price}` : 'Pricing Pending Review'}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
