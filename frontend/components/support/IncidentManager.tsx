'use client';

import React, { useState } from 'react';
import {
  AlertOctagon,
  ShieldAlert,
  Clock,
  CheckCircle2,
  FileText,
  Activity,
  Plus,
} from 'lucide-react';
import { Incident, supportApi } from '@/lib/api/support';

interface IncidentManagerProps {
  incidents: Incident[];
  onRefresh: () => void;
}

export const IncidentManager: React.FC<IncidentManagerProps> = ({
  incidents,
  onRefresh,
}) => {
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  const [newStatus, setNewStatus] = useState('CONTAINMENT');
  const [statusMessage, setStatusMessage] = useState('');
  const [rootCause, setRootCause] = useState('');
  const [resolutionSummary, setResolutionSummary] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // New incident modal state
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');
  const [severity, setSeverity] = useState('SEV-2');

  const handleCreateIncident = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await supportApi.createIncident({
        title,
        summary,
        severity,
      });
      setShowCreateModal(false);
      setTitle('');
      setSummary('');
      onRefresh();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdateStatus = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedIncident) return;
    setSubmitting(true);
    try {
      await supportApi.updateIncidentStatus(selectedIncident.id, {
        status: newStatus,
        message: statusMessage || `Phase advanced to ${newStatus}`,
        root_cause: rootCause || undefined,
        resolution_summary: resolutionSummary || undefined,
      });
      setStatusMessage('');
      setRootCause('');
      setResolutionSummary('');
      const updated = await supportApi.getIncidentDetail(selectedIncident.id);
      setSelectedIncident(updated);
      onRefresh();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <AlertOctagon className="w-5 h-5 text-red-400" />
              Operational Incidents & Severity Governance
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              SEV-1 (Outage) through SEV-4 (Degraded) incident command with timeline audits & postmortems
            </p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-3.5 py-1.5 bg-red-600 hover:bg-red-500 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-lg shadow-red-950/40 transition"
          >
            <Plus className="w-4 h-4" /> Declare Incident
          </button>
        </div>

        {incidents.length === 0 ? (
          <div className="text-center py-12 border border-dashed border-slate-800 rounded-xl">
            <CheckCircle2 className="w-10 h-10 text-emerald-500 mx-auto mb-3" />
            <p className="text-sm text-slate-300 font-semibold">Zero Active Incidents</p>
            <p className="text-xs text-slate-500 mt-1">All production systems operational within SLA.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {incidents.map((inc) => (
              <div
                key={inc.id}
                onClick={() => setSelectedIncident(inc)}
                className={`p-4 rounded-xl border cursor-pointer transition ${
                  selectedIncident?.id === inc.id
                    ? 'bg-slate-800/90 border-red-500/50 shadow-lg'
                    : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className={`text-[10px] font-black px-2 py-0.5 rounded border ${
                    inc.severity === 'SEV-1'
                      ? 'bg-red-500/20 text-red-400 border-red-500/30'
                      : inc.severity === 'SEV-2'
                      ? 'bg-orange-500/20 text-orange-400 border-orange-500/30'
                      : 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                  }`}>
                    {inc.severity}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400 bg-slate-900 px-2 py-0.5 rounded">
                    {inc.status}
                  </span>
                </div>
                <h4 className="text-sm font-bold text-white line-clamp-1">{inc.title}</h4>
                <p className="text-xs text-slate-400 line-clamp-2 mt-1">{inc.impact_summary || inc.description}</p>
                <div className="flex items-center justify-between text-[10px] text-slate-500 mt-3 pt-2 border-t border-slate-800/80">
                  <span>{inc.timelines?.length || 1} Timeline updates</span>
                  <span>{new Date(inc.detected_at || inc.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Incident Detail & Command Console */}
      {selectedIncident && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-2xl grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <span className="text-xs font-bold text-red-400 uppercase">{selectedIncident.severity}</span>
                <h3 className="text-base font-bold text-white mt-0.5">{selectedIncident.title}</h3>
              </div>
              <span className="text-xs font-mono px-3 py-1 bg-slate-800 text-slate-300 rounded border border-slate-700">
                Phase: {selectedIncident.status}
              </span>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs">
              <p className="font-semibold text-slate-300">Incident Summary</p>
              <p className="text-slate-400 mt-1">{selectedIncident.impact_summary || selectedIncident.description}</p>
              {selectedIncident.root_cause && (
                <div className="mt-3 pt-3 border-t border-slate-800">
                  <p className="font-semibold text-amber-400">Root Cause</p>
                  <p className="text-slate-300 mt-0.5">{selectedIncident.root_cause}</p>
                </div>
              )}
            </div>

            {/* Timeline Log */}
            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Incident Timeline</h4>
              <div className="space-y-3 pl-2 border-l-2 border-slate-800">
                {selectedIncident.timelines?.map((t) => (
                  <div key={t.id} className="relative pl-4 text-xs">
                    <div className="absolute -left-[1.35rem] top-1 w-2.5 h-2.5 rounded-full bg-red-400 ring-4 ring-slate-900" />
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-200">{t.milestone}</span>
                      <span className="text-[10px] text-slate-500">
                        {new Date(t.recorded_at).toLocaleTimeString()} ({t.recorded_by})
                      </span>
                    </div>
                    <p className="text-slate-400 mt-0.5">{t.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>


          {/* Incident Control Panel */}
          <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4 text-xs">
            <h4 className="font-bold text-white text-sm">Update Incident Status</h4>
            <form onSubmit={handleUpdateStatus} className="space-y-3">
              <div>
                <label className="block text-slate-400 mb-1">Advance Status Phase</label>
                <select
                  value={newStatus}
                  onChange={(e) => setNewStatus(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
                >
                  <option value="CONTAINMENT">CONTAINMENT</option>
                  <option value="ACTIVE_REMEDY">ACTIVE_REMEDY</option>
                  <option value="MONITORING">MONITORING</option>
                  <option value="RESOLVED">RESOLVED</option>
                  <option value="POSTMORTEM_COMPLETED">POSTMORTEM_COMPLETED</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Timeline Note</label>
                <textarea
                  rows={2}
                  value={statusMessage}
                  onChange={(e) => setStatusMessage(e.target.value)}
                  placeholder="Describe action taken..."
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200 text-xs"
                />
              </div>

              {newStatus === 'POSTMORTEM_COMPLETED' && (
                <div>
                  <label className="block text-slate-400 mb-1">Root Cause Analysis</label>
                  <textarea
                    rows={2}
                    value={rootCause}
                    onChange={(e) => setRootCause(e.target.value)}
                    placeholder="Document root cause..."
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200 text-xs"
                  />
                </div>
              )}

              <button
                type="submit"
                disabled={submitting}
                className="w-full py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg font-bold transition"
              >
                {submitting ? 'Updating...' : 'Publish Status Update'}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Declare Incident Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <AlertOctagon className="w-5 h-5 text-red-400" />
              Declare Operational Incident
            </h3>
            <form onSubmit={handleCreateIncident} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Incident Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Production API elevated 500 error rates"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1 font-semibold">Severity</label>
                  <select
                    value={severity}
                    onChange={(e) => setSeverity(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                  >
                    <option value="SEV-1">SEV-1 (Critical Outage)</option>
                    <option value="SEV-2">SEV-2 (Major Impact)</option>
                    <option value="SEV-3">SEV-3 (Moderate Degradation)</option>
                    <option value="SEV-4">SEV-4 (Minor Glitch)</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Summary & Impact</label>
                <textarea
                  required
                  rows={3}
                  value={summary}
                  onChange={(e) => setSummary(e.target.value)}
                  placeholder="Details regarding customer impact, affected services, and telemetry alerts..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                />
              </div>
              <div className="flex justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg font-bold"
                >
                  {submitting ? 'Declaring...' : 'Declare Incident'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
