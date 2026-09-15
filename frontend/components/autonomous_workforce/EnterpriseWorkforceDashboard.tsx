'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function EnterpriseWorkforceDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [copilotQuery, setCopilotQuery] = useState('What is the active AI Employee roster and consensus status?');
  const [copilotResult, setCopilotResult] = useState<any>(null);
  const [executingAgent, setExecutingAgent] = useState(false);
  const [agentResult, setAgentResult] = useState<any>(null);

  const stats = [
    { label: 'Active AI Employees', value: '3 AI Workers', change: '100% Supervisor Aligned', status: 'optimal' },
    { label: 'Virtual Departments', value: '3 Departments', change: 'Engineering, Security, Data', status: 'optimal' },
    { label: 'Task Success Rate', value: '99.5%', change: 'Zero Policy Violations', status: 'optimal' },
    { label: 'Multi-Agent Consensus Runs', value: '42 Runs', change: '99% Unanimous Agreement', status: 'optimal' },
    { label: 'Automated Peer Reviews', value: '128 Reviews', change: 'P95 Duration 3.4 mins', status: 'optimal' },
    { label: 'Monthly Worker Spend', value: '$1,090 / $6,300', change: '$5,210 Budget Available', status: 'optimal' },
  ];

  const handleRunCopilot = () => {
    setTimeout(() => {
      setCopilotResult({
        answer: "Currently, 3 AI Employees (Aria-Ops, Sentinel-Sec, DataGenius-AI) are active across Engineering, Security, and Data departments. Task success rate is 99.5% with 100% human supervisor alignment.",
        evidence: ["Roster: 3 Active AI Employees", "Consensus Run: cns-run-9081 (Passed)", "Budget Utilized: $1,090 / $6,300 monthly allocation"],
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
        agent: "consensus_agent",
        task: "run_consensus",
        scope: "Production Canary Rollout Promotion",
        result: "Multi-Agent Consensus vote completed: Aria-Ops (Approve), Sentinel-Sec (Approve), DataGenius-AI (Approve). 0.99 Confidence.",
        checkpoint_token: "wf-chk-20260914223000"
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
              Enterprise Autonomous Workforce & Human–AI Collaboration
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-950 text-indigo-400 border border-indigo-800">
              WORKFORCE LAYER OPERATIONAL
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            AI Employees • Virtual Departments • Multi-Agent Consensus • Peer Reviews • Human Supervisor Alignment
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleExecuteAgent}
            disabled={executingAgent}
            className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-medium text-sm rounded-lg shadow-lg shadow-indigo-950/50 transition-all flex items-center gap-2"
          >
            {executingAgent ? 'Running Multi-Agent Consensus...' : '⚡ Trigger Multi-Agent Consensus Vote'}
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
            <span className="text-xs text-indigo-400">{s.change}</span>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'command-center', label: 'Workforce Command Center' },
          { id: 'employees', label: 'AI Employees Roster' },
          { id: 'departments', label: 'Virtual Departments' },
          { id: 'teams', label: 'Teams & Org Chart' },
          { id: 'tasks', label: 'Delegated Tasks' },
          { id: 'consensus', label: 'Multi-Agent Consensus' },
          { id: 'reviews', label: 'Peer Reviews' },
          { id: 'budgets', label: 'Token & Spend Budgets' },
          { id: 'copilot', label: 'Workforce Copilot' },
          { id: 'settings', label: 'Supervisor Settings' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-950/40'
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
            <h2 className="text-lg font-semibold text-white">Active AI Employees & Assigned Tasks</h2>
            <div className="space-y-3">
              {[
                { name: 'Aria-Ops (SRE Lead AI)', role: 'Senior Autonomous SRE', supervisor: 'Alex Rivera (VP Infra)', task: 'Investigate DB Pool Latency', status: 'COMPLETED', success: '99.6%' },
                { name: 'Sentinel-Sec (Cyber Specialist)', role: 'Threat Hunter & Identity Auditor', supervisor: 'David Chen (CISO)', task: 'Audit IAM Privilege Escalation', status: 'COMPLETED', success: '99.8%' },
                { name: 'DataGenius-AI (Data Steward)', role: 'Lakehouse Quality Auditor', supervisor: 'Sarah Jenkins (CDO)', task: 'Verify Golden Record Integrity', status: 'IN_PROGRESS', success: '99.1%' },
              ].map((emp, i) => (
                <div key={i} className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg flex justify-between items-center text-sm">
                  <div>
                    <div className="font-semibold text-slate-200">{emp.name}</div>
                    <div className="text-xs text-slate-400">{emp.role} • Supervisor: {emp.supervisor}</div>
                  </div>
                  <div className="text-right">
                    <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
                      {emp.status}
                    </span>
                    <div className="text-xs text-slate-400 mt-1">Success: {emp.success}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Latest Multi-Agent Consensus</h2>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="text-sm font-semibold text-indigo-400">Production Canary Rollout Promotion</div>
              <p className="text-xs text-slate-300">
                Unanimous approval reached across SRE, Security, and Data AI agents with 0.99 confidence.
              </p>
              <div className="flex justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
                <span>Aria-Ops: APPROVE</span>
                <span>Sentinel-Sec: APPROVE</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'copilot' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-semibold text-white">Workforce Copilot & Org Assistant</h2>
          <div className="flex gap-3">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
            />
            <button
              onClick={handleRunCopilot}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm rounded-lg"
            >
              Ask Workforce Copilot
            </button>
          </div>

          {copilotResult && (
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="text-sm font-medium text-indigo-400">{copilotResult.answer}</div>
              <div className="flex gap-2 text-xs text-slate-400">
                <span>Evidence: {copilotResult.evidence.join(' | ')}</span>
                <span className="ml-auto font-semibold text-emerald-400">Confidence: {(copilotResult.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
          )}
        </div>
      )}

      {agentResult && (
        <div className="p-4 bg-indigo-950/40 border border-indigo-800 rounded-xl flex items-center justify-between text-sm">
          <div>
            <span className="font-bold text-indigo-400">[{agentResult.status}]</span> Level {agentResult.autonomy_level} Action executed by {agentResult.agent}: {agentResult.result}
          </div>
          <span className="text-xs text-slate-400 font-mono">{agentResult.checkpoint_token}</span>
        </div>
      )}
    </div>
  );
}
