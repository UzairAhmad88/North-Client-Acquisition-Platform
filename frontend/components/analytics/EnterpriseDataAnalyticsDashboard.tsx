'use client';

import React, { useState } from 'react';

export default function EnterpriseDataAnalyticsDashboard() {
  const [activeTab, setActiveTab] = useState<'command-center' | 'catalog' | 'metrics' | 'dashboards' | 'text-to-sql' | 'insights'>('command-center');
  const [nlQuery, setNlQuery] = useState('Show monthly net revenue by customer region for this year');
  const [nlResult, setNlResult] = useState<any>(null);
  const [isLoadingQuery, setIsLoadingQuery] = useState(false);

  const stats = [
    { label: 'Overall Quality Score', value: '98.6%', change: '1,240 rules passing', status: 'optimal' },
    { label: 'Ingestion CDC Lag', value: '120 ms', change: '42 pipelines active', status: 'optimal' },
    { label: 'Governed Metrics', value: '148 KPIs', change: 'Single Source of Truth', status: 'optimal' },
    { label: 'Active Data Products', value: '24 Products', change: '514 Subscribers', status: 'optimal' },
    { label: 'Detected Anomalies', value: '2 Active', change: 'EMEA SLA Breach at risk', status: 'warning' },
    { label: 'Monthly FinOps Spend', value: '$4,820', change: '$1,010 optimization opps', status: 'optimal' },
  ];

  const handleRunTextToSql = () => {
    setIsLoadingQuery(true);
    setTimeout(() => {
      setNlResult({
        nl_prompt: nlQuery,
        sql_query: "SELECT date_trunc('month', invoice_date) AS month, customer_region, SUM(net_amount) AS revenue FROM gold_sales_360 WHERE invoice_date >= '2026-01-01' GROUP BY 1, 2 ORDER BY 1 DESC;",
        explanation: "Calculates monthly net revenue grouped by customer region for 2026 using the governed metric 'MTR-FIN-REV'.",
        dataset_used: "DS-GOLD-SALES-360",
        cost_estimation: { estimated_bytes_scanned: 1420000, estimated_cost_usd: 0.004 },
        rows: [
          { month: '2026-08-01', region: 'North America', revenue: '$18,420,000', growth: '+14.2%' },
          { month: '2026-08-01', region: 'EMEA', revenue: '$12,850,000', growth: '+18.1%' },
          { month: '2026-08-01', region: 'APAC', revenue: '$11,580,000', growth: '+22.4%' },
          { month: '2026-07-01', region: 'North America', revenue: '$16,100,000', growth: '+11.8%' },
        ]
      });
      setIsLoadingQuery(false);
    }, 600);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Enterprise Data & Analytics Intelligence Platform
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-cyan-950 text-cyan-400 border border-cyan-800">
              REAL-TIME FABRIC ACTIVE
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Lakehouse Architecture, Governed Metrics Layer, Governed Text-to-SQL, BI Engine, and Decision-Grade AI Intelligence.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-slate-900 border border-slate-700 hover:bg-slate-800 text-white">
            Export Audit Log
          </button>
          <button className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-cyan-600 hover:bg-cyan-500 text-white shadow-sm">
            Launch Data Explorer
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
          { id: 'command-center', label: 'Command Center' },
          { id: 'catalog', label: 'Data Catalog & Marketplace' },
          { id: 'metrics', label: 'Governed Metrics Layer' },
          { id: 'dashboards', label: 'BI Dashboards' },
          { id: 'text-to-sql', label: 'Text-to-SQL Workspace' },
          { id: 'insights', label: 'AI Analytics & Forecasts' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`pb-3 border-b-2 transition-colors ${
              activeTab === tab.id
                ? 'border-cyan-400 text-cyan-400'
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
            <h2 className="text-lg font-semibold text-white">Ingestion Pipelines & Real-Time Fabric</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-800/50 text-slate-400 uppercase">
                  <tr>
                    <th className="p-2.5">Pipeline</th>
                    <th className="p-2.5">Source</th>
                    <th className="p-2.5">Mode</th>
                    <th className="p-2.5">Processed</th>
                    <th className="p-2.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  <tr>
                    <td className="p-2.5 font-semibold text-white">PIPE-CDC-ORDERS</td>
                    <td className="p-2.5 text-slate-300">PostgreSQL Primary</td>
                    <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">CDC</span></td>
                    <td className="p-2.5 text-slate-300">145,200 recs</td>
                    <td className="p-2.5 text-emerald-400 font-medium">RUNNING</td>
                  </tr>
                  <tr>
                    <td className="p-2.5 font-semibold text-white">PIPE-BATCH-FINANCE-DAILY</td>
                    <td className="p-2.5 text-slate-300">Oracle ERP</td>
                    <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-400 border border-indigo-800">BATCH</span></td>
                    <td className="p-2.5 text-slate-300">842,000 recs</td>
                    <td className="p-2.5 text-emerald-400 font-medium">COMPLETED</td>
                  </tr>
                  <tr>
                    <td className="p-2.5 font-semibold text-white">PIPE-STREAM-AI-LOGS</td>
                    <td className="p-2.5 text-slate-300">Kafka Event Fabric</td>
                    <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-purple-950 text-purple-400 border border-purple-800">STREAMING</span></td>
                    <td className="p-2.5 text-slate-300">2,840,100 msg</td>
                    <td className="p-2.5 text-emerald-400 font-medium">RUNNING</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">FinOps & Data Cost Optimization</h2>
            <div className="space-y-3 text-xs">
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                <div className="font-semibold text-slate-200">Partition Gold Sales 360 Dataset</div>
                <div className="text-slate-400 mt-1">Reduces query scan volume by 64%</div>
                <div className="text-emerald-400 font-medium mt-1">Est. Savings: $420 / mo</div>
              </div>
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                <div className="font-semibold text-slate-200">Materialize Monthly Executive View</div>
                <div className="text-slate-400 mt-1">Eliminates complex join aggregations</div>
                <div className="text-emerald-400 font-medium mt-1">Est. Savings: $310 / mo</div>
              </div>
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                <div className="font-semibold text-slate-200">Tier Cold Logs to Glacier</div>
                <div className="text-slate-400 mt-1">Moves 14TB logs to cold storage</div>
                <div className="text-emerald-400 font-medium mt-1">Est. Savings: $280 / mo</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Catalog & Marketplace */}
      {activeTab === 'catalog' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[
            {
              code: 'DP-CUSTOMER-360',
              name: 'Customer 360 Unified Intelligence Product',
              domain: 'CUSTOMER',
              owner: 'Customer Intelligence Team',
              desc: 'Unified 360-degree view of enterprise customers including behavioral, financial, support, and churn features.',
              rating: '4.9 ⭐',
              subscribers: 142
            },
            {
              code: 'DP-SALES-PERFORMANCE',
              name: 'Sales & Revenue Performance Product',
              domain: 'SALES',
              owner: 'Revenue Operations',
              desc: 'Governed sales metrics, pipeline velocity, deal attribution, and quarterly margin analytics.',
              rating: '4.8 ⭐',
              subscribers: 98
            },
            {
              code: 'DP-AI-AGENT-RUNS',
              name: 'Enterprise AI & Agentic Intelligence Product',
              domain: 'AI_OPS',
              owner: 'AI Engineering',
              desc: 'Phase 76 Agent runs, tool execution traces, token consumption, latency, and cost telemetry.',
              rating: '5.0 ⭐',
              subscribers: 210
            },
            {
              code: 'DP-PROCESS-MINING-MART',
              name: 'Process Intelligence & Conformance Mart',
              domain: 'PROCESS',
              owner: 'Process Excellence Lead',
              desc: 'Phase 78 Petri-net event logs, process bottlenecks, SLA breaches, and workflow waste metrics.',
              rating: '4.7 ⭐',
              subscribers: 64
            }
          ].map((prod) => (
            <div key={prod.code} className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-3">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
                    {prod.domain}
                  </span>
                  <h3 className="text-base font-bold text-white mt-1">{prod.name}</h3>
                </div>
                <span className="text-xs text-amber-400 font-semibold">{prod.rating}</span>
              </div>
              <p className="text-xs text-slate-400">{prod.desc}</p>
              <div className="flex justify-between items-center text-xs text-slate-400 pt-2 border-t border-slate-800">
                <span>Owner: {prod.owner}</span>
                <span>{prod.subscribers} Subscribers</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab 3: Governed Metrics Layer */}
      {activeTab === 'metrics' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-lg font-semibold text-white">Single Source of Truth Enterprise KPIs</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-800/50 text-slate-400 uppercase">
                <tr>
                  <th className="p-3">Metric Code</th>
                  <th className="p-3">Metric Name</th>
                  <th className="p-3">Definition & Formula</th>
                  <th className="p-3">Owner</th>
                  <th className="p-3">Current Value</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                <tr>
                  <td className="p-3 font-semibold text-cyan-400">MTR-FIN-REV</td>
                  <td className="p-3 font-medium text-white">Enterprise Net Revenue</td>
                  <td className="p-3 text-slate-300">
                    <div className="font-sans">Total recognized revenue minus discounts and refunds.</div>
                    <code className="text-[11px] text-cyan-300">SUM(gross_amount - discounts - refunds)</code>
                  </td>
                  <td className="p-3 text-slate-400">CFO</td>
                  <td className="p-3 font-bold text-emerald-400">$42,850,000</td>
                  <td className="p-3"><span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">APPROVED</span></td>
                </tr>
                <tr>
                  <td className="p-3 font-semibold text-cyan-400">MTR-CUST-CHURN</td>
                  <td className="p-3 font-medium text-white">Net Customer Churn Rate</td>
                  <td className="p-3 text-slate-300">
                    <div>Trailing 30-day account cancellation rate.</div>
                    <code className="text-[11px] text-cyan-300">(canceled - reactivated) / active * 100</code>
                  </td>
                  <td className="p-3 text-slate-400">VP CS</td>
                  <td className="p-3 font-bold text-emerald-400">1.42%</td>
                  <td className="p-3"><span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">APPROVED</span></td>
                </tr>
                <tr>
                  <td className="p-3 font-semibold text-cyan-400">MTR-OPS-SLA</td>
                  <td className="p-3 font-medium text-white">Process SLA Compliance Rate</td>
                  <td className="p-3 text-slate-300">
                    <div>Percentage of cases resolved strictly within SLA.</div>
                    <code className="text-[11px] text-cyan-300">resolved_in_sla / total_resolved * 100</code>
                  </td>
                  <td className="p-3 text-slate-400">VP Ops</td>
                  <td className="p-3 font-bold text-emerald-400">96.8%</td>
                  <td className="p-3"><span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">APPROVED</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 4: BI Dashboards */}
      {activeTab === 'dashboards' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { title: 'Executive C-Suite Intelligence', code: 'DASH-EXEC-SUMMARY', dept: 'EXECUTIVE', views: 980 },
            { title: 'Enterprise Data Command Center', code: 'DASH-COMMAND-CENTER', dept: 'DATA ARCHITECT', views: 1420 },
            { title: 'Autonomous AI Telemetry', code: 'DASH-AI-TELEMETRY', dept: 'ENGINEERING', views: 1650 }
          ].map((dash) => (
            <div key={dash.code} className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-3">
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-950 text-indigo-400 border border-indigo-800">
                {dash.dept}
              </span>
              <h3 className="text-base font-bold text-white">{dash.title}</h3>
              <p className="text-xs text-slate-400">Code: {dash.code}</p>
              <div className="flex justify-between items-center pt-3 border-t border-slate-800">
                <span className="text-xs text-slate-400">{dash.views} Views</span>
                <button className="px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-white rounded text-xs">
                  View Dashboard
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab 5: Text-to-SQL Workspace */}
      {activeTab === 'text-to-sql' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-5">
          <h2 className="text-lg font-semibold text-white">Governed Natural Language Text-to-SQL Engine</h2>
          <div className="flex gap-3">
            <input
              type="text"
              value={nlQuery}
              onChange={(e) => setNlQuery(e.target.value)}
              className="flex-1 px-4 py-2 bg-slate-950 border border-slate-700 rounded-lg text-sm text-white focus:outline-none"
              placeholder="Ask an analytical question..."
            />
            <button
              onClick={handleRunTextToSql}
              disabled={isLoadingQuery}
              className="px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-sm rounded-lg shadow-sm"
            >
              {isLoadingQuery ? 'Translating & Validating...' : 'Generate & Execute SQL'}
            </button>
          </div>

          {nlResult && (
            <div className="space-y-4 pt-4 border-t border-slate-800">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                  <div className="font-semibold text-slate-400">Generated Governed SQL</div>
                  <pre className="text-cyan-300 font-mono text-[11px] whitespace-pre-wrap">{nlResult.sql_query}</pre>
                </div>
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                  <div className="font-semibold text-slate-400">Query Explanation & Governance Safety</div>
                  <p className="text-slate-300">{nlResult.explanation}</p>
                  <div className="text-emerald-400 font-medium pt-2">
                    ✓ AST Syntax Passed | Read-Only Enforced | Est. Cost: ${nlResult.cost_estimation.estimated_cost_usd}
                  </div>
                </div>
              </div>

              {/* Data Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-800/50 text-slate-400 uppercase">
                    <tr>
                      <th className="p-2.5">Month</th>
                      <th className="p-2.5">Region</th>
                      <th className="p-2.5">Revenue</th>
                      <th className="p-2.5">YoY Growth</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {nlResult.rows.map((row: any, idx: number) => (
                      <tr key={idx}>
                        <td className="p-2.5 font-medium text-white">{row.month}</td>
                        <td className="p-2.5 text-slate-300">{row.region}</td>
                        <td className="p-2.5 font-bold text-cyan-400">{row.revenue}</td>
                        <td className="p-2.5 text-emerald-400">{row.growth}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 6: AI Analytics & Forecasts */}
      {activeTab === 'insights' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Revenue Forecast (30-Day Horizon)</h2>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg text-xs space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">Model: ENSEMBLE_PROPHET_ARIMA</span>
                <span className="text-emerald-400 font-medium">Accuracy MAPE: 1.9%</span>
              </div>
              <div className="text-slate-200">
                Projected Day 30 Revenue: <strong className="text-cyan-400">$45,420,000</strong>
              </div>
              <div className="text-slate-400 text-[11px]">
                95% Prediction Interval: [$44,120,000 — $46,720,000]
              </div>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-lg font-semibold text-white">Active Anomalies & Root Cause Analysis</h2>
            <div className="p-4 bg-amber-950/40 border border-amber-800/60 rounded-lg text-xs space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-bold text-amber-300">ANOM-2026-081: EMEA SLA Breach Warning</span>
                <span className="px-2 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800 text-[10px]">HIGH</span>
              </div>
              <p className="text-slate-300">
                Process SLA Compliance dropped to 92.1% (expected 98.5%).
              </p>
              <div className="text-slate-400 text-[11px] pt-1">
                Root Cause: Manager approval gate queue stall in EMEA Order-to-Cash.
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
