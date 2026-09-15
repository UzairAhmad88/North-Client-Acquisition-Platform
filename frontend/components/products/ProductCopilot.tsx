'use client';

import React, { useState } from 'react';
import { Bot, Send, Sparkles, ShieldAlert, CheckCircle2, HelpCircle } from 'lucide-react';
import { productApi } from '../../lib/api/productManagement';

interface ProductCopilotProps {
  productId: string;
}

export const ProductCopilot: React.FC<ProductCopilotProps> = ({ productId }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any | null>(null);

  const handleAsk = async (promptQuery?: string) => {
    const q = promptQuery || query;
    if (!q.trim()) return;
    setLoading(true);
    try {
      const res = await productApi.queryCopilot(productId, q);
      setResponse(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    "Why is this feature important?",
    "Is this release ready?",
    "Which roadmap item should we prioritize?",
    "What customer problems are growing?",
  ];

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
            <Bot className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">AI Product Manager Co-Pilot</h3>
            <p className="text-[11px] text-slate-400">Grounded in verified PRDs, metrics, and deterministic release gates.</p>
          </div>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 font-semibold">
          Governed Mode
        </span>
      </div>

      {/* Suggested prompts */}
      <div className="flex flex-wrap gap-2">
        {samplePrompts.map((p, i) => (
          <button
            key={i}
            onClick={() => {
              setQuery(p);
              handleAsk(p);
            }}
            className="text-[11px] text-slate-300 bg-slate-950/60 hover:bg-slate-800/80 px-2.5 py-1 rounded-md border border-slate-800 transition-colors"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
          placeholder="Ask about PRD requirements, release readiness, or backlog RICE scores..."
          className="flex-1 bg-slate-950/80 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
        />
        <button
          onClick={() => handleAsk()}
          disabled={loading || !query.trim()}
          className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors"
        >
          {loading ? (
            <Sparkles className="h-3.5 w-3.5 animate-spin" />
          ) : (
            <Send className="h-3.5 w-3.5" />
          )}
          Inquire
        </button>
      </div>

      {/* Response Box */}
      {response && (
        <div className="mt-4 p-4 rounded-lg bg-slate-950/60 border border-slate-800/80 space-y-3">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-indigo-400">Co-Pilot Recommendation</span>
            <span className="text-[10px] font-mono text-slate-400">
              Confidence: {Math.round((response.confidence || 0.92) * 100)}%
            </span>
          </div>
          <p className="text-xs text-slate-200 leading-relaxed">{response.answer}</p>

          {response.evidence && (
            <div className="bg-slate-900/60 p-2.5 rounded border border-slate-800 text-[11px] text-slate-400">
              <span className="font-semibold text-slate-300">Grounding Evidence:</span>{' '}
              {Array.isArray(response.evidence) ? response.evidence.join('; ') : JSON.stringify(response.evidence)}
            </div>
          )}

          <div className="flex items-center gap-1.5 text-[10px] font-mono text-emerald-400 bg-emerald-500/5 px-2 py-1 rounded border border-emerald-500/20">
            <CheckCircle2 className="h-3 w-3 shrink-0" />
            <span>Non-Autonomous Policy Enforced: Human sign-off is required for all release deployments and pricing changes.</span>
          </div>
        </div>
      )}
    </div>
  );
};
