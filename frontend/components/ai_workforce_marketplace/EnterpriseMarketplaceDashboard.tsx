'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function EnterpriseMarketplaceDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [copilotQuery, setCopilotQuery] = useState('Which capability should handle 24/7 incident triage under $5/task?');
  const [copilotResult, setCopilotResult] = useState<any>(null);
  const [executingAgent, setExecutingAgent] = useState(false);
  const [agentResult, setAgentResult] = useState<any>(null);

  const stats = [
    { label: 'Verified Marketplace Capabilities', value: '42 Capabilities', change: '100% Certified & Audited', status: 'optimal' },
    { label: 'Reusable Agent Skills', value: '128 Skills', change: 'Composable Architecture', status: 'optimal' },
    { label: 'Published AI Services', value: '18 Services', change: '99.98% SLA Compliance', status: 'optimal' },
    { label: 'Certified Trust Score', value: '99.4 Avg', change: 'Zero Unverified Listings', status: 'optimal' },
    { label: 'Completed Capability Orders', value: '1,420 Tasks', change: '$2.50 Avg Task Cost', status: 'optimal' },
    { label: 'Service ROI & Savings', value: '$84,500 / mo', change: '3.4x Value Multiplier', status: 'optimal' },
  ];

  const handleRunCopilot = () => {
    setTimeout(() => {
      setCopilotResult({
        answer: "For autonomous incident triage under $5/task, Aria-Ops is certified with 99.6% trust score and $2.50/task cost. Alternative: Sentinel-Sec for security audits.",
        recommended_capability: "Aria-Ops — Autonomous SRE",
        evidence: ["Listing: cap-aria-ops", "Certification: ENTERPRISE_GOLD", "SLA Compliance: 99.98%"],
        confidence: 0.99
      });
    }, 400);
  };

  const handleExecuteAgent = () => {
    setExecutingAgent(true);
    setTimeout(() => {
      setAgentResult({
        status: "EXECUTED",
        autonomy_level: 3,
        agent: "marketplace_orchestrator",
        task: "verify_certification",
        scope: "Aria-Ops — Autonomous SRE",
        result: "ENTERPRISE_GOLD Certification re-verified: Security Score = 99.8, Safety Score = 100.0.",
        checkpoint_token: "mkt-chk-20260914223000"
      });
      setExecutingAgent(false);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Enterprise AI Workforce Marketplace & Capability Exchange
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-950 text-amber-400 border border-amber-800">
              SERVICE ECONOMY OPERATIONAL
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Discoverable AI Capabilities • Composable Skills • Certified Trust Scores • Governed Service Contracts
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleExecuteAgent}
            disabled={executingAgent}
            className="px-4 py-2 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white font-medium text-sm rounded-lg shadow-lg shadow-amber-950/50 transition-all flex items-center gap-2"
          >
            {executingAgent ? 'Verifying Certification...' : '⚡ Verify Enterprise Capability Certification'}
          </button>
        </div>
      </div>

      {/* Stat Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
        {stats.map((s, idx) => (
          <div key={idx} className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between backdrop-blur-sm">
            <span className="text-xs font-medium text-slate-400">{s.label}</span>
            <div className="my-2">
              <span className="text-xl font-bold text-white">{s.value}</span>
            </div>
            <span className="text-xs text-amber-400">{s.change}</span>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'command-center', label: 'Marketplace Command Center' },
          { id: 'capabilities', label: 'Capability Directory' },
          { id: 'skills', label: 'Agent Skills' },
          { id: 'services', label: 'AI Service Catalog' },
          { id: 'teams', label: 'Agent Team Builder' },
          { id: 'certifications', label: 'Certifications & Trust' },
          { id: 'orders', label: 'Orders & Executions' },
          { id: 'budgets', label: 'Cost Centers & ROI' },
          { id: 'copilot', label: 'Marketplace Copilot' },
          { id: 'settings', label: 'Governance Settings' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-amber-600 text-white shadow-md shadow-amber-950/40'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-850'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      {activeTab === 'command-center' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Featured Enterprise Capabilities & Services</h2>
            <div className="space-y-3">
              {[
                { name: 'Aria-Ops — Autonomous SRE', category: 'AI Employees', pricing: '$2.50 / task', trust: '99.6 Trust Score', cert: 'ENTERPRISE_GOLD', status: 'CERTIFIED' },
                { name: 'Sentinel-Sec — Identity Hunter', category: 'AI Employees', pricing: '$4.00 / task', trust: '99.8 Trust Score', cert: 'ENTERPRISE_GOLD', status: 'CERTIFIED' },
                { name: 'Financial Modeling & Stress Test', category: 'Agent Skills', pricing: 'Included', trust: '99.2 Trust Score', cert: 'VERIFIED', status: 'CERTIFIED' },
              ].map((cap, i) => (
                <div key={i} className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg flex justify-between items-center text-sm">
                  <div>
                    <div className="font-semibold text-slate-200">{cap.name}</div>
                    <div className="text-xs text-slate-400">{cap.category} • Price: {cap.pricing}</div>
                  </div>
                  <div className="text-right">
                    <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
                      {cap.cert}
                    </span>
                    <div className="text-xs text-slate-400 mt-1">{cap.trust}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Capability Service Agreement SLA</h2>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="text-sm font-semibold text-amber-400">Autonomous Incident Triage SLA</div>
              <p className="text-xs text-slate-300">
                Guaranteed 5.0 minute SLA target with 99.98% delivery success and independent output verification.
              </p>
              <div className="flex justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
                <span>Avg Duration: 2.4 mins</span>
                <span>Quality Gate: PASSED</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'copilot' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-semibold text-white">AI Marketplace Copilot & Discovery Engine</h2>
          <div className="flex gap-3">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-amber-500"
            />
            <button
              onClick={handleRunCopilot}
              className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white font-medium text-sm rounded-lg"
            >
              Ask Marketplace Copilot
            </button>
          </div>

          {copilotResult && (
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="text-sm font-medium text-amber-400">{copilotResult.answer}</div>
              <div className="flex gap-2 text-xs text-slate-400">
                <span>Evidence: {copilotResult.evidence.join(' | ')}</span>
                <span className="ml-auto font-semibold text-emerald-400">Confidence: {(copilotResult.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
          )}
        </div>
      )}

      {agentResult && (
        <div className="p-4 bg-amber-950/40 border border-amber-800 rounded-xl flex items-center justify-between text-sm">
          <div>
            <span className="font-bold text-amber-400">[{agentResult.status}]</span> Level {agentResult.autonomy_level} Action executed: {agentResult.result}
          </div>
          <span className="text-xs text-slate-400 font-mono">{agentResult.checkpoint_token}</span>
        </div>
      )}
    </div>
  );
}
