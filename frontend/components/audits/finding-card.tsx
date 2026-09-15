"use client";

import React from "react";
import { AlertCircle, AlertTriangle, Info, CheckCircle, ExternalLink } from "lucide-react";
import { AuditFinding } from "@/lib/api/audits";

interface FindingCardProps {
  finding: AuditFinding;
}

export function FindingCard({ finding }: FindingCardProps) {
  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case "HIGH":
        return "bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 border-rose-200";
      case "MEDIUM":
        return "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-200";
      case "LOW":
        return "bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border-blue-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300 border-gray-200";
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "HIGH":
        return <AlertCircle className="w-4 h-4 text-rose-600 dark:text-rose-400" />;
      case "MEDIUM":
        return <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400" />;
      case "LOW":
        return <Info className="w-4 h-4 text-blue-600 dark:text-blue-400" />;
      default:
        return <CheckCircle className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />;
    }
  };

  return (
    <div className="p-4 rounded-xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm space-y-2">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-2">
          {getSeverityIcon(finding.severity)}
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                {finding.category}
              </span>
              <span className="text-xs font-mono text-gray-400">({finding.code})</span>
            </div>
            <h4 className="text-sm font-bold text-gray-900 dark:text-gray-100 mt-0.5">
              {finding.title}
            </h4>
          </div>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          <span className={`px-2 py-0.5 text-[10px] font-bold rounded border ${getSeverityBadge(finding.severity)}`}>
            {finding.severity}
          </span>
          <span className="px-2 py-0.5 text-[10px] font-semibold rounded bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300">
            {finding.confidence} CONFIDENCE
          </span>
        </div>
      </div>

      <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
        {finding.description}
      </p>

      {finding.evidence && Object.keys(finding.evidence).length > 0 && (
        <div className="text-[11px] bg-gray-50 dark:bg-gray-800/60 p-2.5 rounded-lg border border-gray-100 dark:border-gray-800 space-y-1">
          <span className="font-semibold text-gray-500 dark:text-gray-400 uppercase text-[10px]">Evidence:</span>
          <pre className="text-gray-800 dark:text-gray-200 font-mono text-[11px] whitespace-pre-wrap overflow-x-auto">
            {JSON.stringify(finding.evidence, null, 2)}
          </pre>
        </div>
      )}

      {finding.affected_page && (
        <div className="flex items-center justify-between text-[11px] text-gray-500 dark:text-gray-400 pt-1 border-t border-gray-100 dark:border-gray-800">
          <span>Affected Page:</span>
          <a
            href={finding.affected_page}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-indigo-600 dark:text-indigo-400 hover:underline font-mono text-[11px]"
          >
            <span>{finding.affected_page}</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      )}
    </div>
  );
}
