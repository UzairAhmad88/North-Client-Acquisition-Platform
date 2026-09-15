"use client";

import React, { useState } from "react";
import { queryProductCopilot, ProductCopilotResponse } from "@/lib/api/productOs";

export const ProductCopilotView: React.FC = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ProductCopilotResponse | null>(null);

  const sampleQueries = [
    "What should we build next?",
    "How is the product performing?",
    "Which features are underused?",
    "Why is this initiative prioritized?",
  ];

  const handleAsk = async (qText?: string) => {
    const textToQuery = qText || query;
    if (!textToQuery.trim()) return;
    setLoading(true);
    try {
      const res = await queryProductCopilot(textToQuery);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Product Intelligence Copilot</h2>
          <p className="text-xs text-slate-400">
            Evidence-grounded conversational intelligence with explicit citations and confidence bounds
          </p>
        </div>
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-950 text-indigo-400 border border-indigo-800 font-mono">
          Strict Evidence Only
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {sampleQueries.map((sq, idx) => (
          <button
            key={idx}
            onClick={() => {
              setQuery(sq);
              handleAsk(sq);
            }}
            className="text-[11px] px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          >
            "{sq}"
          </button>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          placeholder="Ask product strategy, discovery, roadmap, or feature value questions..."
          className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
        />
        <button
          onClick={() => handleAsk()}
          disabled={loading}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium text-xs rounded-lg transition"
        >
          {loading ? "Analyzing..." : "Ask Copilot"}
        </button>
      </div>

      {result && (
        <div className="p-4 bg-slate-950/80 border border-slate-800 rounded-lg space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-300">Copilot Synthesis:</span>
            <span className="text-[10px] text-emerald-400 font-mono">
              Confidence: {Math.round(result.confidence * 100)}%
            </span>
          </div>
          <p className="text-xs text-slate-200 leading-relaxed">{result.response}</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] text-slate-400 pt-2 border-t border-slate-800/80">
            <div>
              <span className="font-semibold text-slate-300">Verified Evidence Sources:</span>
              <ul className="list-disc list-inside mt-0.5 space-y-0.5 text-slate-400 font-mono text-[10px]">
                {result.evidence_sources.map((s, idx) => (
                  <li key={idx}>{s}</li>
                ))}
              </ul>
            </div>
            <div>
              <span className="font-semibold text-slate-300">Assumptions & Caveats:</span>
              <ul className="list-disc list-inside mt-0.5 space-y-0.5 text-slate-400 font-mono text-[10px]">
                {result.assumptions.map((a, idx) => (
                  <li key={idx}>{a}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="text-[10px] text-amber-400/90 italic pt-1">
            ⚖ {result.governance_notice}
          </div>
        </div>
      )}
    </div>
  );
};
