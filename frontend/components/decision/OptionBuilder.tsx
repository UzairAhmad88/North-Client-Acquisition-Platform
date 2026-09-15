"use client";

import React from "react";
import { DecisionOption } from "@/lib/api/decision_rooms";
import { CheckCircle, DollarSign, AlertCircle, RefreshCw, Zap } from "lucide-react";

interface Props {
  options: DecisionOption[];
  onSelectOption?: (optionId: string) => void;
  selectedOptionId?: string;
}

export const OptionBuilder: React.FC<Props> = ({ options, onSelectOption, selectedOptionId }) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white">Candidate Alternatives & Decision Options</h3>
          <p className="text-xs text-slate-400">Exhaustive option formulation with composite scoring and reversibility ratings.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {options.map((opt) => (
          <div
            key={opt.id}
            className={`bg-slate-900 border rounded-xl p-5 transition-all ${
              selectedOptionId === opt.id
                ? "border-emerald-500/50 bg-emerald-950/10 shadow-lg shadow-emerald-950/20"
                : "border-slate-800 hover:border-slate-700"
            }`}
          >
            <div className="flex items-start justify-between gap-3 mb-2">
              <div>
                <h4 className="text-base font-bold text-white">{opt.name}</h4>
                <p className="text-xs text-slate-400 mt-0.5">{opt.description}</p>
              </div>
              <div className="text-right">
                <div className="text-xs text-slate-400">Composite Score</div>
                <div className="text-xl font-extrabold text-indigo-400">{opt.composite_score}</div>
              </div>
            </div>

            {/* Benefits */}
            <div className="space-y-1.5 my-3">
              <div className="text-xs font-semibold text-slate-300">Key Benefits:</div>
              {opt.benefits.map((b, idx) => (
                <div key={idx} className="flex items-center gap-2 text-xs text-slate-300">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                  <span>{b}</span>
                </div>
              ))}
            </div>

            {/* Metrics footer */}
            <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span className="flex items-center gap-1 font-mono text-slate-300">
                <DollarSign className="w-3.5 h-3.5 text-slate-400" />
                Cost: ${opt.costs.toLocaleString()}
              </span>
              <span className="px-2 py-0.5 bg-slate-800 text-slate-300 rounded text-xs">
                {opt.reversibility}
              </span>
              {onSelectOption && (
                <button
                  onClick={() => onSelectOption(opt.id)}
                  className={`px-3 py-1 rounded text-xs font-semibold transition ${
                    selectedOptionId === opt.id
                      ? "bg-emerald-600 text-white cursor-default"
                      : "bg-indigo-600 hover:bg-indigo-500 text-white"
                  }`}
                >
                  {selectedOptionId === opt.id ? "Selected Option" : "Select for Decision"}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
