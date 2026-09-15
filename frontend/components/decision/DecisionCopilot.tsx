"use client";

import React, { useState } from "react";
import { decisionRoomsApi } from "@/lib/api/decision_rooms";
import { Bot, Send, Sparkles, AlertCircle } from "lucide-react";

interface Props {
  roomId: string;
}

export const DecisionCopilot: React.FC<Props> = ({ roomId }) => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setLoading(true);
    try {
      const res = await decisionRoomsApi.queryCopilot(roomId, query);
      setResponse(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center gap-2">
        <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
          <Bot className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-base font-bold text-white">Collaboration Copilot</h3>
          <p className="text-xs text-slate-400">Ask questions, inspect options, compare trade-offs, or check challenged assumptions.</p>
        </div>
      </div>

      {response && (
        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="font-semibold text-indigo-400 flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5" /> Copilot Analysis
            </span>
            <span className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs">
              {response.statement_category}
            </span>
          </div>

          <p className="text-sm text-slate-200 leading-relaxed">{response.answer}</p>

          {response.tradeoff_highlight && (
            <div className="text-xs text-slate-400 bg-slate-900 p-2.5 rounded border border-slate-800 mt-2">
              <span className="text-amber-400 font-semibold block mb-0.5">Key Trade-off:</span>
              {response.tradeoff_highlight}
            </div>
          )}

          <div className="text-2xs text-slate-400 pt-2 border-t border-slate-900 flex items-center gap-1">
            <AlertCircle className="w-3 h-3 text-slate-400" />
            Decision support only. Final approval and business decisions remain human-owned.
          </div>
        </div>
      )}

      <form onSubmit={handleSend} className="flex items-center gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. Compare candidate options and highlight key risks..."
          className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold flex items-center gap-1.5 transition disabled:opacity-50"
        >
          <Send className="w-4 h-4" />
          {loading ? "Analyzing..." : "Ask"}
        </button>
      </form>
    </div>
  );
};
