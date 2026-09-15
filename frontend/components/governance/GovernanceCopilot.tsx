'use client';

import React, { useState } from 'react';
import { governanceApi, CopilotAnswer } from '@/lib/api/governance';
import { Bot, Send, ShieldAlert, Sparkles, HelpCircle, CheckCircle2, AlertTriangle } from 'lucide-react';

export default function GovernanceCopilot() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<CopilotAnswer[]>([]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const currentQuery = query.trim();
    setQuery('');
    setLoading(true);

    try {
      const response = await governanceApi.askCopilot(currentQuery);
      setHistory((prev) => [response, ...prev]);
    } catch (err) {
      console.error('GRC Copilot Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    'Explain control CTRL-IAM-MFA and its evidence requirements',
    'Summarize our current compliance posture and open critical findings',
    'What evidence is currently stale or aging?',
    'What compensating controls are required for the legacy IP restriction exception?',
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs p-6 space-y-6">
      {/* Header & Non-Negotiable Safety Disclosure */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-100 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Bot className="w-5 h-5 text-indigo-600" />
            <span>GRC AI Copilot & Regulatory Advisor</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Advisory assistant for explaining controls, analyzing evidence gaps, and drafting assessments.
          </p>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 bg-amber-50 text-amber-800 rounded-xl border border-amber-200 text-xs font-semibold">
          <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0" />
          <span>Non-Negotiable: AI cannot declare legal compliance or accept risk autonomously.</span>
        </div>
      </div>

      {/* Query Input Bar */}
      <form onSubmit={handleSend} className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask GRC Copilot about controls, evidence, risks, or frameworks..."
          className="flex-1 text-xs p-3 border border-slate-300 rounded-xl focus:outline-hidden focus:border-indigo-600"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="px-5 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl disabled:opacity-50 transition-all flex items-center gap-2 shrink-0"
        >
          {loading ? (
            <span>Analyzing...</span>
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span>Query</span>
            </>
          )}
        </button>
      </form>

      {/* Quick Prompts */}
      <div className="flex flex-wrap gap-1.5 items-center">
        <span className="text-[11px] font-semibold text-slate-400 mr-1">Quick Inquiries:</span>
        {samplePrompts.map((p, i) => (
          <button
            key={i}
            onClick={() => setQuery(p)}
            className="text-[11px] px-2.5 py-1 bg-slate-100 hover:bg-indigo-50 hover:text-indigo-700 text-slate-600 rounded-lg transition-all"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Response History */}
      <div className="space-y-4">
        {history.length === 0 ? (
          <div className="p-8 text-center text-slate-400 text-xs bg-slate-50/50 rounded-xl border border-dashed border-slate-200">
            Ask questions regarding compliance posture, control health, evidence freshness, or remediation guidance.
          </div>
        ) : (
          history.map((item, idx) => (
            <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-3">
              <div className="text-xs font-bold text-slate-900 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-indigo-600" />
                <span>Q: {item.query}</span>
              </div>

              <div className="text-xs text-slate-700 leading-relaxed whitespace-pre-wrap bg-white p-3 rounded-lg border border-slate-200">
                {item.answer}
              </div>

              {/* Citations & Uncertainty */}
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 text-[11px] pt-1 text-slate-500">
                <div className="flex items-center gap-1.5">
                  <span className="font-semibold text-slate-700">Evidence Citations:</span>
                  {item.evidence_citations.length > 0 ? (
                    item.evidence_citations.map((c, i) => (
                      <span key={i} className="font-mono px-1.5 py-0.5 bg-indigo-50 text-indigo-700 rounded text-[10px]">
                        {c}
                      </span>
                    ))
                  ) : (
                    <span className="text-slate-400">None cited</span>
                  )}
                </div>

                <div className="flex items-center gap-3">
                  <span>Uncertainty Score: <strong className="font-mono text-slate-700">{item.uncertainty_score}</strong></span>
                  <span className="text-slate-400">{new Date(item.timestamp).toLocaleTimeString()}</span>
                </div>
              </div>

              {/* Disclaimer */}
              <div className="text-[10px] text-amber-700 bg-amber-50/70 p-2 rounded-lg border border-amber-200/60">
                {item.disclaimer}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
