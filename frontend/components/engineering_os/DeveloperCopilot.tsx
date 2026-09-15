"use client";

import React, { useState } from "react";
import { queryDeveloperCopilot, DeveloperCopilotResponse } from "@/lib/api/engineeringOs";

export const DeveloperCopilotView: React.FC = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DeveloperCopilotResponse | null>(null);

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await queryDeveloperCopilot(query);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const sampleQueries = [
    "Explain this service architecture and dependency blast radius.",
    "Why is this CI/CD build failing on the staging pipeline?",
    "Find technical debt hotspots and security vulnerabilities.",
    "Analyze release readiness for production canary deployment.",
  ];

  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="pb-4 border-b border-slate-800">
        <h2 className="text-lg font-semibold text-slate-100">Engineering & Developer Copilot</h2>
        <p className="text-xs text-slate-400">
          Grounded technical intelligence distinguishing FACT, INFERENCE, HYPOTHESIS, and RECOMMENDATION
        </p>
      </div>

      <form onSubmit={handleAsk} className="mt-4 flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask Copilot about services, builds, incidents, deployments, or debt..."
          className="flex-1 bg-slate-800/80 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium text-xs px-4 py-2 rounded-lg transition"
        >
          {loading ? "Analyzing..." : "Ask Copilot"}
        </button>
      </form>

      <div className="mt-2 flex flex-wrap gap-2">
        {sampleQueries.map((sq, i) => (
          <button
            key={i}
            type="button"
            onClick={() => setQuery(sq)}
            className="text-[11px] text-slate-400 bg-slate-800/50 hover:bg-slate-800 hover:text-slate-200 px-2 py-1 rounded border border-slate-700/50 transition"
          >
            {sq}
          </button>
        ))}
      </div>

      {result && (
        <div className="mt-5 space-y-3 bg-slate-800/30 p-4 rounded-xl border border-slate-700/60 text-xs">
          <div className="flex items-center justify-between pb-2 border-b border-slate-700/50">
            <span className="font-semibold text-slate-200">Grounded Analysis Result</span>
            <span className="text-[10px] font-mono text-emerald-400">
              Confidence: {Math.round(result.confidence_score * 100)}%
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="font-bold text-cyan-400 uppercase tracking-wider text-[10px] block mb-1">
                Verified Facts
              </span>
              <ul className="list-disc list-inside space-y-1 text-slate-300">
                {result.facts.map((f, i) => (
                  <li key={i}>{f}</li>
                ))}
              </ul>
            </div>

            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="font-bold text-indigo-400 uppercase tracking-wider text-[10px] block mb-1">
                Inferences
              </span>
              <ul className="list-disc list-inside space-y-1 text-slate-300">
                {result.inferences.map((inf, i) => (
                  <li key={i}>{inf}</li>
                ))}
              </ul>
            </div>

            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="font-bold text-amber-400 uppercase tracking-wider text-[10px] block mb-1">
                Hypotheses
              </span>
              <ul className="list-disc list-inside space-y-1 text-slate-300">
                {result.hypotheses.map((h, i) => (
                  <li key={i}>{h}</li>
                ))}
              </ul>
            </div>

            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="font-bold text-emerald-400 uppercase tracking-wider text-[10px] block mb-1">
                Recommendations
              </span>
              <ul className="list-disc list-inside space-y-1 text-slate-300">
                {result.recommendations.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="pt-2 text-[10px] text-slate-500 italic border-t border-slate-700/40">
            {result.governance_notice}
          </div>
        </div>
      )}
    </div>
  );
};
