'use client';

import React, { useState } from 'react';
import { innovationApi, InnovationCopilotResponse } from '../../lib/api/innovation';

interface InnovationCopilotProps {
  workspaceId: string;
}

const PRESET_PROMPTS = [
  'Find problems worth solving.',
  'Generate ideas for mid-market customer segments.',
  'Which ideas have the strongest empirical evidence?',
  'What assumptions should we test first?',
  'Design an experiment for this hypothesis.',
  'Analyze these experiment results.',
  'Which product concept has the best unit economics?',
  'Should we continue, pivot, or stop?',
  'Create an MVP plan.'
];

export const InnovationCopilot: React.FC<InnovationCopilotProps> = ({ workspaceId }) => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState<Array<{ role: 'user' | 'copilot'; text: string; data?: InnovationCopilotResponse }>>([
    {
      role: 'copilot',
      text: 'Hello! I am your Product & Innovation Intelligence Copilot. I analyze customer pain points, score ideas transparently, map critical assumptions, design experiments, and evaluate Stage-Gates without fabricating demand.'
    }
  ]);

  const handleSend = async (textToSend?: string) => {
    const q = textToSend || query;
    if (!q.trim() || isLoading) return;

    setHistory(prev => [...prev, { role: 'user', text: q }]);
    setQuery('');
    setIsLoading(true);

    try {
      const resp = await innovationApi.queryCopilot(q, workspaceId);
      setHistory(prev => [
        ...prev,
        {
          role: 'copilot',
          text: resp.answer,
          data: resp
        }
      ]);
    } catch (err: any) {
      setHistory(prev => [
        ...prev,
        {
          role: 'copilot',
          text: `Error processing innovation query: ${err?.message || 'Server error'}`
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 backdrop-blur-md shadow-2xl flex flex-col h-[650px]">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-indigo-500 animate-pulse" />
          <h3 className="text-base font-semibold text-slate-100">Innovation Copilot (AI R&D Intelligence)</h3>
        </div>
        <span className="text-[11px] px-2 py-0.5 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-300">
          Zero-Hallucination Mode • Grounded Evidence
        </span>
      </div>

      {/* Preset Prompts */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 mb-3 scrollbar-none">
        {PRESET_PROMPTS.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(prompt)}
            disabled={isLoading}
            className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-full border border-slate-800 bg-slate-950/60 hover:border-slate-700 hover:bg-slate-800 text-slate-300 transition-colors disabled:opacity-50"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Message Stream */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-1 mb-4 text-xs">
        {history.map((msg, i) => (
          <div
            key={i}
            className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-xl p-3.5 leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-slate-950 border border-slate-800 text-slate-200 shadow-sm'
              }`}
            >
              <div className="whitespace-pre-line">{msg.text}</div>

              {/* Copilot Grounding Metadata */}
              {msg.data && (
                <div className="mt-3 pt-3 border-t border-slate-800/80 space-y-2 text-[11px]">
                  {msg.data.grounding_evidence && msg.data.grounding_evidence.length > 0 && (
                    <div>
                      <span className="text-slate-400 font-semibold">Evidence Grounding:</span>
                      <ul className="list-disc list-inside text-emerald-400 mt-0.5">
                        {msg.data.grounding_evidence.map((ev, idx) => (
                          <li key={idx}>{ev}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {msg.data.assumptions_identified && msg.data.assumptions_identified.length > 0 && (
                    <div>
                      <span className="text-slate-400 font-semibold">Underlying Assumptions:</span>
                      <ul className="list-disc list-inside text-amber-400 mt-0.5">
                        {msg.data.assumptions_identified.map((asmp, idx) => (
                          <li key={idx}>{asmp}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {msg.data.limitations && msg.data.limitations.length > 0 && (
                    <div>
                      <span className="text-slate-400 font-semibold">Uncertainties & Limitations:</span>
                      <ul className="list-disc list-inside text-slate-400 mt-0.5">
                        {msg.data.limitations.map((lim, idx) => (
                          <li key={idx}>{lim}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-slate-400 italic">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce" />
            Synthesizing evidence, calculating statistical validity, and mapping risks...
          </div>
        )}
      </div>

      {/* Input Form */}
      <form
        onSubmit={e => {
          e.preventDefault();
          handleSend();
        }}
        className="flex gap-2"
      >
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Ask Copilot about problem-solution fit, experiment designs, PRD generation..."
          className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg shadow-lg shadow-indigo-600/30 transition-all disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
};
