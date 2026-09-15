'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function EnterpriseITOperationsDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [copilotQuery, setCopilotQuery] = useState('What service is currently experiencing latency elevation and what is the root cause?');
  const [copilotResult, setCopilotResult] = useState<any>(null);
  const [executingRunbook, setExecutingRunbook] = useState(false);
  const [runbookResult, setRunbookResult] = useState<any>(null);

  const stats = [
    { label: 'Overall Service Health', value: '99.98%', change: '42 Active Tier-1/2 Services', status: 'optimal' },
    { label: 'Mean Time To Detect', value: '2.8 mins', change: 'AIOps Noise Reduction 84.5%', status: 'optimal' },
    { label: 'Mean Time To Respond', value: '8.4 mins', change: '74.2% Runbook Automation Rate', status: 'optimal' },
    { label: 'Active Incidents', value: '1 Active (P2)', change: 'INC-IT-2026-042 (Payments)', status: 'warning' },
    { label: 'SRE Error Budget', value: '89.6% Remaining', change: 'Auth API Burn Rate 0.2', status: 'optimal' },
    { label: 'Monthly Operational Cost', value: '$11,910', change: '$1,240 cost optimization opps', status: 'optimal' },
  ];

  const handleRunCopilot = () => {
    setTimeout(() => {
      setCopilotResult({
        answer: "Active P2 Incident INC-IT-2026-042: Payment Gateway latency elevated (P95 = 145ms). Caused by DB connection pool saturation following Deployment DEP-902.",
        evidence: ["APM Telemetry Stream (P99 = 280ms)", "Deployment Log DEP-902 at 18:31 UTC", "PostgreSQL Connection Metric (98/100 connections)"],
        confidence: 0.95
      });
    }, 400);
  };

  const handleExecuteRunbook = () => {
    setExecutingRunbook(true);
    setTimeout(() => {
      setRunbookResult({
        success: true,
        execution_code: "EXEC-891029",
        runbook_code: "RBK-DB-POOL-SCALE",
        target: "DB-PAYMENTS-PG",
        status: "SUCCESS",
        health_verification: "PASSED (Service latency returned to 42.5ms baseline)",
        rollback_token: "RLB-891029"
      });
      setExecutingRunbook(false);
    }, 600);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Enterprise IT Service Management & Autonomous AIOps
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
              AIOPS ENGINE OPERATIONAL
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            CMDB Topology, APM Observability, Incident Automation, SRE Error Budgets, Governed Runbooks & Operations Copilot.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-slate-900 border border-slate-700 hover:bg-slate-800 text-white">
            Export IT Operations Audit
          </button>
          <button className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-emerald-600 hover:bg-emerald-500 text-white shadow-sm">
            Launch Operations Copilot
          </button>
        </div>
      </div>

      {/* Stats Summary Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {stats.map((item, idx) => (
          <div key={idx} className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 space-y-1">
            <div className="text-xs text-slate-400">{item.label}</div>
            <div className="text-xl font-bold text-white">{item.value}</div>
            <div className={`text-[11px] font-medium ${item.status === 'warning' ? 'text-amber-400' : 'text-emerald-400'}`}>
              {item.change}
            </div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-6 text-sm font-medium">
        {[
          { id: 'command-center', label: 'IT Command Center' },
          { id: 'cmdb', label: 'Service Catalog & CMDB' },
          { id: 'observability', label: 'Observability & APM' },
          { id: 'incidents', label: 'Incidents & Root Cause' },
          { id: 'runbooks', label: 'Runbooks & Automation' },
          { id: 'sre', label: 'SRE, SLOs & Copilot' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`pb-3 border-b-2 transition-colors ${
              activeTab === tab.id
                ? 'border-emerald-400 text-emerald-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab 1: Command Center */}
      {activeTab === 'command-center' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Active IT Services & Health Status</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-800/50 text-slate-400 uppercase">
                  <tr>
                    <th className="p-2.5">Service</th>
                    <th className="p-2.5">Tier</th>
                    <th className="p-2.5">Owner</th>
                    <th className="p-2.5">Availability</th>
                    <th className="p-2.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  <tr>
                    <td className="p-2.5 font-semibold text-white">SVC-AUTH-API</td>
                    <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">TIER_1</span></td>
                    <td className="p-2.5 text-slate-300">IAM Platform Team</td>
                    <td className="p-2.5 text-emerald-400 font-bold">99.995%</td>
                    <td className="p-2.5 text-emerald-400 font-medium">OPERATIONAL</td>
                  </tr>
                  <tr>
                    <td className="p-2.5 font-semibold text-white">SVC-PAYMENT-GATEWAY</td>
                    <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">TIER_1</span></td>
                    <td className="p-2.5 text-slate-300">Payments Platform Team</td>
                    <td className="p-2.5 text-amber-400 font-bold">99.980%</td>
                    <td className="p-2.5 text-amber-400 font-medium">DEGRADED (LATENCY)</td>
                  </tr>
                  <tr>
                    <td className="p-2.5 font-semibold text-white">SVC-ANALYTICS-ENGINE</td>
                    <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-400 border border-indigo-800">TIER_2</span></td>
                    <td className="p-2.5 text-slate-300">Lakehouse Team</td>
                    <td className="p-2.5 text-emerald-400 font-bold">99.920%</td>
                    <td className="p-2.5 text-emerald-400 font-medium">OPERATIONAL</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">AIOps Noise Reduction Summary</h2>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Raw Alerts (24h):</span>
                <span className="text-white font-bold">1,420 Alerts</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Alert Noise Suppressed:</span>
                <span className="text-emerald-400 font-bold">84.5%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Correlated Incidents:</span>
                <span className="text-amber-400 font-bold">3 Incidents</span>
              </div>
              <div className="pt-2 border-t border-slate-800 text-slate-400 text-[11px]">
                Topology correlation linked 14 database connection alerts to single root cause incident INC-IT-2026-042.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: CMDB & Portfolio */}
      {activeTab === 'cmdb' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-lg font-semibold text-white">CMDB Configuration Items & Topology Mapping</h2>
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-xs">
            <div className="font-semibold text-emerald-400">Root Service: SVC-PAYMENT-GATEWAY</div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div className="p-3 bg-slate-900 border border-slate-800 rounded">
                <div className="text-slate-400">End User Session</div>
                <div className="text-white font-medium">Browser / Mobile App</div>
              </div>
              <div className="p-3 bg-slate-900 border border-slate-800 rounded">
                <div className="text-slate-400">Hosted On</div>
                <div className="text-white font-medium">AWS EKS K8s Cluster</div>
              </div>
              <div className="p-3 bg-slate-900 border border-slate-800 rounded">
                <div className="text-slate-400">Database Layer</div>
                <div className="text-white font-medium">PostgreSQL Payments Cluster</div>
              </div>
              <div className="p-3 bg-slate-900 border border-slate-800 rounded">
                <div className="text-slate-400">Third-Party API</div>
                <div className="text-white font-medium">Stripe Adapter API</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Observability & APM */}
      {activeTab === 'observability' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">APM Telemetry (SVC-PAYMENT-GATEWAY)</h2>
            <div className="grid grid-cols-2 gap-4 text-xs">
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                <div className="text-slate-400">Throughput</div>
                <div className="text-xl font-bold text-white">1,420 RPS</div>
              </div>
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                <div className="text-slate-400">P95 Latency</div>
                <div className="text-xl font-bold text-amber-400">88.0 ms</div>
              </div>
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                <div className="text-slate-400">P99 Latency</div>
                <div className="text-xl font-bold text-amber-400">145.0 ms</div>
              </div>
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                <div className="text-slate-400">Error Rate</div>
                <div className="text-xl font-bold text-emerald-400">0.015%</div>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Distributed Tracing (Sample Spans)</h2>
            <div className="space-y-2 text-xs">
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg flex justify-between">
                <div>
                  <div className="font-semibold text-white">POST /api/v1/payments/process</div>
                  <div className="text-slate-400 text-[11px]">Trace: TRC-892019401 | 4 Spans</div>
                </div>
                <div className="text-emerald-400 font-bold">48.2 ms (OK 200)</div>
              </div>
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg flex justify-between">
                <div>
                  <div className="font-semibold text-white">POST /api/v1/payments/process</div>
                  <div className="text-slate-400 text-[11px]">Trace: TRC-892019402 | Connection Pool Timeout</div>
                </div>
                <div className="text-amber-400 font-bold">280.5 ms (504)</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 4: Incidents & Root Cause */}
      {activeTab === 'incidents' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-lg font-semibold text-white">Active Incident: INC-IT-2026-042</h2>
          <div className="p-4 bg-amber-950/40 border border-amber-800 rounded-lg space-y-3 text-xs">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800">
                  P2_HIGH INCIDENT
                </span>
                <h3 className="text-base font-bold text-white mt-1">Payment Gateway Latency Spike</h3>
              </div>
              <span className="text-xs text-amber-400 font-semibold">Status: INVESTIGATING</span>
            </div>
            <p className="text-slate-300">
              Root Cause Hypothesis: Database connection pool exhaustion on primary PostgreSQL payment cluster following Deployment DEP-902.
            </p>
            <div className="pt-2 border-t border-amber-900/50 flex justify-between items-center text-slate-400">
              <span>Commander: payments.sre.lead@enterprise.com</span>
              <button
                onClick={handleExecuteRunbook}
                disabled={executingRunbook}
                className="px-3.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded shadow-sm"
              >
                {executingRunbook ? 'Executing Runbook...' : 'Run Auto-Remediation Runbook'}
              </button>
            </div>
          </div>

          {runbookResult && (
            <div className="p-4 bg-emerald-950/40 border border-emerald-800 rounded-lg text-xs space-y-2">
              <div className="font-bold text-emerald-400">✓ Runbook Execution Result: {runbookResult.status}</div>
              <p className="text-slate-300">Runbook: {runbookResult.runbook_code} Target: {runbookResult.target}</p>
              <div className="text-emerald-300 font-medium">{runbookResult.health_verification}</div>
            </div>
          )}
        </div>
      )}

      {/* Tab 5: Runbooks & Automation */}
      {activeTab === 'runbooks' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
          {[
            { code: 'RBK-DB-POOL-SCALE', name: 'Database Connection Pool Expansion', autonomy: 'L3', desc: 'Scales max DB connection pool size from 100 to 250 under high load' },
            { code: 'RBK-CANARY-ROLLBACK', name: 'Automated Deployment Rollback', autonomy: 'L4', desc: 'Reverts active Kubernetes deployment to previous healthy revision' },
            { code: 'RBK-FAILOVER-DR', name: 'Production DR Failover', autonomy: 'L5', desc: 'Promotes secondary cloud region database replica to primary (Approval Reqd)' }
          ].map((rbk) => (
            <div key={rbk.code} className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-3">
              <div className="flex justify-between">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                  Autonomy {rbk.autonomy}
                </span>
                <span className="text-emerald-400 font-semibold">REVERSIBLE</span>
              </div>
              <h3 className="text-sm font-bold text-white">{rbk.name}</h3>
              <p className="text-slate-400">{rbk.desc}</p>
            </div>
          ))}
        </div>
      )}

      {/* Tab 6: SRE, SLOs & Copilot */}
      {activeTab === 'sre' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-5">
          <h2 className="text-lg font-semibold text-white">Operations Copilot</h2>
          <div className="flex gap-3">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              className="flex-1 px-4 py-2 bg-slate-950 border border-slate-700 rounded-lg text-sm text-white focus:outline-none"
              placeholder="Ask Operations Copilot..."
            />
            <button
              onClick={handleRunCopilot}
              className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm rounded-lg shadow-sm"
            >
              Query Operations Copilot
            </button>
          </div>

          {copilotResult && (
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-xs">
              <div className="font-semibold text-emerald-400">Operations Copilot Response:</div>
              <p className="text-slate-200">{copilotResult.answer}</p>
              <div className="pt-2 border-t border-slate-800 text-slate-400">
                <div className="font-medium text-slate-300">Underlying Evidence Citations:</div>
                <ul className="list-disc list-inside mt-1 text-slate-300">
                  {copilotResult.evidence.map((item: string, idx: number) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
