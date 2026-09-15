"use client";

import React from "react";
import { RoadmapBoard } from "@/lib/api/productOs";

interface Props {
  roadmap: RoadmapBoard | null;
}

export const PrioritizationRoadmapBoardView: React.FC<Props> = ({ roadmap }) => {
  if (!roadmap) return null;

  const columns = [
    { title: "Now (Current Sprint / Quarter)", key: "NOW", items: roadmap.horizons.NOW, color: "border-cyan-500/40" },
    { title: "Next (Upcoming Horizon)", key: "NEXT", items: roadmap.horizons.NEXT, color: "border-indigo-500/40" },
    { title: "Later (Strategic Roadmap)", key: "LATER", items: roadmap.horizons.LATER, color: "border-slate-700" },
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Multi-Horizon Roadmap & Prioritization</h2>
          <p className="text-xs text-slate-400">
            Governed initiative sequencing with RICE / WSJF ranking and dependency verification
          </p>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 text-slate-300">
          Total Initiatives: {roadmap.total_initiatives}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {columns.map((col) => (
          <div key={col.key} className={`bg-slate-950/70 border ${col.color} rounded-lg p-3 space-y-3`}>
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-xs font-semibold text-slate-300">{col.title}</span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                {col.items.length}
              </span>
            </div>

            <div className="space-y-2">
              {col.items.length === 0 ? (
                <div className="text-xs text-slate-600 italic text-center py-4">No initiatives scheduled</div>
              ) : (
                col.items.map((item: any) => (
                  <div
                    key={item.item_id}
                    className="p-3 bg-slate-900/80 border border-slate-800 rounded-lg space-y-1.5 hover:border-slate-700 transition"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium text-slate-200">{item.title}</span>
                      <span className="text-[10px] font-mono text-cyan-400">
                        {item.target_quarter || "Q3"}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono pt-1">
                      <span>Effort: {item.engineering_effort_weeks} wks</span>
                      <span>Confidence: {item.confidence}%</span>
                    </div>
                    {item.dependencies?.length > 0 && (
                      <div className="text-[10px] text-amber-400/90 font-mono">
                        Dependencies: {item.dependencies.length} items
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
