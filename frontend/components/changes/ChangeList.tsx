'use client';

import React from 'react';
import { ChangeRequest } from '@/lib/api/changes';
import { GitPullRequest, ArrowRight, ShieldCheck, Clock, CheckCircle2, AlertTriangle, Filter } from 'lucide-react';

interface ChangeListProps {
  changes: ChangeRequest[];
  onSelectChange?: (change: ChangeRequest) => void;
  selectedChangeId?: string | null;
}

export const ChangeList: React.FC<ChangeListProps> = ({
  changes,
  onSelectChange,
  selectedChangeId,
}) => {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'APPROVED':
      case 'BASELINE_UPDATE':
      case 'IMPLEMENTATION':
      case 'COMPLETED':
        return (
          <span className="flex items-center space-x-1 text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded-full">
            <CheckCircle2 className="w-3 h-3" />
            <span>{status}</span>
          </span>
        );
      case 'PENDING_CLIENT':
      case 'INTERNAL_REVIEW':
        return (
          <span className="flex items-center space-x-1 text-[11px] font-semibold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2.5 py-0.5 rounded-full">
            <Clock className="w-3 h-3" />
            <span>{status}</span>
          </span>
        );
      case 'REJECTED':
        return (
          <span className="flex items-center space-x-1 text-[11px] font-semibold text-red-400 bg-red-500/10 border border-red-500/20 px-2.5 py-0.5 rounded-full">
            <AlertTriangle className="w-3 h-3" />
            <span>{status}</span>
          </span>
        );
      default:
        return (
          <span className="flex items-center space-x-1 text-[11px] font-semibold text-blue-400 bg-blue-500/10 border border-blue-500/20 px-2.5 py-0.5 rounded-full">
            <GitPullRequest className="w-3 h-3" />
            <span>{status}</span>
          </span>
        );
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
          <GitPullRequest className="w-4 h-4 text-blue-400" />
          <span>Change Requests Directory</span>
        </h3>
        <span className="text-xs text-slate-400">{changes.length} Total</span>
      </div>

      {changes.length === 0 ? (
        <p className="text-xs text-slate-500 py-6 text-center">No change requests logged for this project.</p>
      ) : (
        <div className="space-y-3">
          {changes.map((cr) => (
            <div
              key={cr.id}
              onClick={() => onSelectChange && onSelectChange(cr)}
              className={`p-4 rounded-xl border cursor-pointer transition duration-150 space-y-2 ${
                selectedChangeId === cr.id
                  ? 'bg-blue-600/10 border-blue-500/50 shadow-lg'
                  : 'bg-slate-950 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-xs font-bold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                    {cr.change_number}
                  </span>
                  <h4 className="text-sm font-semibold text-white">{cr.title}</h4>
                </div>
                {getStatusBadge(cr.status)}
              </div>

              <p className="text-xs text-slate-400 line-clamp-2">{cr.description}</p>

              <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-slate-900">
                <div className="flex items-center space-x-3">
                  <span>Category: <strong className="text-slate-300">{cr.category}</strong></span>
                  <span>Classification: <strong className="text-amber-400">{cr.classification}</strong></span>
                </div>
                <span>Requested by {cr.requested_by}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
