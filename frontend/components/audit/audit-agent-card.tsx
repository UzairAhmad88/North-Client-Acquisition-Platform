"use client";

import React, { useState } from "react";
import {
  Bot,
  Play,
  ShieldCheck,
  Lock,
  Clock,
  Sparkles,
  Search,
} from "lucide-react";
import { runAuditAgentJob, createAuditJob } from "@/lib/api/audits";

interface AuditAgentCardProps {
  businessId: string;
  businessName: string;
  onJobStarted?: () => void;
}

export function AuditAgentCard({ businessId, businessName, onJobStarted }: AuditAgentCardProps) {
  const [running, setRunning] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const handleRunAgent = async () => {
    try {
      setRunning(true);
      setStatusMessage("Initializing Audit Agent runtime context...");

      // 1. Create Audit Job
      const job = await createAuditJob({
        business_id: businessId,
        pages_requested: 10,
      });

      setStatusMessage("Executing Audit Agent digital presence inspection...");

      // 2. Run Audit Agent via API
      await runAuditAgentJob(job.id);

      setStatusMessage("Audit Agent completed successfully!");
      if (onJobStarted) {
        onJobStarted();
      }
    } catch (err: any) {
      setStatusMessage(`Error: ${err?.message || "Failed to execute Audit Agent"}`);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="p-6 rounded-2xl bg-gradient-to-br from-indigo-900/10 via-purple-900/5 to-transparent dark:from-indigo-950/40 dark:via-purple-950/20 border border-indigo-200/80 dark:border-indigo-800/60 shadow-sm space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-start gap-3">
          <div className="p-3 rounded-xl bg-indigo-600 text-white shadow-md shadow-indigo-500/20">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
                North's Audit Agent
              </h3>
              <span className="px-2.5 py-0.5 text-[10px] font-extrabold uppercase tracking-wider rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
                Phase 16 Registered
              </span>
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-300 mt-1 max-w-xl">
              Autonomous digital presence audit engine. Analyzes website availability, HTTPS, mobile signals, SEO baselines, lead capture CTAs, and information consistency.
            </p>
          </div>
        </div>

        <button
          onClick={handleRunAgent}
          disabled={running}
          className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs shadow-md transition-all duration-150 shrink-0"
        >
          {running ? (
            <>
              <Clock className="w-4 h-4 animate-spin" />
              <span>Running Audit Agent...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4 fill-current" />
              <span>Execute Audit Agent</span>
            </>
          )}
        </button>
      </div>

      {/* Permissions & Safety Badges */}
      <div className="pt-2 grid grid-cols-1 sm:grid-cols-3 gap-3 border-t border-gray-200/60 dark:border-gray-800/60 text-xs">
        <div className="p-2.5 rounded-lg bg-white/70 dark:bg-gray-900/60 border border-gray-200 dark:border-gray-800 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-500 shrink-0" />
          <div>
            <span className="font-semibold text-gray-800 dark:text-gray-200">Permissions:</span>
            <span className="text-gray-500 dark:text-gray-400 block text-[11px]">
              READ_AUDIT, FETCH_WEB, RUN_AUDIT
            </span>
          </div>
        </div>

        <div className="p-2.5 rounded-lg bg-white/70 dark:bg-gray-900/60 border border-gray-200 dark:border-gray-800 flex items-center gap-2">
          <Lock className="w-4 h-4 text-rose-500 shrink-0" />
          <div>
            <span className="font-semibold text-gray-800 dark:text-gray-200">Read-Only Guard:</span>
            <span className="text-gray-500 dark:text-gray-400 block text-[11px]">
              Zero form submission & zero outbound comms
            </span>
          </div>
        </div>

        <div className="p-2.5 rounded-lg bg-white/70 dark:bg-gray-900/60 border border-gray-200 dark:border-gray-800 flex items-center gap-2">
          <Clock className="w-4 h-4 text-indigo-500 shrink-0" />
          <div>
            <span className="font-semibold text-gray-800 dark:text-gray-200">Freshness Policy:</span>
            <span className="text-gray-500 dark:text-gray-400 block text-[11px]">
              Reuse data ≤ 7 days before crawling
            </span>
          </div>
        </div>
      </div>

      {/* Status banner */}
      {statusMessage && (
        <div className="p-3 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 flex items-center gap-2 text-xs font-medium text-indigo-900 dark:text-indigo-200">
          <Sparkles className="w-4 h-4 text-indigo-500 shrink-0 animate-pulse" />
          <span>{statusMessage}</span>
        </div>
      )}
    </div>
  );
}
