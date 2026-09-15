"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Search, ShieldCheck, AlertCircle, RefreshCw, Layers, Calendar, CheckCircle2 } from "lucide-react";
import { getBusinessResearchProfile, BusinessResearchProfile } from "@/lib/api/research";
import { EvidenceCard } from "./evidence-card";
import { ConflictAlert } from "./conflict-alert";
import { ResearchJobModal } from "./research-job-modal";
import { ResearchAgentCard } from "./research-agent-card";

interface BusinessResearchViewProps {
  businessId: string;
  businessName: string;
}

export function BusinessResearchView({ businessId, businessName }: BusinessResearchViewProps) {
  const [profile, setProfile] = useState<BusinessResearchProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [activeFilter, setActiveFilter] = useState<string>("ALL");

  const fetchProfile = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getBusinessResearchProfile(businessId);
      setProfile(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load business research profile.");
    } finally {
      setLoading(false);
    }
  }, [businessId]);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  if (loading) {
    return (
      <div className="p-8 text-center text-sm text-gray-500 animate-pulse">
        Gathering research evidence & profile data...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 text-center">
        <AlertCircle className="w-6 h-6 text-rose-600 dark:text-rose-400 mx-auto mb-2" />
        <p className="text-sm font-semibold text-rose-900 dark:text-rose-200">{error}</p>
        <button
          onClick={fetchProfile}
          className="mt-3 px-3 py-1.5 text-xs font-semibold text-rose-900 bg-white border border-rose-300 rounded-lg hover:bg-rose-50"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!profile) return null;

  const records = profile.records || [];
  const filteredRecords =
    activeFilter === "ALL"
      ? records
      : records.filter((r) => r.research_type === activeFilter);

  return (
    <div className="space-y-6">
      {/* Overview Header Card */}
      <div className="p-6 rounded-xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
            <ShieldCheck className="w-4 h-4" />
            <span>Traceable Evidence Profile</span>
          </div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 mt-1">
            Research Profile: {businessName}
          </h2>
          <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400 mt-1">
            <span>Jobs: {profile.total_jobs}</span>
            <span>Total Evidence: {profile.total_records}</span>
            {profile.last_researched_at && (
              <span>Last Researched: {new Date(profile.last_researched_at).toLocaleDateString()}</span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-2xl font-extrabold text-indigo-600 dark:text-indigo-400">
              {profile.confidence_score}%
            </div>
            <div className="text-[10px] font-semibold uppercase text-gray-500 dark:text-gray-400">
              Confidence Score
            </div>
          </div>

          <button
            onClick={() => setIsModalOpen(true)}
            className="inline-flex items-center gap-2 px-4 py-2.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition-colors shadow-sm"
          >
            <Search className="w-4 h-4" />
            <span>Research Business</span>
          </button>
        </div>
      </div>

      {/* Phase 15 Research Agent Card */}
      <ResearchAgentCard
        businessId={businessId}
        businessName={businessName}
        onJobStarted={fetchProfile}
      />

      {/* Active Conflicts Section */}
      {profile.conflicts && profile.conflicts.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
            <span>Active Evidence Conflicts ({profile.conflicts.length})</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {profile.conflicts.map((c) => (
              <ConflictAlert key={c.id} conflict={c} />
            ))}
          </div>
        </div>
      )}

      {/* Filter Tabs & Evidence Cards Grid */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 overflow-x-auto pb-1 border-b border-gray-200 dark:border-gray-800">
          {[
            { id: "ALL", label: "All Evidence" },
            { id: "IDENTITY", label: "Identity" },
            { id: "CONTACT", label: "Contact" },
            { id: "LOCATION", label: "Location" },
            { id: "SERVICES", label: "Services" },
            { id: "WEBSITE", label: "Website" },
            { id: "SOCIAL", label: "Social" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveFilter(tab.id)}
              className={`px-3 py-1.5 text-xs font-medium rounded-lg whitespace-nowrap transition-colors ${
                activeFilter === tab.id
                  ? "bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-300 font-bold border border-indigo-200 dark:border-indigo-900/50"
                  : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {filteredRecords.length === 0 ? (
          <div className="p-12 text-center border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-xl">
            <Search className="w-8 h-8 text-gray-400 mx-auto mb-2" />
            <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">
              No Research Evidence Available
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 max-w-sm mx-auto">
              Run research on this business to collect public information with source provenance and confidence scores.
            </p>
            <button
              onClick={() => setIsModalOpen(true)}
              className="mt-4 px-4 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg"
            >
              Run Research
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredRecords.map((rec) => (
              <EvidenceCard key={rec.id} record={rec} />
            ))}
          </div>
        )}
      </div>

      {/* Research Modal */}
      <ResearchJobModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        businessId={businessId}
        businessName={businessName}
        onJobCompleted={fetchProfile}
      />
    </div>
  );
}
