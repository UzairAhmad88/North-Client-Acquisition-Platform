"use client";

import React, { useState } from "react";
import { marketingApi, CopilotResponse } from "@/lib/api/marketing";

export const MarketingCopilot: React.FC = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<CopilotResponse[]>([
    {
      query: "What campaigns are performing best?",
      answer: "The top-performing campaign is 'Q3 Enterprise Advisory Modernization Initiative' operating across Email, LinkedIn, and Organic Search with an estimated ROAS of 5.67x and direct pipeline influence.",
      evidence: ["Active Campaign: Q3 Enterprise Advisory Modernization Initiative", "Allocated Budget: $45,000", "Attributed Revenue: $680,000"],
      uncertainty: "Multi-touch attribution models assign weighted credit across channels; ongoing touches may shift final position-based split.",
      timestamp: new Date().toISOString(),
    },
  ]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userQ = query;
    setQuery("");
    setLoading(true);

    try {
      const res = await marketingApi.askCopilot(userQ);
      setHistory((prev) => [...prev, res]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    "What campaigns are performing best?",
    "Which content gaps matter most?",
    "Which channels have the best economics?",
    "What is our Q4 demand forecast?",
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200">Marketing Strategy & Demand Copilot</h3>
          <p className="text-xs text-slate-400 mt-0.5">Evidence-grounded conversational marketing decision support</p>
        </div>
        <span className="text-xs bg-indigo-950 text-indigo-400 border border-indigo-800 px-2.5 py-0.5 rounded-full font-mono">
          AI Guided
        </span>
      </div>

      <div className="space-y-4 max-h-96 overflow-y-auto pr-2 mb-4">
        {history.map((h, i) => (
          <div key={i} className="space-y-2">
            <div className="flex justify-end">
              <div className="bg-indigo-600/30 border border-indigo-500/40 text-xs text-slate-200 px-3 py-2 rounded-lg max-w-[80%]">
                {h.query}
              </div>
            </div>

            <div className="flex justify-start">
              <div className="bg-slate-800/60 border border-slate-700/60 text-xs text-slate-300 p-3.5 rounded-lg max-w-[90%] space-y-2">
                <p className="text-slate-100 leading-relaxed">{h.answer}</p>

                {h.evidence && h.evidence.length > 0 && (
                  <div className="bg-slate-900/80 p-2 rounded border border-slate-700/40 text-[11px] space-y-1">
                    <span className="text-cyan-400 font-semibold uppercase tracking-wider block text-[10px]">
                      Verified Evidence
                    </span>
                    {h.evidence.map((ev, idx) => (
                      <div key={idx} className="flex items-center text-slate-300">
                        <span className="w-1 h-1 rounded-full bg-cyan-400 mr-1.5" />
                        {ev}
                      </div>
                    ))}
                  </div>
                )}

                {h.uncertainty && (
                  <div className="text-[10px] text-amber-400/90 italic">
                    Uncertainty: {h.uncertainty}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Suggested prompts */}
      <div className="flex flex-wrap gap-1.5 mb-3">
        {samplePrompts.map((p, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => setQuery(p)}
            className="text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 px-2.5 py-1 rounded transition"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Form */}
      <form onSubmit={handleSend} className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask Marketing Copilot about campaigns, CAC, content gaps, or forecasting..."
          className="flex-1 bg-slate-800/80 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-xs font-medium transition"
        >
          {loading ? "Analyzing..." : "Ask"}
        </button>
      </form>
    </div>
  );
};
