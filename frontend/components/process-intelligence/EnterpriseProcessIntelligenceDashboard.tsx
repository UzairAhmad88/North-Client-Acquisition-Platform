'use client';

import React, { useState } from 'react';

export default function EnterpriseProcessIntelligenceDashboard() {
  const [selectedProcess, setSelectedProcess] = useState('PRC-O2C');
  const [activeTab, setActiveTab] = useState<'mining' | 'conformance' | 'bottlenecks' | 'simulation' | 'automation'>('mining');

  const stats = [
    { label: 'Cataloged Processes', value: '148', change: 'Covering 8 domains', status: 'optimal' },
    { label: 'Active Process Cases', value: '1,240', change: '+85 today', status: 'optimal' },
    { label: 'Conformance Rate', value: '94.2%', change: 'Fitness 0.965', status: 'optimal' },
    { label: 'Active Bottlenecks', value: '4', change: 'Critical: Approval Gate', status: 'warning' },
    { label: 'Open SLA Breaches', value: '2', change: '4 predicted at risk', status: 'warning' },
    { label: 'Automation Opps', value: '18', change: '$485k annual savings', status: 'optimal' },
    { label: 'Annual Waste Identified', value: '$485,000', change: '240 hrs/mo waiting', status: 'optimal' },
    { label: 'Process AI Agents', value: '14 Active', change: 'L4/L5 Autonomy', status: 'optimal' },
  ];

  const variants = [
    { code: 'VAR-01 (Happy Path)', frequency: '72.4%', duration: '22.4 hrs', cost: '$120', compliance: '100%' },
    { code: 'VAR-02 (Credit Escalation)', frequency: '14.2%', duration: '64.8 hrs', cost: '$210', compliance: '94%' },
    { code: 'VAR-03 (Inventory Rework)', frequency: '8.1%', duration: '48.2 hrs', cost: '$185', compliance: '88%' },
    { code: 'VAR-04 (Manual Override)', frequency: '5.3%', duration: '34.0 hrs', cost: '$160', compliance: '76%' },
  ];

  const bottlenecks = [
    {
      activity: 'Manager Approval Gate',
      type: 'APPROVAL_STALL',
      wait: '38.4 hours',
      queue: '34 cases',
      cost: '$142,000 / yr',
      rootCause: 'Batch approval cadence: managers review queues once weekly',
      waste: 'WAITING',
      mitigation: 'Implement automated AI pre-validation with auto-approval for low-risk orders < $10k'
    },
    {
      activity: 'Invoice Discrepancy Matching',
      type: 'MANUAL_REWORK',
      wait: '18.2 hours',
      queue: '19 cases',
      cost: '$84,000 / yr',
      rootCause: 'PO unit price variance between ERP line items and scanned supplier PDFs',
      waste: 'REWORK',
      mitigation: 'Deploy AutomationAgent with automated 3-way OCR fuzzy matching'
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Enterprise Process Intelligence & Autonomous Optimization
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-950 text-indigo-400 border border-indigo-800">
              MINING ACTIVE
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Empirical process discovery, Petri-net conformance checking, bottleneck intelligence, and governed workflow optimization.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={selectedProcess}
            onChange={(e) => setSelectedProcess(e.target.value)}
            className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-slate-900 border border-slate-700 text-white focus:outline-none"
          >
            <option value="PRC-O2C">PRC-O2C: Order-to-Cash (Finance/Sales)</option>
            <option value="PRC-P2P">PRC-P2P: Procure-to-Pay (Operations)</option>
            <option value="PRC-R2R">PRC-R2R: Record-to-Report (Finance)</option>
            <option value="PRC-I2R">PRC-I2R: Incident-to-Resolution (IT/Sec)</option>
          </select>
          <button className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-indigo-600 hover:bg-indigo-500 text-white shadow-sm">
            Run Process Discovery
          </button>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s, idx) => (
          <div key={idx} className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="text-xs font-medium text-slate-400">{s.label}</div>
            <div className="text-2xl font-bold text-white mt-1">{s.value}</div>
            <div className={`text-xs mt-1 ${s.status === 'optimal' ? 'text-emerald-400' : 'text-amber-400'}`}>
              {s.change}
            </div>
          </div>
        ))}
      </div>

      {/* Main Tabs */}
      <div className="flex gap-2 border-b border-slate-800 text-sm">
        {[
          { key: 'mining', label: 'Process Mining & DFG Flow' },
          { key: 'conformance', label: 'Conformance & Deviations' },
          { key: 'bottlenecks', label: 'Bottlenecks & Lean Waste' },
          { key: 'simulation', label: 'Discrete-Event Simulation' },
          { key: 'automation', label: 'Automation Opportunities & ROI' }
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as any)}
            className={`pb-2.5 px-3 font-medium transition border-b-2 ${
              activeTab === tab.key
                ? 'border-indigo-500 text-white'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'mining' && (
        <div className="space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center space-y-3">
            <div className="flex justify-between items-center text-xs text-slate-400 mb-2">
              <span>Directly-Follows Graph (DFG) • Fitness: 0.965 • Precision: 0.932</span>
              <span className="text-emerald-400">1,240 cases analyzed (30 days)</span>
            </div>
            <div className="h-64 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-center text-slate-500 font-mono text-xs">
              [DISCOVERED WORKFLOW CANVAS: Order Placed (100%) → Credit Check (85%) → Inventory Allocation → Manager Approval (15% delay) → Fulfillment Dispatch → Invoice & Payment]
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-white">Execution Path Variants</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
              {variants.map((v, idx) => (
                <div key={idx} className="bg-slate-950 border border-slate-800 rounded-lg p-3 space-y-1.5">
                  <div className="font-semibold text-indigo-300">{v.code}</div>
                  <div className="text-slate-400">Frequency: <span className="text-white font-bold">{v.frequency}</span></div>
                  <div className="text-slate-400">Avg Duration: <span className="text-white">{v.duration}</span></div>
                  <div className="text-slate-400">Compliance: <span className="text-emerald-400">{v.compliance}</span></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'conformance' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-lg font-bold text-white">Conformance Checking & Policy Compliance</h2>
              <p className="text-xs text-slate-400">Comparing observed execution against approved BPMN baseline</p>
            </div>
            <span className="px-3 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 text-xs font-semibold rounded-lg">
              93.8% CONFORMING
            </span>
          </div>

          <div className="space-y-3 pt-2">
            <div className="bg-slate-950 border border-amber-900/50 rounded-lg p-4 text-xs space-y-2">
              <div className="flex justify-between font-semibold text-amber-300">
                <span>SKIPPED_APPROVAL: Manager Approval bypassed on 12 cases</span>
                <span>CRITICAL SEVERITY</span>
              </div>
              <p className="text-slate-400">
                12 transactions exceeding $25,000 were fulfilled without tier-2 managerial signoff. Root cause: automated timeout override triggered during holiday weekend.
              </p>
            </div>

            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 text-xs space-y-2">
              <div className="flex justify-between font-semibold text-slate-300">
                <span>OUT_OF_SEQUENCE: Credit Check performed after Inventory Allocation</span>
                <span>MEDIUM SEVERITY</span>
              </div>
              <p className="text-slate-400">
                24 occurrences where inventory holds were placed prior to credit authorization, locking warehouse stock unnecessarily.
              </p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'bottlenecks' && (
        <div className="space-y-4">
          {bottlenecks.map((b, idx) => (
            <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-bold text-white">{b.activity}</h3>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-red-950 text-red-400 border border-red-800">
                    {b.type}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-amber-950 text-amber-300 border border-amber-800">
                    WASTE: {b.waste}
                  </span>
                </div>
                <span className="text-sm font-bold text-amber-400">{b.cost}</span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 bg-slate-950 p-3 rounded-lg text-xs text-slate-400">
                <div>Average Wait: <span className="text-white font-semibold">{b.wait}</span></div>
                <div>Queue Depth: <span className="text-white font-semibold">{b.queue}</span></div>
                <div className="col-span-2">Root Cause: <span className="text-slate-300">{b.rootCause}</span></div>
              </div>

              <div className="text-xs text-indigo-300 bg-indigo-950/40 border border-indigo-900/50 p-3 rounded-lg">
                <strong>Recommended Mitigation:</strong> {b.mitigation}
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'simulation' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-lg font-bold text-white">Discrete-Event What-If Simulation</h2>
              <p className="text-xs text-slate-400">Scenario: Remove Manager Approval for Low-Risk Orders (&lt; $10k)</p>
            </div>
            <button className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-indigo-600 text-white">
              Run New Simulation
            </button>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2 text-center">
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <div className="text-xs text-slate-400">Cycle Time Delta</div>
              <div className="text-2xl font-bold text-emerald-400 mt-1">-32.5%</div>
              <div className="text-[11px] text-slate-500 mt-1">Saves 32.0 hrs / case</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <div className="text-xs text-slate-400">Cost Delta</div>
              <div className="text-2xl font-bold text-emerald-400 mt-1">-21.0%</div>
              <div className="text-[11px] text-slate-500 mt-1">Labor & delay savings</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <div className="text-xs text-slate-400">Throughput Capacity</div>
              <div className="text-2xl font-bold text-indigo-400 mt-1">+26.4%</div>
              <div className="text-[11px] text-slate-500 mt-1">5,000 cases tested</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <div className="text-xs text-slate-400">SLA Compliance</div>
              <div className="text-2xl font-bold text-emerald-400 mt-1">+5.2%</div>
              <div className="text-[11px] text-slate-500 mt-1">99.7% target met</div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'automation' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-lg font-bold text-white">Automation Opportunity Prioritization Matrix</h2>
              <p className="text-xs text-slate-400">Ranked by volume, feasibility, and ROI payback window</p>
            </div>
            <span className="text-xs font-bold text-emerald-400">$185k Combined Annual Savings</span>
          </div>

          <div className="space-y-3 pt-2">
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-white text-sm">Standard Invoice Three-Way Matching</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-950 text-indigo-400 border border-indigo-800">
                    AI_AGENT
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-1">Feasibility: 94% • Risk: Low • Automated OCR & Line Item Reconciliation</p>
              </div>
              <div className="text-right">
                <div className="text-base font-bold text-emerald-400">$120,000 / yr savings</div>
                <div className="text-xs text-slate-500">Payback: 1.8 months</div>
              </div>
            </div>

            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-white text-sm">Customer Credit Verification Call</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-950 text-emerald-400 border border-emerald-800">
                    API_AUTOMATION
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-1">Feasibility: 89% • Risk: Low • Direct Dun & Bradstreet API Integration</p>
              </div>
              <div className="text-right">
                <div className="text-base font-bold text-emerald-400">$65,000 / yr savings</div>
                <div className="text-xs text-slate-500">Payback: 2.2 months</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
