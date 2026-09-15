'use client';

import React, { useState } from 'react';
import { SemanticQueryResult, analyticsApi } from '@/lib/api/analytics';

export const NaturalLanguageAnalyticsBar: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SemanticQueryResult | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await analyticsApi.executeSemanticQuery(query.trim());
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const presetQueries = [
    "Why are project estimates inaccurate?",
    "Which services converted best this quarter?",
    "How much AI cost did lead research consume?",
    "Which projects had the most scope changes?",
  ];

  return (
    <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-zinc-100 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-purple-500"></span>
            Natural Language Analytics (Semantic Layer)
          </h3>
          <p className="text-xs text-zinc-400 mt-0.5">
            Ask questions in plain English. Mapped strictly to registered metrics (raw SQL execution prohibited).
          </p>
        </div>
        <span className="text-xs px-2.5 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 font-semibold">
          AI Query Guard v1.0
        </span>
      </div>

      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. 'Why are project estimates inaccurate?' or 'Which services converted best?'"
          className="flex-1 bg-zinc-950 border border-zinc-700/80 rounded-lg px-4 py-2.5 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-lg transition-colors disabled:opacity-50"
        >
          {loading ? 'Analyzing...' : 'Ask'}
        </button>
      </form>

      {/* Preset Suggestions */}
      <div className="flex flex-wrap items-center gap-2 text-xs">
        <span className="text-zinc-500 font-medium">Try asking:</span>
        {presetQueries.map((pq) => (
          <button
            key={pq}
            onClick={() => setQuery(pq)}
            className="px-2.5 py-1 bg-zinc-800/80 hover:bg-zinc-800 text-zinc-300 rounded border border-zinc-700/60 transition-colors"
          >
            {pq}
          </button>
        ))}
      </div>

      {/* Query Result Card */}
      {result && (
        <div className="mt-4 p-4 bg-zinc-950/80 border border-indigo-500/30 rounded-lg space-y-2 text-sm">
          <div className="flex items-center justify-between text-xs text-indigo-400 font-semibold">
            <span>Interpreted Intent: {result.intent}</span>
            <span>Key: {result.query_key}</span>
          </div>
          <p className="text-zinc-200 font-medium">{result.summary}</p>
          <div className="text-xs text-zinc-500 space-y-0.5 pt-2 border-t border-zinc-800/60">
            {result.evidence_notes.map((note, i) => (
              <p key={i}>• {note}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
