"use client";

import React from "react";
import { AlertTriangle, ExternalLink } from "lucide-react";
import { ResearchConflict } from "@/lib/api/research";

interface ConflictAlertProps {
  conflict: ResearchConflict;
}

export function ConflictAlert({ conflict }: ConflictAlertProps) {
  return (
    <div className="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/50 space-y-3">
      <div className="flex items-center gap-2 text-amber-900 dark:text-amber-200 font-bold text-sm">
        <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
        <span>Conflicting Evidence: {conflict.field_name.replace(/_/g, " ")}</span>
      </div>

      <p className="text-xs text-amber-800 dark:text-amber-300">
        Multiple research sources returned conflicting values for this field. Operator review is recommended.
      </p>

      <div className="space-y-2">
        {conflict.competing_values.map((v, idx) => (
          <div
            key={idx}
            className="p-2.5 rounded bg-white dark:bg-gray-800 border border-amber-200 dark:border-amber-900/30 flex items-center justify-between text-xs"
          >
            <div>
              <div className="font-semibold text-gray-900 dark:text-gray-100">{v.value}</div>
              <div className="text-[10px] text-gray-500 dark:text-gray-400 mt-0.5">
                Confidence: {v.confidence} • Observed:{" "}
                {v.observed_at ? new Date(v.observed_at).toLocaleDateString() : "Unknown"}
              </div>
            </div>
            {v.source_url && (
              <a
                href={v.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-amber-700 dark:text-amber-400 hover:underline flex items-center gap-1 shrink-0"
              >
                <span>Source</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
