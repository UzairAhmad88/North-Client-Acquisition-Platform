"use client";

import React from "react";
import { IncidentRecord } from "@/lib/api/engineeringOs";

interface Props {
  incidents: IncidentRecord[];
}

export const IncidentSreObservabilityRadar: React.FC<Props> = ({ incidents }) => {
  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">SRE, Observability & Incident Response</h2>
          <p className="text-xs text-slate-400">
            SEV0–SEV4 incident lifecycle, 5-Whys RCA, timeline tracking, and postmortem remediation
          </p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded bg-rose-950/60 text-rose-400 border border-rose-800/50 font-mono">
          {incidents.filter((i) => i.status !== "RESOLVED").length} Active Incidents
        </span>
      </div>

      <div className="space-y-3 mt-4">
        {incidents.length === 0 ? (
          <div className="text-center py-6 text-slate-500 text-xs">
            All systems operational. No active or past incidents recorded.
          </div>
        ) : (
          incidents.map((inc) => (
            <div
              key={inc.incident_id}
              className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4 hover:border-slate-600 transition"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                <div className="flex items-center gap-2">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      inc.severity === "SEV0" || inc.severity === "SEV1"
                        ? "bg-rose-950 text-rose-300 border border-rose-800"
                        : inc.severity === "SEV2"
                        ? "bg-amber-950 text-amber-300 border border-amber-800"
                        : "bg-slate-800 text-slate-300 border border-slate-700"
                    }`}
                  >
                    {inc.severity}
                  </span>
                  <span className="font-semibold text-slate-100 text-sm">{inc.title}</span>
                </div>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                    inc.status === "RESOLVED"
                      ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                      : "bg-rose-950 text-rose-400 border border-rose-800"
                  }`}
                >
                  {inc.status}
                </span>
              </div>

              <div className="text-xs text-slate-400 mb-2">{inc.customer_impact}</div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-[11px] bg-slate-900/60 p-2.5 rounded border border-slate-800/80">
                <div>
                  <span className="text-slate-500">Affected Services:</span>{" "}
                  <span className="text-slate-200 font-mono">
                    {inc.affected_services?.join(", ") || "None"}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500">Responders:</span>{" "}
                  <span className="text-slate-200">{inc.responders?.join(", ") || "Unassigned"}</span>
                </div>
                <div>
                  <span className="text-slate-500">Postmortem:</span>{" "}
                  <span className={inc.postmortem_completed ? "text-emerald-400 font-bold" : "text-amber-400 font-bold"}>
                    {inc.postmortem_completed ? "Completed & Published" : "Pending 5-Whys RCA"}
                  </span>
                </div>
              </div>

              {inc.mitigation_strategy && (
                <div className="mt-2 text-[11px] text-slate-300">
                  <span className="text-slate-500 font-medium">Mitigation:</span> {inc.mitigation_strategy}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
