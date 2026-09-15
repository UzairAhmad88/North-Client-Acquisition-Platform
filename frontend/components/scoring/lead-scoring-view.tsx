"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Award, RotateCw, History, AlertTriangle, ShieldCheck, Play } from "lucide-react";
import {
  calculateLeadScore,
  getLeadScore,
  getLeadScoreHistory,
  LeadScore,
  LeadScoreHistory,
} from "@/lib/api/scoring";
import { ScoreBadge } from "./score-badge";
import { ScoreBreakdownCard } from "./score-breakdown-card";

interface LeadScoringViewProps {
  leadId: string;
}

export function LeadScoringView({ leadId }: LeadScoringViewProps) {
  const [score, setScore] = useState<LeadScore | null>(null);
  const [history, setHistory] = useState<LeadScoreHistory | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [calculating, setCalculating] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchScoreData = useCallback(async () => {
    try {
      setLoading(true);
      setErrorMsg(null);
      const [scoreRes, histRes] = await Promise.all([
        getLeadScore(leadId),
        getLeadScoreHistory(leadId),
      ]);
      setScore(scoreRes);
      setHistory(histRes);
    } catch (err: any) {
      setErrorMsg("Failed to load lead opportunity score.");
    } finally {
      setLoading(false);
    }
  }, [leadId]);

  useEffect(() => {
    fetchScoreData();
  }, [fetchScoreData]);

  const handleRecalculate = async () => {
    try {
      setCalculating(true);
      setErrorMsg(null);
      const newScore = await calculateLeadScore(leadId);
      setScore(newScore);
      const histRes = await getLeadScoreHistory(leadId);
      setHistory(histRes);
    } catch (err: any) {
      setErrorMsg("Failed to recalculate opportunity score.");
    } finally {
      setCalculating(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-center bg-white dark:bg-gray-850 rounded-2xl border border-gray-200 dark:border-gray-800">
        <RotateCw className="w-6 h-6 text-indigo-600 dark:text-indigo-400 animate-spin mx-auto mb-2" />
        <p className="text-sm text-gray-500">Calculating opportunity score...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header & Recalculate Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-gray-900 dark:text-gray-100">
              Lead Opportunity Scoring Engine
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Deterministic 7-dimension weighted scoring (v{score?.score_version || "1.0"})
            </p>
          </div>
        </div>

        <button
          onClick={handleRecalculate}
          disabled={calculating}
          className="inline-flex items-center justify-center gap-2 px-4 py-2.5 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 rounded-xl transition shadow-sm"
        >
          {calculating ? (
            <>
              <RotateCw className="w-4 h-4 animate-spin" />
              <span>Recalculating...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4" />
              <span>Recalculate Score</span>
            </>
          )}
        </button>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 text-xs text-rose-700 dark:text-rose-300">
          {errorMsg}
        </div>
      )}

      {score && (
        <>
          {/* Main Score Hero Card */}
          <div className="p-6 rounded-2xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-gray-100 dark:border-gray-800">
              <ScoreBadge score={score.total_score} band={score.band} size="lg" />

              <div className="flex flex-col items-start md:items-end gap-1 text-xs">
                <div className="flex items-center gap-1.5">
                  <span className="text-gray-500">Evidence Confidence:</span>
                  <span className="font-bold text-gray-900 dark:text-gray-100 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded">
                    {score.confidence}
                  </span>
                </div>
                <div className="text-gray-400 text-[11px]">
                  Calculated: {new Date(score.calculated_at).toLocaleString()}
                </div>
              </div>
            </div>

            {/* Natural Language Explanation */}
            {score.explanation && (
              <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-800/40 border border-gray-100 dark:border-gray-800 text-xs text-gray-700 dark:text-gray-300 leading-relaxed font-mono whitespace-pre-wrap">
                {score.explanation}
              </div>
            )}

            {/* Breakdown Component */}
            <ScoreBreakdownCard breakdown={score.breakdown} />
          </div>

          {/* History Section */}
          {history && history.history.length > 0 && (
            <div className="p-6 rounded-2xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 space-y-4">
              <div className="flex items-center gap-2 text-sm font-bold text-gray-900 dark:text-gray-100">
                <History className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                <span>Score Version History ({history.total_scores})</span>
              </div>

              <div className="space-y-2">
                {history.history.map((s) => (
                  <div
                    key={s.id}
                    className="flex items-center justify-between p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 text-xs text-gray-700 dark:text-gray-300"
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-mono font-bold text-indigo-600 dark:text-indigo-400">
                        v{s.score_version}
                      </span>
                      <ScoreBadge score={s.total_score} band={s.band} size="sm" />
                    </div>

                    <div className="flex items-center gap-3 text-[11px] text-gray-500">
                      <span>Confidence: {s.confidence}</span>
                      <span>{new Date(s.calculated_at).toLocaleDateString()}</span>
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
