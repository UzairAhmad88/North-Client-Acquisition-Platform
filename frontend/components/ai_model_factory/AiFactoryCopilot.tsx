import React, { useState } from 'react';
import { aiModelFactoryApi, AiCopilotResponse } from '@/lib/api/aiModelFactory';

export const AiFactoryCopilot: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<AiCopilotResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'facts' | 'inferences' | 'hypotheses' | 'recommendations'>('facts');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setLoading(true);
    try {
      const res = await aiModelFactoryApi.queryCopilot(query);
      setResponse(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const sampleQueries = [
    'What is the accuracy and stage of Customer Churn Risk Classifier?',
    'Are there any active PSI drift breaches on production models?',
    'What is our current monthly GPU and token FinOps expenditure?',
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-5">
      <div>
        <h3 className="text-lg font-semibold text-slate-100">Grounded AI Model Factory Copilot</h3>
        <p className="text-xs text-slate-400 mt-0.5">
          Ask conversational queries regarding models, evaluations, drift, GPU utilization, and AI FinOps with strict fact/inference separation.
        </p>
      </div>

      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask AI Model Factory Copilot (e.g. 'Show active model evaluations and drift status')..."
          className="flex-1 bg-slate-800/80 border border-slate-700 rounded-lg px-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium transition disabled:opacity-50"
        >
          {loading ? 'Reasoning...' : 'Ask Copilot'}
        </button>
      </form>

      <div className="flex flex-wrap gap-2 items-center text-xs">
        <span className="text-slate-500 text-[11px]">Suggested Queries:</span>
        {sampleQueries.map((q, idx) => (
          <button
            key={idx}
            onClick={() => setQuery(q)}
            className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/60 text-[11px] transition"
          >
            {q}
          </button>
        ))}
      </div>

      {response && (
        <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/70 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-indigo-400">Grounded Response Matrix</span>
            <div className="flex items-center gap-2">
              <span className="text-xs text-emerald-400 font-mono font-bold">
                Confidence: {(response.confidence_score * 100).toFixed(0)}%
              </span>
            </div>
          </div>

          <div className="flex gap-2 border-b border-slate-700 pb-2 text-xs">
            {(['facts', 'inferences', 'hypotheses', 'recommendations'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1 rounded capitalize font-medium transition ${
                  activeTab === tab
                    ? 'bg-indigo-600 text-white font-bold'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {tab} ({response[tab]?.length || 0})
              </button>
            ))}
          </div>

          <ul className="space-y-2 text-xs text-slate-300">
            {response[activeTab]?.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-slate-900/40 p-2.5 rounded border border-slate-800">
                <span className="text-indigo-400 font-bold">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>

          <p className="text-[10px] text-slate-500 italic pt-2 border-t border-slate-700/50">
            {response.governance_notice}
          </p>
        </div>
      )}
    </div>
  );
};
