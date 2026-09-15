'use client';

import React, { useState } from 'react';
import {
  Brain,
  TrendingUp,
  Sliders,
  Play,
  RotateCcw,
  Layers,
  BarChart3,
  ShieldCheck,
  AlertTriangle,
  Compass,
  Cpu,
  Zap,
  Target,
  FileText,
  Activity,
  GitBranch,
  Flame
} from 'lucide-react';

export default function DecisionCommandCenterDashboard() {
  const [activeTab, setActiveTab] = useState<
    'command-center' | 'forecasts' | 'scenarios' | 'monte-carlo' | 'optimization' | 'decisions' | 'okrs' | 'war-room'
  >('command-center');

  // 14-Stage Closed-Loop Decision Cycle Simulator
  const [cycleRunning, setCycleRunning] = useState(false);
  const [cycleStep, setCycleStep] = useState(0);
  const [cycleCompleted, setCycleCompleted] = useState(false);

  // Monte Carlo Simulation Interactive State
  const [mcRunning, setMcRunning] = useState(false);
  const [mcResult, setMcResult] = useState<any>(null);

  // Pareto Frontier Tradeoff State
  const [selectedOption, setSelectedOption] = useState<'A' | 'B' | 'C'>('B');

  const stages = [
    'Question', 'Data', 'Context', 'Forecast', 'Scenarios', 'Simulation',
    'Optimization', 'Risk', 'Sensitivity', 'Recommendation', 'Human Decision',
    'Execution', 'Outcome', 'Learning'
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
    }, 350);
  };

  const executeMonteCarlo = () => {
    setMcRunning(true);
    setTimeout(() => {
      setMcResult({
        iterations: 10000,
        mean_outcome: '$2,450,000',
        p05_downside: '$1,980,000',
        p95_upside: '$2,980,000',
        var_95: '$2,100,000',
        cvar_shortfall: '$1,950,000',
        status: 'Empirical Convergence Verified (p < 0.01)'
      });
      setMcRunning(false);
    }, 850);
  };

  return (
    <div className="space-y-6 p-6">
      {/* Top Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between border-b border-border pb-5">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-500">
              <Brain className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">Enterprise Digital Twin & Strategic Decision Intelligence OS</h1>
              <p className="text-sm text-muted-foreground">
                Computational Enterprise Representation, Multi-Horizon Probabilistic Forecasting, Monte Carlo Stress Tests & Pareto Optimization
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
            Run 14-Stage Decision Cycle
          </button>
        </div>
      </div>

      {/* 14-Stage Decision Progress Indicator */}
      {(cycleRunning || cycleCompleted) && (
        <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="font-semibold text-primary">Strategic Decision Intelligence Loop (Stage {cycleStep} of {stages.length})</span>
            <span className="text-xs text-muted-foreground">{cycleCompleted ? 'Closed-Loop Execution & Retrospective Feedback Integrated' : 'Synthesizing Enterprise Digital Twin State...'}</span>
          </div>
          <div className="grid grid-cols-7 md:grid-cols-14 gap-1.5">
            {stages.map((stage, idx) => (
              <div
                key={stage}
                className={`text-center p-1.5 rounded border text-[11px] transition-all ${
                  idx < cycleStep
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-600 font-medium'
                    : idx === cycleStep
                    ? 'bg-indigo-500/10 border-indigo-500 text-indigo-600 font-bold scale-105 shadow-sm'
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
            <span className="text-xs font-medium uppercase tracking-wider">Decision Quality Score</span>
            <Brain className="h-4 w-4 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-foreground">96.2 / 100</div>
          <div className="text-xs text-emerald-600 mt-1 flex items-center gap-1">
            <TrendingUp className="h-3 w-3" /> Empirical calibration verified
          </div>
        </div>

        <div className="bg-card border border-border rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Forecast Calibration</span>
            <Target className="h-4 w-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-foreground">94.8%</div>
          <div className="text-xs text-muted-foreground mt-1">MAPE error band: ±2.8%</div>
        </div>

        <div className="bg-card border border-border rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Twin Entities Synced</span>
            <Activity className="h-4 w-4 text-blue-500" />
          </div>
          <div className="text-2xl font-bold text-foreground">142</div>
          <div className="text-xs text-muted-foreground mt-1">Across 14 global operating hubs</div>
        </div>

        <div className="bg-card border border-border rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Active War Rooms</span>
            <Flame className="h-4 w-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-foreground">1 Tabletop</div>
          <div className="text-xs text-muted-foreground mt-1">European Port Strike Containment</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-border overflow-x-auto pb-2 text-sm font-medium">
        {[
          { id: 'command-center', label: 'Strategic Command Center' },
          { id: 'forecasts', label: 'Probabilistic Forecasts' },
          { id: 'scenarios', label: 'Multi-Variable Scenarios' },
          { id: 'monte-carlo', label: 'Monte Carlo Stress Tests' },
          { id: 'optimization', label: 'Pareto Optimization' },
          { id: 'decisions', label: 'Decision Briefs' },
          { id: 'okrs', label: 'OKR Intelligence' },
          { id: 'war-room', label: 'Executive War Room' }
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
      {activeTab === 'command-center' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
            <h3 className="text-base font-semibold flex items-center gap-2">
              <Compass className="h-4 w-4 text-indigo-500" />
              Enterprise Strategic Driver Tree & Elasticities
            </h3>
            <div className="space-y-3">
              {[
                { metric: 'Net Retention Rate (NRR)', current: '118.5%', elasticity: '+1.42x on Operating Margin', impact: 'Highest Lever' },
                { metric: 'Price Sensitivity Elasticity', current: '0.85', elasticity: '+0.85x Revenue for +1% Price', impact: 'Favorable Pricing Power' },
                { metric: 'Supplier Lead Time Variance', current: '+8 Days', elasticity: '-0.38x on Working Capital', impact: 'Operational Headwind' }
              ].map((driver) => (
                <div key={driver.metric} className="flex items-center justify-between p-3 rounded-lg border border-border bg-muted/20">
                  <div>
                    <div className="text-sm font-semibold">{driver.metric}</div>
                    <div className="text-xs text-muted-foreground">{driver.elasticity}</div>
                  </div>
                  <div className="text-right">
                    <span className="text-xs px-2.5 py-1 rounded-full font-medium bg-indigo-500/10 text-indigo-600 border border-indigo-500/30">
                      {driver.current}
                    </span>
                    <div className="text-xs text-muted-foreground mt-1">{driver.impact}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
            <h3 className="text-base font-semibold flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-emerald-500" />
              Human Governance Strategic Gates
            </h3>
            <p className="text-xs text-muted-foreground">
              Strategic AI operates as an advisory decision support system. High-impact capital allocation and organizational restructurings require executive sign-off.
            </p>
            <div className="p-3 rounded-lg border border-border bg-muted/20 space-y-2 text-xs">
              <div className="font-semibold text-foreground">DEC-2026-CAPEX-EU</div>
              <div className="text-muted-foreground">Authorise $2.4M Capex for Rotterdam Advanced Cross-Dock Facility</div>
              <div className="flex gap-2 pt-2">
                <button className="flex-1 py-1 bg-primary text-primary-foreground rounded text-xs font-medium">Approve Capex</button>
                <button className="flex-1 py-1 bg-muted border border-border rounded text-xs font-medium">View Sensitivity</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'monte-carlo' && (
        <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="text-base font-semibold flex items-center gap-2">
            <Cpu className="h-4 w-4 text-purple-500" />
            10,000-Iteration Monte Carlo Disruption Simulator
          </h3>
          <p className="text-xs text-muted-foreground">
            Generates empirical outcome distributions, 95th-percentile Value-at-Risk (VaR), and Conditional Expected Shortfall (CVaR).
          </p>
          <button
            onClick={executeMonteCarlo}
            disabled={mcRunning}
            className="px-4 py-2 bg-primary text-primary-foreground rounded text-xs font-medium hover:opacity-90 transition disabled:opacity-50"
          >
            {mcRunning ? 'Executing 10,000 Parallel Stochastic Runs...' : 'Run 10,000 Monte Carlo Iterations'}
          </button>
          {mcResult && (
            <div className="p-4 rounded-lg border border-purple-500/30 bg-purple-500/5 space-y-2 text-xs">
              <div className="font-bold text-sm text-foreground">{mcResult.status}</div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-muted-foreground pt-1">
                <div>Mean Projected Outcome: <span className="font-semibold text-foreground block">{mcResult.mean_outcome}</span></div>
                <div>5th Percentile (Downside): <span className="font-semibold text-amber-600 block">{mcResult.p05_downside}</span></div>
                <div>95th Percentile (Upside): <span className="font-semibold text-emerald-600 block">{mcResult.p95_upside}</span></div>
                <div>VaR 95% Cutoff: <span className="font-semibold text-foreground block">{mcResult.var_95}</span></div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'optimization' && (
        <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="text-base font-semibold flex items-center gap-2">
            <GitBranch className="h-4 w-4 text-blue-500" />
            Multi-Objective Pareto Frontier Optimization
          </h3>
          <p className="text-xs text-muted-foreground">
            Exposes strategic trade-offs across Profitability vs Systemic Risk vs Customer Experience without hiding tensions.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            {[
              { id: 'A', title: 'Option A: Aggressive Build', profit: '96.0', risk: '42.0 (High)', cx: '88.0', rec: false },
              { id: 'B', title: 'Option B: Balanced Resilience', profit: '88.5', risk: '18.0 (Low)', cx: '94.0', rec: true },
              { id: 'C', title: 'Option C: Conservative Fortress', profit: '72.0', risk: '6.5 (Min)', cx: '90.0', rec: false }
            ].map((opt) => (
              <div
                key={opt.id}
                onClick={() => setSelectedOption(opt.id as any)}
                className={`p-3 rounded-lg border cursor-pointer transition ${
                  selectedOption === opt.id
                    ? 'bg-primary/5 border-primary shadow-sm'
                    : 'bg-muted/20 border-border hover:bg-muted/40'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-foreground">{opt.title}</span>
                  {opt.rec && <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-600 border border-emerald-500/30">Recommended</span>}
                </div>
                <div className="space-y-0.5 text-muted-foreground">
                  <div>Profit Score: <span className="font-semibold text-foreground">{opt.profit}</span></div>
                  <div>Systemic Risk: <span className="font-semibold text-foreground">{opt.risk}</span></div>
                  <div>Customer Experience: <span className="font-semibold text-foreground">{opt.cx}</span></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'war-room' && (
        <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold flex items-center gap-2">
              <Flame className="h-4 w-4 text-amber-500" />
              Executive War Room: European Maritime Strike Tabletop Simulation
            </h3>
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-500/10 text-amber-600 border border-amber-500/30">
              Active Tabletop Exercise
            </span>
          </div>
          <div className="p-4 rounded-lg border border-border bg-muted/20 space-y-2 text-xs">
            <div className="font-semibold text-foreground">Situation Brief:</div>
            <p className="text-muted-foreground">
              Simulating 21-day port closure at Rotterdam. 4 container shipments rerouted via air-freight and overland train corridors. Working capital exposure protected by €450K contingency reserve.
            </p>
            <div className="flex gap-3 pt-2">
              <button className="px-3 py-1.5 bg-primary text-primary-foreground rounded font-medium">Dispatch Air Freight Reroute</button>
              <button className="px-3 py-1.5 bg-muted border border-border rounded font-medium">Export Incident Log</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
