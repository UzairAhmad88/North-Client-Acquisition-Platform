'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function EnterpriseDigitalTwinDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [copilotQuery, setCopilotQuery] = useState('What happens to revenue and capacity if Q4 sales increase by 20%?');
  const [copilotResult, setCopilotResult] = useState<any>(null);
  const [executingAgent, setExecutingAgent] = useState(false);
  const [agentResult, setAgentResult] = useState<any>(null);

  const stats = [
    { label: 'Canonical Twin Health', value: '98.6%', change: 'Real-time State Synchronized', status: 'optimal' },
    { label: 'Active Scenarios', value: '12 Scenarios', change: 'What-If & Monte Carlo Ready', status: 'optimal' },
    { label: 'P50 Forecasted MRR', value: '+$96.5k / mo', change: 'Confidence 0.96 (10k runs)', status: 'optimal' },
    { label: 'Pareto Optimal Actions', value: '3 Action Plans', change: 'Revenue ↔ Risk Balanced', status: 'optimal' },
    { label: 'Twin Graph Entities', value: '14,250 Entities', change: '100% Data Lineage Mapped', status: 'optimal' },
    { label: 'Process Bottlenecks', value: '1 Detected', change: 'DB Connection Pool Saturation', status: 'optimal' },
  ];

  const handleRunCopilot = () => {
    setTimeout(() => {
      setCopilotResult({
        answer: "Monte Carlo simulation (10,000 iterations) over Scenario 'Sales Surge 20%' indicates P50 Expected MRR Growth of +$96.5k/mo with $6,800/mo additional infrastructure cost. The bottleneck will be Database Connection Pool saturation unless scaled.",
        evidence: ["Snapshot: snap-current-live", "Scenario: scn-sales-surge-20", "Simulation: sim-run-1042 (Monte Carlo P50)"],
        confidence: 0.98
      });
    }, 400);
  };

  const handleExecuteAgent = () => {
    setExecutingAgent(true);
    setTimeout(() => {
      setAgentResult({
        status: "EXECUTED",
        autonomy_level: 3,
        agent: "digital_twin_orchestrator",
        task: "run_simulation",
        scope: "scn-sales-surge-20",
        result: "Monte Carlo simulation completed: P10 = +$68k, P50 = +$96.5k, P90 = +$124k MRR growth. 0.05 SLA breach risk.",
        checkpoint_token: "twin-chk-20260914223000"
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
              Enterprise Digital Twin & Autonomous Optimization
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
              SIMULATION & OPTIMIZATION LAYER OPERATIONAL
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Real-Time Enterprise State • Scenario Planning • Monte Carlo Simulations • Prescriptive Optimization
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleExecuteAgent}
            disabled={executingAgent}
            className="px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-medium text-sm rounded-lg shadow-lg shadow-emerald-950/50 transition-all flex items-center gap-2"
          >
            {executingAgent ? 'Running Simulation Agent...' : '⚡ Trigger Monte Carlo Simulation'}
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
            <span className="text-xs text-emerald-400">{s.change}</span>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'command-center', label: 'Twin Command Center' },
          { id: 'enterprise-state', label: 'Real-Time Enterprise State' },
          { id: 'entities', label: 'Entities & Graph' },
          { id: 'scenarios', label: 'What-If Scenarios' },
          { id: 'simulations', label: 'Monte Carlo Simulations' },
          { id: 'forecasts', label: 'Predictive Operations' },
          { id: 'optimization', label: 'Pareto Optimization' },
          { id: 'recommendations', label: 'Prescriptive Actions' },
          { id: 'strategic-planning', label: 'Strategic Planning' },
          { id: 'copilot', label: 'Digital Twin Copilot' },
          { id: 'settings', label: 'Settings & Controls' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950/40'
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
            <h2 className="text-lg font-semibold text-white">Active Scenarios & Simulation Results</h2>
            <div className="space-y-3">
              {[
                { name: 'What if Sales Growth Surges by 20% in Q4?', type: 'Monte Carlo (10,000 runs)', p50: '+$96,500 MRR', risk: 'Low (0.05 SLA risk)', status: 'COMPLETED' },
                { name: 'What if 2 Lead Backend Engineers Depart?', type: 'Discrete Event', p50: '+14 days delay', risk: 'Moderate (0.28)', status: 'COMPLETED' },
                { name: 'What if Cloud Compute Rates Increase 15%?', type: 'Cost Forecast', p50: '+$4,200/mo spend', risk: 'Low (0.02)', status: 'COMPLETED' },
              ].map((scn, i) => (
                <div key={i} className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg flex justify-between items-center text-sm">
                  <div>
                    <div className="font-semibold text-slate-200">{scn.name}</div>
                    <div className="text-xs text-slate-400">{scn.type} • Risk Profile: {scn.risk}</div>
                  </div>
                  <div className="text-right">
                    <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
                      {scn.status}
                    </span>
                    <div className="text-xs text-slate-400 mt-1">P50 Outcome: {scn.p50}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Prescriptive Action Recommendation</h2>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="text-sm font-semibold text-emerald-400">Auto-scale Read Replicas & Shift 2 Engineers to Onboarding Pipeline</div>
              <p className="text-xs text-slate-300">
                Increases Q4 MRR by +$85k with low 0.12 risk score while maintaining 99.98% SLA and eliminating DB pool saturation.
              </p>
              <div className="flex justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
                <span>Expected Benefit: +$85,000</span>
                <span>Cost: $5,400</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'copilot' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-semibold text-white">Digital Twin Copilot & Scenario Intelligence</h2>
          <div className="flex gap-3">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
            />
            <button
              onClick={handleRunCopilot}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm rounded-lg"
            >
              Ask Digital Twin Copilot
            </button>
          </div>

          {copilotResult && (
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="text-sm font-medium text-emerald-400">{copilotResult.answer}</div>
              <div className="flex gap-2 text-xs text-slate-400">
                <span>Evidence: {copilotResult.evidence.join(' | ')}</span>
                <span className="ml-auto font-semibold text-emerald-400">Confidence: {(copilotResult.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
          )}
        </div>
      )}

      {agentResult && (
        <div className="p-4 bg-emerald-950/40 border border-emerald-800 rounded-xl flex items-center justify-between text-sm">
          <div>
            <span className="font-bold text-emerald-400">[{agentResult.status}]</span> Level {agentResult.autonomy_level} Action executed by {agentResult.agent}: {agentResult.result}
          </div>
          <span className="text-xs text-slate-400 font-mono">{agentResult.checkpoint_token}</span>
        </div>
      )}
    </div>
  );
}
