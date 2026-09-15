'use client';

import React, { useState } from 'react';
import { processIntelligenceApi } from '@/lib/api/processIntelligence';
import { Bot, Send, Sparkles, ShieldCheck } from 'lucide-react';

interface Props {
  processId: string;
}

export default function ProcessCopilot({ processId }: Props) {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; text: string }>>([
    {
      role: 'assistant',
      text: 'Hello! I am your Process Intelligence Copilot. Ask me about bottlenecks, variant frequencies, conformance violations, or simulation outcomes.',
    },
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userText = query;
    setQuery('');
    setMessages((prev) => [...prev, { role: 'user', text: userText }]);
    setLoading(true);

    try {
      const res = await processIntelligenceApi.queryCopilot({
        process_id: processId,
        query: userText,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: res.response || 'Analysis complete.',
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: 'Failed to communicate with Process Copilot.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col h-[550px]">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Bot className="w-5 h-5 text-indigo-400" /> Process Intelligence Copilot
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">Evidence-grounded conversational process analytics</p>
        </div>
        <span className="text-xs text-emerald-400 flex items-center gap-1 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
          <ShieldCheck className="w-3.5 h-3.5" /> Guardrails Enforced
        </span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 pr-2">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`p-3.5 rounded-lg text-sm ${
              m.role === 'user'
                ? 'bg-indigo-600/20 border border-indigo-500/30 text-indigo-100 ml-12'
                : 'bg-slate-950 border border-slate-800 text-slate-200 mr-12'
            }`}
          >
            <p>{m.text}</p>
          </div>
        ))}
      </div>

      <form onSubmit={handleSend} className="mt-4 flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask where time is lost or how to optimize this process..."
          className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg flex items-center gap-1.5 text-sm font-medium transition"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
