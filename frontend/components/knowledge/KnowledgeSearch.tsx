'use client';

import React, { useState } from 'react';
import { searchKnowledge, submitSearchFeedback, SearchResult } from '@/lib/api/knowledge';
import {
  Search,
  Sparkles,
  ShieldCheck,
  Clock,
  ThumbsUp,
  ThumbsDown,
  Layers,
  FileText,
  Filter,
  CheckCircle,
} from 'lucide-react';

export default function KnowledgeSearchComponent() {
  const [query, setQuery] = useState('');
  const [domain, setDomain] = useState<string>('');
  const [strategy, setStrategy] = useState<string>('HYBRID');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searched, setSearched] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState<Record<string, boolean>>({});

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const data = await searchKnowledge({
        query: query.trim(),
        domain: domain || undefined,
        strategy,
        top_k: 10,
      });
      setResults(data);
      setSearched(true);
    } catch (err) {
      console.error('Search failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (code: string, isHelpful: boolean) => {
    try {
      await submitSearchFeedback({
        query,
        result_code: code,
        is_helpful: isHelpful,
      });
      setFeedbackGiven((prev) => ({ ...prev, [code]: true }));
    } catch (err) {
      console.error('Feedback failed:', err);
    }
  };

  const getAuthorityBadge = (auth: string) => {
    switch (auth) {
      case 'AUTHORITATIVE':
        return <span className="px-2 py-0.5 text-xs font-semibold rounded bg-emerald-100 text-emerald-800 border border-emerald-300">AUTHORITATIVE</span>;
      case 'CONFIRMED':
        return <span className="px-2 py-0.5 text-xs font-semibold rounded bg-blue-100 text-blue-800 border border-blue-300">CONFIRMED</span>;
      case 'VERIFIED':
        return <span className="px-2 py-0.5 text-xs font-semibold rounded bg-indigo-100 text-indigo-800 border border-indigo-300">VERIFIED</span>;
      case 'INFERRED':
        return <span className="px-2 py-0.5 text-xs font-semibold rounded bg-amber-100 text-amber-800 border border-amber-300">INFERRED (AI)</span>;
      default:
        return <span className="px-2 py-0.5 text-xs font-semibold rounded bg-slate-100 text-slate-700">{auth}</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Search Bar Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="flex gap-2">
            <div className="relative flex-1">
              <Search className="w-5 h-5 text-slate-400 absolute left-3.5 top-3.5" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search across all projects, requirements, decisions, security policies, and lessons..."
                className="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all"
              />
            </div>
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white text-sm font-semibold rounded-xl flex items-center gap-2 transition-colors shadow-sm"
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <Sparkles className="w-4 h-4" />
              )}
              Search
            </button>
          </div>

          {/* Strategy and Domain Filters */}
          <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-slate-100 text-xs text-slate-600">
            <div className="flex items-center gap-3">
              <span className="font-semibold text-slate-700 flex items-center gap-1">
                <Filter className="w-3.5 h-3.5 text-slate-500" />
                Strategy:
              </span>
              {(['HYBRID', 'KEYWORD', 'SEMANTIC'] as const).map((strat) => (
                <button
                  key={strat}
                  type="button"
                  onClick={() => setStrategy(strat)}
                  className={`px-2.5 py-1 rounded-lg font-medium transition-all ${
                    strategy === strat
                      ? 'bg-indigo-100 text-indigo-800 border border-indigo-200 font-semibold'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {strat}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2">
              <span className="font-semibold text-slate-700">Domain:</span>
              <select
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                className="px-2.5 py-1 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
              >
                <option value="">All Domains</option>
                <option value="TECHNICAL">TECHNICAL</option>
                <option value="SECURITY">SECURITY</option>
                <option value="AI">AI</option>
                <option value="CLIENT">CLIENT</option>
                <option value="DECISIONS">DECISIONS</option>
                <option value="GOVERNANCE">GOVERNANCE</option>
                <option value="RELIABILITY">RELIABILITY</option>
              </select>
            </div>
          </div>
        </form>
      </div>

      {/* Results List */}
      <div className="space-y-4">
        {loading ? (
          <div className="p-12 text-center text-slate-500 animate-pulse bg-white rounded-xl border border-slate-200">
            Performing multi-factor hybrid relevance retrieval...
          </div>
        ) : searched && results.length === 0 ? (
          <div className="p-12 text-center bg-white rounded-xl border border-slate-200">
            <p className="text-slate-600 font-medium">No authorized knowledge records found for &quot;{query}&quot;.</p>
            <p className="text-xs text-slate-400 mt-1">Try broadening search terms or switching retrieval strategies.</p>
          </div>
        ) : (
          results.map((r) => (
            <div
              key={r.knowledge_code}
              className="bg-white p-5 rounded-xl border border-slate-200 hover:border-slate-300 shadow-sm transition-all space-y-3"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <span className="font-mono text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
                      {r.knowledge_code}
                    </span>
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                      {r.domain}
                    </span>
                    {getAuthorityBadge(r.authority)}
                    <span className="text-xs text-slate-400 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {r.freshness}
                    </span>
                  </div>
                  <h4 className="text-base font-bold text-slate-900">{r.title}</h4>
                </div>

                <div className="text-right">
                  <div className="text-xs font-mono font-bold text-slate-700">Score: {r.score}</div>
                  <div className="text-[10px] text-slate-400">Relevance Tier</div>
                </div>
              </div>

              <p className="text-sm text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-100">
                {r.snippet}
              </p>

              <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
                <div className="flex items-center gap-4 text-slate-500">
                  <span>Provenance: <strong>{r.provenance}</strong></span>
                  <span>Type: <strong>{r.item_type}</strong></span>
                </div>

                <div className="flex items-center gap-2">
                  {feedbackGiven[r.knowledge_code] ? (
                    <span className="text-emerald-600 font-medium flex items-center gap-1">
                      <CheckCircle className="w-3.5 h-3.5" /> Feedback recorded
                    </span>
                  ) : (
                    <>
                      <span className="text-slate-400">Helpful?</span>
                      <button
                        onClick={() => handleFeedback(r.knowledge_code, true)}
                        className="p-1 text-slate-400 hover:text-emerald-600 hover:bg-slate-100 rounded transition-colors"
                        title="Helpful"
                      >
                        <ThumbsUp className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleFeedback(r.knowledge_code, false)}
                        className="p-1 text-slate-400 hover:text-rose-600 hover:bg-slate-100 rounded transition-colors"
                        title="Not Helpful"
                      >
                        <ThumbsDown className="w-3.5 h-3.5" />
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
