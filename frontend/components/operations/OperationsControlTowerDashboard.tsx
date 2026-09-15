'use client';

import React, { useState } from 'react';
import {
  Globe,
  Building2,
  TrendingUp,
  Truck,
  Package,
  Boxes,
  Users,
  Cpu,
  AlertTriangle,
  CheckCircle2,
  Play,
  RotateCcw,
  Zap,
  Clock,
  Layers,
  BarChart3,
  Search,
  ChevronRight,
  ShieldCheck,
  Compass,
  FileCheck
} from 'lucide-react';

export default function OperationsControlTowerDashboard() {
  const [activeTab, setActiveTab] = useState<
    'control-tower' | 'demand' | 'procurement' | 'inventory' | 'logistics' | 'workforce' | 'digital-twin' | 'exceptions'
  >('control-tower');

  // Closed-loop 10-stage Operations Orchestration Simulator
  const [cycleRunning, setCycleRunning] = useState(false);
  const [cycleStep, setCycleStep] = useState(0);
  const [cycleCompleted, setCycleCompleted] = useState(false);

  // 3-Way Match interactive tool
  const [matchingStatus, setMatchingStatus] = useState<'IDLE' | 'VERIFYING' | 'MATCHED'>('IDLE');

  // What-If Simulation State
  const [simRunning, setSimRunning] = useState(false);
  const [simResult, setSimResult] = useState<any>(null);

  const stages = [
    'Observe', 'Forecast', 'Plan', 'Optimize', 'Simulate',
    'Recommend', 'Approve', 'Execute', 'Verify', 'Learn'
  ];

  const runOperatingCycle = () => {
    setCycleRunning(true);
    setCycleStep(0);
    setCycleCompleted(false);

    let step = 0;
    const interval = setInterval(() => {
      step++;
      setCycleStep(step);
      if (step >= stages.length) {
        clearInterval(interval);
        setCycleRunning(false);
        setCycleCompleted(true);
      }
    }, 400);
  };

  const executeThreeWayMatch = () => {
    setMatchingStatus('VERIFYING');
    setTimeout(() => {
      setMatchingStatus('MATCHED');
    }, 800);
  };

  const runWhatIfSimulation = () => {
    setSimRunning(true);
    setTimeout(() => {
      setSimResult({
        code: 'SIM-2026-SHOCK-48',
        scenario: 'Tier-1 Semiconductor Foundry Outage (14 Days)',
        estimated_revenue_at_risk: '$185,000',
        working_capital_impact: '$42,000',
        mitigation: 'Automated transfer order dispatched to alternate European depot; safety buffer adequate for 21 days.',
        resilience_score: '94.2%'
      });
      setSimRunning(false);
    }, 900);
  };

  return (
    <div className="space-y-6 p-6">
      {/* Top Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between border-b border-border pb-5">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/10 rounded-lg text-blue-500">
              <Globe className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">Global Operations & Resource Control Tower</h1>
              <p className="text-sm text-muted-foreground">
                Autonomous Supply Network Intelligence, Multimodal Logistics, Workforce Scheduling & Digital Twin Orchestration
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={runOperatingCycle}
            disabled={cycleRunning}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground font-medium rounded-lg text-sm hover:opacity-90 transition disabled:opacity-50"
          >
            {cycleRunning ? <RotateCcw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
            Run 10-Stage Operations Cycle
          </button>
        </div>
      </div>

      {/* 10-Stage Cycle Progress Indicator */}
      {(cycleRunning || cycleCompleted) && (
        <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="font-semibold text-primary">Autonomous Operations Loop (Stage {cycleStep} of {stages.length})</span>
            <span className="text-xs text-muted-foreground">{cycleCompleted ? 'Cycle Complete — Continuous Feedback Integrated' : 'Synchronizing Multi-Tier Global Network...'}</span>
          </div>
          <div className="grid grid-cols-5 md:grid-cols-10 gap-2">
            {stages.map((stage, idx) => (
              <div
                key={stage}
                className={`text-center p-2 rounded-lg border text-xs transition-all ${
                  idx < cycleStep
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-600 font-medium'
                    : idx === cycleStep
                    ? 'bg-blue-500/10 border-blue-500 text-blue-600 font-bold scale-105 shadow-sm'
                    : 'bg-muted/40 border-border text-muted-foreground'
                }`}
              >
                {stage}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Top 4 KPI Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card border border-border rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Operational Health</span>
            <Globe className="h-4 w-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-foreground">95.8%</div>
          <div className="text-xs text-emerald-600 mt-1 flex items-center gap-1">
            <TrendingUp className="h-3 w-3" /> +1.4% network resilience
          </div>
        </div>

        <div className="bg-card border border-border rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">On-Time In-Full (OTIF)</span>
            <Truck className="h-4 w-4 text-blue-500" />
          </div>
          <div className="text-2xl font-bold text-foreground">98.4%</div>
          <div className="text-xs text-muted-foreground mt-1">48 shipments tracked live</div>
        </div>

        <div className="bg-card border border-border rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Warehouse Capacity</span>
            <Boxes className="h-4 w-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-foreground">74.2%</div>
          <div className="text-xs text-muted-foreground mt-1">Across 14 global fulfillment nodes</div>
        </div>

        <div className="bg-card border border-border rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Workforce Utilization</span>
            <Users className="h-4 w-4 text-purple-500" />
          </div>
          <div className="text-2xl font-bold text-foreground">86.8%</div>
          <div className="text-xs text-emerald-600 mt-1">Fairness balance score: 0.97</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-border overflow-x-auto pb-2 text-sm font-medium">
        {[
          { id: 'control-tower', label: 'Global Control Tower' },
          { id: 'demand', label: 'Demand & Forecasting' },
          { id: 'procurement', label: 'Procurement & Sourcing' },
          { id: 'inventory', label: 'Inventory & WMS' },
          { id: 'logistics', label: 'Multimodal Logistics' },
          { id: 'workforce', label: 'Workforce Capacity' },
          { id: 'digital-twin', label: 'Supply Digital Twin' },
          { id: 'exceptions', label: 'Exceptions & Risk' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-3 py-1.5 rounded-lg whitespace-nowrap transition ${
              activeTab === tab.id
                ? 'bg-primary text-primary-foreground font-semibold'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Panels */}
      {activeTab === 'control-tower' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
            <h3 className="text-base font-semibold flex items-center gap-2">
              <Compass className="h-4 w-4 text-blue-500" />
              Global Operating Facility Network & Status
            </h3>
            <div className="space-y-3">
              {[
                { name: 'Chicago North Hub (US)', type: 'Distribution Center', cap: '76%', otif: '99.1%', status: 'Optimal' },
                { name: 'Frankfurt Gateway (DE)', type: 'Warehouse & Assembly', cap: '82%', otif: '97.8%', status: 'Optimal' },
                { name: 'Singapore Logistics Hub (SG)', type: 'Multimodal Transit Node', cap: '68%', otif: '98.4%', status: 'Optimal' },
                { name: 'Rotterdam Port Terminal (NL)', type: 'Customs & Freight Hub', cap: '91%', otif: '94.2%', status: 'Port Backlog Alert' }
              ].map((loc) => (
                <div key={loc.name} className="flex items-center justify-between p-3 rounded-lg border border-border bg-muted/20">
                  <div>
                    <div className="text-sm font-semibold">{loc.name}</div>
                    <div className="text-xs text-muted-foreground">{loc.type} • Occupancy: {loc.cap}</div>
                  </div>
                  <div className="text-right">
                    <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${loc.status.includes('Alert') ? 'bg-amber-500/10 text-amber-600 border border-amber-500/30' : 'bg-emerald-500/10 text-emerald-600 border border-emerald-500/30'}`}>
                      {loc.status}
                    </span>
                    <div className="text-xs text-muted-foreground mt-1">OTIF: {loc.otif}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
            <h3 className="text-base font-semibold flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-emerald-500" />
              Human-in-the-Loop Governance Gates
            </h3>
            <p className="text-xs text-muted-foreground">
              Autonomous operations cannot sign strategic supply contracts or execute major inventory write-offs without explicit executive authorization.
            </p>
            <div className="p-3 rounded-lg border border-border bg-muted/20 space-y-2 text-xs">
              <div className="font-semibold text-foreground">Pending Procurement Award</div>
              <div className="text-muted-foreground">PO-2026-Q3-MICRO: $480,000 for 12,000 Microcontroller Units</div>
              <div className="flex gap-2 pt-2">
                <button className="flex-1 py-1 bg-primary text-primary-foreground rounded text-xs font-medium">Authorise Award</button>
                <button className="flex-1 py-1 bg-muted border border-border rounded text-xs font-medium">Request RFQ</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'procurement' && (
        <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="text-base font-semibold flex items-center gap-2">
            <FileCheck className="h-4 w-4 text-blue-500" />
            Automated Three-Way Matching Engine
          </h3>
          <p className="text-xs text-muted-foreground">
            Synchronizes Purchase Orders, Goods Receipt verification scans, and Supplier Invoices to prevent overbilling.
          </p>
          <div className="p-4 rounded-lg border border-border bg-muted/20 space-y-3 text-xs">
            <div className="grid grid-cols-3 gap-2 text-center">
              <div className="p-2 bg-background rounded border">
                <span className="text-muted-foreground block">Purchase Order</span>
                <span className="font-bold">PO-2026-9812</span>
                <span className="block text-emerald-600 font-semibold">$12,500.00</span>
              </div>
              <div className="p-2 bg-background rounded border">
                <span className="text-muted-foreground block">Goods Receipt</span>
                <span className="font-bold">GR-2026-4401</span>
                <span className="block text-emerald-600 font-semibold">500 Units Verified</span>
              </div>
              <div className="p-2 bg-background rounded border">
                <span className="text-muted-foreground block">Supplier Invoice</span>
                <span className="font-bold">INV-PRECISION-91</span>
                <span className="block text-emerald-600 font-semibold">$12,500.00</span>
              </div>
            </div>
            <button
              onClick={executeThreeWayMatch}
              className="w-full py-2 bg-primary text-primary-foreground rounded font-medium text-xs transition hover:opacity-90"
            >
              {matchingStatus === 'VERIFYING' ? 'Verifying Line-Item Math & Cryptographic Signatures...' : matchingStatus === 'MATCHED' ? 'Three-Way Match Verified — Ready for AP Payment' : 'Verify 3-Way Reconciliation'}
            </button>
          </div>
        </div>
      )}

      {activeTab === 'digital-twin' && (
        <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="text-base font-semibold flex items-center gap-2">
            <Cpu className="h-4 w-4 text-purple-500" />
            Supply Network Digital Twin & What-If Simulator
          </h3>
          <p className="text-xs text-muted-foreground">
            Evaluates network resilience, time-to-recover (TTR), and time-to-survive (TTS) under supply shocks.
          </p>
          <button
            onClick={runWhatIfSimulation}
            disabled={simRunning}
            className="px-4 py-2 bg-primary text-primary-foreground rounded text-xs font-medium hover:opacity-90 transition disabled:opacity-50"
          >
            {simRunning ? 'Simulating Supply Disruption Scenario...' : 'Simulate 14-Day Tier-1 Supplier Shock'}
          </button>
          {simResult && (
            <div className="p-4 rounded-lg border border-purple-500/30 bg-purple-500/5 space-y-2 text-xs">
              <div className="font-bold text-sm text-foreground">{simResult.scenario}</div>
              <div className="grid grid-cols-2 gap-2 text-muted-foreground">
                <div>Revenue at Risk: <span className="font-semibold text-foreground">{simResult.estimated_revenue_at_risk}</span></div>
                <div>Network Resilience: <span className="font-semibold text-emerald-600">{simResult.resilience_score}</span></div>
              </div>
              <div className="text-foreground pt-1"><span className="font-semibold">Mitigation Strategy:</span> {simResult.mitigation}</div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'exceptions' && (
        <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="text-base font-semibold flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 text-amber-500" />
            Centralized Operational Exceptions & Risk Queue
          </h3>
          <div className="space-y-3">
            {[
              { id: 'EXC-001', sev: 'HIGH', cat: 'LOGISTICS_CONGESTION', desc: 'Rotterdam Port Terminal customs inspection queue affecting 2 container shipments.', cost: '$12,500', action: 'Expedite priority clearance filing under AEO agreement.' },
              { id: 'EXC-002', sev: 'MEDIUM', cat: 'LABOR_CAPACITY', desc: 'Chicago North night shift short 4 high-reach forklift certified operators.', cost: '$4,200', action: 'Autonomous scheduling agent reassigned certified daytime floaters.' }
            ].map((exc) => (
              <div key={exc.id} className="p-3 rounded-lg border border-border bg-muted/20 space-y-1 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-foreground">{exc.id} • {exc.cat}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/10 text-amber-600 border border-amber-500/30">{exc.sev}</span>
                </div>
                <div className="text-muted-foreground">{exc.desc}</div>
                <div className="text-xs pt-1"><span className="font-medium text-foreground">Recommended Action:</span> {exc.action}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
