'use client';

import React from 'react';
import { BusinessHealthReport } from '@/lib/api/business_os';

interface BusinessHealthProps {
  healthReport: BusinessHealthReport;
}

export const BusinessHealth: React.FC<BusinessHealthProps> = ({ healthReport }) => {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'HEALTHY':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'STABLE':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'WATCH':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'AT_RISK':
        return 'bg-orange-500/10 text-orange-400 border-orange-500/30';
      case 'CRITICAL':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      default:
        return 'bg-slate-500/10 text-slate-400 border-slate-500/30';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span>🏥</span> 10-Dimension Business Health Index
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Explainable organizational health composite with positive & negative driver attribution.
          </p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-black text-emerald-400">
            {Number(healthReport.overall_health_score).toFixed(1)}
            <span className="text-sm font-normal text-slate-400"> / 100</span>
          </div>
          <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold border mt-1 ${getStatusBadge(healthReport.overall_status)}`}>
            {healthReport.overall_status}
          </span>
        </div>
      </div>

      {/* 10 Dimensions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(healthReport.dimensions || {}).map(([key, dim]) => (
          <div key={key} className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-slate-200 text-sm">{dim.dimension_name}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getStatusBadge(dim.status)}`}>
                {Number(dim.score).toFixed(1)} ({dim.status})
              </span>
            </div>

            {/* Drivers */}
            <div className="mt-2 space-y-1 text-xs">
              {dim.positive_drivers.map((d, i) => (
                <div key={i} className="text-emerald-400/90 flex items-start gap-1">
                  <span className="text-emerald-500 font-bold">✓</span> {d}
                </div>
              ))}
              {dim.negative_drivers.map((d, i) => (
                <div key={i} className="text-rose-400/90 flex items-start gap-1">
                  <span className="text-rose-500 font-bold">⚠</span> {d}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
