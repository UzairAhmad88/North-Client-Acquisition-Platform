'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function EnterpriseDataPlatformDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [copilotQuery, setCopilotQuery] = useState('Where does net revenue come from and what is its freshness?');
  const [copilotResult, setCopilotResult] = useState<any>(null);
  const [executingAgent, setExecutingAgent] = useState(false);
  const [agentResult, setAgentResult] = useState<any>(null);

  const stats = [
    { label: 'Total Governed Data Assets', value: '1,420', change: '98.4% Catalog Coverage', status: 'optimal' },
    { label: 'Active Data Pipelines', value: '184 Pipelines', change: '99.2% SLA Compliance', status: 'optimal' },
    { label: 'Data Quality Score', value: '98.8%', change: 'Freshness SLA 99.1%', status: 'optimal' },
    { label: 'Master Data (Golden Records)', value: '42,500', change: '0.992 Match Confidence', status: 'optimal' },
    { label: 'ML Features in Feature Store', value: '1,280 Features', change: 'Online Low Latency', status: 'optimal' },
    { label: 'Data Platform Spend', value: '$18,450 / mo', change: '$650 optimization identified', status: 'optimal' },
  ];

  const handleRunCopilot = () => {
    setTimeout(() => {
      setCopilotResult({
        answer: "Net revenue is calculated in table gold_customer_revenue_daily (Gold Layer) sourced from Production OLTP PostgreSQL via ELT pipeline pip-orders-elt-01. Data freshness is 12 minutes (within 15-min SLA).",
        generated_sql: "SELECT SUM(amount_usd) FROM gold_customer_revenue_daily WHERE date = CURRENT_DATE;",
        evidence: ["Table: gold_customer_revenue_daily", "Pipeline: pip-orders-elt-01", "Glossary: Net Daily Revenue"],
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
        agent: "data_quality_agent",
        task: "run_quality_check",
        scope: "gold_customer_revenue_daily",
        result: "Quality check completed. 14,250 records evaluated: 0 nulls, 0 duplicate keys, 100% referential integrity.",
        checkpoint_token: "chk-20260914193000"
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
              Enterprise Data Platform & Autonomous Data Operations
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-cyan-950 text-cyan-400 border border-cyan-800">
              DATA LAKEHOUSE & MDM OPERATIONAL
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Governed Data Operating System • Lineage • Quality • Master Data Management • Autonomous Data Ops
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleExecuteAgent}
            disabled={executingAgent}
            className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-medium text-sm rounded-lg shadow-lg shadow-cyan-950/50 transition-all flex items-center gap-2"
          >
            {executingAgent ? 'Running Agent Task...' : '⚡ Trigger Autonomous Quality Agent'}
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
            <span className="text-xs text-cyan-400">{s.change}</span>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'command-center', label: 'Data Command Center' },
          { id: 'sources', label: 'Data Sources' },
          { id: 'pipelines', label: 'Pipelines & ELT' },
          { id: 'lakehouse', label: 'Medallion Lakehouse' },
          { id: 'catalog', label: 'Data Catalog' },
          { id: 'lineage', label: 'Data Lineage' },
          { id: 'governance', label: 'Governance & Privacy' },
          { id: 'quality', label: 'Data Quality' },
          { id: 'mdm', label: 'Master Data (MDM)' },
          { id: 'copilot', label: 'Data Copilot' },
          { id: 'agents', label: 'Autonomous Data Agents' },
          { id: 'costs', label: 'Data FinOps' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-950/40'
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
            <h2 className="text-lg font-semibold text-white">Active Data Pipelines & Medallion Layers</h2>
            <div className="space-y-3">
              {[
                { name: 'Orders Medallion ELT Pipeline', type: 'ELT', layer: 'Gold Layer', status: 'SUCCESS', records: '142,500 recs', duration: '12.4s' },
                { name: 'User Identity CDC Sync', type: 'CDC', layer: 'Silver Layer', status: 'RUNNING', records: '48,200 recs', duration: 'Streaming' },
                { name: 'Stripe SaaS Ingestion', type: 'API Ingestion', layer: 'Bronze Layer', status: 'SUCCESS', records: '12,900 recs', duration: '4.2s' },
              ].map((pip, i) => (
                <div key={i} className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg flex justify-between items-center text-sm">
                  <div>
                    <div className="font-semibold text-slate-200">{pip.name}</div>
                    <div className="text-xs text-slate-400">{pip.type} • Target: {pip.layer}</div>
                  </div>
                  <div className="text-right">
                    <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
                      {pip.status}
                    </span>
                    <div className="text-xs text-slate-400 mt-1">{pip.records} ({pip.duration})</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Data Quality & Freshness SLA</h2>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Completeness</span>
                <span className="font-bold text-emerald-400">99.4%</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-500 h-full w-[99.4%]"></div>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Timeliness / Freshness</span>
                <span className="font-bold text-cyan-400">99.1%</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-cyan-500 h-full w-[99.1%]"></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'copilot' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-semibold text-white">Data Copilot & Governed SQL Engine</h2>
          <div className="flex gap-3">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-cyan-500"
            />
            <button
              onClick={handleRunCopilot}
              className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-sm rounded-lg"
            >
              Ask Data Copilot
            </button>
          </div>

          {copilotResult && (
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
              <div className="text-sm font-medium text-cyan-400">{copilotResult.answer}</div>
              <div className="p-3 bg-slate-900 rounded font-mono text-xs text-slate-300">
                {copilotResult.generated_sql}
              </div>
              <div className="flex gap-2 text-xs text-slate-400">
                <span>Evidence: {copilotResult.evidence.join(' | ')}</span>
                <span className="ml-auto font-semibold text-emerald-400">Confidence: {(copilotResult.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
          )}
        </div>
      )}

      {agentResult && (
        <div className="p-4 bg-cyan-950/40 border border-cyan-800 rounded-xl flex items-center justify-between text-sm">
          <div>
            <span className="font-bold text-cyan-400">[{agentResult.status}]</span> Level {agentResult.autonomy_level} Action executed by {agentResult.agent}: {agentResult.result}
          </div>
          <span className="text-xs text-slate-400 font-mono">{agentResult.checkpoint_token}</span>
        </div>
      )}
    </div>
  );
}
