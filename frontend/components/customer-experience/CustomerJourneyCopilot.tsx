'use client';

import React, { useState } from 'react';
import { Bot, Send, Sparkles, ShieldCheck, Database } from 'lucide-react';
import { customerExperienceApi } from '../../lib/api/customerExperience';

interface CustomerJourneyCopilotProps {
  customerId?: string;
}

export const CustomerJourneyCopilot: React.FC<CustomerJourneyCopilotProps> = ({ customerId = 'cust-demo-001' }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversation, setConversation] = useState<Array<{ role: 'user' | 'assistant'; text: string; evidence?: string[] }>>([
    {
      role: 'assistant',
      text: "Hello! I am your Customer Experience & Journey Intelligence Copilot. Ask me anything about customer journeys, friction points, churn predictions, or VoC themes.",
      evidence: ['customer_experience_platform_service'],
    },
  ]);

  const handleSend = async () => {
    if (!query.trim() || loading) return;
    const userQ = query.trim();
    setQuery('');
    setConversation((prev) => [...prev, { role: 'user', text: userQ }]);
    setLoading(true);

    try {
      const res = await customerExperienceApi.askCopilot(userQ, customerId);
      setConversation((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: res.answer,
          evidence: res.supporting_evidence_sources || res.supporting_evidence,
        },
      ]);
    } catch (e: any) {
      setConversation((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: "I encountered an error retrieving journey evidence. Please verify your permissions.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4 flex flex-col h-[480px]">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Bot className="h-4 w-4 text-indigo-400" />
          Customer Journey Copilot (Evidence Grounded)
        </h3>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-semibold">
          Phase 57 AI
        </span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 pr-1">
        {conversation.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded-lg text-xs leading-relaxed ${
              msg.role === 'user'
                ? 'bg-indigo-600/20 border border-indigo-500/30 text-indigo-200 ml-6'
                : 'bg-slate-800/50 border border-slate-800 text-slate-300 mr-6'
            }`}
          >
            <div className="font-semibold mb-1 flex items-center gap-1.5 text-[10px] uppercase font-mono text-slate-400">
              {msg.role === 'user' ? 'You' : <><Sparkles className="h-3 w-3 text-indigo-400" /> CX Copilot</>}
            </div>
            <p>{msg.text}</p>
            {msg.evidence && msg.evidence.length > 0 && (
              <div className="mt-2 pt-1.5 border-t border-slate-800/60 flex items-center gap-1.5 text-[10px] text-slate-400">
                <Database className="h-3 w-3 text-cyan-400" />
                <span>Evidence: {msg.evidence.join(', ')}</span>
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-800 text-xs text-slate-400 animate-pulse mr-6">
            Synthesizing customer journey telemetry and verifying governance boundaries...
          </div>
        )}
      </div>

      <div className="flex items-center gap-2 pt-2 border-t border-slate-800">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask e.g. Where did the customer experience friction?"
          className="flex-1 px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          onClick={handleSend}
          disabled={loading || !query.trim()}
          className="px-3.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors"
        >
          <Send className="h-3.5 w-3.5" />
          Ask
        </button>
      </div>
    </div>
  );
};
