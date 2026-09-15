"use client";

import React, { useState } from "react";
import { CicdPipelineRecord, DeploymentRecord, ReleaseReadinessCheck } from "@/lib/api/engineeringOs";

interface Props {
  pipelines: CicdPipelineRecord[];
  deployments: DeploymentRecord[];
  readiness: ReleaseReadinessCheck | null;
}

export const CicdDeploymentReleaseBoard: React.FC<Props> = ({ pipelines, deployments, readiness }) => {
  const [activeTab, setActiveTab] = useState<"pipelines" | "deployments" | "readiness">("deployments");

  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">CI/CD, Deployments & 10-Point Release Gate</h2>
          <p className="text-xs text-slate-400">
            Pipeline workflows, artifact provenance, Canary/Blue-Green deployments, and release readiness verification
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800/80 p-1 rounded-lg border border-slate-700/50">
          <button
            onClick={() => setActiveTab("deployments")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "deployments"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Deployments ({deployments.length})
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
            onClick={() => setActiveTab("readiness")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "readiness"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Release Gate
          </button>
        </div>
      </div>

      <div className="mt-4">
        {activeTab === "deployments" && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/50 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">Application</th>
                  <th className="p-3">Version</th>
                  <th className="p-3">Environment</th>
                  <th className="p-3">Strategy</th>
                  <th className="p-3">Operator / Approval</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {deployments.map((dep) => (
                  <tr key={dep.deployment_id} className="hover:bg-slate-800/30 transition">
                    <td className="p-3 font-medium text-slate-100">{dep.application_name}</td>
                    <td className="p-3 font-mono text-indigo-400">{dep.version}</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded text-[11px] bg-slate-800 font-bold text-slate-300 border border-slate-700">
                        {dep.environment}
                      </span>
                    </td>
                    <td className="p-3 text-slate-400">{dep.strategy}</td>
                    <td className="p-3 text-slate-300">
                      <div>{dep.operator}</div>
                      <div className="text-[10px] text-slate-500 font-mono">{dep.approval_status}</div>
                    </td>
                    <td className="p-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          dep.status === "ACTIVE_HEALTHY" || dep.status === "SUCCESS"
                            ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                            : "bg-amber-950 text-amber-400 border border-amber-800"
                        }`}
                      >
                        {dep.status}
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
                className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-3 flex flex-col md:flex-row items-start md:items-center justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-100 text-sm">{pipe.name}</span>
                    <span className="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded font-mono">
                      {pipe.trigger_type}
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-400 mt-1">
                    Duration: {pipe.last_run_duration_sec}s · Pipeline ID: {pipe.pipeline_id}
                  </div>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  {pipe.stages.map((stg, i) => (
                    <div
                      key={i}
                      className={`px-2.5 py-1 rounded text-[11px] font-mono flex items-center gap-1.5 ${
                        stg.status === "PASSED"
                          ? "bg-emerald-950/80 text-emerald-400 border border-emerald-800/50"
                          : stg.status === "FAILED"
                          ? "bg-rose-950/80 text-rose-400 border border-rose-800/50"
                          : "bg-slate-800 text-slate-300"
                      }`}
                    >
                      <span>{stg.stage_name}</span>
                      <span className="text-[9px] opacity-75">({stg.duration_sec}s)</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "readiness" && (
          <div className="bg-slate-800/40 rounded-xl p-5 border border-slate-700/60">
            {readiness ? (
              <div>
                <div className="flex items-center justify-between pb-3 border-b border-slate-700/50 mb-4">
                  <div>
                    <h3 className="font-bold text-slate-100 text-base">
                      Release Readiness: {readiness.version}
                    </h3>
                    <p className="text-xs text-slate-400">
                      Automated 10-point governance gate verification
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-black text-emerald-400">
                      {readiness.readiness_score_pct}% Complete
                    </div>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                        readiness.ready_for_production
                          ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                          : "bg-rose-950 text-rose-400 border border-rose-800"
                      }`}
                    >
                      {readiness.ready_for_production ? "Ready for Production" : "Release Blocked"}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  {Object.entries(readiness.gate_checklist).map(([key, val]) => (
                    <div
                      key={key}
                      className={`p-2.5 rounded-lg border flex items-center justify-between ${
                        val
                          ? "bg-emerald-950/30 border-emerald-800/40 text-slate-200"
                          : "bg-rose-950/30 border-rose-800/40 text-rose-200"
                      }`}
                    >
                      <span className="capitalize">{key.replace(/_/g, " ")}</span>
                      <span className="font-bold font-mono">
                        {val ? "✓ PASSED" : "✗ BLOCKED"}
                      </span>
                    </div>
                  ))}
                </div>

                {readiness.blockers?.length > 0 && (
                  <div className="mt-4 p-3 bg-rose-950/50 border border-rose-800 rounded-lg text-xs text-rose-300">
                    <span className="font-bold">Active Blockers:</span>
                    <ul className="list-disc list-inside mt-1">
                      {readiness.blockers.map((b, i) => (
                        <li key={i}>{b}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center text-slate-500 py-6">No release readiness evaluated.</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
