'use client';

import React from 'react';
import { ShieldCheck, ShieldAlert, LifeBuoy, AlertOctagon, Wrench, Sparkles, Activity } from 'lucide-react';

interface SupportDashboardOverviewProps {
  activeTicketsCount: number;
  openIncidentsCount: number;
  activeWarrantyCount: number;
  healthScore: number;
  healthStatus: string;
  maintenanceOrdersDueCount: number;
  slaComplianceRate?: number;
  onRunDiagnostics?: () => void;
}

export const SupportDashboardOverview: React.FC<SupportDashboardOverviewProps> = ({
  activeTicketsCount,
  openIncidentsCount,
  activeWarrantyCount,
  healthScore,
  healthStatus,
  maintenanceOrdersDueCount,
  slaComplianceRate = 98.5,
  onRunDiagnostics,
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Active Support Tickets */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400 font-medium">Active Support Tickets</p>
          <p className="text-2xl font-black text-white mt-1">{activeTicketsCount}</p>
          <p className="text-[10px] text-cyan-400 mt-0.5">SLA Compliance: {slaComplianceRate}%</p>
        </div>
        <div className="p-3 bg-cyan-500/10 border border-cyan-500/20 rounded-xl text-cyan-400">
          <LifeBuoy className="w-6 h-6" />
        </div>
      </div>

      {/* Operational Incidents */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400 font-medium">Active Incidents</p>
          <p className="text-2xl font-black text-white mt-1">
            <span className={openIncidentsCount > 0 ? 'text-red-400' : 'text-emerald-400'}>
              {openIncidentsCount}
            </span>
          </p>
          <p className="text-[10px] text-slate-500 mt-0.5">
            {openIncidentsCount > 0 ? 'Critical response active' : 'Zero active outages'}
          </p>
        </div>
        <div className={`p-3 rounded-xl border ${
          openIncidentsCount > 0
            ? 'bg-red-500/10 border-red-500/20 text-red-400'
            : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
        }`}>
          <AlertOctagon className="w-6 h-6" />
        </div>
      </div>

      {/* Warranty & Maintenance */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400 font-medium">Warranty & Maintenance</p>
          <p className="text-2xl font-black text-white mt-1">{activeWarrantyCount} Active</p>
          <p className="text-[10px] text-amber-400 mt-0.5">{maintenanceOrdersDueCount} work orders pending</p>
        </div>
        <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl text-amber-400">
          <Wrench className="w-6 h-6" />
        </div>
      </div>

      {/* Client Health Score */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400 font-medium">Client Health Index</p>
          <div className="flex items-center gap-2 mt-1">
            <p className="text-2xl font-black text-white">{healthScore.toFixed(0)}/100</p>
            <span className={`text-[10px] px-2 py-0.5 rounded font-semibold uppercase ${
              healthStatus === 'HEALTHY'
                ? 'bg-emerald-500/20 text-emerald-400'
                : healthStatus === 'AT_RISK'
                ? 'bg-amber-500/20 text-amber-400'
                : 'bg-red-500/20 text-red-400'
            }`}>
              {healthStatus}
            </span>
          </div>
          <p className="text-[10px] text-slate-500 mt-0.5">Automated telemetry scoring</p>
        </div>
        <div className="p-3 bg-purple-500/10 border border-purple-500/20 rounded-xl text-purple-400">
          <Activity className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
};
