"use client";

import React from "react";
import { ComponentScore } from "@/lib/api/scoring";

interface ScoreBreakdownCardProps {
  breakdown: Record<string, ComponentScore>;
}

const COMPONENT_LABELS: Record<string, { title: string; weightLabel: string }> = {
  website_need: { title: "Website Need", weightLabel: "25% Weight" },
  online_presence: { title: "Online Presence", weightLabel: "15% Weight" },
  lead_capture: { title: "Lead Capture Opportunity", weightLabel: "15% Weight" },
  automation_potential: { title: "Automation Potential", weightLabel: "20% Weight" },
  business_activity: { title: "Business Activity", weightLabel: "10% Weight" },
  contactability: { title: "Contactability", weightLabel: "10% Weight" },
  service_fit: { title: "Service Fit", weightLabel: "5% Weight" },
};

export function ScoreBreakdownCard({ breakdown }: ScoreBreakdownCardProps) {
  if (!breakdown || Object.keys(breakdown).length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <h4 className="text-sm font-bold text-gray-900 dark:text-gray-100">
        Weighted Dimension Breakdown
      </h4>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {Object.entries(breakdown).map(([key, item]) => {
          const meta = COMPONENT_LABELS[key] || {
            title: key.replace(/_/g, " ").toUpperCase(),
            weightLabel: `${Math.round((item.weight || 0) * 100)}% Weight`,
          };
          const roundedScore = Math.round(item.score);

          return (
            <div
              key={key}
              className="p-3.5 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-800 space-y-2"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-gray-800 dark:text-gray-200">
                  {meta.title}
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] text-gray-500 font-mono">
                    {meta.weightLabel}
                  </span>
                  <span className="font-bold font-mono text-indigo-600 dark:text-indigo-400">
                    {roundedScore} / 100
                  </span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-gray-200 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                <div
                  className={`h-2 rounded-full transition-all duration-300 ${
                    roundedScore >= 80
                      ? "bg-emerald-500"
                      : roundedScore >= 60
                      ? "bg-indigo-500"
                      : roundedScore >= 40
                      ? "bg-amber-500"
                      : "bg-gray-400"
                  }`}
                  style={{ width: `${roundedScore}%` }}
                />
              </div>

              <div className="flex items-center justify-between text-[11px] text-gray-500 dark:text-gray-400 pt-1">
                <span>Contribution: +{item.weighted_contribution} pts</span>
                {item.status && <span className="uppercase text-[10px]">{item.status}</span>}
              </div>

              {item.reasons && item.reasons.length > 0 && (
                <ul className="text-[11px] text-gray-600 dark:text-gray-300 list-disc pl-4 space-y-0.5 pt-1 border-t border-gray-100 dark:border-gray-800/50">
                  {item.reasons.map((r, idx) => (
                    <li key={idx}>{r}</li>
                  ))}
                </ul>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
