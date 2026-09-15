'use client';

import React, { useEffect, useState } from 'react';
import {
  SearchResponse,
  SearchResultItem,
  SearchSuggestion,
  searchApi,
} from '@/lib/api/search';

export const GlobalSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [activeType, setActiveType] = useState<string>('ALL');
  const [searchResponse, setSearchResponse] = useState<SearchResponse | null>(null);
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (overrideQuery?: string) => {
    const q = overrideQuery !== undefined ? overrideQuery : query;
    if (!q.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await searchApi.search({
        q: q.trim(),
        entity_type: activeType === 'ALL' ? undefined : activeType,
      });
      setSearchResponse(res);
      setSuggestions([]);
    } catch (err: any) {
      setError(err.message || 'Search execution failed');
    } finally {
      setLoading(false);
    }
  };

  const handleQueryChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const text = e.target.value;
    setQuery(text);

    if (text.length >= 2) {
      try {
        const suggs = await searchApi.getSuggestions(text);
        setSuggestions(suggs || []);
      } catch {
        setSuggestions([]);
      }
    } else {
      setSuggestions([]);
    }
  };

  const selectSuggestion = (text: string) => {
    setQuery(text);
    setSuggestions([]);
    handleSearch(text);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col space-y-6">
      {/* Top Search Header */}
      <div className="flex flex-col space-y-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
            Global Unified Platform Search
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Instant search across leads, projects, proposals, contracts, requirements, and knowledge.
          </p>
        </div>

        {/* Search Bar Input */}
        <div className="relative">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSearch();
            }}
            className="flex space-x-2"
          >
            <div className="relative flex-1">
              <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400 text-sm">
                🔍
              </span>
              <input
                type="text"
                value={query}
                onChange={handleQueryChange}
                placeholder="Search everything (e.g. 'restaurants in Peshawar', 'projects at risk', 'proposals')..."
                className="w-full bg-slate-950 border border-slate-700 rounded-lg pl-9 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
              />
            </div>
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="px-5 py-2.5 bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white text-xs font-bold rounded-lg shadow transition"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>

          {/* Autocomplete Suggestions Dropdown */}
          {suggestions.length > 0 && (
            <div className="absolute left-0 right-0 top-full mt-1 bg-slate-950 border border-slate-800 rounded-lg shadow-2xl z-40 overflow-hidden divide-y divide-slate-800/60">
              {suggestions.map((s, idx) => (
                <button
                  key={idx}
                  onClick={() => selectSuggestion(s.query || s.text)}
                  className="w-full text-left px-4 py-2.5 hover:bg-slate-800/60 flex items-center justify-between text-xs text-slate-300 transition-colors"
                >
                  <div className="flex items-center space-x-2">
                    <span className="text-slate-500">{s.type === 'RECENT_SEARCH' ? '🕒' : '✨'}</span>
                    <span>{s.text}</span>
                  </div>
                  {s.category && (
                    <span className="text-[10px] uppercase bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded font-mono">
                      {s.category}
                    </span>
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Entity Category Filter Tabs */}
        <div className="flex items-center space-x-1 overflow-x-auto bg-slate-950/60 p-1 rounded-lg border border-slate-800">
          {(['ALL', 'LEAD', 'PROJECT', 'PROPOSAL', 'CONTRACT', 'DOCUMENT', 'TASK'] as const).map(
            (type) => (
              <button
                key={type}
                onClick={() => {
                  setActiveType(type);
                  if (query.trim()) handleSearch();
                }}
                className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${
                  activeType === type
                    ? 'bg-cyan-600 text-white shadow'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {type}
              </button>
            )
          )}
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-950/60 border border-red-800 rounded-lg text-red-200 text-xs">
          {error}
        </div>
      )}

      {/* Search Results & Telemetry */}
      {searchResponse && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400 pb-2 border-b border-slate-800">
            <span>
              Found <strong className="text-slate-200">{searchResponse.total_count}</strong> result(s) for &quot;{searchResponse.query}&quot;
            </span>
            <div className="flex items-center space-x-3 text-[11px] font-mono">
              <span>Latency: {searchResponse.latency_ms}ms</span>
              <span className="bg-slate-800 px-2 py-0.5 rounded border border-slate-700 text-emerald-400">
                {searchResponse.index_freshness}
              </span>
            </div>
          </div>

          {searchResponse.results.length === 0 ? (
            <div className="text-center py-12 text-slate-500 text-sm border border-dashed border-slate-800 rounded-lg">
              No matching records found. Try adjusting your query or entity category.
            </div>
          ) : (
            <div className="space-y-3">
              {searchResponse.results.map((item: SearchResultItem) => (
                <div
                  key={item.id}
                  className="p-4 rounded-lg bg-slate-950/50 border border-slate-800 hover:border-cyan-600/40 transition-all flex flex-col space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs bg-slate-800 text-slate-300 font-mono px-2 py-0.5 rounded border border-slate-700">
                        {item.entity_type}
                      </span>
                      <h4 className="text-sm font-semibold text-slate-100">{item.title}</h4>
                      {item.status && (
                        <span className="text-[10px] bg-cyan-950/60 text-cyan-300 px-1.5 py-0.5 rounded font-mono border border-cyan-800/40">
                          {item.status}
                        </span>
                      )}
                    </div>
                    <span className="text-xs text-slate-500 font-mono">
                      Score: {Math.round(item.score * 100)}%
                    </span>
                  </div>

                  <p
                    className="text-xs text-slate-300 leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: item.snippet }}
                  />

                  {item.action_url && (
                    <div className="pt-1">
                      <a
                        href={item.action_url}
                        className="text-xs text-cyan-400 hover:text-cyan-300 font-medium inline-flex items-center gap-1"
                      >
                        Open Record ↗
                      </a>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
