"use client";

import React from "react";
import { Globe, ShieldCheck, Activity, Smartphone, Phone, Mail, Clock, ExternalLink } from "lucide-react";
import { BusinessAudit } from "@/lib/api/audits";

interface AuditOverviewProps {
  audit: BusinessAudit;
}

export function AuditOverview({ audit }: AuditOverviewProps) {
  const getHealthBadge = (health: string) => {
    switch (health) {
      case "HEALTHY":
        return "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20";
      case "FAIR":
        return "bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20";
      case "NEEDS_ATTENTION":
        return "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20";
      default:
        return "bg-gray-500/10 text-gray-600 dark:text-gray-400 border-gray-500/20";
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "AVAILABLE":
        return "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300";
      case "NO_WEBSITE":
        return "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300";
      default:
        return "bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300";
    }
  };

  const metrics = audit.metrics || {};

  return (
    <div className="p-6 rounded-2xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-gray-100 dark:border-gray-800">
        <div>
          <div className="flex items-center gap-2">
            <Globe className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
              Website & Digital Presence Overview
            </h3>
          </div>
          {audit.target_url ? (
            <a
              href={audit.target_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline inline-flex items-center gap-1 mt-1 font-mono"
            >
              <span>{audit.target_url}</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          ) : (
            <span className="text-xs text-gray-400 mt-1 block">No Website Target</span>
          )}
        </div>

        <div className="flex items-center gap-2">
          <span className={`px-3 py-1 text-xs font-bold rounded-full border ${getHealthBadge(audit.overall_health)}`}>
            {audit.overall_health.replace(/_/g, " ")}
          </span>
          <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusBadge(audit.status)}`}>
            {audit.status}
          </span>
        </div>
      </div>

      {audit.summary && (
        <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
          {audit.summary}
        </p>
      )}

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
          <div className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase">
            Pages Analyzed
          </div>
          <div className="text-xl font-bold text-gray-900 dark:text-gray-100 mt-1">
            {metrics.pages_analyzed ?? 0}
          </div>
        </div>

        <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
          <div className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase">
            HTTPS Security
          </div>
          <div className="text-sm font-bold text-gray-900 dark:text-gray-100 mt-1">
            {metrics.https_enabled ? "Enabled" : "Not Observed"}
          </div>
        </div>

        <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
          <div className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase">
            Contact Form
          </div>
          <div className="text-sm font-bold text-gray-900 dark:text-gray-100 mt-1">
            {metrics.contact_form_detected ? "Detected" : "Missing"}
          </div>
        </div>

        <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
          <div className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase">
            Mobile Viewport
          </div>
          <div className="text-sm font-bold text-gray-900 dark:text-gray-100 mt-1">
            {metrics.viewport_present ? "Good Signal" : "Warning"}
          </div>
        </div>

        <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
          <div className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase">
            Social Profiles
          </div>
          <div className="text-xl font-bold text-gray-900 dark:text-gray-100 mt-1">
            {metrics.social_links_count ?? 0}
          </div>
        </div>

        <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
          <div className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase">
            Call To Actions
          </div>
          <div className="text-xl font-bold text-gray-900 dark:text-gray-100 mt-1">
            {metrics.cta_count ?? 0}
          </div>
        </div>

        <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
          <div className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase">
            Images Missing ALT
          </div>
          <div className="text-xl font-bold text-gray-900 dark:text-gray-100 mt-1">
            {metrics.images_without_alt ?? 0}
          </div>
        </div>

        <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
          <div className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase">
            Avg Response
          </div>
          <div className="text-xl font-bold text-gray-900 dark:text-gray-100 mt-1">
            {metrics.average_response_time_ms ? `${metrics.average_response_time_ms} ms` : "N/A"}
          </div>
        </div>
      </div>
    </div>
  );
}
