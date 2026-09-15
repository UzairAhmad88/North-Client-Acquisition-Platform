"use client";

import React, { useState } from "react";
import { X, Search, Play, AlertCircle } from "lucide-react";
import { createResearchJob, runResearchJob, ResearchJob } from "@/lib/api/research";

interface ResearchJobModalProps {
  isOpen: boolean;
  onClose: () => void;
  businessId: string;
  businessName: string;
  onJobCompleted?: (job: ResearchJob) => void;
}

const AVAILABLE_SECTIONS = [
  { id: "IDENTITY", label: "Business Identity" },
  { id: "CONTACT", label: "Contact Channels (Email & Phone)" },
  { id: "LOCATION", label: "Location & Address" },
  { id: "SERVICES", label: "Known Services & Capabilities" },
  { id: "WEBSITE", label: "Website Metadata" },
  { id: "SOCIAL", label: "Social Media Presence" },
];

export function ResearchJobModal({
  isOpen,
  onClose,
  businessId,
  businessName,
  onJobCompleted,
}: ResearchJobModalProps) {
  const [selectedSections, setSelectedSections] = useState<string[]>(["ALL"]);
  const [providerType, setProviderType] = useState<"MOCK" | "WEB">("MOCK");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const toggleSection = (id: string) => {
    if (id === "ALL") {
      setSelectedSections(["ALL"]);
      return;
    }

    let updated = selectedSections.filter((s) => s !== "ALL");
    if (updated.includes(id)) {
      updated = updated.filter((s) => s !== id);
    } else {
      updated.push(id);
    }

    if (updated.length === 0) {
      updated = ["ALL"];
    }
    setSelectedSections(updated);
  };

  const handleStartResearch = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSubmitting(true);
      setError(null);

      // 1. Create Job
      const job = await createResearchJob({
        business_id: businessId,
        sections: selectedSections,
        provider_type: providerType,
      });

      // 2. Run Job
      const completedJob = await runResearchJob(job.id, providerType);

      if (onJobCompleted) {
        onJobCompleted(completedJob);
      }
      onClose();
    } catch (err: any) {
      setError(err?.message || "Failed to execute research job.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 rounded-2xl max-w-lg w-full p-6 shadow-xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 text-xs font-bold uppercase tracking-wider">
          <Search className="w-4 h-4" />
          <span>Research Engine</span>
        </div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 mt-1">
          Research Business: {businessName}
        </h2>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
          Select evidence sections and research provider to gather public facts.
        </p>

        {error && (
          <div className="mt-4 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/40 border border-rose-200 text-xs text-rose-700 dark:text-rose-300 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleStartResearch} className="mt-5 space-y-4">
          <div>
            <label className="text-xs font-semibold text-gray-700 dark:text-gray-300 block mb-2">
              Research Provider
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setProviderType("MOCK")}
                className={`p-3 rounded-xl border text-left text-xs transition-colors ${
                  providerType === "MOCK"
                    ? "border-indigo-600 bg-indigo-50/50 dark:bg-indigo-950/30 text-indigo-900 dark:text-indigo-200 font-semibold"
                    : "border-gray-200 dark:border-gray-800 text-gray-700 dark:text-gray-300"
                }`}
              >
                <div className="font-bold">Mock Provider</div>
                <div className="text-[11px] text-gray-500 mt-0.5">
                  Deterministic synthetic evidence for testing.
                </div>
              </button>

              <button
                type="button"
                onClick={() => setProviderType("WEB")}
                className={`p-3 rounded-xl border text-left text-xs transition-colors ${
                  providerType === "WEB"
                    ? "border-indigo-600 bg-indigo-50/50 dark:bg-indigo-950/30 text-indigo-900 dark:text-indigo-200 font-semibold"
                    : "border-gray-200 dark:border-gray-800 text-gray-700 dark:text-gray-300"
                }`}
              >
                <div className="font-bold">Web Scraper</div>
                <div className="text-[11px] text-gray-500 mt-0.5">
                  Safe live HTML parser with SSRF protection.
                </div>
              </button>
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-gray-700 dark:text-gray-300 block mb-2">
              Target Evidence Sections
            </label>
            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              <label className="flex items-center gap-2.5 p-2 rounded-lg bg-gray-50 dark:bg-gray-800 text-xs cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedSections.includes("ALL")}
                  onChange={() => toggleSection("ALL")}
                  className="rounded text-indigo-600 focus:ring-indigo-500"
                />
                <span className="font-bold text-gray-900 dark:text-gray-100">
                  ALL Sections (Comprehensive)
                </span>
              </label>

              {AVAILABLE_SECTIONS.map((sec) => (
                <label
                  key={sec.id}
                  className="flex items-center gap-2.5 p-2 rounded-lg border border-gray-100 dark:border-gray-800 text-xs cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  <input
                    type="checkbox"
                    checked={
                      selectedSections.includes("ALL") || selectedSections.includes(sec.id)
                    }
                    onChange={() => toggleSection(sec.id)}
                    className="rounded text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className="text-gray-800 dark:text-gray-200">{sec.label}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="pt-4 border-t border-gray-100 dark:border-gray-800 flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="inline-flex items-center gap-2 px-5 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5" />
              <span>{submitting ? "Gathering Evidence..." : "Start Research"}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
