'use client';

import React, { useState } from 'react';
import { digitalTwinApi, CopilotResponse } from '@/lib/api/digitalTwin';

export const TwinCopilot: React.FC = () => {
  const [query, setQuery] = useState('What happens if we increase prices by 10% and boost conversion to 10%?');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<CopilotResponse | null>(null);

  const handleAskCopilot = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await digitalTwinApi.queryCopilot(query);
      setResponse((res as any)?.data || res);
    } catch (err) {
      console.error('Copilot query failed', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-bold text-white">Strategic What-If Copilot</h3>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            Natural Language AI
          </span>
        </div>
        <p className="text-xs text-slate-400 mt-0.5">
          Ask complex strategic questions in natural language. Copilot parameterizes scenarios and executes sandboxed simulations.
        </p>
      </div>

      <div className="flex gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAskCopilot()}
          placeholder="Ask a strategic question (e.g. 'What if support volume doubles and we hire 2 developers?')..."
          className="flex-1 px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-indigo-500"
        />
        <button
          onClick={handleAskCopilot}
          disabled={loading || !query.trim()}
          className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition shadow-lg shadow-indigo-600/25 flex items-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Evaluating...
            </>
          ) : (
            'Simulate Query'
          )}
        </button>
      </div>

      {response && (
        <div className="p-5 bg-slate-950/70 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-indigo-400 uppercase tracking-wider">Intent: {response.intent}</span>
            <span className="text-slate-500">Confidence: {(response.confidence * 100).toFixed(0)}%</span>
          </div>

          <p className="text-sm text-slate-200 leading-relaxed">{response.explanation}</p>

          <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-300">
            <strong>Governance Notice:</strong> {response.governance_notice}
          </div>
        </div>
      )}
    </div>
  );
};
