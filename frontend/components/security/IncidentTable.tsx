'use client';

import React from 'react';
import { SecurityIncidentItem } from '@/lib/api/securityOps';
import { ShieldAlert, Compass, Users, Layers, ExternalLink } from 'lucide-react';

interface IncidentTableProps {
  incidents: SecurityIncidentItem[];
  loading: boolean;
  onOpenWorkspace: (incidentId: string) => void;
  onOpenBlastRadius: (incidentId: string) => void;
}

export default function IncidentTable({
  incidents,
  loading,
  onOpenWorkspace,
  onOpenBlastRadius,
}: IncidentTableProps) {
  const getSeverityBadge = (severity: string) => {
    const s = severity.toLowerCase();
    if (s === 'critical') return 'bg-rose-100 text-rose-800 border-rose-300';
    if (s === 'high') return 'bg-orange-100 text-orange-800 border-orange-300';
    return 'bg-amber-100 text-amber-800 border-amber-300';
  };

  const getStatusBadge = (status: string) => {
    const st = status.toLowerCase();
    if (st === 'detected') return 'bg-rose-50 text-rose-700 border-rose-200';
    if (st === 'investigating') return 'bg-amber-50 text-amber-700 border-amber-200';
    if (st === 'contained') return 'bg-blue-50 text-blue-700 border-blue-200';
    if (st === 'closed') return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    return 'bg-slate-50 text-slate-700 border-slate-200';
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-rose-600" />
            Confirmed Security Incidents
          </h3>
          <p className="text-xs text-slate-500">
            Coordinated containment, root-cause investigations, and blast radius quantification (Sections 18-23)
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-700">
          <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-y border-slate-200">
            <tr>
              <th className="py-2.5 px-3">Incident ID</th>
              <th className="py-2.5 px-3">Title & Scope</th>
              <th className="py-2.5 px-3">Severity</th>
              <th className="py-2.5 px-3">Status</th>
              <th className="py-2.5 px-3">Affected Entities</th>
              <th className="py-2.5 px-3">Lead Owner</th>
              <th className="py-2.5 px-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  Loading incidents...
                </td>
              </tr>
            ) : incidents.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  Zero open security incidents.
                </td>
              </tr>
            ) : (
              incidents.map((inc) => (
                <tr key={inc.incident_id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3 px-3 font-mono font-bold text-indigo-700 whitespace-nowrap">
                    {inc.incident_id}
                  </td>
                  <td className="py-3 px-3">
                    <div className="font-semibold text-slate-900">{inc.title}</div>
                    <div className="text-[11px] text-slate-500 line-clamp-1">{inc.description}</div>
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${getSeverityBadge(inc.severity)}`}>
                      {inc.severity.toUpperCase()}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${getStatusBadge(inc.status)}`}>
                      {inc.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-600">
                    <div className="flex items-center gap-1.5 text-[11px]">
                      <Users className="w-3.5 h-3.5 text-slate-400" />
                      <span>{inc.affected_users.length} users</span>
                      <span className="text-slate-300">•</span>
                      <span>{inc.affected_services.length} services</span>
                    </div>
                  </td>
                  <td className="py-3 px-3 text-slate-700 font-medium">
                    {inc.owner || 'Unassigned'}
                  </td>
                  <td className="py-3 px-3 text-right space-x-1.5 whitespace-nowrap">
                    <button
                      onClick={() => onOpenBlastRadius(inc.incident_id)}
                      className="px-2.5 py-1 text-[11px] font-medium rounded-md bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors inline-flex items-center gap-1"
                    >
                      <Layers className="w-3 h-3" /> Blast Radius
                    </button>
                    <button
                      onClick={() => onOpenWorkspace(inc.incident_id)}
                      className="px-2.5 py-1 text-[11px] font-medium rounded-md bg-indigo-600 text-white hover:bg-indigo-700 transition-colors inline-flex items-center gap-1 shadow-xs"
                    >
                      <Compass className="w-3 h-3" /> Workspace
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
