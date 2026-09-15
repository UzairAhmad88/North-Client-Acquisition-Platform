'use client';

import React, { useState } from 'react';
import {
  Database,
  GitBranch,
  CheckCircle2,
  AlertTriangle,
  Layers,
  Network,
  Search,
  Brain,
  Shield,
  DollarSign,
  Activity,
  Terminal,
  Clock,
  Sparkles,
  ArrowUpRight,
  Filter,
  RefreshCw,
  FileText
} from 'lucide-react';

export default function DataCommandCenterDashboard() {
  const [activeTab, setActiveTab] = useState<'overview' | 'lineage' | 'graph' | 'nl_studio' | 'governance'>('overview');
  const [selectedDomain, setSelectedDomain] = useState<string>('ALL');

  const stats = [
    { label: 'Data Sources', value: '48 Active', icon: Database, trend: '+4 this month', color: 'emerald' },
    { label: 'Pipeline Health', value: '99.8%', icon: GitBranch, trend: '420 jobs / hr', color: 'blue' },
    { label: 'Quality Score', value: '99.4/100', icon: CheckCircle2, trend: '6 dimensions verified', color: 'indigo' },
    { label: 'Freshness Lag', value: '1.2s', icon: Clock, trend: 'Zero SLA breach', color: 'emerald' },
    { label: 'Knowledge Graph', value: '14,820 Nodes', icon: Network, trend: '48,190 Edges', color: 'purple' },
    { label: 'Monthly FinOps', value: '$1,420.50', icon: DollarSign, trend: '-18% optimized', color: 'amber' },
  ];

  const recentIncidents = [
    { id: 'inc_841', dataset: 'gold.customer_transactions', severity: 'MEDIUM', status: 'RESOLVED', lag: '2.4s', time: '12m ago' },
    { id: 'inc_840', dataset: 'silver.clickstream_events', severity: 'LOW', status: 'AUTO_HEALED', lag: '1.1s', time: '1h ago' },
  ];

  const certifiedDataProducts = [
    { name: 'Customer 360', tier: 'GOLD', sla: '99.99%', consumers: 18, owner: 'Customer Intelligence Team', status: 'CERTIFIED' },
    { name: 'Sales & Revenue Mart', tier: 'GOLD', sla: '99.95%', consumers: 24, owner: 'Finance Analytics', status: 'CERTIFIED' },
    { name: 'AI Model Feature Store', tier: 'GOLD', sla: '99.90%', consumers: 12, owner: 'ML Platform', status: 'CERTIFIED' },
    { name: 'Engineering Telemetry', tier: 'SILVER', sla: '99.50%', consumers: 9, owner: 'DevOps & SRE', status: 'ACTIVE' },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Top Banner Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/20">
              <Database className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-indigo-300 bg-clip-text text-transparent">
                Autonomous Data & Knowledge Operating System
              </h1>
              <p className="text-sm text-slate-400">
                Central Governed Information Layer connecting Sources, Pipelines, Graphs, Analytics & AI Agents
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-3 py-2 text-xs font-medium rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 transition">
            <RefreshCw className="w-3.5 h-3.5 text-indigo-400" />
            Live Sync: Healthy
          </button>
          <button className="flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white shadow-md shadow-indigo-600/30 transition">
            <Terminal className="w-3.5 h-3.5" />
            Run Autonomous Loop
          </button>
        </div>
      </div>

      {/* Hero Telemetry Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {stats.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <div key={idx} className="bg-slate-900/80 border border-slate-800/80 rounded-xl p-4 flex flex-col justify-between hover:border-slate-700 transition">
              <div className="flex items-center justify-between text-slate-400 mb-2">
                <span className="text-xs font-medium uppercase tracking-wider">{stat.label}</span>
                <Icon className="w-4 h-4 text-indigo-400" />
              </div>
              <div>
                <div className="text-xl font-bold text-white tracking-tight">{stat.value}</div>
                <div className="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                  <span className="text-emerald-400 font-medium">{stat.trend}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Sector Navigation Tabs */}
      <div className="flex overflow-x-auto gap-2 border-b border-slate-800 pb-2 scrollbar-none">
        {[
          { key: 'overview', label: 'Command Center', icon: Activity },
          { key: 'lineage', label: 'End-to-End Lineage', icon: GitBranch },
          { key: 'graph', label: 'Knowledge Graph', icon: Network },
          { key: 'nl_studio', label: 'Natural Language Studio', icon: Sparkles },
          { key: 'governance', label: 'Governance & Privacy', icon: Shield },
        ].map((tab) => {
          const TabIcon = tab.icon;
          const isSelected = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`flex items-center gap-2 px-4 py-2 text-xs font-medium rounded-lg transition whitespace-nowrap ${
                isSelected
                  ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
              }`}
            >
              <TabIcon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Main Workspace Panels */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Certified Data Products */}
          <div className="lg:col-span-2 bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-semibold text-white">Governed Data Products</h2>
                <p className="text-xs text-slate-400">Discoverable, contract-enforced analytical products</p>
              </div>
              <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                100% Contract Valid
              </span>
            </div>

            <div className="divide-y divide-slate-800/80">
              {certifiedDataProducts.map((p, i) => (
                <div key={i} className="py-3 flex items-center justify-between hover:bg-slate-800/30 px-2 rounded-lg transition">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
                      <Layers className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-white flex items-center gap-2">
                        {p.name}
                        <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono">
                          {p.tier}
                        </span>
                      </div>
                      <div className="text-xs text-slate-400">{p.owner} • {p.consumers} active consumers</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs font-mono text-emerald-400 font-semibold">{p.sla} SLO</div>
                    <div className="text-[11px] text-slate-500">Tier-1 Guaranteed</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Incidents & Observability */}
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-white">Data Observability & Incidents</h2>
              <span className="text-xs text-slate-400">Zero Critical</span>
            </div>

            <div className="space-y-3">
              {recentIncidents.map((inc) => (
                <div key={inc.id} className="p-3 rounded-lg bg-slate-800/40 border border-slate-800 flex items-start justify-between">
                  <div>
                    <div className="text-xs font-semibold text-slate-200">{inc.dataset}</div>
                    <div className="text-[11px] text-slate-400 mt-0.5">Lag: {inc.lag} • {inc.time}</div>
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {inc.status}
                  </span>
                </div>
              ))}
            </div>

            <div className="pt-2 border-t border-slate-800">
              <div className="text-xs font-medium text-slate-300 mb-2">Automated Quality Checks</div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="p-2 rounded bg-slate-800/30 border border-slate-800">
                  <div className="text-slate-400">Completeness</div>
                  <div className="text-emerald-400 font-bold">99.8%</div>
                </div>
                <div className="p-2 rounded bg-slate-800/30 border border-slate-800">
                  <div className="text-slate-400">Freshness</div>
                  <div className="text-emerald-400 font-bold">100.0%</div>
                </div>
                <div className="p-2 rounded bg-slate-800/30 border border-slate-800">
                  <div className="text-slate-400">Validity</div>
                  <div className="text-emerald-400 font-bold">99.5%</div>
                </div>
                <div className="p-2 rounded bg-slate-800/30 border border-slate-800">
                  <div className="text-slate-400">Consistency</div>
                  <div className="text-emerald-400 font-bold">99.2%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Lineage Tab */}
      {activeTab === 'lineage' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h2 className="text-sm font-semibold text-white">Full Lifecycle Data Lineage Graph</h2>
              <p className="text-xs text-slate-400">Traces raw source records through transformations to metrics, dashboards, and AI decisions</p>
            </div>
            <div className="text-xs font-mono text-indigo-400">Depth: 7 Tiers</div>
          </div>

          <div className="p-6 bg-slate-950/70 border border-slate-800/90 rounded-lg flex flex-col md:flex-row items-center justify-between gap-4 overflow-x-auto">
            <div className="flex flex-col items-center p-3 rounded-lg bg-slate-900 border border-slate-700 text-center min-w-[140px]">
              <span className="text-[10px] uppercase tracking-wider text-slate-400 font-bold">Raw Source</span>
              <span className="text-xs font-semibold text-white mt-1">Postgres DB</span>
              <span className="text-[10px] text-emerald-400">transactions_cdc</span>
            </div>
            <div className="text-slate-500 font-bold">→</div>
            <div className="flex flex-col items-center p-3 rounded-lg bg-slate-900 border border-slate-700 text-center min-w-[140px]">
              <span className="text-[10px] uppercase tracking-wider text-amber-400 font-bold">Bronze Layer</span>
              <span className="text-xs font-semibold text-white mt-1">S3 Lakehouse</span>
              <span className="text-[10px] text-slate-400">raw_events.parquet</span>
            </div>
            <div className="text-slate-500 font-bold">→</div>
            <div className="flex flex-col items-center p-3 rounded-lg bg-slate-900 border border-slate-700 text-center min-w-[140px]">
              <span className="text-[10px] uppercase tracking-wider text-slate-300 font-bold">Silver Layer</span>
              <span className="text-xs font-semibold text-white mt-1">Cleansed DWH</span>
              <span className="text-[10px] text-slate-400">dim_customers</span>
            </div>
            <div className="text-slate-500 font-bold">→</div>
            <div className="flex flex-col items-center p-3 rounded-lg bg-slate-900 border border-indigo-500/40 text-center min-w-[140px] shadow-lg shadow-indigo-500/10">
              <span className="text-[10px] uppercase tracking-wider text-indigo-400 font-bold">Gold Mart</span>
              <span className="text-xs font-semibold text-white mt-1">Customer 360</span>
              <span className="text-[10px] text-indigo-300">fact_customer_revenue</span>
            </div>
            <div className="text-slate-500 font-bold">→</div>
            <div className="flex flex-col items-center p-3 rounded-lg bg-purple-950/40 border border-purple-500/40 text-center min-w-[140px]">
              <span className="text-[10px] uppercase tracking-wider text-purple-400 font-bold">AI Model & Action</span>
              <span className="text-xs font-semibold text-white mt-1">Churn Predictor</span>
              <span className="text-[10px] text-purple-300">Auto Retention Offer</span>
            </div>
          </div>
        </div>
      )}

      {/* Knowledge Graph Tab */}
      {activeTab === 'graph' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h2 className="text-sm font-semibold text-white">Enterprise Knowledge Graph (Ontology Engine)</h2>
              <p className="text-xs text-slate-400">Interactive graph connecting Customers, Projects, Requirements, Code, Services, Data & Decisions</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 font-mono">
                14,820 Nodes • 48,190 Edges
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 rounded-lg bg-slate-950/60 border border-slate-800 space-y-2">
              <div className="text-xs font-bold text-slate-300 uppercase tracking-wider">Top Entity Types</div>
              <ul className="text-xs space-y-1.5 text-slate-400">
                <li className="flex justify-between"><span>Customer</span><span className="font-mono text-slate-200">1,420</span></li>
                <li className="flex justify-between"><span>Service / Microservice</span><span className="font-mono text-slate-200">84</span></li>
                <li className="flex justify-between"><span>Dataset / Table</span><span className="font-mono text-slate-200">312</span></li>
                <li className="flex justify-between"><span>Certified Metric</span><span className="font-mono text-slate-200">65</span></li>
                <li className="flex justify-between"><span>AI Agent / Model</span><span className="font-mono text-slate-200">42</span></li>
              </ul>
            </div>

            <div className="p-4 rounded-lg bg-slate-950/60 border border-slate-800 space-y-2 md:col-span-2">
              <div className="text-xs font-bold text-slate-300 uppercase tracking-wider">Traversable Semantic Relationships</div>
              <div className="flex flex-wrap gap-1.5 pt-1">
                {['OWNS', 'USES', 'DEPENDS_ON', 'IMPLEMENTS', 'PRODUCES', 'CONSUMES', 'RELATED_TO', 'BELONGS_TO', 'AFFECTS', 'DERIVED_FROM'].map((rel) => (
                  <span key={rel} className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-indigo-300 border border-slate-700">
                    {rel}
                  </span>
                ))}
              </div>
              <p className="text-xs text-slate-400 pt-2">
                Allows complex queries like: <span className="text-slate-200 italic">&ldquo;Which customers are affected by this database incident?&rdquo;</span> or <span className="text-slate-200 italic">&ldquo;Which models depend on this dataset?&rdquo;</span>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Natural Language Studio Tab */}
      {activeTab === 'nl_studio' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="border-b border-slate-800 pb-3">
            <h2 className="text-sm font-semibold text-white">Natural Language Data & AI Query Studio</h2>
            <p className="text-xs text-slate-400">Ask business questions in plain English; queries are mapped to certified metrics with strict read-only safety</p>
          </div>

          <div className="flex gap-3">
            <input
              type="text"
              readOnly
              value="Show revenue by customer for Q3 2026"
              className="flex-1 px-4 py-2 text-xs rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none"
            />
            <button className="px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition">
              Run Safe Query
            </button>
          </div>

          <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-3 font-mono text-xs">
            <div className="flex items-center justify-between text-slate-400 border-b border-slate-800 pb-2">
              <span className="text-emerald-400 font-bold">✓ Safety Validated (Read-Only)</span>
              <span className="text-slate-400">Resolved Metric: Annual Recurring Revenue</span>
            </div>
            <div className="text-indigo-300">
              SELECT c.name, SUM(t.amount) AS revenue FROM customers c JOIN transactions t ON c.id = t.customer_id GROUP BY c.name ORDER BY revenue DESC LIMIT 3;
            </div>
            <div className="pt-2 text-slate-300">
              <div className="grid grid-cols-2 border-b border-slate-800 pb-1 text-slate-500">
                <span>Customer</span>
                <span className="text-right">Revenue</span>
              </div>
              <div className="grid grid-cols-2 py-1"><span>Acme Corp</span><span className="text-right text-emerald-400 font-semibold">$142,500.00</span></div>
              <div className="grid grid-cols-2 py-1"><span>GlobalTech</span><span className="text-right text-emerald-400 font-semibold">$98,200.50</span></div>
              <div className="grid grid-cols-2 py-1"><span>NorthStar Inc</span><span className="text-right text-emerald-400 font-semibold">$76,400.00</span></div>
            </div>
          </div>
        </div>
      )}

      {/* Governance & Privacy Tab */}
      {activeTab === 'governance' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="border-b border-slate-800 pb-3">
            <h2 className="text-sm font-semibold text-white">Enterprise Data Governance, Privacy & Security Layer</h2>
            <p className="text-xs text-slate-400">Classifications, PII scanning, masking policies, and access controls</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-lg bg-slate-950/60 border border-slate-800 space-y-2">
              <div className="text-xs font-bold text-slate-300 uppercase tracking-wider">Classification Tiers</div>
              <div className="space-y-1.5 text-xs">
                <div className="flex justify-between p-2 rounded bg-slate-900 border border-slate-800">
                  <span className="font-semibold text-slate-200">PUBLIC</span>
                  <span className="text-slate-400">Marketing & Public Documentation</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-900 border border-slate-800">
                  <span className="font-semibold text-indigo-300">INTERNAL</span>
                  <span className="text-slate-400">Standard Operational Datasets</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-900 border border-slate-800">
                  <span className="font-semibold text-amber-300">CONFIDENTIAL</span>
                  <span className="text-slate-400">Financial Reports & CRM Data</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-900 border border-slate-800">
                  <span className="font-semibold text-rose-400">RESTRICTED</span>
                  <span className="text-slate-400">PII, Credentials, Secrets</span>
                </div>
              </div>
            </div>

            <div className="p-4 rounded-lg bg-slate-950/60 border border-slate-800 space-y-2">
              <div className="text-xs font-bold text-slate-300 uppercase tracking-wider">Active Masking Strategies</div>
              <ul className="text-xs space-y-2 text-slate-400">
                <li className="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between items-center">
                  <span>Customer Email</span>
                  <span className="font-mono text-indigo-400 text-[11px]">a***@example.com (PARTIAL)</span>
                </li>
                <li className="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between items-center">
                  <span>SSN / Tax Identifier</span>
                  <span className="font-mono text-rose-400 text-[11px]">[REDACTED]</span>
                </li>
                <li className="p-2 rounded bg-slate-900 border border-slate-800 flex justify-between items-center">
                  <span>Credit Card PAN</span>
                  <span className="font-mono text-amber-400 text-[11px]">4111********1111 (TOKENIZED)</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
