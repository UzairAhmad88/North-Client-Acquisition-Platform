'use client';

import React, { useState } from 'react';
import {
  LifeBuoy,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  ShieldX,
  FileCode,
  Clock,
  ExternalLink,
  MessageSquare,
  CheckCircle2,
  AlertTriangle,
} from 'lucide-react';
import { SupportRequest, supportApi } from '@/lib/api/support';

interface SupportRequestTrackerProps {
  requests: SupportRequest[];
  onRefresh: () => void;
}

export const SupportRequestTracker: React.FC<SupportRequestTrackerProps> = ({
  requests,
  onRefresh,
}) => {
  const [selectedRequest, setSelectedRequest] = useState<SupportRequest | null>(null);
  const [troubleshootLoading, setTroubleshootLoading] = useState(false);
  const [troubleshootResult, setTroubleshootResult] = useState<any>(null);
  const [actionLoading, setActionLoading] = useState(false);

  const handleTroubleshoot = async (req: SupportRequest) => {
    setSelectedRequest(req);
    setTroubleshootLoading(true);
    try {
      const res = await supportApi.troubleshoot(req.id);
      setTroubleshootResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setTroubleshootLoading(false);
    }
  };

  const handleUpdateStatus = async (id: string, status: string) => {
    setActionLoading(true);
    try {
      await supportApi.updateStatus(id, { status, notes: `Status changed to ${status}` });
      onRefresh();
      if (selectedRequest?.id === id) {
        setSelectedRequest(null);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleRouteToChange = async (id: string) => {
    if (!confirm('Route this out-of-scope ticket to Phase 28 Change Management?')) return;
    setActionLoading(true);
    try {
      await supportApi.routeToChange(id, { notes: 'Routed to Change Request workflow.' });
      onRefresh();
      if (selectedRequest?.id === id) {
        setSelectedRequest(null);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleWarrantyDecision = async (id: string, approve: boolean) => {
    setActionLoading(true);
    try {
      await supportApi.evaluateWarranty(id, {
        approve_warranty: approve,
        exclusion_reason: approve ? undefined : 'Excluded: Third-party outage or custom modification outside baseline',
      });
      onRefresh();
    } catch (err) {
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <LifeBuoy className="w-5 h-5 text-cyan-400" />
              Support Requests & Ticket Classification
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Deterministic categorization before work commences — defect vs support vs change request
            </p>
          </div>
          <span className="text-xs font-semibold px-3 py-1 bg-slate-800 text-slate-300 rounded-full border border-slate-700">
            {requests.length} Total Tickets
          </span>
        </div>

        {requests.length === 0 ? (
          <div className="text-center py-12 border border-dashed border-slate-800 rounded-xl">
            <LifeBuoy className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <p className="text-sm text-slate-400">No support tickets reported yet.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="pb-3 px-3">Ticket / Title</th>
                  <th className="pb-3 px-3">Classification</th>
                  <th className="pb-3 px-3">Priority</th>
                  <th className="pb-3 px-3">Status</th>
                  <th className="pb-3 px-3">Warranty</th>
                  <th className="pb-3 px-3">SLA Status</th>
                  <th className="pb-3 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {requests.map((req) => (
                  <tr key={req.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3.5 px-3">
                      <div className="font-semibold text-white">{req.title}</div>
                      <div className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">{req.description}</div>
                    </td>
                    <td className="py-3.5 px-3">
                      <span className={`inline-flex items-center gap-1 font-mono text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                        req.classification === 'DEFECT'
                          ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                          : req.classification === 'CHANGE_REQUEST'
                          ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30'
                          : req.classification === 'INCIDENT'
                          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                          : 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                      }`}>
                        {req.classification}
                      </span>
                    </td>
                    <td className="py-3.5 px-3">
                      <span className={`font-semibold ${
                        req.priority === 'CRITICAL' ? 'text-red-400' : req.priority === 'HIGH' ? 'text-amber-400' : 'text-slate-300'
                      }`}>
                        {req.priority}
                      </span>
                    </td>
                    <td className="py-3.5 px-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                        {req.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-3">
                      {req.warranty_status === 'COVERED' ? (
                        <span className="inline-flex items-center gap-1 text-[10px] text-emerald-400 font-semibold bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                          <ShieldCheck className="w-3 h-3" /> Covered
                        </span>
                      ) : req.warranty_status === 'NOT_COVERED' ? (
                        <span className="inline-flex items-center gap-1 text-[10px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded border border-slate-700">
                          <ShieldX className="w-3 h-3" /> Excluded
                        </span>
                      ) : (
                        <div className="flex items-center gap-1">
                          <button
                            onClick={() => handleWarrantyDecision(req.id, true)}
                            className="text-[10px] px-1.5 py-0.5 bg-emerald-600/30 hover:bg-emerald-600/50 text-emerald-300 rounded"
                          >
                            Approve
                          </button>
                          <button
                            onClick={() => handleWarrantyDecision(req.id, false)}
                            className="text-[10px] px-1.5 py-0.5 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded"
                          >
                            Exclude
                          </button>
                        </div>
                      )}
                    </td>
                    <td className="py-3.5 px-3">
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                        req.sla_status === 'PAUSED'
                          ? 'bg-amber-500/20 text-amber-400'
                          : req.sla_status === 'BREACHED'
                          ? 'bg-red-500/20 text-red-400'
                          : 'bg-emerald-500/20 text-emerald-400'
                      }`}>
                        {req.sla_status}
                      </span>
                    </td>
                    <td className="py-3.5 px-3 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          onClick={() => handleTroubleshoot(req)}
                          className="px-2.5 py-1 text-[11px] bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 rounded flex items-center gap-1 transition"
                        >
                          <Sparkles className="w-3 h-3" /> AI Diagnose
                        </button>
                        {req.classification === 'CHANGE_REQUEST' && req.status !== 'RESOLVED' && (
                          <button
                            onClick={() => handleRouteToChange(req.id)}
                            className="px-2.5 py-1 text-[11px] bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 border border-purple-500/30 rounded flex items-center gap-1 transition"
                          >
                            Route Change
                          </button>
                        )}
                        {req.status === 'NEW' && (
                          <button
                            onClick={() => handleUpdateStatus(req.id, 'IN_PROGRESS')}
                            className="px-2.5 py-1 text-[11px] bg-cyan-600/20 hover:bg-cyan-600/40 text-cyan-300 border border-cyan-500/30 rounded transition"
                          >
                            Triage
                          </button>
                        )}
                        {req.status === 'IN_PROGRESS' && (
                          <button
                            onClick={() => handleUpdateStatus(req.id, 'RESOLVED')}
                            className="px-2.5 py-1 text-[11px] bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 rounded transition"
                          >
                            Resolve
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>


      {/* AI Diagnostic Modal */}
      {selectedRequest && troubleshootResult && (
        <div className="bg-slate-900 border border-indigo-500/40 rounded-xl p-6 shadow-2xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              AI Diagnostic Troubleshooting: {selectedRequest.title}
            </h3>
            <button
              onClick={() => {
                setSelectedRequest(null);
                setTroubleshootResult(null);
              }}
              className="text-xs text-slate-400 hover:text-white"
            >
              Close
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
              <p className="font-semibold text-amber-400 mb-2">Likely Root Causes</p>
              <ul className="space-y-1 text-slate-300 list-disc list-inside">
                {troubleshootResult.possible_root_causes?.map((c: string, idx: number) => (
                  <li key={idx}>{c}</li>
                ))}
              </ul>
            </div>

            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
              <p className="font-semibold text-emerald-400 mb-2">Recommended Troubleshooting Steps</p>
              <ul className="space-y-1 text-slate-300 list-disc list-inside">
                {troubleshootResult.suggested_steps?.map((s: string, idx: number) => (
                  <li key={idx}>{s}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800 text-xs flex items-center justify-between">
            <span className="text-slate-400">
              AI Confidence: {(troubleshootResult.confidence * 100).toFixed(0)}% • Prevention Tips:{' '}
              {troubleshootResult.prevention_tips?.join(', ')}
            </span>
            <button
              onClick={() => handleUpdateStatus(selectedRequest.id, 'IN_REPAIR')}
              className="px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-white rounded text-xs font-semibold"
            >
              Move to In Repair
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
