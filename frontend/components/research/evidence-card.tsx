"use client";

import React from "react";
import { CheckCircle2, AlertTriangle, ShieldCheck, ExternalLink, Clock } from "lucide-react";
import { ResearchRecord } from "@/lib/api/research";

interface EvidenceCardProps {
  record: ResearchRecord;
}

export function EvidenceCard({ record }: EvidenceCardProps) {
  const getConfidenceBadge = (confidence: string) => {
    switch (confidence) {
      case "HIGH":
        return "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200";
      case "MEDIUM":
        return "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300 border-gray-200";
    }
  };

  const getSourceTrustBadge = (trust: string) => {
    switch (trust) {
      case "OFFICIAL":
        return "bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300";
      case "HIGH_TRUST":
        return "bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300";
      default:
        return "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400";
    }
  };

  return (
    <div className="p-4 rounded-xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm space-y-2">
      <div className="flex items-center justify-between gap-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
          {record.field_name.replace(/_/g, " ")}
        </span>
        <div className="flex items-center gap-1.5">
          <span className={`px-2 py-0.5 text-[10px] font-bold rounded border ${getConfidenceBadge(record.confidence)}`}>
            {record.confidence} CONFIDENCE
          </span>
          <span className={`px-2 py-0.5 text-[10px] font-semibold rounded ${getSourceTrustBadge(record.source_trust)}`}>
            {record.source_trust}
          </span>
        </div>
      </div>

      <div className="text-sm font-bold text-gray-900 dark:text-gray-100 break-words">
        {record.normalized_value}
      </div>

      {record.evidence_text && (
        <p className="text-xs text-gray-600 dark:text-gray-400 italic bg-gray-50 dark:bg-gray-800/50 p-2 rounded">
          "{record.evidence_text}"
        </p>
      )}

      <div className="flex items-center justify-between text-[11px] text-gray-500 dark:text-gray-400 pt-1 border-t border-gray-100 dark:border-gray-800">
        <div className="flex items-center gap-1">
          <Clock className="w-3 h-3" />
          <span>Observed: {new Date(record.observed_at).toLocaleDateString()}</span>
        </div>

        {record.source_url && (
          <a
            href={record.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-indigo-600 dark:text-indigo-400 hover:underline"
          >
            <span>Source</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>
    </div>
  );
}
