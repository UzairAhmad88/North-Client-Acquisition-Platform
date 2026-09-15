'use client';

import React from 'react';
import { SecurityDetectionItem } from '@/lib/api/securityOps';
import { Crosshair, ExternalLink, ShieldAlert } from 'lucide-react';

interface DetectionTableProps {
  detections: SecurityDetectionItem[];
  loading: boolean;
  onRefresh: () => void;
}

export default function DetectionTable({ detections, loading, onRefresh }: DetectionTableProps) {
  const getSeverityBadge = (severity: string) => {
    const s = severity.toLowerCase();
    if (s === 'critical') return 'bg-rose-100 text-rose-800 border-rose-300';
    if (s === 'high') return 'bg-orange-100 text-orange-800 border-orange-300';
    if (s === 'medium') return 'bg-amber-100 text-amber-800 border-amber-300';
    return 'bg-slate-100 text-slate-700 border-slate-300';
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Crosshair className="w-5 h-5 text-rose-600" />
            Automated Threat Detections
          </h3>
          <p className="text-xs text-slate-500">
            Real-time detections evaluated against deterministic, threshold, and sequence rules (Sections 8-15)
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-full">
          {detections.length} Active Detections
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-700">
          <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-y border-slate-200">
            <tr>
              <th className="py-2.5 px-3">Rule Name</th>
              <th className="py-2.5 px-3">Anomaly Type</th>
              <th className="py-2.5 px-3">MITRE ATT&CK</th>
              <th className="py-2.5 px-3">Risk Score</th>
              <th className="py-2.5 px-3">Confidence</th>
              <th className="py-2.5 px-3">Severity</th>
              <th className="py-2.5 px-3">Detected At</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  Loading detections...
                </td>
              </tr>
            ) : detections.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  Zero active threats detected. Platform baseline secure.
                </td>
              </tr>
            ) : (
              detections.map((det) => (
                <tr key={det.detection_id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-2.5 px-3 font-semibold text-slate-900">
                    {det.rule_name}
                  </td>
                  <td className="py-2.5 px-3 font-mono text-[11px] text-slate-600">
                    {det.anomaly_type}
                  </td>
                  <td className="py-2.5 px-3">
                    {det.mitre_technique_id ? (
                      <span className="inline-flex items-center gap-1 font-mono text-[11px] bg-slate-100 text-slate-800 px-2 py-0.5 rounded border border-slate-200">
                        {det.mitre_technique_id}
                        <span className="text-[10px] text-slate-500">({det.mitre_tactic?.split('_')[1] || 'Tactics'})</span>
                      </span>
                    ) : (
                      <span className="text-slate-400">-</span>
                    )}
                  </td>
                  <td className="py-2.5 px-3 font-bold text-slate-800">
                    {det.risk_score} <span className="text-[10px] font-normal text-slate-400">/100</span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-600 font-medium">
                    {Math.round(det.confidence * 100)}%
                  </td>
                  <td className="py-2.5 px-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${getSeverityBadge(det.severity)}`}>
                      {det.severity.toUpperCase()}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-500 whitespace-nowrap">
                    {new Date(det.detected_at).toLocaleTimeString()}
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
