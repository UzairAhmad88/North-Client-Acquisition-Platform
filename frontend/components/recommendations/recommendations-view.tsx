"use client";

import React, { useState, useEffect } from "react";
import {
  ServiceRecommendation,
  calculateLeadRecommendations,
  getLeadRecommendations,
  acceptRecommendation,
  rejectRecommendation,
} from "@/lib/api/recommendations";
import { RecommendationBadge } from "./recommendation-badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, RefreshCw, CheckCircle2, XCircle, AlertCircle, Info, FileText } from "lucide-react";

interface RecommendationsViewProps {
  leadId: string;
}

export function RecommendationsView({ leadId }: RecommendationsViewProps) {
  const [recommendations, setRecommendations] = useState<ServiceRecommendation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [calculating, setCalculating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [rejectingId, setRejectingId] = useState<string | null>(null);
  const [rejectReason, setRejectReason] = useState<string>("");

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getLeadRecommendations(leadId);
      setRecommendations(res.data);
    } catch (err: any) {
      setError(err?.message || "Failed to load service recommendations.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, [leadId]);

  const handleCalculate = async () => {
    try {
      setCalculating(true);
      setError(null);
      const newRecs = await calculateLeadRecommendations(leadId);
      setRecommendations(newRecs);
    } catch (err: any) {
      setError(err?.message || "Failed to calculate recommendations.");
    } finally {
      setCalculating(false);
    }
  };

  const handleAccept = async (id: string) => {
    try {
      const updated = await acceptRecommendation(id);
      setRecommendations((prev) => prev.map((r) => (r.id === id ? updated : r)));
    } catch (err: any) {
      alert("Error accepting recommendation: " + (err?.message || "Unknown error"));
    }
  };

  const handleRejectSubmit = async (id: string) => {
    try {
      const updated = await rejectRecommendation(id, rejectReason);
      setRecommendations((prev) => prev.map((r) => (r.id === id ? updated : r)));
      setRejectingId(null);
      setRejectReason("");
    } catch (err: any) {
      alert("Error rejecting recommendation: " + (err?.message || "Unknown error"));
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
        <span className="ml-2 text-sm text-slate-500">Loading service recommendations...</span>
      </div>
    );
  }

  const top3 = recommendations.slice(0, 3);
  const remaining = recommendations.slice(3);
  const hasStale = recommendations.some((r) => r.status === "STALE");

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            Recommended North's Services
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Explainable service fit recommendations derived from business profile, digital research, website audit, and opportunity scoring.
          </p>
        </div>
        <Button
          onClick={handleCalculate}
          disabled={calculating}
          variant="outline"
          size="sm"
          className="gap-2"
        >
          {calculating ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <RefreshCw className="w-4 h-4" />
          )}
          Recalculate Recommendations
        </Button>
      </div>

      {hasStale && (
        <div className="p-3 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 text-amber-800 dark:text-amber-300 rounded-lg text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>
            Some recommendations are <strong>STALE</strong> because underlying business research or website audit findings were updated. Click recalculate to refresh.
          </span>
        </div>
      )}

      {error && (
        <div className="p-3 bg-red-50 text-red-700 rounded-lg text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {recommendations.length === 0 ? (
        <Card className="p-8 text-center bg-slate-50 dark:bg-slate-900/50 border-dashed">
          <Info className="w-8 h-8 text-slate-400 mx-auto mb-3" />
          <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300">No Recommendations Generated Yet</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
            Click the calculate button above to evaluate North's service catalog against this lead's business context and audit evidence.
          </p>
          <Button onClick={handleCalculate} disabled={calculating} size="sm" className="mt-4 gap-2">
            {calculating && <Loader2 className="w-4 h-4 animate-spin" />}
            Calculate Recommendations Now
          </Button>
        </Card>
      ) : (
        <div className="space-y-6">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Top Recommended Services</h3>
            <div className="grid gap-4 md:grid-cols-1">
              {top3.map((rec) => (
                <Card key={rec.id} className="overflow-hidden border border-slate-200 dark:border-slate-800 shadow-sm">
                  <CardHeader className="bg-slate-50/50 dark:bg-slate-900/50 pb-3">
                    <div className="flex items-start justify-between gap-4 flex-wrap">
                      <div>
                        <CardTitle className="text-lg font-bold text-slate-900 dark:text-white">
                          {rec.service_name || "Service Candidate"}
                        </CardTitle>
                        <CardDescription className="text-xs mt-1">
                          Version {rec.recommendation_version} · Catalog Item
                        </CardDescription>
                      </div>
                      <RecommendationBadge
                        score={rec.relevance_score}
                        band={rec.band}
                        priority={rec.priority}
                        confidence={rec.confidence}
                        status={rec.status}
                      />
                    </div>
                  </CardHeader>

                  <CardContent className="pt-4 space-y-4">
                    {/* Why Recommended */}
                    <div>
                      <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300 mb-1 flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                        Why This Service Is Relevant:
                      </h4>
                      <ul className="list-disc list-inside text-xs text-slate-600 dark:text-slate-400 space-y-1 pl-1">
                        {rec.reasons.map((reason, idx) => (
                          <li key={idx}>{reason}</li>
                        ))}
                      </ul>
                    </div>

                    {/* Evidence */}
                    {rec.evidence.length > 0 && (
                      <div>
                        <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300 mb-1 flex items-center gap-1.5">
                          <FileText className="w-3.5 h-3.5 text-blue-500" />
                          Observable Evidence ({rec.evidence.length} trace records):
                        </h4>
                        <div className="space-y-1">
                          {rec.evidence.map((ev, idx) => (
                            <div key={idx} className="p-2 rounded bg-slate-100 dark:bg-slate-900 text-[11px] text-slate-700 dark:text-slate-300 border border-slate-200/50 dark:border-slate-800">
                              <span className="font-semibold uppercase text-[10px] text-blue-600 dark:text-blue-400 mr-2">
                                [{ev.source}]
                              </span>
                              {ev.description || ev.type}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Limitations */}
                    {rec.limitations.length > 0 && (
                      <div>
                        <h4 className="text-xs font-bold text-slate-500 mb-1 flex items-center gap-1.5">
                          <Info className="w-3.5 h-3.5 text-slate-400" />
                          Objective Limitations & Caveats:
                        </h4>
                        <ul className="list-disc list-inside text-[11px] text-slate-500 space-y-0.5 pl-1 italic">
                          {rec.limitations.map((lim, idx) => (
                            <li key={idx}>{lim}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Actions */}
                    <div className="pt-2 flex items-center justify-between border-t border-slate-100 dark:border-slate-800 flex-wrap gap-2">
                      <div className="text-[11px] text-slate-400">
                        {rec.status === "ACCEPTED" && rec.accepted_at && (
                          <span className="text-emerald-600 font-medium">
                            Accepted by team on {new Date(rec.accepted_at).toLocaleDateString()}
                          </span>
                        )}
                        {rec.status === "REJECTED" && (
                          <span className="text-red-500 font-medium">
                            Rejected: {rec.rejection_reason || "No reason given"}
                          </span>
                        )}
                      </div>

                      {rec.status !== "ACCEPTED" && rec.status !== "REJECTED" && (
                        <div className="flex items-center gap-2 ml-auto">
                          <Button
                            onClick={() => handleAccept(rec.id)}
                            size="sm"
                            variant="default"
                            className="bg-emerald-600 hover:bg-emerald-700 text-white gap-1 text-xs"
                          >
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            Accept Service
                          </Button>
                          <Button
                            onClick={() => setRejectingId(rec.id)}
                            size="sm"
                            variant="outline"
                            className="text-red-600 hover:bg-red-50 gap-1 text-xs"
                          >
                            <XCircle className="w-3.5 h-3.5" />
                            Reject
                          </Button>
                        </div>
                      )}
                    </div>

                    {/* Rejection Form Modal/Inline */}
                    {rejectingId === rec.id && (
                      <div className="p-3 bg-red-50 dark:bg-red-950/30 border border-red-200 rounded-lg text-xs space-y-2">
                        <label className="font-semibold text-red-800 dark:text-red-300">
                          Rejection Reason (Optional):
                        </label>
                        <input
                          type="text"
                          value={rejectReason}
                          onChange={(e) => setRejectReason(e.target.value)}
                          placeholder="e.g. Service already implemented in-house..."
                          className="w-full p-2 border rounded text-xs text-slate-900 bg-white"
                        />
                        <div className="flex gap-2 justify-end">
                          <Button size="sm" variant="ghost" onClick={() => setRejectingId(null)}>
                            Cancel
                          </Button>
                          <Button size="sm" variant="destructive" onClick={() => handleRejectSubmit(rec.id)}>
                            Confirm Rejection
                          </Button>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {remaining.length > 0 && (
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Other Candidates</h3>
              <div className="grid gap-3">
                {remaining.map((rec) => (
                  <div key={rec.id} className="p-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center justify-between gap-4">
                    <div>
                      <span className="font-bold text-sm text-slate-900 dark:text-white">{rec.service_name}</span>
                      <p className="text-xs text-slate-500 line-clamp-1">{rec.reasons[0] || "Catalog candidate"}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <RecommendationBadge score={rec.relevance_score} band={rec.band} size="sm" />
                      {rec.status !== "ACCEPTED" && rec.status !== "REJECTED" && (
                        <Button onClick={() => handleAccept(rec.id)} size="sm" variant="outline" className="text-xs">
                          Accept
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
