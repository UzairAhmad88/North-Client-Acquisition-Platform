'use client';

import React, { useState } from 'react';
import { ReliabilityIncident, IncidentPostmortem } from '@/lib/api/reliability';

interface Props {
  incidents: ReliabilityIncident[];
  onDeclareIncident: (data: Partial<ReliabilityIncident>) => void;
  onAcknowledge: (id: string) => void;
  onMitigate: (id: string) => void;
  onResolve: (id: string) => void;
  onViewPostmortem: (incidentId: string) => void;
}

export function IncidentManager({
  incidents,
  onDeclareIncident,
  onAcknowledge,
  onMitigate,
  onResolve,
  onViewPostmortem,
}: Props) {
  const [showDeclareModal, setShowDeclareModal] = useState(false);
  const [title, setTitle] = useState('');
  const [severity, setSeverity] = useState('SEV2_MAJOR');
  const [affectedServices, setAffectedServices] = useState('database, payments');
  const [impactSummary, setImpactSummary] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !impactSummary) return;

    onDeclareIncident({
      title,
      severity: severity as any,
      affected_services: affectedServices.split(',').map((s) => s.trim()),
      impact_summary: impactSummary,
    });

    setTitle('');
    setImpactSummary('');
    setShowDeclareModal(false);
  };

  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case 'SEV1_CRITICAL':
        return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      case 'SEV2_MAJOR':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      case 'SEV3_MODERATE':
        return 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40';
      default:
        return 'bg-slate-500/20 text-slate-300 border-slate-500/40';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Incident Lifecycle & Blameless Postmortems</h3>
          <p className="text-xs text-slate-400">
            SEV-1 through SEV-4 command center with five-whys and structured resolution runbooks
          </p>
        </div>

        <button
          onClick={() => setShowDeclareModal(true)}
          className="px-4 py-2 bg-rose-600/80 hover:bg-rose-600 text-white text-xs font-semibold rounded-xl transition shadow-lg shadow-rose-900/30 flex items-center gap-2"
        >
          <span>🚨</span> Declare Incident
        </button>
      </div>

      {/* Incidents Table / List */}
      <div className="space-y-3">
        {incidents.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-xs border border-dashed border-slate-800 rounded-xl">
            No active or historical incidents recorded. Platform nominal.
          </div>
        ) : (
          incidents.map((inc) => {
            const isResolved = inc.status === 'RESOLVED' || inc.status === 'CLOSED';
            return (
              <div
                key={inc.id}
                className="bg-slate-950/60 border border-slate-800/80 p-4 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getSeverityBadge(inc.severity)}`}>
                      {inc.severity}
                    </span>
                    <span className="text-xs font-semibold text-white">{inc.title}</span>
                    <span className="text-[10px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded-full">
                      {inc.status}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400">{inc.impact_summary}</div>
                  <div className="text-[10px] text-slate-500 flex items-center gap-3">
                    <span>Services: {inc.affected_services?.join(', ') || 'N/A'}</span>
                    <span>•</span>
                    <span>Started: {new Date(inc.started_at).toLocaleString()}</span>
                  </div>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  {inc.status === 'TRIGGERED' && (
                    <button
                      onClick={() => onAcknowledge(inc.id)}
                      className="px-3 py-1.5 bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 text-xs rounded-lg transition"
                    >
                      Acknowledge
                    </button>
                  )}
                  {(inc.status === 'TRIGGERED' || inc.status === 'ACKNOWLEDGED' || inc.status === 'INVESTIGATING') && (
                    <button
                      onClick={() => onMitigate(inc.id)}
                      className="px-3 py-1.5 bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 border border-cyan-500/30 text-xs rounded-lg transition"
                    >
                      Mark Mitigated
                    </button>
                  )}
                  {inc.status === 'MITIGATED' && (
                    <button
                      onClick={() => onResolve(inc.id)}
                      className="px-3 py-1.5 bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 text-xs rounded-lg transition"
                    >
                      Resolve Incident
                    </button>
                  )}
                  {isResolved && (
                    <button
                      onClick={() => onViewPostmortem(inc.id)}
                      className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs rounded-lg transition"
                    >
                      Postmortem
                    </button>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Modal to declare incident */}
      {showDeclareModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl max-w-lg w-full space-y-4">
            <h4 className="text-lg font-bold text-white flex items-center gap-2">
              <span>🚨</span> Declare Reliability Incident
            </h4>
            <form onSubmit={handleSubmit} className="space-y-3">
              <div>
                <label className="block text-xs text-slate-400 mb-1">Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Primary DB Replica Connection Timeout"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white"
                  required
                />
              </div>

              <div>
                <label className="block text-xs text-slate-400 mb-1">Severity</label>
                <select
                  value={severity}
                  onChange={(e) => setSeverity(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white"
                >
                  <option value="SEV1_CRITICAL">SEV1 - Critical Outage (Customer facing)</option>
                  <option value="SEV2_MAJOR">SEV2 - Major Degradation (High error rate)</option>
                  <option value="SEV3_MODERATE">SEV3 - Moderate Subsystem Issue</option>
                  <option value="SEV4_LOW">SEV4 - Minor / Cosmetic / Non-urgent</option>
                </select>
              </div>

              <div>
                <label className="block text-xs text-slate-400 mb-1">Affected Services (comma-separated)</label>
                <input
                  type="text"
                  value={affectedServices}
                  onChange={(e) => setAffectedServices(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="block text-xs text-slate-400 mb-1">Impact Summary</label>
                <textarea
                  value={impactSummary}
                  onChange={(e) => setImpactSummary(e.target.value)}
                  placeholder="Briefly describe what is failing and user impact..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white h-20"
                  required
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowDeclareModal(false)}
                  className="px-4 py-2 bg-slate-800 text-slate-300 text-xs rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold rounded-lg"
                >
                  Declare Incident
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
