"use client";

import React, { useState } from "react";
import {
  QualificationResult,
  runLeadQualification,
  overrideLeadQualification,
} from "@/lib/api/qualification";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface QualificationCardProps {
  leadId: string;
  initialQualification?: QualificationResult | null;
  onUpdated?: (qualification: QualificationResult) => void;
}

export function QualificationCard({
  leadId,
  initialQualification,
  onUpdated,
}: QualificationCardProps) {
  const [qualification, setQualification] = useState<QualificationResult | null>(
    initialQualification || null
  );
  const [loading, setLoading] = useState(false);
  const [overrideOpen, setOverrideOpen] = useState(false);
  const [overrideDecision, setOverrideDecision] = useState<string>("QUALIFIED");
  const [overrideReason, setOverrideReason] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleRunQualification = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await runLeadQualification(leadId);
      setQualification(res);
      if (onUpdated) onUpdated(res);
    } catch (err: any) {
      setError(err.message || "Failed to execute Qualification Agent");
    } finally {
      setLoading(false);
    }
  };

  const handleOverrideSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!overrideReason.trim()) {
      setError("Please provide a justification reason for human override.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await overrideLeadQualification(leadId, {
        decision: overrideDecision as any,
        reason: overrideReason,
      });
      setQualification(res);
      setOverrideOpen(false);
      if (onUpdated) onUpdated(res);
    } catch (err: any) {
      setError(err.message || "Failed to apply human override");
    } finally {
      setLoading(false);
    }
  };

  const getDecisionBadge = (dec: string, isOverride: boolean = false) => {
    const baseClass = "px-3 py-1 text-xs font-extrabold uppercase rounded-md tracking-wider border ";
    switch (dec) {
      case "QUALIFIED":
        return (
          <span className={baseClass + "bg-emerald-100 text-emerald-900 border-emerald-300 dark:bg-emerald-950 dark:text-emerald-200"}>
            {isOverride ? "OVERRIDDEN: " : ""}QUALIFIED
          </span>
        );
      case "POTENTIALLY_QUALIFIED":
        return (
          <span className={baseClass + "bg-blue-100 text-blue-900 border-blue-300 dark:bg-blue-950 dark:text-blue-200"}>
            {isOverride ? "OVERRIDDEN: " : ""}POTENTIALLY QUALIFIED
          </span>
        );
      case "NEEDS_REVIEW":
        return (
          <span className={baseClass + "bg-amber-100 text-amber-900 border-amber-300 dark:bg-amber-950 dark:text-amber-200"}>
            {isOverride ? "OVERRIDDEN: " : ""}NEEDS REVIEW
          </span>
        );
      case "NOT_QUALIFIED":
        return (
          <span className={baseClass + "bg-rose-100 text-rose-900 border-rose-300 dark:bg-rose-950 dark:text-rose-200"}>
            {isOverride ? "OVERRIDDEN: " : ""}NOT QUALIFIED
          </span>
        );
      case "INSUFFICIENT_DATA":
      default:
        return (
          <span className={baseClass + "bg-slate-100 text-slate-800 border-slate-300 dark:bg-slate-800 dark:text-slate-200"}>
            {isOverride ? "OVERRIDDEN: " : ""}INSUFFICIENT DATA
          </span>
        );
    }
  };

  const getReadinessBadge = (r: string) => {
    switch (r) {
      case "READY":
        return <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400">Ready for Outreach</span>;
      case "NEEDS_MANUAL_REVIEW":
        return <span className="text-xs font-semibold text-amber-600 dark:text-amber-400">Needs Manual Review</span>;
      case "OUTREACH_BLOCKED":
        return <span className="text-xs font-semibold text-rose-600 dark:text-rose-400">Outreach Blocked (DNC)</span>;
      default:
        return <span className="text-xs font-semibold text-slate-500">Not Recommended</span>;
    }
  };

  const activeDecision = qualification?.human_override_decision || qualification?.decision;

  return (
    <Card className="shadow-md border border-slate-200 dark:border-slate-800">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3 border-b border-slate-100 dark:border-slate-800">
        <div>
          <CardTitle className="text-lg font-bold">Qualification Agent Assessment</CardTitle>
          <p className="text-xs text-slate-500 mt-1">
            Internal evaluation of lead viability, evidence, and outreach readiness
          </p>
        </div>
        <div className="flex gap-2">
          {qualification && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => setOverrideOpen(!overrideOpen)}
              disabled={loading}
            >
              {overrideOpen ? "Cancel Override" : "Human Override"}
            </Button>
          )}
          <Button
            size="sm"
            onClick={handleRunQualification}
            disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 text-white"
          >
            {loading ? "Running Agent..." : qualification ? "Re-Qualify" : "Run Qualification Agent"}
          </Button>
        </div>
      </CardHeader>

      <CardContent className="pt-4 space-y-4">
        {error && (
          <div className="p-3 text-xs rounded-lg bg-rose-50 text-rose-700 border border-rose-200 dark:bg-rose-950 dark:text-rose-300">
            {error}
          </div>
        )}

        {overrideOpen && (
          <form onSubmit={handleOverrideSubmit} className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-3">
            <h4 className="text-xs font-bold uppercase text-slate-700 dark:text-slate-300">Human Override Decision</h4>
            <div className="flex gap-2">
              <select
                value={overrideDecision}
                onChange={(e) => setOverrideDecision(e.target.value)}
                className="text-xs rounded-md border border-slate-300 dark:border-slate-700 p-2 bg-white dark:bg-slate-800"
              >
                <option value="QUALIFIED">QUALIFIED</option>
                <option value="POTENTIALLY_QUALIFIED">POTENTIALLY_QUALIFIED</option>
                <option value="NEEDS_REVIEW">NEEDS_REVIEW</option>
                <option value="NOT_QUALIFIED">NOT_QUALIFIED</option>
                <option value="INSUFFICIENT_DATA">INSUFFICIENT_DATA</option>
              </select>
              <input
                type="text"
                placeholder="Reason / justification for override..."
                value={overrideReason}
                onChange={(e) => setOverrideReason(e.target.value)}
                className="flex-1 text-xs rounded-md border border-slate-300 dark:border-slate-700 p-2 bg-white dark:bg-slate-800"
              />
              <Button type="submit" size="sm" disabled={loading} className="bg-emerald-600 text-white">
                Save Override
              </Button>
            </div>
          </form>
        )}

        {!qualification ? (
          <div className="p-6 text-center text-slate-500 text-sm border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-xl">
            No qualification assessment has been run for this lead yet.
            <br />
            <span className="text-xs text-slate-400">
              Click &quot;Run Qualification Agent&quot; above to perform an automated internal evaluation.
            </span>
          </div>
        ) : (
          <>
            {/* Status Header */}
            <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-3">
                {getDecisionBadge(activeDecision || "UNKNOWN", !!qualification.human_override_decision)}
                <div>
                  <div className="text-xs text-slate-500">Confidence</div>
                  <div className="text-xs font-bold text-slate-800 dark:text-slate-200">
                    {qualification.confidence} CONFIDENCE
                  </div>
                </div>
              </div>
              <div>
                <div className="text-xs text-slate-500">Outreach Status</div>
                {getReadinessBadge(qualification.outreach_readiness)}
              </div>
              <div>
                <div className="text-xs text-slate-500">Version</div>
                <div className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  {qualification.qualification_version}
                </div>
              </div>
            </div>

            {/* Human Override note if present */}
            {qualification.human_override_decision && (
              <div className="p-3 text-xs rounded-lg bg-indigo-50 dark:bg-indigo-950/50 border border-indigo-200 text-indigo-900 dark:text-indigo-200">
                <span className="font-bold">Human Override: </span>
                {qualification.human_override_reason || "No reason specified."}
                <span className="block text-[10px] text-indigo-600 dark:text-indigo-400 mt-0.5">
                  Applied at {qualification.overridden_at ? new Date(qualification.overridden_at).toLocaleString() : "N/A"}
                </span>
              </div>
            )}

            {/* Summary */}
            {qualification.summary && (
              <div>
                <h4 className="text-xs font-bold uppercase text-slate-500 tracking-wider mb-1">Executive Summary</h4>
                <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed bg-white dark:bg-slate-950 p-3 rounded-lg border border-slate-100 dark:border-slate-800">
                  {qualification.summary}
                </p>
              </div>
            )}

            {/* Factors */}
            {qualification.factors && qualification.factors.length > 0 && (
              <div>
                <h4 className="text-xs font-bold uppercase text-slate-500 tracking-wider mb-2">Key Decision Factors</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {qualification.factors.map((f, idx) => (
                    <div key={idx} className="p-2.5 rounded-lg border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-950">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-xs font-bold text-slate-800 dark:text-slate-200">{f.name}</span>
                        <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${
                          f.status === "STRONG" ? "bg-emerald-100 text-emerald-800" :
                          f.status === "MODERATE" ? "bg-blue-100 text-blue-800" :
                          f.status === "BLOCKED" ? "bg-rose-100 text-rose-800" : "bg-slate-100 text-slate-700"
                        }`}>
                          {f.status}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-600 dark:text-slate-400">{f.assessment}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Reasons & Risks & Missing Info */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
              {qualification.reasons && qualification.reasons.length > 0 && (
                <div className="p-3 rounded-lg bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900/40">
                  <h5 className="text-[11px] font-bold text-emerald-800 dark:text-emerald-300 mb-1.5">Supporting Reasons</h5>
                  <ul className="list-disc list-inside text-[11px] text-emerald-900 dark:text-emerald-200 space-y-1">
                    {qualification.reasons.map((r, i) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                </div>
              )}

              {qualification.risks && qualification.risks.length > 0 && (
                <div className="p-3 rounded-lg bg-amber-50/50 dark:bg-amber-950/20 border border-amber-100 dark:border-amber-900/40">
                  <h5 className="text-[11px] font-bold text-amber-800 dark:text-amber-300 mb-1.5">Identified Risks</h5>
                  <ul className="list-disc list-inside text-[11px] text-amber-900 dark:text-amber-200 space-y-1">
                    {qualification.risks.map((rk, i) => (
                      <li key={i}>{rk}</li>
                    ))}
                  </ul>
                </div>
              )}

              {qualification.missing_information && qualification.missing_information.length > 0 && (
                <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                  <h5 className="text-[11px] font-bold text-slate-700 dark:text-slate-300 mb-1.5">Missing Information</h5>
                  <ul className="list-disc list-inside text-[11px] text-slate-600 dark:text-slate-400 space-y-1">
                    {qualification.missing_information.map((m, i) => (
                      <li key={i}>{m}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
