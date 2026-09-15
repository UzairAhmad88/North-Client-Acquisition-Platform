'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function EnterpriseAIPlatformDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [copilotQuery, setCopilotQuery] = useState('Which model has the best accuracy for ITOps root-cause analysis?');
  const [copilotResult, setCopilotResult] = useState<any>(null);
  const [executingAgent, setExecutingAgent] = useState(false);
  const [agentResult, setAgentResult] = useState<any>(null);

  const stats = [
    { label: 'Registered Production Models', value: '48 Models', change: '100% Evaluation Gate Passed', status: 'optimal' },
    { label: 'Active ML Projects', value: '14 Projects', change: '84 Active Experiments', status: 'optimal' },
    { label: 'LLM Gateway Throughput', value: '4.2M Tokens/day', change: 'P95 Latency 38.5ms', status: 'optimal' },
    { label: 'Model Accuracy Average', value: '96.4%', change: 'Zero Safety Gate Violations', status: 'optimal' },
    { label: 'Autonomous AI Agents', value: '17 Agents', change: '99.1% Success Rate', status: 'optimal' },
    { label: 'Monthly AI Spend', value: '$32,450 / mo', change: '$1,200 token loop optimization', status: 'optimal' },
  ];

  const handleRunCopilot = () => {
    setTimeout(() => {
      setCopilotResult({
        answer: "Uzaii-Ops-Copilot-Llama3-70B (v2.4.0) has the highest accuracy (96.4%) and lowest drift (0.02). Current P95 latency is 38.5ms with 100% safety gate compliance.",
        evidence: ["Model Registry: mdl-ops-copilot-70b", "Evaluation Run: eval-run-9081", "Endpoint: ep-ops-copilot-v2"],
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
        agent: "evaluation_agent",
        task: "run_eval_suite",
        scope: "mdl-ops-copilot-70b",
        result: "Golden Safety & Accuracy evaluation suite completed: 1,000 test cases passed. Accuracy = 96.4%, Safety = 99.8%.",
        checkpoint_token: "ai-chk-20260914193000"
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
              Enterprise AI/ML Platform & Autonomous AI Operations
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-violet-950 text-violet-400 border border-violet-800">
              MLOPS & LLM GATEWAY OPERATIONAL
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Model Registry • LLM Gateway • RAG Platform • Safety & Evaluation Gates • Autonomous AI Ops
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleExecuteAgent}
            disabled={executingAgent}
            className="px-4 py-2 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-medium text-sm rounded-lg shadow-lg shadow-violet-950/50 transition-all flex items-center gap-2"
          >
            {executingAgent ? 'Running Evaluation Agent...' : '⚡ Trigger Model Evaluation Agent'}
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
            <span className="text-xs text-violet-400">{s.change}</span>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'command-center', label: 'AI Command Center' },
          { id: 'projects', label: 'ML Projects' },
          { id: 'experiments', label: 'Experiments & Runs' },
          { id: 'registry', label: 'Model Registry' },
          { id: 'evaluations', label: 'Evaluation & Gates' },
          { id: 'deployments', label: 'Deployments & Canary' },
          { id: 'llm-gateway', label: 'LLM Gateway' },
          { id: 'prompts', label: 'Prompt Studio' },
          { id: 'rag', label: 'RAG & Vector Search' },
          { id: 'agents', label: 'AI Agents & Trajectories' },
          { id: 'drift', label: 'Drift & Retraining' },
          { id: 'copilot', label: 'AI Copilot' },
          { id: 'costs', label: 'AI FinOps' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-violet-600 text-white shadow-md shadow-violet-950/40'
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
            <h2 className="text-lg font-semibold text-white">Registered Enterprise Models & Deployments</h2>
            <div className="space-y-3">
              {[
                { name: 'Uzaii-Ops-Copilot-Llama3-70B', type: 'LLM (GenAI)', stage: 'PRODUCTION', strategy: 'CANARY (90/10)', accuracy: '96.4%', latency: '38.5ms' },
                { name: 'Uzaii-Fraud-Detector-XGBoost', type: 'Classifier (ML)', stage: 'PRODUCTION', strategy: 'BLUE_GREEN', accuracy: '99.1%', latency: '8.2ms' },
                { name: 'Uzaii-Embedding-V3-Large', type: 'Vector Embedding', stage: 'PRODUCTION', strategy: 'ROLLING', accuracy: '98.4%', latency: '12.0ms' },
              ].map((mdl, i) => (
                <div key={i} className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg flex justify-between items-center text-sm">
                  <div>
                    <div className="font-semibold text-slate-200">{mdl.name}</div>
                    <div className="text-xs text-slate-400">{mdl.type} • Strategy: {mdl.strategy}</div>
                  </div>
                  <div className="text-right">
                    <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
                      {mdl.stage}
                    </span>
                    <div className="text-xs text-slate-400 mt-1">Accuracy: {mdl.accuracy} ({mdl.latency})</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Model Safety & Gate Compliance</h2>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Prompt Injection Defense</span>
                <span className="font-bold text-emerald-400">99.8%</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-500 h-full w-[99.8%]"></div>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Jailbreak Resistance</span>
                <span className="font-bold text-violet-400">100.0%</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-violet-500 h-full w-[100%]"></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'copilot' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-semibold text-white">AI Copilot & Model Analytics Assistant</h2>
          <div className="flex gap-3">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-violet-500"
            />
            <button
              onClick={handleRunCopilot}
              className="px-4 py-2 bg-violet-600 hover:bg-violet-500 text-white font-medium text-sm rounded-lg"
            >
              Ask AI Copilot
            </button>
          </div>

          {copilotResult && (
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="text-sm font-medium text-violet-400">{copilotResult.answer}</div>
              <div className="flex gap-2 text-xs text-slate-400">
                <span>Evidence: {copilotResult.evidence.join(' | ')}</span>
                <span className="ml-auto font-semibold text-emerald-400">Confidence: {(copilotResult.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
          )}
        </div>
      )}

      {agentResult && (
        <div className="p-4 bg-violet-950/40 border border-violet-800 rounded-xl flex items-center justify-between text-sm">
          <div>
            <span className="font-bold text-violet-400">[{agentResult.status}]</span> Level {agentResult.autonomy_level} Action executed by {agentResult.agent}: {agentResult.result}
          </div>
          <span className="text-xs text-slate-400 font-mono">{agentResult.checkpoint_token}</span>
        </div>
      )}
    </div>
  );
}
