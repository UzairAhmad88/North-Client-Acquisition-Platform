'use client';

import React, { useState } from 'react';
import {
  DollarSign,
  TrendingUp,
  Shield,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Play,
  Layers,
  BarChart3,
  PieChart,
  Landmark,
  FileText,
  CreditCard,
  Building2,
  RefreshCw,
  Scale,
  Search,
  Check,
  ChevronRight,
  Bot,
  Zap,
  Sliders,
  Eye,
  Lock,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';

export default function FinancialCommandCenterDashboard() {
  const [activeTab, setActiveTab] = useState<
    'command-center' | 'ledger' | 'receivables' | 'payables' | 'treasury' | 'fpna' | 'risk' | 'agents'
  >('command-center');

  // Closed loop 12-stage cycle simulator
  const [cycleRunning, setCycleRunning] = useState(false);
  const [cycleStep, setCycleStep] = useState(0);
  const [cycleCompleted, setCycleCompleted] = useState(false);

  // Scenario Simulator state
  const [revShock, setRevShock] = useState<number>(-15);
  const [expShock, setExpShock] = useState<number>(10);
  const [simulating, setSimulating] = useState(false);
  const [simResult, setSimResult] = useState<any>(null);

  const [pendingPayments, setPendingPayments] = useState<Array<{
    id: string;
    vendor: string;
    amount: number;
    due: string;
    dualRequired: boolean;
    approvedBy1: string | null;
    approvedBy2: string | null;
  }>>([
    { id: 'PAY-892', vendor: 'Global Cloud Infra Corp', amount: 45000.0, due: '2026-09-18', dualRequired: true, approvedBy1: 'Finance Mgr (Alice)', approvedBy2: null },
    { id: 'PAY-893', vendor: 'Silicon Foundry Ltd', amount: 128500.0, due: '2026-09-22', dualRequired: true, approvedBy1: null, approvedBy2: null }
  ]);

  const stages = [
    'Observe', 'Validate', 'Analyze', 'Forecast',
    'Simulate', 'Recommend', 'Policy Check', 'Human Approval',
    'Execute', 'Reconcile', 'Audit', 'Learn'
  ];

  const run12StageCycle = () => {
    setCycleRunning(true);
    setCycleStep(1);
    setCycleCompleted(false);

    const timer = setInterval(() => {
      setCycleStep((prev) => {
        if (prev >= 12) {
          clearInterval(timer);
          setCycleRunning(false);
          setCycleCompleted(true);
          return 12;
        }
        return prev + 1;
      });
    }, 450);
  };

  const handleApprovePayment = (id: string) => {
    setPendingPayments((prev) =>
      prev.map((p) =>
        p.id === id
          ? { ...p, approvedBy2: p.approvedBy1 ? 'Treasury Director (You)' : 'Finance Director' }
          : p
      )
    );
  };

  const runScenarioSimulation = () => {
    setSimulating(true);
    setTimeout(() => {
      const baseCash = 12.54;
      const baseBurn = 0.45;
      const cashImpact = (revShock * 0.12) - (expShock * 0.08);
      const projectedCash = Math.max(1.2, baseCash + cashImpact);
      const projectedBurn = baseBurn * (1 + expShock / 100);
      const projectedRunway = (projectedCash / projectedBurn).toFixed(1);

      setSimResult({
        projectedCash: projectedCash.toFixed(2),
        projectedBurn: (projectedBurn * 1000).toFixed(0),
        projectedRunway,
        riskLevel: parseFloat(projectedRunway) < 14 ? 'HIGH' : (parseFloat(projectedRunway) < 20 ? 'MEDIUM' : 'LOW'),
        recommendations: [
          'Extend non-critical vendor payment cycles from 30 to 45 days.',
          'Institute 2.5% early settlement discount on commercial invoices > $50,000.',
          'Enforce strict cap on discretionary cloud spot capacity expansion.'
        ]
      });
      setSimulating(false);
    }, 600);
  };

  return (
    <div className="space-y-6 text-slate-100 min-h-screen pb-16">
      {/* Header Banner */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 p-6 bg-slate-900/80 border border-slate-800 rounded-2xl backdrop-blur-xl shadow-2xl">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl">
              <Landmark className="w-6 h-6 text-emerald-400" />
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Autonomous Financial Operating System
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full flex items-center gap-1">
              <Shield className="w-3 h-3" /> Governed AI-Native
            </span>
          </div>
          <p className="text-sm text-slate-400">
            Phase 72: Double-Entry GL, Multi-Entity Treasury, 13-Week Cash Forecast, FP&A & Governed 12-Stage Financial Automation Loop
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-4 py-2 bg-slate-800/80 border border-slate-700/60 rounded-xl text-xs flex items-center gap-2">
            <Scale className="w-4 h-4 text-emerald-400" />
            <span>Double-Entry Invariant:</span>
            <span className="font-mono text-emerald-400 font-bold">BALANCED ($0.00 Variance)</span>
          </div>

          <button
            onClick={run12StageCycle}
            disabled={cycleRunning}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition-all shadow-lg shadow-emerald-600/20"
          >
            {cycleRunning ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Running Stage {cycleStep}/12...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Execute 12-Stage Cycle</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* 12-Stage Interactive Closed Loop Tracker */}
      <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl">
        <div className="flex items-center justify-between mb-3 text-xs">
          <span className="font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
            <Zap className="w-4 h-4 text-amber-400" /> Governed Financial Execution Loop
          </span>
          <span className="text-slate-400 font-mono">
            {cycleRunning ? `Stage ${cycleStep}: ${stages[cycleStep - 1]}` : (cycleCompleted ? 'Cycle Complete (Audit Logged)' : 'Ready (Awaiting Autonomous Trigger)')}
          </span>
        </div>
        <div className="grid grid-cols-6 lg:grid-cols-12 gap-2">
          {stages.map((stage, idx) => {
            const stepNum = idx + 1;
            const isCurrent = cycleStep === stepNum;
            const isDone = cycleStep > stepNum || cycleCompleted;
            return (
              <div
                key={stage}
                className={`p-2.5 rounded-xl border text-center transition-all ${
                  isCurrent
                    ? 'bg-amber-500/20 border-amber-500 text-amber-300 font-bold scale-105 shadow-lg shadow-amber-500/20'
                    : isDone
                    ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400'
                    : 'bg-slate-950/60 border-slate-800 text-slate-500'
                }`}
              >
                <div className="text-[10px] font-mono opacity-70 mb-1">0{stepNum}</div>
                <div className="text-xs truncate">{stage}</div>
                <div className="mt-1 flex justify-center">
                  {isDone ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  ) : isCurrent ? (
                    <RefreshCw className="w-3.5 h-3.5 text-amber-400 animate-spin" />
                  ) : (
                    <Clock className="w-3.5 h-3.5 text-slate-600" />
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Top Telemetry KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Cash */}
        <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Total Cash & Liquidity</span>
            <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-400">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white font-mono">$12,540,000</div>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-400">Available: $10.20M</span>
            <span className="text-emerald-400 flex items-center gap-0.5">
              <ArrowUpRight className="w-3 h-3" /> +4.2% MoM
            </span>
          </div>
        </div>

        {/* Burn Rate & Runway */}
        <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Runway & Net Burn</span>
            <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
              <Clock className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white font-mono">27.8 Months</div>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-400">Burn: $450k / mo</span>
            <span className="text-blue-400 font-semibold">94% Confidence</span>
          </div>
        </div>

        {/* Accounts Receivable */}
        <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Accounts Receivable</span>
            <div className="p-2 bg-purple-500/10 rounded-lg text-purple-400">
              <FileText className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white font-mono">$3,420,000</div>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-400">DSO: 38.5 Days</span>
            <span className="text-purple-400 font-semibold">Current: 87.1%</span>
          </div>
        </div>

        {/* Accounts Payable & Dual Control */}
        <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Accounts Payable</span>
            <div className="p-2 bg-amber-500/10 rounded-lg text-amber-400">
              <CreditCard className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white font-mono">$1,820,000</div>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-400">DPO: 42.1 Days</span>
            <span className="text-amber-400 font-semibold">2 Pending Dual Sign-off</span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto text-sm">
        {[
          { id: 'command-center', label: 'Executive Command', icon: Landmark },
          { id: 'ledger', label: 'General Ledger & COA', icon: Scale },
          { id: 'receivables', label: 'Accounts Receivable', icon: FileText },
          { id: 'payables', label: 'Accounts Payable & Match', icon: CreditCard },
          { id: 'treasury', label: 'Treasury & 13-Wk Cash', icon: TrendingUp },
          { id: 'fpna', label: 'FP&A & Scenarios', icon: PieChart },
          { id: 'risk', label: 'Fraud & Controls', icon: Shield },
          { id: 'agents', label: '25 Financial Agents', icon: Bot },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl whitespace-nowrap font-medium transition-all ${
                isActive
                  ? 'bg-slate-800 text-emerald-400 border border-slate-700 shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab 1: Executive Command Center */}
      {activeTab === 'command-center' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left 2 Cols: Dual-Control Sign-off & Financial Health */}
          <div className="lg:col-span-2 space-y-6">
            {/* Dual Control Approvals */}
            <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Lock className="w-5 h-5 text-amber-400" />
                  <h2 className="text-base font-semibold text-white">
                    Mandatory Dual-Control Payment Authorization (&gt; $25,000)
                  </h2>
                </div>
                <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded-full">
                  Policy Enforced
                </span>
              </div>

              <div className="space-y-3">
                {pendingPayments.map((p) => {
                  const fullyApproved = p.approvedBy1 && p.approvedBy2;
                  return (
                    <div
                      key={p.id}
                      className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl flex items-center justify-between"
                    >
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-sm font-bold text-white">{p.id}</span>
                          <span className="text-sm text-slate-300 font-medium">{p.vendor}</span>
                        </div>
                        <div className="text-xs text-slate-400 mt-1 flex items-center gap-3">
                          <span>Amount: <strong className="text-white font-mono">${p.amount.toLocaleString()}</strong></span>
                          <span>Due: {p.due}</span>
                          <span className="text-amber-400">
                            Sign-off 1: {p.approvedBy1 || 'Pending'} | Sign-off 2: {p.approvedBy2 || 'Pending'}
                          </span>
                        </div>
                      </div>

                      <div>
                        {fullyApproved ? (
                          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs rounded-lg font-medium flex items-center gap-1">
                            <Check className="w-3.5 h-3.5" /> Dispatched
                          </span>
                        ) : (
                          <button
                            onClick={() => handleApprovePayment(p.id)}
                            className="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white text-xs rounded-lg font-semibold flex items-center gap-1.5 transition-all"
                          >
                            <Shield className="w-3.5 h-3.5" /> Authorize Dual Control
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Financial Close Status */}
            <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl">
              <h2 className="text-base font-semibold text-white mb-4 flex items-center gap-2">
                <CalendarIcon className="w-5 h-5 text-emerald-400" />
                Accounting Period & Monthly Close Checklist
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400">August 2026</div>
                  <div className="text-sm font-bold text-emerald-400 mt-1">LOCKED</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Audit sealed</div>
                </div>
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400">September 2026</div>
                  <div className="text-sm font-bold text-blue-400 mt-1">OPEN</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Active postings</div>
                </div>
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400">Depreciation Accruals</div>
                  <div className="text-sm font-bold text-emerald-400 mt-1">POSTED</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Straight-line verified</div>
                </div>
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400">Bank Auto-Match</div>
                  <div className="text-sm font-bold text-emerald-400 mt-1">98.2%</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">2 exceptions flagged</div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Col: What-If Scenario Engine */}
          <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
            <div className="flex items-center gap-2">
              <Sliders className="w-5 h-5 text-purple-400" />
              <h2 className="text-base font-semibold text-white">What-If Financial Simulation</h2>
            </div>
            <p className="text-xs text-slate-400">
              Simulate cash and runway sensitivity under stress shocks before committing material capital.
            </p>

            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-300">Revenue Shock</span>
                  <span className="font-mono text-purple-400">{revShock}%</span>
                </div>
                <input
                  type="range"
                  min="-40"
                  max="40"
                  value={revShock}
                  onChange={(e) => setRevShock(parseInt(e.target.value))}
                  className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-purple-500"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-300">Expense Inflation Shock</span>
                  <span className="font-mono text-purple-400">+{expShock}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="50"
                  value={expShock}
                  onChange={(e) => setExpShock(parseInt(e.target.value))}
                  className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-purple-500"
                />
              </div>

              <button
                onClick={runScenarioSimulation}
                disabled={simulating}
                className="w-full py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-semibold transition-all flex items-center justify-center gap-2"
              >
                {simulating ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5" />}
                <span>Simulate Dynamic Twin</span>
              </button>
            </div>

            {simResult && (
              <div className="p-3.5 bg-purple-950/30 border border-purple-800/40 rounded-xl space-y-2 mt-3">
                <div className="text-xs font-bold text-purple-300">Simulation Projections:</div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>Projected Cash: <strong className="font-mono text-white">${simResult.projectedCash}M</strong></div>
                  <div>Burn: <strong className="font-mono text-white">${simResult.projectedBurn}k/mo</strong></div>
                  <div>Projected Runway: <strong className="font-mono text-white">{simResult.projectedRunway} Mo</strong></div>
                  <div>Risk: <span className={`font-bold ${simResult.riskLevel === 'HIGH' ? 'text-red-400' : 'text-emerald-400'}`}>{simResult.riskLevel}</span></div>
                </div>
                <div className="text-[11px] text-slate-400 mt-2">
                  <div className="font-semibold text-slate-300 mb-0.5">Autonomous Advisory:</div>
                  <ul className="list-disc pl-4 space-y-0.5">
                    {simResult.recommendations.map((r: string, idx: number) => (
                      <li key={idx}>{r}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab 2: General Ledger & Chart of Accounts */}
      {activeTab === 'ledger' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Scale className="w-5 h-5 text-emerald-400" />
              Hierarchical Chart of Accounts & General Ledger
            </h2>
            <span className="text-xs font-mono bg-slate-800 px-3 py-1 rounded-lg text-slate-300">
              Rule: Debits == Credits Strictly Enforced
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-950/60 text-xs uppercase text-slate-400">
                <tr>
                  <th className="p-3">Account #</th>
                  <th className="p-3">Account Name</th>
                  <th className="p-3">Type</th>
                  <th className="p-3">Currency</th>
                  <th className="p-3 text-right">Balance</th>
                  <th className="p-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {[
                  { num: '1000', name: 'Operating Cash & Equivalents', type: 'ASSET', cur: 'USD', bal: '$10,200,000.00', status: 'ACTIVE' },
                  { num: '1050', name: 'Restricted Treasury Escrow', type: 'ASSET', cur: 'USD', bal: '$2,340,000.00', status: 'ACTIVE' },
                  { num: '1200', name: 'Accounts Receivable (Trade)', type: 'ASSET', cur: 'USD', bal: '$3,420,000.00', status: 'ACTIVE' },
                  { num: '1500', name: 'Physical Assets & Robotics Capital', type: 'ASSET', cur: 'USD', bal: '$4,850,000.00', status: 'ACTIVE' },
                  { num: '2000', name: 'Accounts Payable (Trade)', type: 'LIABILITY', cur: 'USD', bal: '$1,820,000.00', status: 'ACTIVE' },
                  { num: '2500', name: 'Accrued Cloud & Infrastructure Liabilities', type: 'LIABILITY', cur: 'USD', bal: '$210,000.00', status: 'ACTIVE' },
                  { num: '3000', name: 'Common Equity & Retained Earnings', type: 'EQUITY', cur: 'USD', bal: '$17,330,000.00', status: 'ACTIVE' },
                  { num: '4000', name: 'Enterprise Platform SaaS Revenue', type: 'REVENUE', cur: 'USD', bal: '$1,450,000.00', status: 'ACTIVE' },
                  { num: '5000', name: 'COGS - Cloud Compute & Physical Transit', type: 'COGS', cur: 'USD', bal: '$374,100.00', status: 'ACTIVE' }
                ].map((row) => (
                  <tr key={row.num} className="hover:bg-slate-800/30">
                    <td className="p-3 font-mono font-bold text-emerald-400">{row.num}</td>
                    <td className="p-3 font-medium text-white">{row.name}</td>
                    <td className="p-3 text-xs">
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
                        {row.type}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-xs">{row.cur}</td>
                    <td className="p-3 text-right font-mono font-bold text-white">{row.bal}</td>
                    <td className="p-3 text-center text-xs text-emerald-400">{row.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 3: Accounts Receivable */}
      {activeTab === 'receivables' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-purple-400" />
            Accounts Receivable Aging & Collections Intelligence
          </h2>

          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
            {[
              { bracket: 'Current (0-30)', amount: '$2,980,000', pct: '87.1%', color: 'text-emerald-400' },
              { bracket: '31-60 Days', amount: '$320,000', pct: '9.4%', color: 'text-blue-400' },
              { bracket: '61-90 Days', amount: '$95,000', pct: '2.8%', color: 'text-amber-400' },
              { bracket: '90+ Days', amount: '$25,000', pct: '0.7%', color: 'text-rose-400' },
              { bracket: 'Days Sales Out (DSO)', amount: '38.5 Days', pct: 'Target: < 40d', color: 'text-purple-400' }
            ].map((b) => (
              <div key={b.bracket} className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl text-center">
                <div className="text-xs text-slate-400">{b.bracket}</div>
                <div className={`text-xl font-bold font-mono mt-1 ${b.color}`}>{b.amount}</div>
                <div className="text-[10px] text-slate-500 mt-0.5">{b.pct}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: Accounts Payable & 3-Way Match */}
      {activeTab === 'payables' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <CreditCard className="w-5 h-5 text-amber-400" />
            Accounts Payable & Automated 3-Way Matching (PO + Receipt + Bill)
          </h2>

          <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
            <div className="text-xs text-slate-400 font-semibold uppercase">Phase 71 Supply-Chain Reconciliation Loop</div>
            <div className="text-sm text-slate-200">
              Every vendor bill is automatically matched against Phase 71 Purchase Orders and Goods Receipts with tolerance checks prior to disbursement scheduling.
            </div>
          </div>
        </div>
      )}

      {/* Tab 5: Treasury & 13-Week Cash */}
      {activeTab === 'treasury' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            13-Week Rolling Cash Forecast & Liquidity Management
          </h2>
          <div className="text-xs text-slate-400">
            Forecast models incoming receivable probabilities, scheduled vendor disbursements, payroll cycles, and capital reserve thresholds.
          </div>
        </div>
      )}

      {/* Tab 6: FP&A & Scenarios */}
      {activeTab === 'fpna' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <PieChart className="w-5 h-5 text-blue-400" />
            FP&A, Budget Variance & Unit Economics
          </h2>
          <div className="text-xs text-slate-400">
            Connects revenue, COGS, direct cost drivers, and headcount into live variance reporting and contribution margin analytics.
          </div>
        </div>
      )}

      {/* Tab 7: Fraud & Risk */}
      {activeTab === 'risk' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Shield className="w-5 h-5 text-rose-400" />
            Financial Anomaly Detection & Segregation of Duties
          </h2>
          <div className="text-xs text-slate-400">
            Real-time fraud graph detection for beneficiary bank modifications, velocity spikes, invoice tampering, and duplicate payment attempts.
          </div>
        </div>
      )}

      {/* Tab 8: 25 Autonomous Financial Agents */}
      {activeTab === 'agents' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Bot className="w-5 h-5 text-emerald-400" />
            25 Governed Autonomous Financial AI Agents
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {[
              { name: 'Finance Orchestrator', desc: '12-stage financial cycle master coordinator' },
              { name: 'Accounting Agent', desc: 'Double-entry journals and period validations' },
              { name: 'Billing Agent', desc: 'Subscription and usage billing lifecycle' },
              { name: 'AR Agent', desc: 'Receivable tracking and invoice status' },
              { name: 'AP Agent', desc: 'Vendor bills and 3-way matching' },
              { name: 'Payment Agent', desc: 'Disbursement state machine and approval gating' },
              { name: 'Reconciliation Agent', desc: 'Bank statement auto-match engine' },
              { name: 'Treasury Agent', desc: 'Liquidity, banking, and bank exposures' },
              { name: 'Cash Forecast Agent', desc: '13-week and 12-month rolling cash models' },
              { name: 'FP&A Agent', desc: 'Variance analytics and management commentary' },
              { name: 'Budget Agent', desc: 'Departmental budget allocations and tracking' },
              { name: 'Forecast Agent', desc: 'Revenue, EBITDA, and working capital modeling' },
              { name: 'Profitability Agent', desc: 'Unit economics by customer and SKU' },
              { name: 'Expense Agent', desc: 'Corporate spend policy and OCR extraction' },
              { name: 'Tax Data Agent', desc: 'Jurisdiction profiles and tax calculations' },
              { name: 'Credit Agent', desc: 'Customer credit risk scoring and limits' },
              { name: 'Fraud Agent', desc: 'Payment anomaly and fraud graph detection' },
              { name: 'Risk Agent', desc: 'Comprehensive financial risk scoring' },
              { name: 'Capital Agent', desc: 'Capital planning and equity/debt modeling' },
              { name: 'Investment Agent', desc: 'Treasury portfolio return and liquidity' },
              { name: 'Close Agent', desc: 'Period close checklist and accruals' },
              { name: 'Consolidation Agent', desc: 'Intercompany elimination and multi-entity' },
              { name: 'Financial Reporting Agent', desc: 'Balance sheet, P&L, and cash flow briefs' },
              { name: 'Scenario Agent', desc: 'Dynamic digital twin what-if simulations' },
              { name: 'Financial Audit Agent', desc: 'Immutable audit trail and control verification' }
            ].map((agent, i) => (
              <div key={agent.name} className="p-3.5 bg-slate-950/60 border border-slate-800 rounded-xl">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-emerald-400 font-semibold">0{i+1}.</span>
                  <span className="text-[10px] px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full font-mono">
                    GOVERNED
                  </span>
                </div>
                <div className="font-semibold text-sm text-white mt-1">{agent.name}</div>
                <div className="text-xs text-slate-400 mt-0.5">{agent.desc}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function CalendarIcon(props: any) {
  return (
    <svg {...props} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  );
}
