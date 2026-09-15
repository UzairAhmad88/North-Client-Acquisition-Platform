'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function PlanetaryInfrastructureDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [strategyQuery, setStrategyQuery] = useState('What happens if US-East region experiences a 20% traffic surge during an energy price spike?');
  const [strategyResult, setStrategyResult] = useState<any>(null);
  const [globalKillSwitch, setGlobalKillSwitch] = useState<boolean>(false);
  const [safeMode, setSafeMode] = useState<boolean>(false);
  const [failoverRunning, setFailoverRunning] = useState<boolean>(false);
  const [failoverResult, setFailoverResult] = useState<any>(null);

  const stats = [
    { label: 'Active Fabric Clusters', value: '14 Clusters', change: 'Multi-Region Active-Active', status: 'optimal' },
    { label: 'Verified Agent Mesh Nodes', value: '1,840 Agents', change: 'mTLS + Cryptographic Attestation', status: 'optimal' },
    { label: 'Global Resilience Score', value: '99.4 / 100', change: 'Zero Single Points of Failure', status: 'optimal' },
    { label: 'Achieved RTO / RPO', value: '1.2s RTO / 0s RPO', change: 'Real-time Synchronized', status: 'optimal' },
    { label: 'Grid Carbon Intensity', value: '112 g/kWh Avg', change: 'Carbon-Aware Workload Routing', status: 'optimal' },
    { label: 'Emergency Status', value: globalKillSwitch ? 'KILL SWITCH ENGAGED' : (safeMode ? 'SAFE MODE ACTIVE' : 'NORMAL OPERATIONS'), change: globalKillSwitch || safeMode ? 'Restricted Execution' : 'Full Governed Autonomy', status: globalKillSwitch || safeMode ? 'danger' : 'optimal' },
  ];

  const nodes = [
    { id: 'node-us-east-01', name: 'US-East Planetary Cluster Alpha', region: 'US_EAST', type: 'CLOUD_CLUSTER', carbon: '140.2 g/kWh', workloads: 1420, health: 99.9, status: 'HEALTHY' },
    { id: 'node-eu-central-02', name: 'EU-Central Planetary Cluster Beta', region: 'EU_CENTRAL', type: 'REGIONAL_DC', carbon: '95.0 g/kWh', workloads: 980, health: 99.9, status: 'HEALTHY' },
    { id: 'node-edge-factory-03', name: 'Munich Edge Smart Facility Rack', region: 'EDGE_GERMANY', type: 'FACTORY_RACK', carbon: '110.0 g/kWh', workloads: 45, health: 99.7, status: 'HEALTHY' },
  ];

  const meshAgents = [
    { id: 'mesh-agent-sentinel', name: 'Sentinel Prime — Cross-Org Threat Hunter', org: 'Apex Cyber Defense Inc.', attestation: 'VERIFIED', trust: 99.8, quarantine: 'CLEAN', tier: 'PRODUCTION' },
    { id: 'mesh-agent-routeoptima', name: 'RouteOptima — Autonomous Freight Broker', org: 'Quantum Global Logistics GmbH', attestation: 'VERIFIED', trust: 98.9, quarantine: 'CLEAN', tier: 'PRODUCTION' },
  ];

  const pipeline = [
    { id: 'agent-sre-v5-candidate', name: 'Aria-Ops v5 Candidate', currentTier: 'VALIDATED', targetTier: 'CERTIFIED', passRate: '100.0%', isolation: 'CONTAINER_EBPF_SANDBOX', status: 'READY_FOR_CERTIFICATION' },
    { id: 'agent-sentinel-prime', name: 'Sentinel Prime', currentTier: 'PRODUCTION', targetTier: 'PRODUCTION', passRate: '100.0%', isolation: 'PRODUCTION_SCOPED', status: 'ACTIVE_PRODUCTION' },
  ];

  const handleRunStrategySimulation = () => {
    setStrategyResult({
      query: strategyQuery,
      scenario: "US-East Traffic Surge & Low-Carbon Rerouting",
      assumptions: [
        "20% workload increase on US-East Alpha",
        "EU-Central carbon intensity 32% lower than US-East",
        "Low-latency regional edge failover verified (<15ms)"
      ],
      pareto_recommendations: [
        "Reroute 35% of off-peak background workloads to EU-Central (Saves 12% cost & lowers carbon footprint by 18%).",
        "Maintain high-priority real-time API execution on US-East Alpha."
      ],
      confidence: 0.99
    });
  };

  const handleExecuteFailover = () => {
    setFailoverRunning(true);
    setTimeout(() => {
      setFailoverResult({
        action: "AUTOMATED_REGION_FAILOVER",
        failed_region: "US_EAST_SIMULATED",
        target_region: "EU_CENTRAL",
        failover_duration_seconds: 1.2,
        rto_achieved: "1.2s",
        rpo_achieved: "0s",
        residency_compliance: "PRESERVED",
        status: "FAILOVER_HEALTHY"
      });
      setFailoverRunning(false);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Planetary-Scale AI Infrastructure & Global Agent Mesh OS
            </h1>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${globalKillSwitch || safeMode ? 'bg-rose-950 text-rose-400 border border-rose-800' : 'bg-cyan-950 text-cyan-400 border border-cyan-800'}`}>
              {globalKillSwitch ? 'GLOBAL KILL SWITCH ENGAGED' : (safeMode ? 'SAFE MODE ACTIVE' : 'PLANETARY INTELLIGENCE FABRIC ACTIVE')}
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Global Agent Mesh • Cloud-Edge Orchestration • Multi-Region Active-Active DR • Energy FinOps • Emergency Governance
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleExecuteFailover}
            disabled={failoverRunning}
            className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-medium rounded-lg transition-all"
          >
            {failoverRunning ? 'Simulating Failover...' : '⚡ Test Region Failover'}
          </button>
          <button
            onClick={() => setSafeMode(!safeMode)}
            className={`px-3 py-2 text-xs font-semibold rounded-lg transition-all border ${
              safeMode
                ? 'bg-amber-950 text-amber-300 border-amber-800'
                : 'bg-slate-900 text-slate-300 border-slate-700 hover:bg-slate-800'
            }`}
          >
            {safeMode ? '🛡️ Safe Mode Enabled' : '🛡️ Enable Safe Mode'}
          </button>
          <button
            onClick={() => setGlobalKillSwitch(!globalKillSwitch)}
            className={`px-4 py-2 text-xs font-semibold rounded-lg shadow-lg transition-all flex items-center gap-2 ${
              globalKillSwitch
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-950/50'
                : 'bg-rose-600 hover:bg-rose-500 text-white shadow-rose-950/50'
            }`}
          >
            {globalKillSwitch ? '▶️ Resume Global Fabric' : '🛑 GLOBAL KILL SWITCH'}
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
            <span className={`text-xs ${s.status === 'danger' ? 'text-rose-400' : 'text-cyan-400'}`}>{s.change}</span>
          </div>
        ))}
      </div>

      {/* Tabs Navigation */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'command-center', label: 'Global Command Center' },
          { id: 'agent-mesh', label: 'Agent Mesh' },
          { id: 'global-fabric', label: 'Planetary Fabric Nodes' },
          { id: 'resilience', label: 'Resilience & DR Engine' },
          { id: 'infra-twin', label: 'Physical & Digital Twin' },
          { id: 'promotion', label: 'Agent Promotion Pipeline' },
          { id: 'security-soc', label: 'Security SOC & Quarantine' },
          { id: 'sandbox-sim', label: 'Multi-Agent Simulation Fabric' },
          { id: 'strategy', label: 'Planetary Strategic Simulator' },
          { id: 'emergency', label: 'Emergency Controls & Kill Switch' },
          { id: 'governance', label: 'Machine Governance Fabric' },
          { id: 'finops', label: 'Energy & Compute FinOps' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all ${
              activeTab === tab.id
                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-950'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Interactive Widgets Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Planetary Strategic Simulator */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-cyan-400">🌏</span> Planetary Strategic Simulator & Early Warning
            </h3>
            <span className="text-xs text-slate-400">Pareto Optimization</span>
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={strategyQuery}
              onChange={(e) => setStrategyQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            />
            <button
              onClick={handleRunStrategySimulation}
              className="px-3 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-medium rounded-lg transition-all"
            >
              Simulate Scenario
            </button>
          </div>

          {strategyResult && (
            <div className="bg-slate-950 border border-cyan-900/50 rounded-lg p-3 space-y-2 text-xs">
              <div className="text-cyan-300 font-semibold border-b border-slate-800 pb-1">
                Simulation: {strategyResult.scenario}
              </div>
              <ul className="list-disc list-inside text-slate-400 space-y-1">
                {strategyResult.pareto_recommendations.map((r: string, idx: number) => (
                  <li key={idx}>{r}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Multi-Region Active-Active Failover Test Output */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-indigo-400">⚡</span> Global Resilience & Region Failover Engine
            </h3>
            <span className="text-xs text-slate-400">Active-Active Replication</span>
          </div>
          <p className="text-xs text-slate-400">
            Simulate instantaneous regional outages to test zero-data-loss active-active failover execution.
          </p>

          {failoverResult ? (
            <div className="bg-slate-950 border border-indigo-900/50 rounded-lg p-3 space-y-1.5 text-xs">
              <div className="flex justify-between text-indigo-300 font-semibold border-b border-slate-800 pb-1">
                <span>Action: {failoverResult.action}</span>
                <span className="text-emerald-400">{failoverResult.status}</span>
              </div>
              <div className="grid grid-cols-2 gap-2 text-slate-300 pt-1">
                <div><strong className="text-slate-400">Failed Region:</strong> {failoverResult.failed_region}</div>
                <div><strong className="text-slate-400">Target Region:</strong> {failoverResult.target_region}</div>
                <div><strong className="text-slate-400">RTO Achieved:</strong> {failoverResult.rto_achieved}</div>
                <div><strong className="text-slate-400">RPO Achieved:</strong> {failoverResult.rpo_achieved}</div>
              </div>
            </div>
          ) : (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 text-center text-xs text-slate-500">
              Click &quot;Test Region Failover&quot; above to execute an active-active regional failover test.
            </div>
          )}
        </div>
      </div>

      {/* Main Tab Content Display */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
        {activeTab === 'command-center' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Planetary Infrastructure Overview</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <h4 className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-2">Planetary Fabric Clusters</h4>
                <ul className="space-y-2 text-xs">
                  {nodes.map((n) => (
                    <li key={n.id} className="flex justify-between items-center border-b border-slate-900 pb-1">
                      <span className="text-slate-200 font-medium">{n.name}</span>
                      <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 text-[10px] font-mono">{n.health}% Health</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <h4 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-2">Verified Agent Mesh Nodes</h4>
                <ul className="space-y-2 text-xs">
                  {meshAgents.map((m) => (
                    <li key={m.id} className="flex justify-between items-center border-b border-slate-900 pb-1">
                      <span className="text-slate-200 font-medium">{m.name}</span>
                      <span className="text-cyan-400 font-mono text-[10px]">{m.tier}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'agent-mesh' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Global Agent Mesh Directory</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Agent Name</th>
                    <th className="p-2.5">Organization</th>
                    <th className="p-2.5">Attestation</th>
                    <th className="p-2.5">Trust Score</th>
                    <th className="p-2.5">Quarantine</th>
                    <th className="p-2.5">Promotion Tier</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {meshAgents.map((m) => (
                    <tr key={m.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-semibold text-white">{m.name}</td>
                      <td className="p-2.5 text-slate-300">{m.org}</td>
                      <td className="p-2.5 font-mono text-emerald-400">{m.attestation}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{m.trust}</td>
                      <td className="p-2.5 font-mono text-emerald-400 text-[10px]">{m.quarantine}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 text-[10px] font-bold">{m.tier}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'promotion' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Agent Promotion & Certification Pipeline</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Agent Name</th>
                    <th className="p-2.5">Current Tier</th>
                    <th className="p-2.5">Target Tier</th>
                    <th className="p-2.5">Adversarial Pass Rate</th>
                    <th className="p-2.5">Sandbox Isolation</th>
                    <th className="p-2.5">Pipeline Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {pipeline.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-semibold text-white">{p.name}</td>
                      <td className="p-2.5 font-mono text-amber-400">{p.currentTier}</td>
                      <td className="p-2.5 font-mono text-cyan-400">{p.targetTier}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{p.passRate}</td>
                      <td className="p-2.5 font-mono text-slate-400 text-[10px]">{p.isolation}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 text-[10px] font-bold">{p.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {['global-fabric', 'resilience', 'infra-twin', 'security-soc', 'sandbox-sim', 'strategy', 'emergency', 'governance', 'finops'].includes(activeTab) && (
          <div className="space-y-3 py-4 text-center">
            <div className="inline-block p-3 rounded-full bg-slate-950 border border-slate-800 text-cyan-400 mb-2 text-xl">
              ⚡
            </div>
            <h4 className="text-sm font-semibold text-white capitalize">{activeTab.replace('-', ' ')} Operational Control</h4>
            <p className="text-xs text-slate-400 max-w-lg mx-auto">
              Planetary-scale intelligent fabric, zero-trust attestation, and emergency killswitch isolation active for {activeTab}.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
