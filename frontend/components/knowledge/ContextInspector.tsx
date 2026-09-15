'use client';

import React, { useState } from 'react';
import { assembleAiContext, ContextBundle } from '@/lib/api/knowledge';
import { Brain, ShieldAlert, Cpu, Terminal, CheckCircle, AlertTriangle } from 'lucide-react';

export default function ContextInspectorComponent() {
  const [taskIntent, setTaskIntent] = useState('Prepare estimate and architecture for multi-tenant logistics portal');
  const [agentId, setAgentId] = useState('estimation_agent');
  const [budgetTokens, setBudgetTokens] = useState(4000);
  const [loading, setLoading] = useState(false);
  const [bundle, setBundle] = useState<ContextBundle | null>(null);

  const handleAssemble = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!taskIntent.trim()) return;

    setLoading(true);
    try {
      const res = await assembleAiContext({
        task_intent: taskIntent.trim(),
        agent_id: agentId,
        budget_tokens: budgetTokens,
      });
      setBundle(res);
    } catch (err) {
      console.error('Context assembly failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <Brain className="w-5 h-5 text-purple-600" />
          AI Context Engine & Prompt Injection Defense Inspector
        </h3>
        <p className="text-xs text-slate-500 mt-1">
          Section 31-35 & 70: Live demonstration of permission-filtered, budget-bounded context assembly with mandatory &lt;UNTRUSTED_RETRIEVED_KNOWLEDGE&gt; security encapsulation.
        </p>

        <form onSubmit={handleAssemble} className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="md:col-span-2">
            <label className="font-semibold text-slate-700 block mb-1">Target AI Agent Task Intent</label>
            <input
              type="text"
              value={taskIntent}
              onChange={(e) => setTaskIntent(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label className="font-semibold text-slate-700 block mb-1">Target Agent</label>
            <select
              value={agentId}
              onChange={(e) => setAgentId(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="estimation_agent">estimation_agent</option>
              <option value="proposal_agent">proposal_agent</option>
              <option value="support_agent">support_agent</option>
              <option value="solution_agent">solution_agent</option>
              <option value="executive_agent">executive_agent</option>
            </select>
          </div>

          <div className="md:col-span-3 flex justify-between items-center pt-2">
            <div className="flex items-center gap-2">
              <span className="text-slate-500">Token Budget:</span>
              <span className="font-bold text-slate-900">{budgetTokens} tokens</span>
            </div>
            <button
              type="submit"
              disabled={loading || !taskIntent.trim()}
              className="px-5 py-2.5 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white font-semibold rounded-lg shadow-sm flex items-center gap-1.5 transition-colors"
            >
              {loading ? 'Assembling Context...' : 'Assemble AI Context Bundle'}
            </button>
          </div>
        </form>
      </div>

      {bundle && (
        <div className="space-y-4 animate-in fade-in duration-150">
          {/* Summary KPIs */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <span className="text-xs text-slate-400 font-semibold block">Request Code</span>
              <span className="font-mono text-sm font-bold text-purple-600">{bundle.request_code}</span>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <span className="text-xs text-slate-400 font-semibold block">Retrieved Items</span>
              <span className="text-lg font-bold text-slate-900">{bundle.items_count} items</span>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <span className="text-xs text-slate-400 font-semibold block">Tokens Consumed</span>
              <span className="text-lg font-bold text-indigo-600">
                {bundle.consumed_tokens} / {bundle.budget_tokens}
              </span>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <span className="text-xs text-slate-400 font-semibold block">Citations Traceable</span>
              <span className="text-lg font-bold text-emerald-600">{bundle.citations.length}</span>
            </div>
          </div>

          {/* Uncertainty Disclosures */}
          {bundle.uncertainty_disclosures && bundle.uncertainty_disclosures.length > 0 && (
            <div className="bg-amber-50 p-4 rounded-xl border border-amber-200 space-y-1 text-xs text-amber-900">
              <div className="font-bold flex items-center gap-1.5 text-amber-800">
                <AlertTriangle className="w-4 h-4 text-amber-600" />
                Uncertainty & Disclosure Signals (Rule 17)
              </div>
              {bundle.uncertainty_disclosures.map((disc, idx) => (
                <p key={idx} className="font-mono text-[11px] pl-5">{disc}</p>
              ))}
            </div>
          )}

          {/* Raw Encapsulated Terminal View */}
          <div className="bg-slate-950 text-slate-200 p-6 rounded-2xl border border-slate-800 font-mono text-xs space-y-2">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800 text-slate-400">
              <span className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-emerald-400" />
                Prompt Injection Defense Boundary Stream
              </span>
              <span className="text-[10px] text-slate-500">ISO/IEC 42001 & NIST AI RMF Compliant</span>
            </div>
            <pre className="overflow-x-auto whitespace-pre-wrap leading-relaxed max-h-96 text-[11px] text-emerald-300">
              {bundle.encapsulated_context}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
