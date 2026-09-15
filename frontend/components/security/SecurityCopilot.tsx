'use client';

import React, { useState } from 'react';
import { securityOpsApi } from '@/lib/api/securityOps';
import { Bot, Send, ShieldCheck, Sparkles, BookOpen, AlertCircle } from 'lucide-react';

export default function SecurityCopilot() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversation, setConversation] = useState<Array<{ role: 'user' | 'assistant'; text: string; evidence?: string[] }>>([
    {
      role: 'assistant',
      text: 'Hello, I am your grounded Security AI Copilot. I can synthesize attack chains, explain detection timelines, quantify blast radius, and recommend containment steps based on live telemetry evidence. I cannot execute mutating commands.',
      evidence: ['System Guardrail Policy', 'BaseAgent Runtime'],
    },
  ]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userText = query;
    setQuery('');
    setConversation((prev) => [...prev, { role: 'user', text: userText }]);
    setLoading(true);

    try {
      const res = await securityOpsApi.queryCopilot(userText);
      setConversation((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: res.answer_markdown,
          evidence: res.evidence_sources,
        },
      ]);
    } catch (err: any) {
      setConversation((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: 'Error consulting Security Copilot engine. Please review backend logs.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    'What is our current enterprise security posture grade?',
    'Explain the blast radius of current active incidents.',
    'Summarize recent brute force and prompt injection telemetry.',
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div className="flex justify-between items-center border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Bot className="w-5 h-5 text-indigo-600" />
            Security Operations AI Copilot
          </h3>
          <p className="text-xs text-slate-500">
            Grounded investigation intelligence with evidence citations (Sections 29 & 30)
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
          <ShieldCheck className="w-3.5 h-3.5" /> Read-Only Advisory AI
        </span>
      </div>

      {/* Chat Messages */}
      <div className="h-80 overflow-y-auto space-y-3 p-2">
        {conversation.map((msg, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div
              className={`p-3.5 rounded-2xl text-xs max-w-2xl ${
                msg.role === 'user'
                  ? 'bg-indigo-600 text-white rounded-br-none'
                  : 'bg-slate-50 border border-slate-200 text-slate-800 rounded-bl-none'
              }`}
            >
              <p className="leading-relaxed whitespace-pre-wrap">{msg.text}</p>

              {msg.evidence && msg.evidence.length > 0 && (
                <div className="mt-2.5 pt-2 border-t border-slate-200/60 flex flex-wrap items-center gap-1.5">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                    <BookOpen className="w-3 h-3" /> Evidence:
                  </span>
                  {msg.evidence.map((ev, i) => (
                    <span
                      key={i}
                      className="text-[10px] font-mono bg-white px-2 py-0.5 rounded border border-slate-200 text-slate-600"
                    >
                      {ev}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 text-xs text-slate-400 italic p-2">
            <Sparkles className="w-4 h-4 animate-spin text-indigo-500" />
            <span>Analyzing incident evidence and correlating graph...</span>
          </div>
        )}
      </div>

      {/* Sample Prompts */}
      <div className="flex flex-wrap gap-2 pt-1">
        {samplePrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => setQuery(p)}
            className="text-[11px] px-2.5 py-1 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Input */}
      <form onSubmit={handleSend} className="flex gap-2 pt-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask Security AI Copilot about attacks, blast radius, or telemetry..."
          className="flex-1 px-4 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="px-4 py-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50 transition-colors flex items-center gap-1.5 shadow-xs"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
