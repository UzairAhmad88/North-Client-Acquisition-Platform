'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function EnterpriseFederationDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [copilotQuery, setCopilotQuery] = useState('Find the best external provider for 24/7 cross-org SOC containment under $300/order');
  const [copilotResult, setCopilotResult] = useState<any>(null);
  const [runningSimulation, setRunningSimulation] = useState(false);
  const [simResult, setSimResult] = useState<any>(null);

  const stats = [
    { label: 'Connected Organizations', value: '18 Orgs', change: '100% Zero-Trust Verified', status: 'optimal' },
    { label: 'Federated Agent Identities', value: '142 Identities', change: 'mTLS + JWT Certificates', status: 'optimal' },
    { label: 'Active B2B Contracts', value: '48 Contracts', change: 'Machine-Readable SLAs', status: 'optimal' },
    { label: 'Running Work Orders', value: '84 Orders', change: 'Sandbox + Output Sanitized', status: 'optimal' },
    { label: 'Settled B2B Transactions', value: '$1.24M Settled', change: 'Zero Unreconciled Invoices', status: 'optimal' },
    { label: 'Federation Trust Score', value: '99.2 Avg Trust', change: 'Continuous Attestation', status: 'optimal' },
  ];

  const organizations = [
    { id: 'org-apex-cyber', name: 'Apex Cyber Defense Inc.', domain: 'apexcyber.com', industry: 'Cybersecurity & SOC', status: 'ACTIVE', trust: 99.8, attestation: 'ISO27001_SOC2_TYPE2', agents: 14 },
    { id: 'org-quantum-logistics', name: 'Quantum Global Logistics GmbH', domain: 'quantumlogistics.eu', industry: 'Supply Chain & Transport', status: 'ACTIVE', trust: 98.9, attestation: 'SOC2_TYPE2', agents: 8 },
    { id: 'org-fintech-matrix', name: 'Matrix Financial Automation Corp', domain: 'matrixfin.com', industry: 'FinTech & Accounting', status: 'PENDING_REVIEW', trust: 96.5, attestation: 'SOC1_SOC2_TYPE2', agents: 5 },
  ];

  const contracts = [
    { id: 'contract-fed-001', number: 'FC-2026-APEX-009', buyer: 'Uzaii Enterprise Corp', seller: 'Apex Cyber Defense Inc.', scope: 'Automated Cross-Org Threat Intel & Managed SOC', maxValue: '$25,000.00', sla: '99.9%', humanApproval: 'Required > $5,000', status: 'ACTIVE' },
    { id: 'contract-fed-002', number: 'FC-2026-QUANTUM-014', buyer: 'Uzaii Logistics Division', seller: 'Quantum Global Logistics GmbH', scope: 'Autonomous Freight Dispatch & Route Optimization', maxValue: '$15,000.00', sla: '99.5%', humanApproval: 'Auto-Approved < $5,000', status: 'ACTIVE' },
  ];

  const negotiations = [
    { id: 'neg-001', buyerAgent: 'Buyer-Agent-ProcureX', sellerAgent: 'Apex-SalesAgent-01', service: '24/7 Managed SOC Telemetry Analysis', quote: '$300.00', agreedPrice: '$250.00', status: 'AGREED', confidence: '98%', guardrails: 'PASSED' },
    { id: 'neg-002', buyerAgent: 'Buyer-Agent-Logistics', sellerAgent: 'Quantum-Dispatcher-Agent', service: 'Cross-Border Cargo Routing & Clearance', quote: '$80.00', agreedPrice: '$65.00', status: 'AGREED', confidence: '96%', guardrails: 'PASSED' },
  ];

  const workOrders = [
    { id: 'wo-fed-801', number: 'WO-2026-0914-01', contract: 'FC-2026-APEX-009', agent: 'Apex-Sentinel-Prime', service: 'Zero-Trust Threat Telemetry Scan', price: '$250.00', status: 'DELIVERED', sanitized: 'YES', quality: '99.7%' },
    { id: 'wo-fed-802', number: 'WO-2026-0914-02', contract: 'FC-2026-QUANTUM-014', agent: 'Quantum-RouteOptima', service: 'EU Corridor Freight Optimization', price: '$65.00', status: 'SETTLED', sanitized: 'YES', quality: '98.9%' },
  ];

  const handleRunCopilot = () => {
    setCopilotResult({
      recommended_provider: 'Apex Cyber Defense Inc. (Sentinel Prime Agent)',
      negotiated_price: '$250.00 / order (16.6% savings vs quote)',
      sla_guarantee: '99.9% uptime, < 5 min response time',
      trust_score: '99.8 / 100.0 (ISO 27001 + SOC 2 Type II)',
      reasoning: 'Apex Cyber meets all zero-trust criteria, has highest historical SLA compliance, and existing active federation agreement FC-2026-APEX-009.',
      risk_level: 'LOW (Within Pre-approved Level 4 Autonomy Limit)',
    });
  };

  const handleSimulateNegotiation = () => {
    setRunningSimulation(true);
    setTimeout(() => {
      setSimResult({
        simulation_id: 'sim-b2b-9921',
        buyer_agent: 'Uzaii-Procurement-Agent',
        seller_agent: 'Apex-SalesAgent-01',
        initial_offer: '$300.00',
        counter_offer: '$240.00',
        final_agreed_price: '$250.00',
        guardrails_status: 'ALL PASSED',
        legal_data_transfers: 'ZERO EXFILTRATION (Sanitized API Gateway)',
        governance_approval: 'AUTO-APPROVED (Under $5,000 threshold)',
      });
      setRunningSimulation(false);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Enterprise AI Federation & Autonomous B2B Commerce OS
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-950 text-indigo-400 border border-indigo-800">
              ZERO-TRUST B2B FEDERATION ACTIVE
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Cross-Organization Agent Networks • Machine-Readable Contracts • Autonomous B2B Negotiation & Settlement • Level 5 Governance
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleSimulateNegotiation}
            disabled={runningSimulation}
            className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white font-medium text-sm rounded-lg shadow-lg shadow-indigo-950/50 transition-all flex items-center gap-2"
          >
            {runningSimulation ? 'Simulating Negotiation...' : '⚡ Simulate Autonomous B2B Negotiation'}
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
          { id: 'command-center', label: 'Federation Command Center' },
          { id: 'organizations', label: 'Federated Organizations' },
          { id: 'identities', label: 'Zero-Trust Agent Identities' },
          { id: 'discovery', label: 'Capability Search' },
          { id: 'contracts', label: 'Contracts Workspace' },
          { id: 'negotiations', label: 'Negotiation Engine' },
          { id: 'work-orders', label: 'Work Order Tracker' },
          { id: 'procurement', label: 'B2B Procurement Copilot' },
          { id: 'payments', label: 'Invoicing & Settlement' },
          { id: 'disputes', label: 'SLA & Disputes' },
          { id: 'trust', label: 'Security & Trust Scorecard' },
          { id: 'analytics', label: 'Federated Economics' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all ${
              activeTab === tab.id
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-950'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Interactive Copilot & Simulation Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* B2B Procurement Copilot */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-indigo-400">🤖</span> Autonomous B2B AI Procurement Copilot
            </h3>
            <span className="text-xs text-slate-400">Explainable Provider Selection</span>
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
            />
            <button
              onClick={handleRunCopilot}
              className="px-3 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded-lg transition-all"
            >
              Analyze Provider
            </button>
          </div>

          {copilotResult && (
            <div className="bg-slate-950 border border-indigo-900/50 rounded-lg p-3 space-y-2 text-xs">
              <div className="flex justify-between items-center text-indigo-300 font-semibold border-b border-slate-800 pb-1">
                <span>Recommended: {copilotResult.recommended_provider}</span>
                <span className="text-emerald-400">{copilotResult.risk_level}</span>
              </div>
              <p className="text-slate-300"><strong className="text-slate-400">Price:</strong> {copilotResult.negotiated_price}</p>
              <p className="text-slate-300"><strong className="text-slate-400">SLA:</strong> {copilotResult.sla_guarantee}</p>
              <p className="text-slate-300"><strong className="text-slate-400">Trust:</strong> {copilotResult.trust_score}</p>
              <p className="text-slate-400 italic pt-1 border-t border-slate-900">{copilotResult.reasoning}</p>
            </div>
          )}
        </div>

        {/* B2B Negotiation Simulator */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-cyan-400">⚖️</span> Autonomous Negotiation & Guardrail Simulator
            </h3>
            <span className="text-xs text-slate-400">Pre-Execution Test Engine</span>
          </div>
          <p className="text-xs text-slate-400">
            Simulate buyer-agent and seller-agent negotiation rounds under strict financial, legal, and zero-trust safety guardrails.
          </p>

          {simResult ? (
            <div className="bg-slate-950 border border-cyan-900/50 rounded-lg p-3 space-y-1.5 text-xs">
              <div className="flex justify-between text-cyan-300 font-semibold border-b border-slate-800 pb-1">
                <span>Simulation: {simResult.simulation_id}</span>
                <span className="text-emerald-400">{simResult.guardrails_status}</span>
              </div>
              <div className="grid grid-cols-2 gap-2 text-slate-300 pt-1">
                <div><strong className="text-slate-400">Initial Quote:</strong> {simResult.initial_offer}</div>
                <div><strong className="text-slate-400">Agreed Price:</strong> {simResult.final_agreed_price}</div>
                <div><strong className="text-slate-400">Data Boundaries:</strong> {simResult.legal_data_transfers}</div>
                <div><strong className="text-slate-400">Governance:</strong> {simResult.governance_approval}</div>
              </div>
            </div>
          ) : (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 text-center text-xs text-slate-500">
              Click &quot;Simulate Autonomous B2B Negotiation&quot; above to execute a real-time negotiation protocol run.
            </div>
          )}
        </div>
      </div>

      {/* Main Tab Content Display */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
        {activeTab === 'command-center' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Active Federation Overview</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <h4 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-2">Connected Partner Organizations</h4>
                <ul className="space-y-2 text-xs">
                  {organizations.map((org) => (
                    <li key={org.id} className="flex justify-between items-center border-b border-slate-900 pb-1">
                      <span className="text-slate-200 font-medium">{org.name}</span>
                      <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 text-[10px] font-mono">{org.trust} Trust</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <h4 className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-2">Machine-Readable Active Contracts</h4>
                <ul className="space-y-2 text-xs">
                  {contracts.map((c) => (
                    <li key={c.id} className="flex justify-between items-center border-b border-slate-900 pb-1">
                      <span className="text-slate-200 font-medium">{c.number} — {c.seller}</span>
                      <span className="text-slate-400">{c.maxValue}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'organizations' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Federated Organizations Directory</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Organization</th>
                    <th className="p-2.5">Domain</th>
                    <th className="p-2.5">Industry</th>
                    <th className="p-2.5">Trust Score</th>
                    <th className="p-2.5">Security Attestation</th>
                    <th className="p-2.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {organizations.map((o) => (
                    <tr key={o.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-semibold text-white">{o.name}</td>
                      <td className="p-2.5 font-mono text-slate-400">{o.domain}</td>
                      <td className="p-2.5">{o.industry}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{o.trust}</td>
                      <td className="p-2.5 font-mono text-slate-400">{o.attestation}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-400 text-[10px] font-bold">{o.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'contracts' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Machine-Readable B2B Federation Contracts</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Contract Number</th>
                    <th className="p-2.5">Buyer</th>
                    <th className="p-2.5">Seller</th>
                    <th className="p-2.5">Scope</th>
                    <th className="p-2.5">Max Value</th>
                    <th className="p-2.5">SLA Target</th>
                    <th className="p-2.5">Governance</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {contracts.map((c) => (
                    <tr key={c.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-mono text-cyan-400 font-semibold">{c.number}</td>
                      <td className="p-2.5">{c.buyer}</td>
                      <td className="p-2.5 font-semibold text-white">{c.seller}</td>
                      <td className="p-2.5 text-slate-400">{c.scope}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{c.maxValue}</td>
                      <td className="p-2.5">{c.sla}</td>
                      <td className="p-2.5 text-amber-400 font-mono text-[10px]">{c.humanApproval}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'negotiations' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Autonomous Agent-to-Agent Negotiation Log</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Buyer Agent</th>
                    <th className="p-2.5">Seller Agent</th>
                    <th className="p-2.5">Service Requested</th>
                    <th className="p-2.5">Initial Quote</th>
                    <th className="p-2.5">Agreed Price</th>
                    <th className="p-2.5">Guardrail Checks</th>
                    <th className="p-2.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {negotiations.map((n) => (
                    <tr key={n.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-mono text-slate-300">{n.buyerAgent}</td>
                      <td className="p-2.5 font-mono text-indigo-400">{n.sellerAgent}</td>
                      <td className="p-2.5 font-medium text-white">{n.service}</td>
                      <td className="p-2.5 line-through text-slate-500">{n.quote}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{n.agreedPrice}</td>
                      <td className="p-2.5 text-emerald-400 font-mono text-[10px]">{n.guardrails}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 text-[10px] font-bold">{n.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'work-orders' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Autonomous Work Order Execution Tracker</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Work Order #</th>
                    <th className="p-2.5">Executing Agent</th>
                    <th className="p-2.5">Service Name</th>
                    <th className="p-2.5">Price</th>
                    <th className="p-2.5">Sanitized Output</th>
                    <th className="p-2.5">Quality Score</th>
                    <th className="p-2.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {workOrders.map((w) => (
                    <tr key={w.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-mono text-indigo-300">{w.number}</td>
                      <td className="p-2.5 font-mono text-slate-300">{w.agent}</td>
                      <td className="p-2.5 font-medium text-white">{w.service}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{w.price}</td>
                      <td className="p-2.5 text-emerald-400 font-mono text-[10px]">{w.sanitized}</td>
                      <td className="p-2.5">{w.quality}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-400 text-[10px] font-bold">{w.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {['identities', 'discovery', 'procurement', 'payments', 'disputes', 'trust', 'analytics'].includes(activeTab) && (
          <div className="space-y-3 py-4 text-center">
            <div className="inline-block p-3 rounded-full bg-slate-950 border border-slate-800 text-indigo-400 mb-2 text-xl">
              🛡️
            </div>
            <h4 className="text-sm font-semibold text-white capitalize">{activeTab.replace('-', ' ')} Operational Suite</h4>
            <p className="text-xs text-slate-400 max-w-lg mx-auto">
              Real-time zero-trust isolation, machine-readable contracts, and automated settlement engine active for {activeTab}.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
