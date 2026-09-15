'use client';

import React, { useState } from 'react';
import { PolicyItem, administrationApi } from '@/lib/api/administration';

interface PolicyEngineViewProps {
  policies: PolicyItem[];
  onRefresh: () => void;
}

export function PolicyEngineView({ policies, onRefresh }: PolicyEngineViewProps) {
  const [selectedDomain, setSelectedDomain] = useState<string>('ALL');
  const [evalDomain, setEvalDomain] = useState<string>('AI');
  const [evalAction, setEvalAction] = useState<string>('execute_prompt');
  const [evalActorType, setEvalActorType] = useState<string>('agent');
  const [evalAmount, setEvalAmount] = useState<string>('');
  const [evalContext, setEvalContext] = useState<string>('{}');
  const [evalResult, setEvalResult] = useState<{ action_result: string; reason: string } | null>(null);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const domains = ['ALL', 'AI', 'SECURITY', 'COMMUNICATION', 'FINANCE', 'DATA', 'ACCESS', 'EXECUTION'];

  const filteredPolicies =
    selectedDomain === 'ALL'
      ? policies
      : policies.filter((p) => p.domain.toUpperCase() === selectedDomain.toUpperCase());

  const handleRunEvaluation = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsEvaluating(true);
    setEvalResult(null);
    try {
      let parsedContext = {};
      try {
        parsedContext = JSON.parse(evalContext);
      } catch {
        parsedContext = {};
      }

      const res = await administrationApi.evaluatePolicy({
        domain: evalDomain,
        action: evalAction,
        actor_type: evalActorType,
        context: parsedContext,
        amount: evalAmount ? parseFloat(evalAmount) : undefined,
      });
      setEvalResult(res);
    } catch (err: any) {
      alert(`Policy evaluation error: ${err.message || err}`);
    } finally {
      setIsEvaluating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Policy Simulator Section */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur shadow-xl">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <span>⚡</span>
          <span>Interactive Policy Simulator & Rule Evaluator</span>
        </h3>
        <p className="text-xs text-slate-400 mt-1">
          Simulate runtime actions against active enterprise governance policies and verify deterministic resolution.
        </p>

        <form onSubmit={handleRunEvaluation} className="mt-4 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Domain</label>
            <select
              value={evalDomain}
              onChange={(e) => setEvalDomain(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
            >
              {domains.filter((d) => d !== 'ALL').map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Target Action</label>
            <input
              type="text"
              value={evalAction}
              onChange={(e) => setEvalAction(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200 font-mono"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Actor Type</label>
            <select
              value={evalActorType}
              onChange={(e) => setEvalActorType(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
            >
              <option value="agent">AI Agent</option>
              <option value="user">Human User</option>
              <option value="system">System Daemon</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Monetary / Cost Amount</label>
            <input
              type="number"
              placeholder="e.g. 5000"
              value={evalAmount}
              onChange={(e) => setEvalAmount(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
            />
          </div>

          <div className="md:col-span-3">
            <label className="block text-xs font-semibold text-slate-300 mb-1">Context JSON</label>
            <input
              type="text"
              value={evalContext}
              onChange={(e) => setEvalContext(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200 font-mono"
            />
          </div>

          <div className="flex items-end">
            <button
              type="submit"
              disabled={isEvaluating}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2 px-4 rounded-lg text-xs transition"
            >
              {isEvaluating ? 'Evaluating...' : 'Test Policy Action'}
            </button>
          </div>
        </form>

        {evalResult && (
          <div
            className={`mt-4 p-4 rounded-xl border flex items-center justify-between ${
              evalResult.action_result === 'ALLOW'
                ? 'bg-emerald-950/40 border-emerald-800/60 text-emerald-300'
                : evalResult.action_result === 'REVIEW'
                ? 'bg-amber-950/40 border-amber-800/60 text-amber-300'
                : 'bg-rose-950/40 border-rose-800/60 text-rose-300'
            }`}
          >
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider">Verdict:</span>
                <span className="text-sm font-black uppercase font-mono px-2 py-0.5 rounded bg-black/40">
                  {evalResult.action_result}
                </span>
              </div>
              <p className="text-xs mt-1 text-slate-200">{evalResult.reason}</p>
            </div>
            <span className="text-2xl">
              {evalResult.action_result === 'ALLOW' ? '✅' : evalResult.action_result === 'REVIEW' ? '⚠️' : '🛑'}
            </span>
          </div>
        )}
      </div>

      {/* Policy Registry Header & Filter */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/50 p-4 rounded-xl border border-slate-800 backdrop-blur">
        <div>
          <h3 className="text-lg font-semibold text-white">Active Policy Definitions</h3>
          <p className="text-xs text-slate-400">
            Hard constraints, guardrails, and compliance rules governing cross-cutting platform actions
          </p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400">Domain:</label>
          <select
            value={selectedDomain}
            onChange={(e) => setSelectedDomain(e.target.value)}
            className="bg-slate-800 text-xs text-slate-200 border border-slate-700 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            {domains.map((dom) => (
              <option key={dom} value={dom}>
                {dom}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Policies List */}
      <div className="space-y-4">
        {filteredPolicies.map((pol) => (
          <div key={pol.policy_id} className="bg-slate-900/40 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-2">
              <div className="flex items-center gap-2.5">
                <span className="text-sm font-bold text-white">{pol.name}</span>
                <code className="text-xs font-mono text-cyan-400 bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-800/40">
                  {pol.policy_id}
                </code>
                <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-indigo-950/60 text-indigo-300 border border-indigo-800/50">
                  {pol.domain}
                </span>
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                  Priority: {pol.priority}
                </span>
              </div>
              <span className="text-xs text-slate-500">Version: v{pol.version}</span>
            </div>

            <p className="text-xs text-slate-400">{pol.description}</p>

            {/* Rules Table */}
            {pol.rules && pol.rules.length > 0 && (
              <div className="overflow-x-auto rounded-lg border border-slate-800/80 mt-2">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950/60 text-slate-400 text-[11px] uppercase border-b border-slate-800">
                    <tr>
                      <th className="p-2.5">Rule Name</th>
                      <th className="p-2.5">Condition Expression</th>
                      <th className="p-2.5">Enforced Action</th>
                      <th className="p-2.5">Reason / Constraint</th>
                      <th className="p-2.5">Security Level</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/40 text-slate-300 font-mono text-[11px]">
                    {pol.rules.map((rule) => (
                      <tr key={rule.rule_id} className="hover:bg-slate-800/20">
                        <td className="p-2.5 font-sans font-medium text-white">{rule.name}</td>
                        <td className="p-2.5 text-cyan-300">{rule.condition}</td>
                        <td className="p-2.5">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              rule.action === 'ALLOW'
                                ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                                : rule.action === 'REVIEW'
                                ? 'bg-amber-950 text-amber-300 border border-amber-800'
                                : 'bg-rose-950 text-rose-300 border border-rose-800'
                            }`}
                          >
                            {rule.action}
                          </span>
                        </td>
                        <td className="p-2.5 font-sans text-slate-400">{rule.reason}</td>
                        <td className="p-2.5">
                          {rule.is_mandatory_security ? (
                            <span className="text-[10px] text-rose-400 font-semibold uppercase">MANDATORY</span>
                          ) : (
                            <span className="text-[10px] text-slate-500 font-semibold uppercase">STANDARD</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
