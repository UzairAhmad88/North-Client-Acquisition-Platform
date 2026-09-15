"use client";

import React from "react";
import Link from "next/link";
import { GitCommit, ArrowRight } from "lucide-react";
import { LeadPipelineSnapshot } from "@/lib/api/dashboard";

interface PipelineSnapshotProps {
  pipeline: LeadPipelineSnapshot;
}

const STAGES = [
  { key: "NEW", label: "New", color: "bg-blue-500" },
  { key: "RESEARCHING", label: "Researching", color: "bg-cyan-500" },
  { key: "QUALIFIED", label: "Qualified", color: "bg-emerald-500" },
  { key: "CONTACTED", label: "Contacted", color: "bg-amber-500" },
  { key: "RESPONDED", label: "Responded", color: "bg-indigo-500" },
  { key: "INTERESTED", label: "Interested", color: "bg-purple-500" },
  { key: "MEETING", label: "Meeting", color: "bg-pink-500" },
  { key: "PROPOSAL", label: "Proposal", color: "bg-violet-500" },
  { key: "WON", label: "Won", color: "bg-emerald-600" },
  { key: "LOST", label: "Lost", color: "bg-gray-400" },
];

export function PipelineSnapshot({ pipeline }: PipelineSnapshotProps) {
  const counts = pipeline.counts || {};
  const totalLeads = Object.values(counts).reduce((a, b) => a + b, 0);

  return (
    <div className="p-6 rounded-xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm">
      <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
        <div className="flex items-center gap-2">
          <GitCommit className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
          <h2 className="text-base font-bold text-gray-900 dark:text-gray-100">
            Lead Pipeline Snapshot
          </h2>
        </div>
        <Link
          href="/leads"
          className="text-xs font-medium text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
        >
          <span>View all leads</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      <div className="mt-4">
        {totalLeads === 0 ? (
          <div className="py-6 text-center text-sm text-gray-500 dark:text-gray-400">
            No leads currently in the pipeline.
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
            {STAGES.map((s) => {
              const count = counts[s.key] || 0;
              const pct = totalLeads > 0 ? Math.round((count / totalLeads) * 100) : 0;
              return (
                <Link
                  key={s.key}
                  href={`/leads?status=${s.key}`}
                  className="p-3 rounded-lg border border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/40 hover:border-indigo-300 dark:hover:border-indigo-700 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-gray-600 dark:text-gray-400">
                      {s.label}
                    </span>
                    <span
                      className={`w-2 h-2 rounded-full ${s.color}`}
                      title={`${pct}% of total`}
                    />
                  </div>
                  <div className="text-xl font-bold text-gray-900 dark:text-gray-100 mt-1">
                    {count}
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1 mt-2 overflow-hidden">
                    <div
                      className={`h-full ${s.color} transition-all duration-300`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
