'use client';

import React, { useState } from 'react';
import { Bot, Send, Sparkles, ShieldAlert, Cpu, ArrowRight } from 'lucide-react';
import { WorkforceCopilotResponse } from '../../lib/api/workforce';

interface WorkforceCopilotProps {
  onQuery?: (query: string) => Promise<WorkforceCopilotResponse>;
}

export const WorkforceCopilot: React.FC<WorkforceCopilotProps> = ({ onQuery }) => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Array<{
    role: 'user' | 'assistant';
    content: string;
    evidence?: string[];
    suggestedActions?: string[];
  }>>([
    {
      role: 'assistant',
      content: 'I am the AI Workforce Copilot. I coordinate specialized knowledge workers, inspect task graph progress, analyze workforce economics, and track supervision queues. How can I assist workforce operations today?',
    },
  ]);

  const sampleQueries = [
    'Which AI workers are currently operating at peak capacity?',
    'What tasks are waiting for human executive review?',
    'How much did the AI workforce save in human labor hours this month?',
    'Decompose our objective: Launch AI customer support service in Q4',
  ];

  const handleSend = async (customQuery?: string) => {
    const textToSend = customQuery || query;
    if (!textToSend.trim() || isLoading) return;

    setMessages((prev) => [...prev, { role: 'user', content: textToSend }]);
    setQuery('');
    setIsLoading(true);

    try {
      if (onQuery) {
        const res = await onQuery(textToSend);
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: res.answer,
            evidence: res.evidence,
            suggestedActions: res.suggested_actions,
          },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: `The workforce is operating nominally across 20 active profiles. All workers are within their $15/day budget ceilings with zero policy violations recorded.`,
            evidence: ['20 active workers', '42.5 human hours saved this week'],
            suggestedActions: ['Inspect pending reviews', 'View Department budgets'],
          },
        ]);
      }
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Unable to process workforce query: ${err.message || 'Unknown error'}.`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[650px] rounded-xl border border-slate-700/60 bg-slate-900/60 backdrop-blur-sm overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-800 bg-slate-950/40">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-indigo-500/10 border border-indigo-500/30">
            <Bot className="h-5 w-5 text-indigo-400" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              Workforce Intelligence Copilot
              <span className="px-2 py-0.5 rounded text-[10px] bg-indigo-500/20 text-indigo-300 font-normal">
                Multi-Agent OS
              </span>
            </h3>
            <p className="text-[11px] text-slate-400">Autonomous workforce tracking, task decomposition, and supervision analytics.</p>
          </div>
        </div>
        <div className="flex items-center gap-1 text-[11px] text-amber-400/80 bg-amber-500/10 px-2.5 py-1 rounded-md border border-amber-500/20">
          <ShieldAlert className="h-3.5 w-3.5 mr-1" />
          Governed Advisory
        </div>
      </div>

      {/* Message Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${
              msg.role === 'user' ? 'items-end' : 'items-start'
            }`}
          >
            <div
              className={`max-w-[85%] rounded-xl p-4 text-xs leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-indigo-600 text-white rounded-br-none shadow-md shadow-indigo-600/20'
                  : 'bg-slate-950/80 border border-slate-800 text-slate-200 rounded-bl-none space-y-3'
              }`}
            >
              <div>{msg.content}</div>

              {msg.role === 'assistant' && (
                <>
                  {msg.evidence && msg.evidence.length > 0 && (
                    <div className="pt-2 border-t border-slate-800/80">
                      <div className="text-[10px] uppercase font-bold text-slate-400 mb-1">Observed Telemetry:</div>
                      <ul className="space-y-0.5 text-slate-300">
                        {msg.evidence.map((ev, i) => (
                          <li key={i} className="flex items-center gap-1.5 text-[11px]">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                            {ev}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {msg.suggestedActions && msg.suggestedActions.length > 0 && (
                    <div className="pt-2 border-t border-slate-800/80">
                      <div className="text-[10px] uppercase font-bold text-indigo-400 mb-1">Suggested Actions:</div>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {msg.suggestedActions.map((act, i) => (
                          <span
                            key={i}
                            className="px-2 py-1 rounded bg-indigo-950/40 border border-indigo-500/30 text-indigo-300 text-[10px] font-medium flex items-center gap-1"
                          >
                            <ArrowRight className="h-2.5 w-2.5" />
                            {act}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-indigo-400 p-3 bg-slate-950/50 rounded-lg max-w-sm">
            <Cpu className="h-4 w-4 animate-spin" />
            <span>Synthesizing multi-agent workforce telemetry...</span>
          </div>
        )}
      </div>

      {/* Suggested Quick Prompts */}
      <div className="px-4 py-2 bg-slate-950/40 border-t border-slate-800 flex items-center gap-2 overflow-x-auto">
        <span className="text-[10px] uppercase font-bold text-slate-500 whitespace-nowrap">Suggested:</span>
        {sampleQueries.map((q, i) => (
          <button
            key={i}
            onClick={() => handleSend(q)}
            className="text-[11px] text-slate-400 hover:text-white bg-slate-900 border border-slate-800 hover:border-slate-700 px-2.5 py-1 rounded-full whitespace-nowrap transition-all cursor-pointer"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <div className="p-3 bg-slate-950/80 border-t border-slate-800 flex items-center gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask about worker status, workload, task decomposition, or ROI..."
          className="flex-1 bg-slate-900 border border-slate-700/80 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          disabled={isLoading || !query.trim()}
          onClick={() => handleSend()}
          className="p-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-50 transition-all cursor-pointer"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};
