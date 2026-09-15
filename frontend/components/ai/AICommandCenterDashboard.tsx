'use client';

import React, { useState } from 'react';
import {
  Bot,
  Brain,
  Network,
  Cpu,
  Layers,
  ShieldAlert,
  ShieldCheck,
  Zap,
  CheckCircle2,
  Clock,
  Coins,
  AlertTriangle,
  Play,
  RotateCcw,
  Sparkles,
  Search,
  Database,
  Lock,
  GitPullRequest
} from 'lucide-react';

export default function AICommandCenterDashboard() {
  const [activeTab, setActiveTab] = useState<
    'overview' | 'agents' | 'tasks' | 'workflows' | 'approvals' | 'memory' | 'tools' | 'governance'
  >('overview');

  const [lockdownActive, setLockdownActive] = useState(false);
  const [naturalQuery, setNaturalQuery] = useState('');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [executingTask, setExecutingTask] = useState(false);

  const handleRunCommand = () => {
    if (!naturalQuery) return;
    setExecutingTask(true);
    setTimeout(() => {
      setQueryResult({
        query: naturalQuery,
        assignedSupervisor: 'EnterpriseSupervisor',
        status: 'COMPLETED_SIMULATION',
        decomposedSteps: [
          'Parsed natural language intent & policy scope',
          'Retrieved cross-domain memory from Episodic & Semantic fabrics',
          'Dispatched tasks to AnalystAgent & CriticAgent',
          'Synthesized governed executive action brief'
        ],
        autonomyLevel: 'L4 (Execute Within Policy)',
        cost: '$0.038',
        executionTime: '420ms'
      });
      setExecutingTask(false);
    }, 600);
  };

  const toggleLockdown = () => {
    setLockdownActive(!lockdownActive);
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header Banner */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between border-b border-border pb-5">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-500/10 rounded-lg text-purple-500">
              <Bot className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">Autonomous Enterprise AI Operating System (AEAI-OS)</h1>
              <p className="text-sm text-muted-foreground">
                Multi-Agent Intelligence Mesh, 7-Layer Memory Fabric, Tool Gateway & Governed Autonomous Execution
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={toggleLockdown}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
              lockdownActive
                ? 'bg-amber-600 hover:bg-amber-700 text-white animate-pulse'
                : 'bg-red-600/90 hover:bg-red-700 text-white'
            }`}
          >
            <ShieldAlert className="h-4 w-4" />
            {lockdownActive ? 'LOCKED DOWN (READ-ONLY)' : 'EMERGENCY LOCKDOWN'}
          </button>
        </div>
      </div>

      {/* KPI Top Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl border border-border bg-card/60 backdrop-blur">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-muted-foreground">AI System Health</span>
            <ShieldCheck className="h-4 w-4 text-emerald-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-foreground">98.4%</div>
          <div className="mt-1 text-xs text-emerald-500 font-medium flex items-center gap-1">
            Zero policy violations in 24h
          </div>
        </div>

        <div className="p-4 rounded-xl border border-border bg-card/60 backdrop-blur">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-muted-foreground">Active Agent Mesh</span>
            <Network className="h-4 w-4 text-indigo-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-foreground">16 Agents / 9 Supervisors</div>
          <div className="mt-1 text-xs text-muted-foreground">28 active inter-agent channels</div>
        </div>

        <div className="p-4 rounded-xl border border-border bg-card/60 backdrop-blur">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-muted-foreground">Tasks Executed (24h)</span>
            <Zap className="h-4 w-4 text-amber-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-foreground">1,240 Autonomous</div>
          <div className="mt-1 text-xs text-muted-foreground">18 routed to human approval</div>
        </div>

        <div className="p-4 rounded-xl border border-border bg-card/60 backdrop-blur">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-muted-foreground">AI Net ROI</span>
            <Coins className="h-4 w-4 text-emerald-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-emerald-500">+384.2%</div>
          <div className="mt-1 text-xs text-muted-foreground">14,200 hrs saved this quarter</div>
        </div>
      </div>

      {/* Natural Language Business Control Bar */}
      <div className="p-4 rounded-xl border border-purple-500/20 bg-purple-500/5 backdrop-blur space-y-3">
        <div className="flex items-center gap-2 text-sm font-semibold text-purple-400">
          <Sparkles className="h-4 w-4" />
          Natural-Language Governed Business Control
        </div>
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="E.g., 'Analyze Q3 enterprise churn risks and prepare mitigation strategy under L4 autonomy'"
            value={naturalQuery}
            onChange={(e) => setNaturalQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleRunCommand()}
            className="flex-1 bg-background border border-border rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <button
            onClick={handleRunCommand}
            disabled={executingTask || !naturalQuery}
            className="px-5 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
          >
            {executingTask ? 'Processing...' : 'Dispatch Task'}
          </button>
        </div>

        {queryResult && (
          <div className="mt-3 p-3 bg-card rounded-lg border border-border text-xs space-y-2">
            <div className="flex justify-between items-center">
              <span className="font-semibold text-foreground">Supervisor: {queryResult.assignedSupervisor}</span>
              <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-500 rounded font-medium">{queryResult.status}</span>
            </div>
            <div className="text-muted-foreground">Autonomy: {queryResult.autonomyLevel} | Cost: {queryResult.cost} | Latency: {queryResult.executionTime}</div>
            <div className="space-y-1">
              {queryResult.decomposedSteps.map((s: string, idx: number) => (
                <div key={idx} className="flex items-center gap-1.5 text-foreground/80">
                  <CheckCircle2 className="h-3 w-3 text-emerald-500" />
                  {s}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Main Tabs */}
      <div className="flex border-b border-border space-x-4">
        {[
          { id: 'overview', label: 'Mesh Overview', icon: Network },
          { id: 'agents', label: 'Agent Registry', icon: Bot },
          { id: 'tasks', label: 'Task Graphs', icon: Layers },
          { id: 'workflows', label: 'Workflows', icon: GitPullRequest },
          { id: 'approvals', label: 'Human Approvals', icon: ShieldCheck },
          { id: 'memory', label: '7-Layer Memory', icon: Brain },
          { id: 'tools', label: 'Tool Gateway', icon: Cpu },
          { id: 'governance', label: 'Governance & ROI', icon: Lock },
        ].map((tab) => {
          const Icon = tab.icon;
          const active = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 pb-3 text-sm font-medium border-b-2 transition-colors ${
                active
                  ? 'border-purple-500 text-purple-400 font-semibold'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              <Icon className="h-4 w-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="p-5 rounded-xl border border-border bg-card/60 backdrop-blur space-y-4">
            <h3 className="text-base font-semibold">Hierarchical Supervisor Hierarchy</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
              {[
                { name: 'EnterpriseSupervisor', role: 'Master Cross-Domain Orchestration', status: 'Active' },
                { name: 'BusinessSupervisor', role: 'GTM, Sales & CRM Supervision', status: 'Active' },
                { name: 'FinanceSupervisor', role: 'Treasury, Payments & AP/AR (Phase 72)', status: 'Active' },
                { name: 'OperationsSupervisor', role: 'Supply Chain & Logistics (Phase 74)', status: 'Active' },
                { name: 'StrategySupervisor', role: 'Digital Twin & Monte Carlo (Phase 75)', status: 'Active' },
                { name: 'SecuritySupervisor', role: 'Zero-Trust Defense & Threats (Phase 66)', status: 'Active' },
                { name: 'ComplianceSupervisor', role: 'Regulatory & Trust Governance (Phase 73)', status: 'Active' },
                { name: 'CustomerSupervisor', role: 'Customer 360 & Experience Health', status: 'Active' },
                { name: 'EngineeringSupervisor', role: 'SDLC, CI/CD & Infra Operations', status: 'Active' },
              ].map((s, idx) => (
                <div key={idx} className="p-3 bg-muted/40 rounded-lg border border-border/80">
                  <div className="font-semibold text-foreground text-xs">{s.name}</div>
                  <div className="text-[11px] text-muted-foreground mt-0.5">{s.role}</div>
                  <div className="mt-2 text-[10px] text-emerald-500 font-semibold uppercase">{s.status}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="p-5 rounded-xl border border-border bg-card/60 backdrop-blur space-y-3">
            <h3 className="text-base font-semibold">7-Layer Persistent Memory Fabric</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
              <div className="p-2.5 bg-muted/30 rounded border border-border">Working Memory (Task Context)</div>
              <div className="p-2.5 bg-muted/30 rounded border border-border">Episodic Memory (Outcomes & Logs)</div>
              <div className="p-2.5 bg-muted/30 rounded border border-border">Semantic Memory (Facts & Rules)</div>
              <div className="p-2.5 bg-muted/30 rounded border border-border">Procedural Memory (Runbooks)</div>
              <div className="p-2.5 bg-muted/30 rounded border border-border">User Context (Preferences)</div>
              <div className="p-2.5 bg-muted/30 rounded border border-border">Organizational Memory</div>
              <div className="p-2.5 bg-muted/30 rounded border border-border">Decision Memory (Phase 75)</div>
              <div className="p-2.5 bg-muted/30 rounded border border-border">Knowledge Fabric (Hybrid RAG)</div>
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-4">
          <div className="p-5 rounded-xl border border-border bg-card/60 backdrop-blur space-y-3">
            <h3 className="text-base font-semibold flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-amber-500" />
              Pending Human Approvals (3)
            </h3>
            <div className="space-y-2 text-xs">
              <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg space-y-1">
                <div className="font-semibold text-foreground">APPR-2026-CAPEX-EU</div>
                <div className="text-muted-foreground">Authorize $450,000 procurement commitment to EU Tier-1 foundry.</div>
                <div className="flex gap-2 mt-2">
                  <button className="px-2.5 py-1 bg-emerald-600 text-white rounded font-medium">Approve</button>
                  <button className="px-2.5 py-1 bg-muted hover:bg-muted/80 rounded font-medium">Reject</button>
                </div>
              </div>
            </div>
          </div>

          <div className="p-5 rounded-xl border border-border bg-card/60 backdrop-blur space-y-2 text-xs">
            <h3 className="text-base font-semibold">Autonomy Level Matrix</h3>
            <div className="space-y-1 text-muted-foreground">
              <div><strong className="text-foreground">L0:</strong> Observe Only</div>
              <div><strong className="text-foreground">L1:</strong> Analyze Telemetry</div>
              <div><strong className="text-foreground">L2:</strong> Formulate Recommendations</div>
              <div><strong className="text-foreground">L3:</strong> Prepare Action Draft</div>
              <div><strong className="text-foreground">L4:</strong> Execute Within Policy Limits</div>
              <div><strong className="text-foreground">L5:</strong> Governed Autonomous Execution</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
