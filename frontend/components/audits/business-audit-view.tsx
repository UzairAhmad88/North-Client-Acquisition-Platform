"use client";

import React, { useEffect, useState } from "react";
import {
  Globe,
  Play,
  RotateCw,
  AlertTriangle,
  History,
  CheckCircle2,
  ListFilter,
} from "lucide-react";
import {
  BusinessAudit,
  BusinessAuditHistory,
  createAuditJob,
  getBusinessAuditHistory,
  getLatestBusinessAudit,
  runAuditJob,
} from "@/lib/api/audits";
import { AuditOverview } from "./audit-overview";
import { FindingCard } from "./finding-card";

interface BusinessAuditViewProps {
  businessId: string;
  businessWebsite?: string | null;
}

export function BusinessAuditView({ businessId, businessWebsite }: BusinessAuditViewProps) {
  const [history, setHistory] = useState<BusinessAuditHistory | null>(null);
  const [latestAudit, setLatestAudit] = useState<BusinessAudit | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [running, setRunning] = useState<boolean>(false);
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchAuditData = async () => {
    try {
      setLoading(true);
      setErrorMsg(null);
      const histData = await getBusinessAuditHistory(businessId);
      setHistory(histData);
      setLatestAudit(histData.latest_audit || null);
    } catch (err: any) {
      if (err?.status === 404) {
        setLatestAudit(null);
      } else {
        setErrorMsg("Failed to load website audit data.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAuditData();
  }, [businessId]);

  const handleRunAudit = async () => {
    try {
      setRunning(true);
      setErrorMsg(null);
      const job = await createAuditJob({ business_id: businessId });
      await runAuditJob(job.id, "MOCK");
      await fetchAuditData();
    } catch (err: any) {
      setErrorMsg("Failed to execute website audit.");
    } finally {
      setRunning(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-center bg-white dark:bg-gray-850 rounded-2xl border border-gray-200 dark:border-gray-800">
        <RotateCw className="w-6 h-6 text-indigo-600 dark:text-indigo-400 animate-spin mx-auto mb-2" />
        <p className="text-sm text-gray-500">Loading website audit record...</p>
      </div>
    );
  }

  const categories = [
    "ALL",
    "SECURITY",
    "SEO",
    "MOBILE",
    "LEAD_CAPTURE",
    "SOCIAL",
    "BUSINESS_INFORMATION",
    "TECHNICAL",
    "CONTENT",
  ];

  const filteredFindings = latestAudit?.findings
    ? selectedCategory === "ALL"
      ? latestAudit.findings
      : latestAudit.findings.filter((f) => f.category === selectedCategory)
    : [];

  return (
    <div className="space-y-6">
      {/* Top Action Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400">
            <Globe className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-gray-900 dark:text-gray-100">
              Website & Digital Presence Audit Engine
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Evidence-backed technical, security, SEO, mobile & lead capture analysis
            </p>
          </div>
        </div>

        <button
          onClick={handleRunAudit}
          disabled={running}
          className="inline-flex items-center justify-center gap-2 px-4 py-2.5 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 rounded-xl transition shadow-sm"
        >
          {running ? (
            <>
              <RotateCw className="w-4 h-4 animate-spin" />
              <span>Analyzing Website...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4" />
              <span>Run Website Audit</span>
            </>
          )}
        </button>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 text-xs text-rose-700 dark:text-rose-300">
          {errorMsg}
        </div>
      )}

      {/* Audit State View */}
      {!latestAudit ? (
        <div className="p-12 text-center bg-white dark:bg-gray-850 rounded-2xl border border-gray-200 dark:border-gray-800 space-y-4">
          <Globe className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto" />
          <div>
            <h4 className="text-base font-bold text-gray-900 dark:text-gray-100">
              No Audit Performed Yet
            </h4>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 max-w-md mx-auto">
              Run a website audit to evaluate publicly accessible digital presence, security headers, mobile signals, SEO baselines, and lead capture mechanisms.
            </p>
          </div>
          <button
            onClick={handleRunAudit}
            disabled={running}
            className="inline-flex items-center gap-2 px-4 py-2 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition"
          >
            <Play className="w-3.5 h-3.5" />
            <span>Run Initial Audit</span>
          </button>
        </div>
      ) : (
        <>
          {/* Overview Component */}
          <AuditOverview audit={latestAudit} />

          {/* Findings Section */}
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <h4 className="text-sm font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
                <ListFilter className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                <span>Audit Findings ({filteredFindings.length})</span>
              </h4>

              {/* Category Filters */}
              <div className="flex items-center gap-1 overflow-x-auto pb-1 max-w-full">
                {categories.map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`px-2.5 py-1 text-[11px] font-bold rounded-lg transition whitespace-nowrap ${
                      selectedCategory === cat
                        ? "bg-indigo-600 text-white"
                        : "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
                    }`}
                  >
                    {cat.replace(/_/g, " ")}
                  </button>
                ))}
              </div>
            </div>

            {filteredFindings.length === 0 ? (
              <div className="p-6 text-center bg-white dark:bg-gray-850 rounded-xl border border-gray-200 dark:border-gray-800 text-xs text-gray-500">
                No findings reported under category "{selectedCategory.replace(/_/g, " ")}".
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredFindings.map((finding) => (
                  <FindingCard key={finding.id} finding={finding} />
                ))}
              </div>
            )}
          </div>

          {/* Audit History Timeline */}
          {history && history.audits.length > 0 && (
            <div className="p-6 rounded-2xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 space-y-4">
              <div className="flex items-center gap-2 text-sm font-bold text-gray-900 dark:text-gray-100">
                <History className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                <span>Audit Version History ({history.total_audits})</span>
              </div>

              <div className="space-y-2">
                {history.audits.map((a) => (
                  <div
                    key={a.id}
                    className="flex items-center justify-between p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 text-xs text-gray-700 dark:text-gray-300"
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-mono font-bold text-indigo-600 dark:text-indigo-400">
                        v{a.audit_version}
                      </span>
                      <span>{a.summary}</span>
                    </div>

                    <div className="flex items-center gap-3 text-[11px] text-gray-500">
                      <span className="font-semibold text-gray-800 dark:text-gray-200">
                        {a.overall_health}
                      </span>
                      <span>
                        {a.completed_at
                          ? new Date(a.completed_at).toLocaleDateString()
                          : new Date(a.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
