"use client";

import React from "react";
import { TraceabilityEntry } from "@/lib/api/productOs";

interface Props {
  matrix: TraceabilityEntry[];
}

export const RequirementsTraceabilityMatrixView: React.FC<Props> = ({ matrix }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-slate-100">End-to-End Requirement Traceability Matrix</h2>
        <p className="text-xs text-slate-400">
          Unbroken lineage: Problem ➔ Insight ➔ Opportunity ➔ Initiative ➔ Requirement ➔ User Story ➔ Release
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 font-medium">
              <th className="py-2.5 px-3">Requirement</th>
              <th className="py-2.5 px-3">Type</th>
              <th className="py-2.5 px-3">Underlying Problem</th>
              <th className="py-2.5 px-3">Opportunity</th>
              <th className="py-2.5 px-3">Roadmap Item</th>
              <th className="py-2.5 px-3">User Stories</th>
              <th className="py-2.5 px-3 text-right">Health Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {matrix.map((row) => (
              <tr key={row.requirement_id} className="hover:bg-slate-800/30 transition">
                <td className="py-3 px-3">
                  <div className="font-medium text-slate-200">{row.requirement_title}</div>
                  <span className="text-[10px] text-slate-500 font-mono">{row.requirement_id}</span>
                </td>
                <td className="py-3 px-3 font-mono text-[11px] text-slate-400">
                  {row.requirement_type}
                </td>
                <td className="py-3 px-3">
                  <div className="text-slate-300 line-clamp-1">{row.problem.title}</div>
                  <span className="text-[10px] text-rose-400/90 font-mono">{row.problem.severity}</span>
                </td>
                <td className="py-3 px-3">
                  <div className="text-slate-300 line-clamp-1">{row.opportunity.title}</div>
                  <span className="text-[10px] text-emerald-400 font-mono">Score: {row.opportunity.score}/10</span>
                </td>
                <td className="py-3 px-3">
                  <div className="text-slate-300 line-clamp-1">{row.roadmap_initiative.title}</div>
                  <span className="text-[10px] text-cyan-400 font-mono">{row.roadmap_initiative.horizon}</span>
                </td>
                <td className="py-3 px-3">
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[11px]">
                    {row.user_stories.length} stories
                  </span>
                </td>
                <td className="py-3 px-3 text-right font-mono">
                  <span
                    className={`font-semibold ${
                      row.completeness_score >= 80
                        ? "text-emerald-400"
                        : row.completeness_score >= 50
                        ? "text-amber-400"
                        : "text-rose-400"
                    }`}
                  >
                    {row.completeness_score}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
