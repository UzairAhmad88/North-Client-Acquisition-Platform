"use client";

import React, { useState } from "react";
import { DataSourceItem, DataPipelineItem, DataDomainItem } from "@/lib/api/enterpriseDataOs";

interface Props {
  sources: DataSourceItem[];
  pipelines: DataPipelineItem[];
  domains: DataDomainItem[];
}

export const DataSourcesPipelinesPanel: React.FC<Props> = ({ sources, pipelines, domains }) => {
  const [activeTab, setActiveTab] = useState<"sources" | "pipelines" | "domains">("sources");

  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Data Sources, Pipelines & Domain Taxonomy</h2>
          <p className="text-xs text-slate-400">
            Source connectivity, zero-credential secret isolation, batch/streaming DAG pipelines, and domains
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800/80 p-1 rounded-lg border border-slate-700/50">
          <button
            onClick={() => setActiveTab("sources")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "sources"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Sources ({sources.length})
          </button>
          <button
            onClick={() => setActiveTab("pipelines")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "pipelines"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Pipelines ({pipelines.length})
          </button>
          <button
            onClick={() => setActiveTab("domains")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "domains"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Domains ({domains.length})
          </button>
        </div>
      </div>

      <div className="mt-4">
        {activeTab === "sources" && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/50 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">Source Name</th>
                  <th className="p-3">Type / Provider</th>
                  <th className="p-3">Endpoint</th>
                  <th className="p-3">Auth Isolation</th>
                  <th className="p-3">Reliability</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {sources.map((src) => (
                  <tr key={src.source_id} className="hover:bg-slate-800/30 transition">
                    <td className="p-3 font-medium text-slate-100 flex items-center gap-2">
                      <span className="font-mono text-indigo-400">{src.name}</span>
                    </td>
                    <td className="p-3 text-slate-300">
                      {src.source_type} ({src.provider})
                    </td>
                    <td className="p-3 font-mono text-[11px] text-slate-400">{src.connection_endpoint}</td>
                    <td className="p-3">
                      <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-emerald-400 border border-emerald-900 font-mono">
                        {src.auth_type} (Zero Raw Secrets)
                      </span>
                    </td>
                    <td className="p-3 font-mono font-bold text-emerald-400">{src.reliability_score}%</td>
                    <td className="p-3">
                      <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold">
                        {src.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === "pipelines" && (
          <div className="space-y-3">
            {pipelines.map((pipe) => (
              <div
                key={pipe.pipeline_id}
                className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-3.5 flex flex-col md:flex-row items-start md:items-center justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-100 text-sm">{pipe.name}</span>
                    <span className="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded font-mono">
                      {pipe.schedule_type}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    Owner: {pipe.owner_team} · Target: <span className="font-mono text-indigo-300">{pipe.target_dataset}</span> · SLA: {pipe.sla_minutes} min
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-[11px] bg-emerald-950/80 text-emerald-400 border border-emerald-800/50 px-2.5 py-1 rounded font-mono font-bold">
                    ✓ {pipe.last_run_status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "domains" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {domains.map((dom) => (
              <div
                key={dom.domain_id}
                className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4 hover:border-slate-600 transition"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-slate-100 text-sm">{dom.name}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-950 text-indigo-400 border border-indigo-800 font-mono">
                    {dom.slug}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mb-3">{dom.description}</p>
                <div className="flex justify-between items-center text-[11px] text-slate-500 pt-2 border-t border-slate-800">
                  <span>Owner: {dom.owner_team}</span>
                  <span className="text-slate-300">{dom.lead_steward_email}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
