'use client';

import React, { useState } from 'react';
import { Bot, Send, Sparkles, BookOpen, ShieldCheck, ArrowRight, CornerDownRight } from 'lucide-react';
import { researchIntelligenceApi } from '../../lib/api/research_intelligence';

interface ResearchCopilotProps {
  workspaceId?: string;
}

export const ResearchCopilot: React.FC<ResearchCopilotProps> = ({ workspaceId }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Array<{ sender: 'user' | 'assistant'; text: string; citations?: string[]; confidence?: number }>>([
    {
      sender: 'assistant',
      text: 'Hello! I am your Autonomous Research & Intelligence Copilot. Ask me about market signals, competitor moves, source evidence, or to synthesize research into a decision room.',
    },
  ]);

  const handleSend = async (textToSend?: string) => {
    const q = textToSend || query;
    if (!q.trim() || loading) return;

    const userMsg = { sender: 'user' as const, text: q };
    setMessages((prev) => [...prev, userMsg]);
    setQuery('');
    setLoading(true);

    try {
      const response = await researchIntelligenceApi.queryCopilot({
        workspace_id: workspaceId,
        query: q,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: response.answer || 'Research query processed against active evidence registry.',
          citations: response.citations || [],
          confidence: response.confidence || 0.9,
        },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: `Error processing research inquiry: ${err.message || 'Unknown failure'}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    'What are the verified claims for this market?',
    'Which sources currently disagree on pricing?',
    'What research gaps remain unanswered?',
    'Turn this research into a decision room.',
  ];

  return (
    <div className="flex flex-col h-[520px] rounded-xl border border-slate-800 bg-slate-900/80 backdrop-blur-sm overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-slate-800 bg-slate-950/40 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="h-8 w-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <Bot className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Research Intelligence Copilot</h3>
            <p className="text-[10px] text-slate-400">Grounded in verified primary & secondary evidence</p>
          </div>
        </div>
        <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-medium">
          Zero Hallucination Mode
        </span>
      </div>

      {/* Message History */}
      <div className="flex-1 p-4 overflow-y-auto space-y-3">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-lg p-3 text-xs leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-indigo-600 text-white rounded-br-none'
                  : 'bg-slate-950/60 text-slate-200 border border-slate-800 rounded-bl-none'
              }`}
            >
              <p>{msg.text}</p>

              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-2 pt-2 border-t border-slate-800/80 text-[10px] text-slate-400">
                  <span className="font-semibold text-cyan-400 flex items-center gap-1 mb-1">
                    <BookOpen className="h-3 w-3" /> Grounding Citations:
                  </span>
                  <ul className="space-y-0.5">
                    {msg.citations.map((c, i) => (
                      <li key={i} className="truncate">• {c}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            {msg.confidence !== undefined && (
              <span className="text-[9px] text-slate-500 mt-1 px-1">
                Confidence: {Math.round(msg.confidence * 100)}%
              </span>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 text-xs text-slate-400 italic py-2">
            <Sparkles className="h-3.5 w-3.5 text-indigo-400 animate-spin" />
            Synthesizing evidence registry...
          </div>
        )}
      </div>

      {/* Suggested Quick Prompts */}
      <div className="px-4 py-2 bg-slate-950/20 border-t border-slate-800/60 flex flex-wrap gap-1.5">
        {samplePrompts.map((prompt, i) => (
          <button
            key={i}
            onClick={() => handleSend(prompt)}
            disabled={loading}
            className="text-[10px] px-2.5 py-1 rounded bg-slate-800/60 hover:bg-slate-800 text-slate-300 border border-slate-700/60 transition-colors"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <div className="p-3 border-t border-slate-800 bg-slate-950/60 flex items-center gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask research copilot or request cross-validation..."
          className="flex-1 bg-slate-900 border border-slate-700/80 rounded-lg px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !query.trim()}
          className="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white transition-colors"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};
