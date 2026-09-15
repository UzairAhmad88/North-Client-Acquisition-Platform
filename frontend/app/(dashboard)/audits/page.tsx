"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { Globe, Play, RotateCw, CheckCircle2, AlertCircle, Clock } from "lucide-react";
import { listBusinesses } from "@/lib/api/businesses";
import {
  AuditJob,
  createAuditJob,
  listAuditJobs,
  runAuditJob,
} from "@/lib/api/audits";

import { AuditAgentCard } from "@/components/audit/audit-agent-card";

export default function AuditsPage() {
  const [jobs, setJobs] = useState<AuditJob[]>([]);
  const [totalJobs, setTotalJobs] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Launch state
  const [businesses, setBusinesses] = useState<any[]>([]);
  const [selectedBusinessId, setSelectedBusinessId] = useState("");
  const [runnerType, setRunnerType] = useState<"MOCK" | "REAL">("MOCK");
  const [starting, setStarting] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const [jobsRes, bizRes] = await Promise.all([
        listAuditJobs({ page: 1, page_size: 25 }),
        listBusinesses({ page: 1, page_size: 100 }),
      ]);
      setJobs(jobsRes.data);
      setTotalJobs(jobsRes.total);
      setBusinesses(bizRes.data);
    } catch (err: any) {
      setError(err?.message || "Failed to load website audit jobs.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleLaunchAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedBusinessId) return;

    try {
      setStarting(true);
      const job = await createAuditJob({
        business_id: selectedBusinessId,
      });
      await runAuditJob(job.id, runnerType);
      await fetchData();
      setSelectedBusinessId("");
    } catch (err: any) {
      alert(err?.message || "Failed to execute audit job");
    } finally {
      setStarting(false);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "COMPLETED":
        return "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300";
      case "RUNNING":
        return "bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 animate-pulse";
      case "PARTIAL":
        return "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300";
      case "FAILED":
        return "bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300";
    }
  };

  return (
    <main className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-gray-200 dark:border-gray-800">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
            <Globe className="w-4 h-4" />
            <span>Phase 11 — Website Audit System</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100 mt-1">
            Digital Presence & Technical Audit Engine
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
            Audit website availability, HTTPS configuration, mobile usability, SEO baselines, lead-capture CTAs, and business information consistency.
          </p>
        </div>

        <button
          onClick={fetchData}
          className="inline-flex items-center gap-2 px-3.5 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-750 transition-colors shadow-sm self-start sm:self-auto"
        >
          <RotateCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Phase 16 Audit Agent Card */}
      {selectedBusinessId && (
        <AuditAgentCard
          businessId={selectedBusinessId}
          businessName={businesses.find((b) => b.id === selectedBusinessId)?.name || "Selected Business"}
          onJobStarted={fetchData}
        />
      )}

      {/* Launch Card */}
      <div className="p-6 rounded-2xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm">
        <h2 className="text-base font-bold text-gray-900 dark:text-gray-100 mb-3">
          Launch Target Website Audit
        </h2>
        <form onSubmit={handleLaunchAudit} className="grid grid-cols-1 sm:grid-cols-4 gap-3 items-end">
          <div className="sm:col-span-2">
            <label className="text-xs font-semibold text-gray-700 dark:text-gray-300 block mb-1">
              Select Target Business
            </label>
            <select
              value={selectedBusinessId}
              onChange={(e) => setSelectedBusinessId(e.target.value)}
              required
              className="w-full text-xs p-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">-- Select a business to audit --</option>
              {businesses.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.name} ({b.website_url || "No website URL recorded"})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-gray-700 dark:text-gray-300 block mb-1">
              Audit Runner Mode
            </label>
            <select
              value={runnerType}
              onChange={(e) => setRunnerType(e.target.value as "MOCK" | "REAL")}
              className="w-full text-xs p-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500"
            >
              <option value="MOCK">Mock Audit Runner (Synthetic Analysis)</option>
              <option value="REAL">Real Web Audit Runner (SSRF Protected)</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={starting || !selectedBusinessId}
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition disabled:opacity-50"
          >
            <Play className="w-4 h-4" />
            <span>{starting ? "Auditing..." : "Run Audit"}</span>
          </button>
        </form>
      </div>

      {/* Jobs Table */}
      <div className="p-6 rounded-2xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm">
        <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
          <h2 className="text-base font-bold text-gray-900 dark:text-gray-100">
            Recent Audit Jobs ({totalJobs})
          </h2>
        </div>

        {jobs.length === 0 ? (
          <div className="py-12 text-center text-sm text-gray-500 dark:text-gray-400">
            No audit jobs executed yet. Select a target business above to run an audit.
          </div>
        ) : (
          <div className="overflow-x-auto mt-4">
            <table className="w-full text-left text-xs">
              <thead className="bg-gray-50 dark:bg-gray-800/50 text-gray-500 uppercase">
                <tr>
                  <th className="p-3">Job ID</th>
                  <th className="p-3">Target URL</th>
                  <th className="p-3">Status</th>
                  <th className="p-3">Pages Analyzed</th>
                  <th className="p-3">Findings</th>
                  <th className="p-3">Created</th>
                  <th className="p-3">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
                {jobs.map((job) => (
                  <tr key={job.id} className="hover:bg-gray-50/50 dark:hover:bg-gray-800/30">
                    <td className="p-3 font-mono text-gray-900 dark:text-gray-100">
                      {job.id.slice(0, 8)}...
                    </td>
                    <td className="p-3 font-mono text-indigo-600 dark:text-indigo-400 truncate max-w-[200px]">
                      {job.target_url || "N/A"}
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 font-semibold rounded-full ${getStatusBadge(job.status)}`}>
                        {job.status}
                      </span>
                    </td>
                    <td className="p-3 text-gray-700 dark:text-gray-300">{job.pages_analyzed}</td>
                    <td className="p-3 text-indigo-600 font-semibold">{job.findings_count}</td>
                    <td className="p-3 text-gray-500">
                      {new Date(job.created_at).toLocaleString()}
                    </td>
                    <td className="p-3">
                      <Link
                        href={`/businesses/${job.business_id}?tab=audit`}
                        className="font-semibold text-indigo-600 hover:underline"
                      >
                        View Audit Report
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
}
