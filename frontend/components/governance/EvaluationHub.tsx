"use client";

import React, { useState } from "react";
import { EvaluationDataset, EvaluationRun, governanceApi } from "@/lib/api/governance";
import { Play, CheckCircle2, AlertTriangle, ShieldCheck, Award } from "lucide-react";

interface EvaluationHubProps {
  datasets: EvaluationDataset[];
  runs: EvaluationRun[];
  onRefresh: () => void;
}

export const EvaluationHub: React.FC<EvaluationHubProps> = ({ datasets, runs, onRefresh }) => {
  const [runningId, setRunningId] = useState<string | null>(null);

  const handleRunBenchmark = async (datasetId: string, taskType: string) => {
    setRunningId(datasetId);
    try {
      await governanceApi.runEvaluationBenchmark({
        dataset_id: datasetId,
        agent_key: `${taskType.toLowerCase()}_agent`,
        baseline_score: 90.0,
      });
      onRefresh();
    } catch (err) {
      console.error("Benchmark run failed:", err);
    } finally {
      setRunningId(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Golden Datasets Catalog */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-zinc-100">Golden Test Datasets & Benchmark Suites</h3>
            <p className="text-xs text-zinc-400 mt-1">
              Curated test cases evaluating structural validity, evidence grounding, and policy compliance.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {datasets.map((ds) => (
            <div key={ds.id} className="bg-zinc-950 border border-zinc-800 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-semibold text-zinc-200 text-sm">{ds.name}</h4>
                  <div className="text-[11px] text-zinc-500 font-mono">{ds.dataset_key}</div>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold flex items-center gap-1">
                  <Award className="w-3 h-3" /> Golden Suite
                </span>
              </div>

              <p className="text-xs text-zinc-400">{ds.description}</p>

              <div className="flex items-center justify-between pt-2 border-t border-zinc-850">
                <span className="text-xs text-zinc-500">{ds.cases?.length || 5} curated cases</span>
                <button
                  onClick={() => handleRunBenchmark(ds.id, ds.task_type)}
                  disabled={runningId === ds.id}
                  className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white transition disabled:opacity-50"
                >
                  <Play className="w-3.5 h-3.5" />
                  {runningId === ds.id ? "Running..." : "Run Benchmark"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Benchmark Execution Runs & Regression History */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-zinc-100">Benchmark Runs & Regression Detection</h3>
          <span className="text-xs text-zinc-400">Strict gate: Quality drop &gt;5% blocks promotion</span>
        </div>

        <div className="divide-y divide-zinc-800/60 overflow-hidden">
          {runs.length === 0 ? (
            <div className="p-6 text-center text-zinc-500">No benchmark evaluations recorded yet.</div>
          ) : (
            runs.map((r) => (
              <div key={r.id} className="py-3 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-zinc-200 text-sm">{r.agent_key}</span>
                    <span className="text-xs text-zinc-400 font-mono">
                      (Prompt {r.prompt_version} / Model {r.model_version})
                    </span>
                  </div>
                  <div className="text-xs text-zinc-500 mt-1">
                    Score: <span className="text-zinc-200 font-semibold">{r.overall_score}%</span> • Passed:{" "}
                    {r.passed_cases_count} / Failed: {r.failed_cases_count}
                  </div>
                </div>

                <div>
                  {r.regression_detected ? (
                    <span className="px-2.5 py-1 rounded text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20 flex items-center gap-1">
                      <AlertTriangle className="w-3.5 h-3.5" /> Regression Detected (Blocked)
                    </span>
                  ) : (
                    <span className="px-2.5 py-1 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Evaluation Passed
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default EvaluationHub;
