'use client';

import React from 'react';
import { VendorProfileItem } from '@/lib/api/governance';
import { Building2, Network, ShieldCheck, AlertTriangle } from 'lucide-react';

interface VendorRiskTableProps {
  vendors: VendorProfileItem[];
}

export default function VendorRiskTable({ vendors }: VendorRiskTableProps) {
  const getCriticalityBadge = (crit: string) => {
    switch (crit) {
      case 'CRITICAL':
        return <span className="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-bold">CRITICAL</span>;
      case 'HIGH':
        return <span className="px-2 py-0.5 rounded bg-orange-100 text-orange-800 font-bold">HIGH</span>;
      case 'MEDIUM':
        return <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold">MEDIUM</span>;
      default:
        return <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-bold">LOW</span>;
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Building2 className="w-5 h-5 text-indigo-600" />
            <span>Third-Party & Vendor Risk Management (TPRM)</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Vendor profiles, data access tiers, and architectural blast-radius dependency mapping.
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg">
          {vendors.length} Vendors Monitored
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
              <th className="p-3.5">Vendor Code</th>
              <th className="p-3.5">Vendor Name & Service</th>
              <th className="p-3.5">Criticality</th>
              <th className="p-3.5">Data Access Level</th>
              <th className="p-3.5">Security / Privacy Risk</th>
              <th className="p-3.5">Dependent Subsystems</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {vendors.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-6 text-center text-slate-400">
                  No third-party vendors cataloged.
                </td>
              </tr>
            ) : (
              vendors.map((v) => (
                <tr key={v.vendor_code} className="hover:bg-slate-50/70 transition-colors">
                  <td className="p-3.5 font-mono font-bold text-slate-900">{v.vendor_code}</td>
                  <td className="p-3.5">
                    <div className="font-semibold text-slate-900">{v.name}</div>
                    <div className="text-[11px] text-slate-500">{v.service_provided}</div>
                  </td>
                  <td className="p-3.5">{getCriticalityBadge(v.criticality)}</td>
                  <td className="p-3.5">
                    <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-semibold text-[10px]">
                      {v.data_access_level}
                    </span>
                  </td>
                  <td className="p-3.5">
                    <div className="text-slate-800 font-medium">Sec: {v.security_risk}</div>
                    <div className="text-[11px] text-slate-500">Priv: {v.privacy_risk}</div>
                  </td>
                  <td className="p-3.5 max-w-xs">
                    <div className="flex flex-wrap gap-1">
                      {v.dependent_services.map((svc, i) => (
                        <span
                          key={i}
                          className="px-1.5 py-0.5 bg-indigo-50 text-indigo-700 font-mono text-[10px] rounded border border-indigo-100"
                        >
                          {svc}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="p-3.5 font-semibold text-emerald-700">{v.status}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
