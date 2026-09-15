"use client";

import React from "react";
import { ServiceCatalogItem } from "@/lib/api/engineeringOs";

interface Props {
  services: ServiceCatalogItem[];
}

export const ServiceApiArchitectureMap: React.FC<Props> = ({ services }) => {
  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Service Catalog & Architecture Graph</h2>
          <p className="text-xs text-slate-400">
            Microservices, OpenAPI specs, SLO targets, runtime dependencies, and cost attribution
          </p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded bg-indigo-950/60 text-indigo-400 border border-indigo-800/50 font-mono">
          {services.length} Microservices Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
        {services.map((svc) => (
          <div
            key={svc.service_id}
            className="bg-slate-800/40 border border-slate-700/60 rounded-lg p-4 hover:border-indigo-500/50 transition flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-slate-100 text-sm">{svc.name}</span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                    svc.health_state === "HEALTHY"
                      ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                      : svc.health_state === "DEGRADED"
                      ? "bg-amber-950 text-amber-400 border border-amber-800"
                      : "bg-rose-950 text-rose-400 border border-rose-800"
                  }`}
                >
                  {svc.health_state}
                </span>
              </div>

              <div className="text-xs text-slate-400 mb-3 space-y-1">
                <div className="flex justify-between">
                  <span>Owner:</span>
                  <span className="text-slate-200 font-medium">{svc.owner_team}</span>
                </div>
                <div className="flex justify-between">
                  <span>Runtime:</span>
                  <span className="text-slate-200 font-mono">{svc.runtime}</span>
                </div>
                <div className="flex justify-between">
                  <span>Environment:</span>
                  <span className="text-slate-200">{svc.environment}</span>
                </div>
              </div>

              <div className="bg-slate-900/80 rounded p-2.5 mb-3 border border-slate-800 text-xs">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-slate-400">SLO Target:</span>
                  <span className="font-mono text-emerald-400 font-bold">{svc.slo_target_pct}%</span>
                </div>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-slate-400">Current SLO:</span>
                  <span className="font-mono text-slate-200">{svc.current_slo_pct}%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">Budget Remaining:</span>
                  <span
                    className={`font-mono font-bold ${
                      svc.error_budget_remaining_pct < 20 ? "text-rose-400" : "text-emerald-400"
                    }`}
                  >
                    {svc.error_budget_remaining_pct}%
                  </span>
                </div>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-700/40 flex justify-between items-center text-[11px] text-slate-400">
              <span>Monthly Cost: ${svc.monthly_cost_usd.toLocaleString()}</span>
              <span className="text-indigo-400">
                {svc.dependencies?.length || 0} Downstream Deps
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
