'use client';

import React, { useState } from 'react';
import { CopilotResponse, businessOSApi } from '@/lib/api/business_os';

export const ExecutiveAssistant: React.FC = () => {
  const [query, setQuery] = useState<string>('');
  const [response, setResponse] = useState<CopilotResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleAsk = async (textToQuery?: string) => {
    const q = textToQuery || query;
    if (!q.trim()) return;
    try {
      setIsLoading(true);
      const res = await businessOSApi.queryCopilot(q);
      setResponse(res);
      if (!textToQuery) setQuery('');
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="border-b border-slate-800 pb-4 mb-6">
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <span>🤖</span> Executive AI Assistant (Strategic Copilot)
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Grounded decision-support assistant with metric traceability and strict action guardrails.
        </p>
      </div>

      <div className="space-y-4">
        {/* Response Box */}
        {response && (
          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-5">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-3 border-b border-slate-800 pb-2">
              <span>Query: <strong className="text-slate-200">"{response.user_query}"</strong></span>
              <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-semibold">
                Confidence: {response.confidence}
              </span>
            </div>

            <div className="text-sm text-slate-200 leading-relaxed whitespace-pre-line mb-4">
              {response.answer_markdown}
            </div>

            {/* Evidence Sources */}
            {response.evidence_sources.length > 0 && (
              <div className="mt-4 pt-3 border-t border-slate-800/80 text-xs">
                <span className="font-bold text-slate-400">Verified Evidence Sources:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {response.evidence_sources.map((src, i) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300 text-[11px]">
                      {src.domain || src.table || src.policy}: {src.metric || src.rule || src.count || ''}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Suggested Followups */}
            {response.suggested_followups.length > 0 && (
              <div className="mt-4 pt-3 border-t border-slate-800/80">
                <span className="text-xs font-bold text-indigo-400">Suggested Follow-Up Inquiries:</span>
                <div className="flex flex-wrap gap-2 mt-1.5">
                  {response.suggested_followups.map((fol, i) => (
                    <button
                      key={i}
                      onClick={() => handleAsk(fol)}
                      className="px-2.5 py-1 bg-indigo-950/40 hover:bg-indigo-900/60 border border-indigo-800/60 text-indigo-300 rounded text-xs transition-all"
                    >
                      {fol}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Input */}
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
            placeholder="Ask a strategic question (e.g. 'How is the business doing?', 'What are our biggest risks?')..."
            className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
          />
          <button
            onClick={() => handleAsk()}
            disabled={isLoading || !query.trim()}
            className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-lg text-xs font-semibold transition-all"
          >
            {isLoading ? 'Synthesizing...' : 'Ask Copilot'}
          </button>
        </div>
      </div>
    </div>
  );
};
