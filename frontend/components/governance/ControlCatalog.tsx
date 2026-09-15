'use client';

import React, { useState } from 'react';
import { GovernanceControlItem } from '@/lib/api/governance';
import { Shield, Play, CheckCircle2, AlertTriangle, XCircle, HelpCircle } from 'lucide-react';

interface ControlCatalogProps {
  controls: GovernanceControlItem[];
  onTestControl: (controlCode: string) => void;
}

export default function ControlCatalog({ controls, onTestControl }: ControlCatalogProps) {
  const [selectedDomain, setSelectedDomain] = useState<string>('ALL');

  const domains = ['ALL', 'SECURITY', 'IDENTITY', 'PRIVACY', 'AI', 'OPERATIONS', 'RELIABILITY'];

  const filteredControls =
    selectedDomain === 'ALL'
      ? controls
      : controls.filter((c) => c.domain === selectedDomain);

  const getHealthBadge = (status: string) => {
    switch (status) {
      case 'HEALTHY':
        return (
          <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full font-bold">
            <CheckCircle2 className="w-3 h-3" /> Healthy
          </span>
        );
      case 'DEGRADED':
        return (
          <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 px-2.5 py-0.5 rounded-full font-bold">
            <AlertTriangle className="w-3 h-3" /> Degraded
          </span>
        );
      case 'FAILING':
        return (
          <span className="inline-flex items-center gap-1 text-rose-700 bg-rose-50 px-2.5 py-0.5 rounded-full font-bold">
            <XCircle className="w-3 h-3" /> Failing
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-slate-600 bg-slate-100 px-2.5 py-0.5 rounded-full font-bold">
            <HelpCircle className="w-3 h-3" /> Unknown
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Shield className="w-5 h-5 text-indigo-600" />
            <span>Operational Control Catalog</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Technical and administrative controls satisfying compliance obligations.
          </p>
        </div>

        {/* Domain Filter Pills */}
        <div className="flex items-center gap-1 overflow-x-auto max-w-full pb-1">
          {domains.map((dom) => (
            <button
              key={dom}
              onClick={() => setSelectedDomain(dom)}
              className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
                selectedDomain === dom
                  ? 'bg-indigo-600 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {dom}
            </button>
          ))}
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
              <th className="p-3.5">Code</th>
              <th className="p-3.5">Control Name & Objective</th>
              <th className="p-3.5">Domain</th>
              <th className="p-3.5">Type & Automation</th>
              <th className="p-3.5">Health</th>
              <th className="p-3.5">Implementations</th>
              <th className="p-3.5">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {filteredControls.map((ctrl) => (
              <tr key={ctrl.control_code} className="hover:bg-slate-50/70 transition-colors">
                <td className="p-3.5 font-mono font-bold text-slate-900">{ctrl.control_code}</td>
                <td className="p-3.5 max-w-xs">
                  <div className="font-semibold text-slate-900">{ctrl.name}</div>
                  <div className="text-[11px] text-slate-500 mt-0.5 line-clamp-1">{ctrl.objective}</div>
                </td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">
                    {ctrl.domain}
                  </span>
                </td>
                <td className="p-3.5">
                  <div className="font-medium text-slate-800">{ctrl.control_type}</div>
                  <div className="text-[11px] text-slate-500">{ctrl.automation_level}</div>
                </td>
                <td className="p-3.5">{getHealthBadge(ctrl.health_status)}</td>
                <td className="p-3.5 max-w-xs">
                  <div className="flex flex-wrap gap-1">
                    {ctrl.implementations.map((impl, idx) => (
                      <span
                        key={idx}
                        className="px-1.5 py-0.5 bg-indigo-50 text-indigo-700 font-mono text-[10px] rounded border border-indigo-100"
                      >
                        {impl}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="p-3.5">
                  <button
                    onClick={() => onTestControl(ctrl.control_code)}
                    className="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 text-slate-700 font-semibold rounded-lg transition-all"
                  >
                    <Play className="w-3 h-3" />
                    <span>Test</span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
