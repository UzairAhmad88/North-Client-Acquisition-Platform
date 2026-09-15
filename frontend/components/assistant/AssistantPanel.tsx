'use client';

import React, { useState } from 'react';
import { AssistantQueryResponse, searchApi } from '@/lib/api/search';

export const AssistantPanel: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<
    Array<{ role: 'user' | 'assistant'; content: string; sources?: any[]; actions?: any[] }>
  >([
    {
      role: 'assistant',
      content:
        'Hello! I am your Uzaii Platform Assistant. Ask me anything about qualified leads, at-risk projects, requirements, proposals, or operational metrics.',
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    const userText = question.trim();
    setQuestion('');
    setMessages((prev) => [...prev, { role: 'user', content: userText }]);
    setLoading(true);
    setError(null);

    try {
      const response = await searchApi.askAssistant({ question: userText });
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.answer,
          sources: response.sources,
          actions: response.suggested_actions,
        },
      ]);
    } catch (err: any) {
      setError(err.message || 'Assistant response failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col h-[700px]">
      {/* Header */}
      <div className="flex justify-between items-center pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-indigo-400"></span>
            Platform Natural-Language Assistant
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Grounded question answering with provenance citations and authorized query planning.
          </p>
        </div>
        <span className="text-[11px] font-mono bg-indigo-950/60 text-indigo-300 px-2 py-1 rounded border border-indigo-800/40">
          PROVENANCE-AWARE
        </span>
      </div>

      {error && (
        <div className="my-3 p-3 bg-red-950/60 border border-red-800 text-red-200 text-xs rounded-lg">
          {error}
        </div>
      )}

      {/* Message Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 my-2">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex flex-col space-y-2 ${
              m.role === 'user' ? 'items-end' : 'items-start'
            }`}
          >
            <div
              className={`p-4 rounded-xl text-xs leading-relaxed max-w-2xl ${
                m.role === 'user'
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-slate-950 border border-slate-800 text-slate-200 shadow'
              }`}
            >
              <div className="font-bold text-[10px] uppercase tracking-wider mb-1 opacity-70">
                {m.role === 'user' ? 'You' : 'Uzaii Assistant'}
              </div>
              <p className="whitespace-pre-wrap">{m.content}</p>

              {/* Source References */}
              {m.sources && m.sources.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-800/60 space-y-1">
                  <span className="text-[10px] font-bold text-slate-400 uppercase">
                    Cited Sources:
                  </span>
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {m.sources.map((s, sIdx) => (
                      <a
                        key={sIdx}
                        href={s.action_url || '#'}
                        className="text-[10px] bg-slate-900 hover:bg-slate-800 text-cyan-300 px-2 py-1 rounded border border-slate-700 inline-flex items-center gap-1"
                      >
                        <span>📄</span>
                        <span className="font-semibold">{s.title}</span>
                        <span className="text-slate-500">({s.entity_type})</span>
                      </a>
                    ))}
                  </div>
                </div>
              )}

              {/* Quick Actions */}
              {m.actions && m.actions.length > 0 && (
                <div className="mt-2 pt-2 border-t border-slate-800/40 flex flex-wrap gap-1.5">
                  {m.actions.map((act, aIdx) => (
                    <a
                      key={aIdx}
                      href={act.url || '#'}
                      className="text-[10px] bg-cyan-950/60 hover:bg-cyan-900 text-cyan-200 px-2.5 py-1 rounded border border-cyan-800/50 inline-flex items-center gap-1"
                    >
                      <span>⚡</span> {act.label} ↗
                    </a>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-center space-x-2 text-xs text-slate-500 italic p-3 animate-pulse">
            <span>Thinking and retrieving authorized context...</span>
          </div>
        )}
      </div>

      {/* Input Bar */}
      <form onSubmit={handleAsk} className="pt-3 border-t border-slate-800 flex space-x-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question (e.g. 'Show projects currently at risk', 'Find proposal for ABC Restaurant')..."
          disabled={loading}
          className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-bold rounded-lg shadow transition"
        >
          {loading ? 'Asking...' : 'Ask Assistant'}
        </button>
      </form>
    </div>
  );
};
