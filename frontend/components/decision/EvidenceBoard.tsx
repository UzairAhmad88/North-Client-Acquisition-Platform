"use client";

import React from "react";
import { DecisionEvidence } from "@/lib/api/decision_rooms";
import { FileText, CheckCircle2, HelpCircle, AlertCircle, Database } from "lucide-react";

interface Props {
  evidence: DecisionEvidence[];
}

export const EvidenceBoard: React.FC<Props> = ({ evidence }) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white">Evidence Board & Grounding Layer</h3>
          <p className="text-xs text-slate-400">Strict separation of verified facts, statistical inferences, hypotheses, and unknowns.</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2 py-1 bg-emerald-500/10 text-emerald-400 text-xs rounded border border-emerald-500/20">
            FACT
          </span>
          <span className="px-2 py-1 bg-blue-500/10 text-blue-400 text-xs rounded border border-blue-500/20">
            INFERENCE
          </span>
          <span className="px-2 py-1 bg-amber-500/10 text-amber-400 text-xs rounded border border-amber-500/20">
            HYPOTHESIS
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {evidence.map((item) => (
          <div key={item.id} className="bg-slate-900 border border-slate-800 rounded-lg p-4 space-y-3">
            <div className="flex items-center justify-between">
              <span className={`px-2 py-0.5 rounded text-xs font-semibold uppercase tracking-wider ${
                item.statement_category === "FACT"
                  ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                  : item.statement_category === "INFERENCE"
                  ? "bg-blue-500/10 text-blue-400 border border-blue-500/20"
                  : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
              }`}>
                {item.statement_category}
              </span>
              <span className="text-xs text-slate-400 font-mono">
                Trust: {item.authority} ({Math.round(item.confidence * 100)}%)
              </span>
            </div>

            <p className="text-slate-200 text-sm font-medium leading-relaxed">
              "{item.claim}"
            </p>

            <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs text-slate-400">
              <span className="flex items-center gap-1">
                <Database className="w-3.5 h-3.5 text-slate-400" />
                Source: {item.source}
              </span>
              <span className="text-slate-400">{item.freshness}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
