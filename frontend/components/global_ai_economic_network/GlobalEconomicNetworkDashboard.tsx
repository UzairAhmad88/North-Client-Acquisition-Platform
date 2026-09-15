'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function GlobalEconomicNetworkDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [copilotQuery, setCopilotQuery] = useState('Where are we overspending across external AI services and how can we optimize compute costs?');
  const [copilotResult, setCopilotResult] = useState<any>(null);
  const [emergencyPause, setEmergencyPause] = useState<boolean>(false);
  const [simulatingShock, setSimulatingShock] = useState<boolean>(false);
  const [shockResult, setShockResult] = useState<any>(null);

  const stats = [
    { label: 'Autonomous M2M Transactions', value: '1,420 Orders', change: '92.4% Autonomy Rate', status: 'optimal' },
    { label: 'Total Settled Network Volume', value: '$3.48M Settled', change: 'Zero Settlement Lag', status: 'optimal' },
    { label: 'Network Resilience Score', value: '98.4 / 100', change: 'Multi-Cloud Failover', status: 'optimal' },
    { label: 'AP / AR Reconciliation', value: '100% Balanced', change: 'Zero Unmatched Invoices', status: 'optimal' },
    { label: 'Net Machine ROI', value: '$142,500 / mo', change: '3.4x Value Multiplier', status: 'optimal' },
    { label: 'Emergency Economic Pause', value: emergencyPause ? 'PAUSED' : 'ACTIVE', change: emergencyPause ? 'Killswitch Triggered' : 'Zero-Trust Operations', status: emergencyPause ? 'danger' : 'optimal' },
  ];

  const entities = [
    { id: 'node-uzaii-hq', name: 'Uzaii Global Enterprise HQ', type: 'ORGANIZATION', domain: 'uzaii.com', trust: 99.9, resilience: 99.2, contracts: 48, status: 'ACTIVE_BUYER_SELLER' },
    { id: 'node-apex-cyber', name: 'Apex Cyber Defense Inc.', type: 'SUPPLIER_PROVIDER', domain: 'apexcyber.com', trust: 99.8, resilience: 98.5, contracts: 14, status: 'PREFERRED_VENDOR' },
    { id: 'node-quantum-logistics', name: 'Quantum Global Logistics GmbH', type: 'SUPPLIER_PROVIDER', domain: 'quantumlogistics.eu', trust: 98.9, resilience: 97.8, contracts: 8, status: 'PREFERRED_VENDOR' },
  ];

  const catalog = [
    { id: 'prod-sec-soc-01', sku: 'SKU-SOC-247-CONTAIN', provider: 'Apex Cyber Defense Inc.', title: '24/7 Autonomous SOC Incident Containment', category: 'AI_SERVICE', pricing: 'DYNAMIC_USAGE', price: '$235.00', sla: '99.9% SLA' },
    { id: 'prod-freight-opt-02', sku: 'SKU-LOG-EU-DISPATCH', provider: 'Quantum Global Logistics GmbH', title: 'Autonomous Multimodal Cargo Dispatch', category: 'OUTCOME_CONTRACT', pricing: 'OUTCOME_BASED', price: '$65.00', sla: '99.5% SLA' },
    { id: 'prod-compute-h100', sku: 'SKU-CMP-H100-BURST', provider: 'Global AI Infrastructure Grid', title: 'H100 Distributed Compute Cluster Bursting', category: 'COMPUTE', pricing: 'USAGE_BASED', price: '$4.20 / hr', sla: '99.99% Uptime' },
  ];

  const orders = [
    { id: 'm2m-order-9001', number: 'M2M-2026-0914-8801', buyer: 'Uzaii Enterprise Corp', seller: 'Apex Cyber Defense Inc.', product: '24/7 Autonomous SOC Incident Containment', price: '$235.00', tier: 'Tier 4 (Bounded)', status: 'SETTLED' },
    { id: 'm2m-order-9002', number: 'M2M-2026-0914-8802', buyer: 'Uzaii Logistics Division', seller: 'Quantum Global Logistics GmbH', product: 'Autonomous Multimodal Cargo Dispatch', price: '$65.00', tier: 'Tier 4 (Bounded)', status: 'FULFILLED' },
  ];

  const handleQueryCopilot = () => {
    setCopilotResult({
      query: copilotQuery,
      executive_summary: "Analysis indicates peak ROI (3.4x) on federated cybersecurity automation. GPU compute cost can be reduced 8.5% via dynamic spot routing.",
      key_metrics: {
        autonomous_rate: "92.4%",
        oversight_rate: "100% on actions > $10,000",
        resilience: "98.4 / 100",
        monthly_roi: "$142,500 / mo"
      },
      recommendations: [
        "Enable dynamic compute bursting for off-peak model evaluation.",
        "Maintain dual-sourcing across Apex Cyber & Backup SOC to keep resilience above 98.0."
      ]
    });
  };

  const handleSimulateShock = () => {
    setSimulatingShock(true);
    setTimeout(() => {
      setShockResult({
        scenario: "PRIMARY_PROVIDER_OUTAGE",
        affected_provider: "Apex Cyber Defense Inc.",
        failover_action: "AUTOMATIC_FAILOVER_TO_BACKUP_SOC",
        failover_latency_seconds: 1.4,
        financial_exposure_usd: "$250.00",
        resilience_impact: "MINIMAL (-0.2%)",
        status: "FAILOVER_VERIFIED_SUCCESSFUL"
      });
      setSimulatingShock(false);
    }, 500);
  };

  const handleToggleEmergencyPause = () => {
    const nextState = !emergencyPause;
    setEmergencyPause(nextState);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Global AI Economic Network & Autonomous Machine Commerce OS
            </h1>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${emergencyPause ? 'bg-rose-950 text-rose-400 border border-rose-800' : 'bg-emerald-950 text-emerald-400 border border-emerald-800'}`}>
              {emergencyPause ? 'EMERGENCY ECONOMIC PAUSE ACTIVE' : 'MACHINE-NATIVE ECONOMY ACTIVE'}
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Enterprise-to-Enterprise Economic Mesh • Machine-to-Machine Commerce • Dynamic Pricing • Supply Chain Twin • Level 5 Autonomy Governance
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleSimulateShock}
            disabled={simulatingShock}
            className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-medium rounded-lg transition-all"
          >
            {simulatingShock ? 'Simulating Shock...' : '⚡ Simulate Supply-Chain Shock'}
          </button>
          <button
            onClick={handleToggleEmergencyPause}
            className={`px-4 py-2 text-xs font-semibold rounded-lg shadow-lg transition-all flex items-center gap-2 ${
              emergencyPause
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-950/50'
                : 'bg-rose-600 hover:bg-rose-500 text-white shadow-rose-950/50'
            }`}
          >
            {emergencyPause ? '▶️ Resume Economic Operations' : '🛑 GLOBAL AI ECONOMIC PAUSE'}
          </button>
        </div>
      </div>

      {/* Stat Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
        {stats.map((s, idx) => (
          <div key={idx} className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between backdrop-blur-sm">
            <span className="text-xs font-medium text-slate-400">{s.label}</span>
            <div className="my-2">
              <span className={`text-xl font-bold ${s.status === 'danger' ? 'text-rose-400' : 'text-white'}`}>{s.value}</span>
            </div>
            <span className={`text-xs ${s.status === 'danger' ? 'text-rose-400' : 'text-emerald-400'}`}>{s.change}</span>
          </div>
        ))}
      </div>

      {/* Tabs Navigation */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'command-center', label: 'Economic Command Center' },
          { id: 'entities', label: 'Machine-Native Orgs' },
          { id: 'provider-graph', label: 'Provider Graph' },
          { id: 'catalog', label: 'Product & Service Catalog' },
          { id: 'm2m-commerce', label: 'M2M Commerce Engine' },
          { id: 'supply-chain', label: 'Supply Chain Twin' },
          { id: 'risk-graph', label: 'Global Risk Graph' },
          { id: 'disputes', label: 'Dispute & Evidence Network' },
          { id: 'copilot', label: 'Autonomous Strategy Assistant' },
          { id: 'emergency-pause', label: 'Emergency Controls' },
          { id: 'governance', label: 'Autonomy Tiers & Audit' },
          { id: 'analytics', label: 'Economic KPIs & ROI' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all ${
              activeTab === tab.id
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Interactive Widgets Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Autonomous Strategy Assistant */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-emerald-400">🧠</span> Autonomous Strategy & Economic Assistant
            </h3>
            <span className="text-xs text-slate-400">Explainable Economic Query</span>
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
            />
            <button
              onClick={handleQueryCopilot}
              className="px-3 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium rounded-lg transition-all"
            >
              Analyze Strategy
            </button>
          </div>

          {copilotResult && (
            <div className="bg-slate-950 border border-emerald-900/50 rounded-lg p-3 space-y-2 text-xs">
              <div className="text-emerald-300 font-semibold border-b border-slate-800 pb-1">
                Executive Analysis: {copilotResult.executive_summary}
              </div>
              <div className="grid grid-cols-2 gap-2 text-slate-300 pt-1">
                <div><strong className="text-slate-400">Autonomy Rate:</strong> {copilotResult.key_metrics.autonomous_rate}</div>
                <div><strong className="text-slate-400">Resilience:</strong> {copilotResult.key_metrics.resilience}</div>
                <div><strong className="text-slate-400">Monthly ROI:</strong> {copilotResult.key_metrics.monthly_roi}</div>
                <div><strong className="text-slate-400">Human Oversight:</strong> {copilotResult.key_metrics.oversight_rate}</div>
              </div>
              <ul className="list-disc list-inside text-slate-400 pt-1 border-t border-slate-900 space-y-1">
                {copilotResult.recommendations.map((r: string, idx: number) => (
                  <li key={idx}>{r}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Supply-Chain Shock Simulation Results */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-cyan-400">🌐</span> Supply-Chain Digital Twin & Shock Simulator
            </h3>
            <span className="text-xs text-slate-400">Contingency Analysis</span>
          </div>
          <p className="text-xs text-slate-400">
            Simulate regional provider outages, geopolitical disruptions, or price spikes to verify autonomous contingency rerouting.
          </p>

          {shockResult ? (
            <div className="bg-slate-950 border border-cyan-900/50 rounded-lg p-3 space-y-1.5 text-xs">
              <div className="flex justify-between text-cyan-300 font-semibold border-b border-slate-800 pb-1">
                <span>Scenario: {shockResult.scenario}</span>
                <span className="text-emerald-400">{shockResult.status}</span>
              </div>
              <div className="grid grid-cols-2 gap-2 text-slate-300 pt-1">
                <div><strong className="text-slate-400">Affected Provider:</strong> {shockResult.affected_provider}</div>
                <div><strong className="text-slate-400">Failover Action:</strong> {shockResult.failover_action}</div>
                <div><strong className="text-slate-400">Failover Latency:</strong> {shockResult.failover_latency_seconds}s</div>
                <div><strong className="text-slate-400">Resilience Delta:</strong> {shockResult.resilience_impact}</div>
              </div>
            </div>
          ) : (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 text-center text-xs text-slate-500">
              Click &quot;Simulate Supply-Chain Shock&quot; above to execute a real-time contingency failover test.
            </div>
          )}
        </div>
      </div>

      {/* Main Tab Content Display */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
        {activeTab === 'command-center' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Global Economic Mesh Overview</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <h4 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-2">Connected Machine-Native Entities</h4>
                <ul className="space-y-2 text-xs">
                  {entities.map((e) => (
                    <li key={e.id} className="flex justify-between items-center border-b border-slate-900 pb-1">
                      <span className="text-slate-200 font-medium">{e.name}</span>
                      <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 text-[10px] font-mono">{e.trust} Trust</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <h4 className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-2">Machine-to-Machine Active Orders</h4>
                <ul className="space-y-2 text-xs">
                  {orders.map((o) => (
                    <li key={o.id} className="flex justify-between items-center border-b border-slate-900 pb-1">
                      <span className="text-slate-200 font-medium">{o.number} — {o.seller}</span>
                      <span className="text-emerald-400 font-bold">{o.price}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'entities' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Machine-Native Entities Directory</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Entity Name</th>
                    <th className="p-2.5">Type</th>
                    <th className="p-2.5">Domain</th>
                    <th className="p-2.5">Trust Score</th>
                    <th className="p-2.5">Resilience</th>
                    <th className="p-2.5">Commercial Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {entities.map((e) => (
                    <tr key={e.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-semibold text-white">{e.name}</td>
                      <td className="p-2.5 font-mono text-emerald-400">{e.type}</td>
                      <td className="p-2.5 font-mono text-slate-400">{e.domain}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{e.trust}</td>
                      <td className="p-2.5 font-bold text-cyan-400">{e.resilience}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 text-[10px] font-bold">{e.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'catalog' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Machine-Native Product & Service Catalog</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">SKU</th>
                    <th className="p-2.5">Product Title</th>
                    <th className="p-2.5">Provider</th>
                    <th className="p-2.5">Category</th>
                    <th className="p-2.5">Pricing Model</th>
                    <th className="p-2.5">Current Dynamic Price</th>
                    <th className="p-2.5">SLA</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {catalog.map((c) => (
                    <tr key={c.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-mono text-cyan-400 font-semibold">{c.sku}</td>
                      <td className="p-2.5 font-semibold text-white">{c.title}</td>
                      <td className="p-2.5 text-slate-300">{c.provider}</td>
                      <td className="p-2.5 text-slate-400">{c.category}</td>
                      <td className="p-2.5 font-mono text-amber-400 text-[10px]">{c.pricing}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{c.price}</td>
                      <td className="p-2.5 text-slate-400">{c.sla}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'm2m-commerce' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Machine-to-Machine Commercial Orders</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Order Number</th>
                    <th className="p-2.5">Buyer Entity</th>
                    <th className="p-2.5">Seller Entity</th>
                    <th className="p-2.5">Product Purchased</th>
                    <th className="p-2.5">Price</th>
                    <th className="p-2.5">Autonomy Tier</th>
                    <th className="p-2.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {orders.map((o) => (
                    <tr key={o.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-mono text-emerald-400">{o.number}</td>
                      <td className="p-2.5 text-slate-300">{o.buyer}</td>
                      <td className="p-2.5 font-semibold text-white">{o.seller}</td>
                      <td className="p-2.5 text-slate-400">{o.product}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{o.price}</td>
                      <td className="p-2.5 text-cyan-400 font-mono text-[10px]">{o.tier}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 text-[10px] font-bold">{o.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {['provider-graph', 'supply-chain', 'risk-graph', 'disputes', 'copilot', 'emergency-pause', 'governance', 'analytics'].includes(activeTab) && (
          <div className="space-y-3 py-4 text-center">
            <div className="inline-block p-3 rounded-full bg-slate-950 border border-slate-800 text-emerald-400 mb-2 text-xl">
              ⚙️
            </div>
            <h4 className="text-sm font-semibold text-white capitalize">{activeTab.replace('-', ' ')} Suite Active</h4>
            <p className="text-xs text-slate-400 max-w-lg mx-auto">
              Real-time graph orchestration, Level 5 governance risk auditing, and automated financial controls active for {activeTab}.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
