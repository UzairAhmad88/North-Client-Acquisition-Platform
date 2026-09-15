'use client';

import React, { useState } from 'react';
import {
  Cpu,
  GitBranch,
  GitPullRequest,
  GitCommit,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Activity,
  AlertTriangle,
  Play,
  CheckCircle2,
  XCircle,
  Clock,
  RotateCcw,
  Layers,
  Terminal,
  Server,
  Zap,
  DollarSign,
  TrendingUp,
  Workflow,
  Search,
  BookOpen,
  FileCode,
  Gauge,
  Sparkles,
  BarChart3,
  Flame,
  Check,
  ChevronRight,
  Eye,
  Settings
} from 'lucide-react';

export default function DevSecOpsSoftwareFactoryDashboard() {
  const [roleView, setRoleView] = useState<'executive' | 'manager' | 'tech_lead' | 'developer' | 'sre' | 'security' | 'release'>('tech_lead');
  const [activeTab, setActiveTab] = useState<'overview' | 'factory_cycle' | 'provenance' | 'progressive_delivery' | 'sre_slo' | 'incident_rca'>('overview');

  // Cycle simulator state
  const [cycleRunning, setCycleRunning] = useState(false);
  const [cycleStep, setCycleStep] = useState(0);
  const [cycleResult, setCycleResult] = useState<any>(null);

  // Canary deployment simulator state
  const [canaryTraffic, setCanaryTraffic] = useState(10);
  const [canaryErrorRate, setCanaryErrorRate] = useState(0.04);
  const [rollbackTriggered, setRollbackTriggered] = useState(false);

  // Self healing runbook approval state
  const [pendingApproval, setPendingApproval] = useState(true);
  const [remediationStatus, setRemediationStatus] = useState<'IDLE' | 'PENDING_APPROVAL' | 'EXECUTING' | 'VERIFIED'>('PENDING_APPROVAL');

  const doraMetrics = [
    { label: 'Deployment Frequency', value: '14.2 / day', tier: 'ELITE', change: '+18%' },
    { label: 'Lead Time for Changes', value: '42 mins', tier: 'ELITE', change: '-24%' },
    { label: 'Change Failure Rate', value: '0.8%', tier: 'ELITE', change: '-45%' },
    { label: 'MTTR (Mean Time to Restore)', value: '11 mins', tier: 'ELITE', change: '-60%' },
  ];

  const factoryPhases = [
    { id: 1, name: '1. Requirement & Architecture Graph', agent: 'PlannerAgent', status: 'COMPLETED', time: '1.2s' },
    { id: 2, name: '2. Sandbox Code Generation & Linting', agent: 'CodingAgent', status: 'COMPLETED', time: '4.8s' },
    { id: 3, name: '3. 9-Factor Multi-Dimensional Review', agent: 'ReviewAgent', status: 'COMPLETED', time: '2.1s' },
    { id: 4, name: '4. Zero-Trust Security Gate & SBOM Scan', agent: 'SecurityAgent', status: 'COMPLETED', time: '1.9s' },
    { id: 5, name: '5. Test Impact & Flakiness Isolation', agent: 'TestAgent', status: 'COMPLETED', time: '5.3s' },
    { id: 6, name: '6. Multi-Tier Cached CI/CD Build', agent: 'BuildSystem', status: 'COMPLETED', time: '3.4s' },
    { id: 7, name: '7. Cryptographic Provenance Attestation', agent: 'ProvenanceEngine', status: 'COMPLETED', time: '0.8s' },
    { id: 8, name: '8. Canary Rollout & SLO Telemetry', agent: 'DeploymentAgent', status: 'COMPLETED', time: '6.2s' },
  ];

  const runAutonomousCycle = () => {
    setCycleRunning(true);
    setCycleStep(1);
    setCycleResult(null);

    const interval = setInterval(() => {
      setCycleStep((prev) => {
        if (prev >= 8) {
          clearInterval(interval);
          setCycleRunning(false);
          setCycleResult({
            cycleId: 'cycle_dsops_' + Math.floor(Math.random() * 9000 + 1000),
            status: 'SUCCESS',
            duration: '25.7s',
            provenanceHash: 'sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
            canaryHealth: 'HEALTHY (0.02% error rate)',
            humanReviewer: 'Approved by DevSecOps Guardrail',
          });
          return 8;
        }
        return prev + 1;
      });
    }, 450);
  };

  const handleRollback = () => {
    setRollbackTriggered(true);
    setCanaryTraffic(0);
    setCanaryErrorRate(0.01);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
              <Zap className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
                Autonomous DevSecOps & AI Software Factory
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-medium">
                  Phase 67 Enterprise
                </span>
              </h1>
              <p className="text-sm text-slate-400">
                End-to-End Autonomous Software Engineering, CI/CD Intelligence & Governed Self-Healing Delivery Layer
              </p>
            </div>
          </div>
        </div>

        {/* Role Switcher */}
        <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 p-1 rounded-lg text-xs">
          <span className="px-2 text-slate-400 font-semibold uppercase">Perspective:</span>
          {(['executive', 'manager', 'tech_lead', 'developer', 'sre', 'security', 'release'] as const).map((r) => (
            <button
              key={r}
              onClick={() => setRoleView(r)}
              className={`px-2.5 py-1 rounded transition-colors ${
                roleView === r
                  ? 'bg-indigo-600 text-white font-medium shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              {r.replace('_', ' ').toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* DORA Metrics & Executive Telemetry */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {doraMetrics.map((m, i) => (
          <div key={i} className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 relative overflow-hidden">
            <div className="flex justify-between items-start">
              <span className="text-xs font-medium text-slate-400">{m.label}</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                {m.tier}
              </span>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-white">{m.value}</span>
              <span className="text-xs font-semibold text-emerald-400">{m.change}</span>
            </div>
            <div className="mt-3 text-[11px] text-slate-500 flex items-center gap-1">
              <TrendingUp className="h-3 w-3 text-emerald-400" />
              Automated telemetry verified across all environments
            </div>
          </div>
        ))}
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 space-x-1">
        {[
          { id: 'overview', label: 'Command Center', icon: Gauge },
          { id: 'factory_cycle', label: 'AI Software Factory Cycle', icon: Play },
          { id: 'provenance', label: 'Artifact Provenance & Supply Chain', icon: Layers },
          { id: 'progressive_delivery', label: 'Progressive Delivery & Rollback', icon: GitBranch },
          { id: 'sre_slo', label: 'SRE Topology & Error Budgets', icon: Server },
          { id: 'incident_rca', label: 'Incident RCA & Governed Healing', icon: ShieldAlert },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${
                isActive
                  ? 'border-indigo-500 text-indigo-400 bg-indigo-500/10 rounded-t-lg'
                  : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
              }`}
            >
              <Icon className="h-4 w-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab 1: Command Center Overview */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {/* Active Repositories & Build Health */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-semibold text-white flex items-center gap-2">
                  <GitBranch className="h-5 w-5 text-indigo-400" />
                  Authorized Repositories & CI/CD Intelligence
                </h3>
                <span className="text-xs text-slate-400">18 active repositories indexed</span>
              </div>
              <div className="divide-y divide-slate-800">
                {[
                  { name: 'uzaii-develop-by-norths/core-api', branch: 'main', build: 'SUCCESS', testCoverage: '94.2%', secScore: '98/100', cache: '91% hit' },
                  { name: 'uzaii-develop-by-norths/auth-service', branch: 'main', build: 'SUCCESS', testCoverage: '98.5%', secScore: '100/100', cache: '96% hit' },
                  { name: 'uzaii-develop-by-norths/billing-engine', branch: 'main', build: 'SUCCESS', testCoverage: '96.1%', secScore: '97/100', cache: '88% hit' },
                  { name: 'uzaii-develop-by-norths/web-portal', branch: 'release/v4.2', build: 'BUILDING', testCoverage: '89.4%', secScore: '95/100', cache: '84% hit' },
                ].map((repo, i) => (
                  <div key={i} className="py-3 flex items-center justify-between">
                    <div>
                      <span className="font-mono text-sm text-indigo-300 font-semibold">{repo.name}</span>
                      <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
                        <span>Branch: {repo.branch}</span>
                        <span>•</span>
                        <span>Coverage: {repo.testCoverage}</span>
                        <span>•</span>
                        <span>Build Cache: {repo.cache}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                        {repo.secScore}
                      </span>
                      <span className={`text-xs px-2 py-0.5 rounded font-bold ${repo.build === 'SUCCESS' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400 animate-pulse'}`}>
                        {repo.build}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 9-Factor Multi-Dimensional Review Summary */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
              <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
                <ShieldCheck className="h-5 w-5 text-emerald-400" />
                9-Factor Automated Review Matrix
              </h3>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { factor: 'Correctness & Logic', score: '98%', status: 'PASSED' },
                  { factor: 'Architecture Drift', score: '0 Violations', status: 'PASSED' },
                  { factor: 'Phase 66 Zero-Trust Security', score: 'No CVEs', status: 'PASSED' },
                  { factor: 'Performance & Concurrency', score: 'p99 < 85ms', status: 'PASSED' },
                  { factor: 'Maintainability & Smells', score: 'A (Grade)', status: 'PASSED' },
                  { factor: 'Test Impact & Coverage', score: '94.8%', status: 'PASSED' },
                  { factor: 'Error Handling & Faults', score: 'Full Guard', status: 'PASSED' },
                  { factor: 'Observability & Tracing', score: 'OpenTelemetry OK', status: 'PASSED' },
                  { factor: 'Backward API Compatibility', score: 'Non-Breaking', status: 'PASSED' },
                ].map((f, i) => (
                  <div key={i} className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                    <div className="text-xs text-slate-400">{f.factor}</div>
                    <div className="text-base font-bold text-white mt-1">{f.score}</div>
                    <span className="inline-block mt-1 text-[10px] font-semibold text-emerald-400">
                      ✓ {f.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column: AI Agent Roster & Cloud FinOps */}
          <div className="space-y-6">
            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-semibold text-white flex items-center gap-2">
                  <Terminal className="h-5 w-5 text-indigo-400" />
                  17 Autonomous AI Agents
                </h3>
                <span className="text-xs text-emerald-400 font-semibold">ALL GATED</span>
              </div>
              <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
                {[
                  { name: 'EngineeringOrchestratorAgent', role: 'Master Lifecycle Coordinator', active: true },
                  { name: 'PlannerAgent', role: 'Requirements & Arch Analyzer', active: true },
                  { name: 'CodingAgent', role: 'Isolated Sandbox Generator', active: true },
                  { name: 'ReviewAgent', role: '9-Factor PR Evaluator', active: true },
                  { name: 'SecurityAgent', role: 'Phase 66 Zero-Trust Auditor', active: true },
                  { name: 'TestAgent', role: 'Test Impact & Flakiness Isolation', active: true },
                  { name: 'ReleaseAgent', role: '6-Dimension Risk Evaluator', active: true },
                  { name: 'DeploymentAgent', role: 'Progressive Canary Controller', active: true },
                  { name: 'SreAgent', role: 'SLO Error Budget Watcher', active: true },
                  { name: 'IncidentAgent', role: 'Production Triage & RCA', active: true },
                  { name: 'RemediationAgent', role: 'Governed Runbook Self-Healer', active: true },
                ].map((ag, i) => (
                  <div key={i} className="p-2.5 rounded bg-slate-950 border border-slate-800 flex justify-between items-center">
                    <div>
                      <div className="text-xs font-semibold text-indigo-300 font-mono">{ag.name}</div>
                      <div className="text-[11px] text-slate-400">{ag.role}</div>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                      ACTIVE
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Cloud FinOps Allocation */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
              <h3 className="font-semibold text-white mb-3 flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-emerald-400" />
                Engineering FinOps Allocation
              </h3>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between text-slate-400">
                  <span>CI/CD & Multi-tier Build Runners</span>
                  <span className="font-semibold text-white">$1,420 / mo (Cache saved $4,800)</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Autonomous AI Agent Execution</span>
                  <span className="font-semibold text-white">$380 / mo</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Production Kubernetes & Canary</span>
                  <span className="font-semibold text-white">$2,850 / mo</span>
                </div>
                <div className="pt-2 border-t border-slate-800 flex justify-between font-semibold text-emerald-400">
                  <span>Net Efficiency vs Manual Ops</span>
                  <span>+68% Cost Reduction</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: AI Software Factory Cycle Simulator */}
      {activeTab === 'factory_cycle' && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Play className="h-5 w-5 text-indigo-400" />
                Autonomous Software Factory End-to-End Cycle
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Executes: Requirement → AI Plan → Sandbox Code → Review → Security → Test → Build → Release → Canary → Telemetry
              </p>
            </div>
            <button
              onClick={runAutonomousCycle}
              disabled={cycleRunning}
              className={`px-5 py-2.5 rounded-lg font-semibold text-sm flex items-center gap-2 transition-all ${
                cycleRunning
                  ? 'bg-indigo-600/50 text-indigo-200 cursor-not-allowed'
                  : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30'
              }`}
            >
              <Play className="h-4 w-4" />
              {cycleRunning ? 'Executing Pipeline...' : 'Run Autonomous Factory Cycle'}
            </button>
          </div>

          {/* Phase Progress Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {factoryPhases.map((phase) => {
              const isDone = cycleStep >= phase.id;
              const isCurrent = cycleStep === phase.id && cycleRunning;
              return (
                <div
                  key={phase.id}
                  className={`p-4 rounded-xl border transition-all ${
                    isCurrent
                      ? 'bg-indigo-950/60 border-indigo-500 ring-2 ring-indigo-500/50 animate-pulse'
                      : isDone
                      ? 'bg-slate-950 border-emerald-500/50'
                      : 'bg-slate-950/40 border-slate-800 opacity-60'
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs font-semibold text-indigo-300 font-mono">{phase.agent}</span>
                    {isDone ? (
                      <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                    ) : (
                      <Clock className="h-4 w-4 text-slate-500" />
                    )}
                  </div>
                  <div className="font-medium text-sm text-white mb-2">{phase.name}</div>
                  <div className="flex justify-between items-center text-xs text-slate-400">
                    <span>Status: {isDone ? 'COMPLETED' : 'PENDING'}</span>
                    <span>{isDone ? phase.time : '--'}</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Cycle Results Panel */}
          {cycleResult && (
            <div className="bg-emerald-950/20 border border-emerald-500/40 rounded-xl p-5 space-y-3">
              <div className="flex items-center gap-2 text-emerald-400 font-semibold">
                <CheckCircle2 className="h-5 w-5" />
                Software Factory Delivery Cycle Verified & Deployed
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
                <div className="bg-slate-950 p-3 rounded border border-slate-800">
                  <div className="text-slate-400">CYCLE ID:</div>
                  <div className="text-white font-bold mt-1">{cycleResult.cycleId}</div>
                </div>
                <div className="bg-slate-950 p-3 rounded border border-slate-800">
                  <div className="text-slate-400">EXECUTION TIME:</div>
                  <div className="text-white font-bold mt-1">{cycleResult.duration}</div>
                </div>
                <div className="bg-slate-950 p-3 rounded border border-slate-800">
                  <div className="text-slate-400">CANARY HEALTH:</div>
                  <div className="text-emerald-400 font-bold mt-1">{cycleResult.canaryHealth}</div>
                </div>
                <div className="bg-slate-950 p-3 rounded border border-slate-800">
                  <div className="text-slate-400">GOVERNANCE GATE:</div>
                  <div className="text-indigo-400 font-bold mt-1">{cycleResult.humanReviewer}</div>
                </div>
              </div>
              <div className="text-xs text-slate-400 font-mono break-all pt-2 border-t border-slate-800">
                <span className="text-emerald-400 font-semibold">SUPPLY CHAIN PROVENANCE ATTESTATION:</span> {cycleResult.provenanceHash}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 3: Artifact Provenance & Supply Chain */}
      {activeTab === 'provenance' && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-6">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Layers className="h-5 w-5 text-indigo-400" />
              End-to-End Cryptographic Artifact Provenance Chain
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              Guarantees full lineage: Requirement → Commit → Build → Artifact → Release → Canary Deployment
            </p>
          </div>

          <div className="relative border-l-2 border-indigo-500/40 ml-4 pl-6 space-y-6">
            {[
              { title: '1. Requirement Spec', id: 'REQ-8821: Autonomous JWT Token Rotation', hash: 'req_hash_e9a1', verified: true },
              { title: '2. Git Commit', id: 'Commit: 9b2d8e1 ("Implement JIT token invalidation")', hash: 'sha1:9b2d8e1', verified: true },
              { title: '3. CI/CD Build Run', id: 'Build: #4812 (Passed unit, contract & security)', hash: 'bld_run_0412', verified: true },
              { title: '4. Container Artifact & SBOM', id: 'ghcr.io/uzaii/core-api:v4.2.1', hash: 'sha256:7f83b1657ff1fc53b92dc181...', verified: true },
              { title: '5. Release Candidate', id: 'Release: REL-2026.4.2 (Zero CVEs, Signed Cosign)', hash: 'sig_cosign_valid', verified: true },
              { title: '6. Production Deployment', id: 'Cluster: prod-us-east-1 (Canary 10% Traffic)', hash: 'dep_prod_canary', verified: true },
            ].map((step, i) => (
              <div key={i} className="relative">
                <div className="absolute -left-[31px] top-0.5 p-1 rounded-full bg-indigo-600 text-white">
                  <Check className="h-3 w-3" />
                </div>
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <span className="text-xs text-indigo-400 font-semibold">{step.title}</span>
                    <div className="text-white font-medium mt-1">{step.id}</div>
                    <div className="text-xs text-slate-500 font-mono mt-1">{step.hash}</div>
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    VERIFIED
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: Progressive Delivery & Rollback */}
      {activeTab === 'progressive_delivery' && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <GitBranch className="h-5 w-5 text-indigo-400" />
                Progressive Canary Rollout & Policy-Governed Rollback
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Automated regression detection triggers instant rollback if error rate exceeds 0.5% or latency exceeds 200ms
              </p>
            </div>
            {rollbackTriggered ? (
              <span className="px-3 py-1.5 rounded-lg bg-red-500/20 text-red-400 border border-red-500/30 text-xs font-bold flex items-center gap-1.5">
                <RotateCcw className="h-4 w-4" /> ROLLBACK COMPLETED (v4.2.0 Restored)
              </span>
            ) : (
              <button
                onClick={handleRollback}
                className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-bold flex items-center gap-1.5 transition-colors"
              >
                <RotateCcw className="h-4 w-4" /> Emergency Rollback
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400">Canary Traffic Share</span>
              <div className="text-2xl font-bold text-white mt-1">{canaryTraffic}%</div>
              <div className="w-full bg-slate-800 rounded-full h-2 mt-3 overflow-hidden">
                <div className="bg-indigo-500 h-full transition-all" style={{ width: `${canaryTraffic}%` }}></div>
              </div>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400">Canary Error Rate</span>
              <div className={`text-2xl font-bold mt-1 ${canaryErrorRate > 0.05 ? 'text-red-400' : 'text-emerald-400'}`}>
                {(canaryErrorRate * 100).toFixed(2)}%
              </div>
              <span className="text-[11px] text-slate-500 mt-2 block">Threshold: &lt; 0.50%</span>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400">Canary p99 Latency</span>
              <div className="text-2xl font-bold text-white mt-1">42ms</div>
              <span className="text-[11px] text-emerald-400 mt-2 block">Within 200ms SLO target</span>
            </div>
          </div>
        </div>
      )}

      {/* Tab 5: SRE Topology & SLOs */}
      {activeTab === 'sre_slo' && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-6">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Server className="h-5 w-5 text-indigo-400" />
              Service Topology, SLOs & Error Budgets
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              Live error budget consumption influencing progressive release gatekeeping
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { name: 'auth-service', slo: '99.95%', actual: '99.99%', budget: '84% remaining', burn: '0.12x', status: 'HEALTHY' },
              { name: 'payment-service', slo: '99.99%', actual: '99.995%', budget: '92% remaining', burn: '0.08x', status: 'HEALTHY' },
              { name: 'core-api', slo: '99.90%', actual: '99.92%', budget: '68% remaining', burn: '0.45x', status: 'ATTENTION' },
            ].map((svc, i) => (
              <div key={i} className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                <div className="flex justify-between items-start">
                  <span className="font-mono text-sm font-semibold text-white">{svc.name}</span>
                  <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${svc.status === 'HEALTHY' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                    {svc.status}
                  </span>
                </div>
                <div className="flex justify-between text-xs text-slate-400">
                  <span>Target: {svc.slo}</span>
                  <span className="text-white font-semibold">Actual: {svc.actual}</span>
                </div>
                <div className="text-xs text-slate-400">
                  <span>Error Budget: </span>
                  <span className="text-emerald-400 font-semibold">{svc.budget}</span>
                </div>
                <div className="text-[11px] text-slate-500">1h Burn Rate: {svc.burn}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 6: Incident RCA & Governed Remediation */}
      {activeTab === 'incident_rca' && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-6">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <ShieldAlert className="h-5 w-5 text-indigo-400" />
              Automated Incident RCA & Governed Runbook Self-Healing
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              Separates FACT from HYPOTHESIS; blocks autonomous destructive commands without human gatekeeper approval.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* RCA Panel */}
            <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
              <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                <span className="text-xs font-bold text-red-400 flex items-center gap-1.5">
                  <AlertTriangle className="h-4 w-4" /> INC-4921: DB Connection Pool Exhaustion
                </span>
                <span className="text-xs text-slate-500">Detected 6m ago</span>
              </div>
              <div className="space-y-3 text-xs">
                <div>
                  <span className="text-slate-400 uppercase font-semibold text-[10px]">VERIFIED FACTS:</span>
                  <p className="text-slate-200 mt-1">
                    • 100% connection pool saturation on Postgres primary.<br />
                    • Recent commit 82a0b1 deployed in canary 12 minutes prior.
                  </p>
                </div>
                <div>
                  <span className="text-slate-400 uppercase font-semibold text-[10px]">AI HYPOTHESES (Confidence 92%):</span>
                  <p className="text-slate-200 mt-1">
                    • Unclosed cursor in bulk invoice export query leaking connections across worker pool.
                  </p>
                </div>
                <div>
                  <span className="text-slate-400 uppercase font-semibold text-[10px]">RECOMMENDED RUNBOOK:</span>
                  <p className="text-indigo-300 font-semibold mt-1">
                    RUNBOOK-402: Flush stale idle connections & scale connection pooler
                  </p>
                </div>
              </div>
            </div>

            {/* Governed Runbook Execution Gate */}
            <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
              <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                <span className="text-xs font-bold text-white flex items-center gap-1.5">
                  <Terminal className="h-4 w-4 text-indigo-400" /> Governed Self-Healing Approval Gate
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 font-semibold">
                  HUMAN APPROVAL REQUIRED
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Phase 67 security boundary: Autonomous production mutation blocked by default. Approver identity will be cryptographically logged to Phase 66 audit ledger.
              </p>
              <div className="p-3 rounded bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300">
                Action: pg_terminate_backend(pid) WHERE state = 'idle in transaction' &gt; 30s
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => setRemediationStatus('VERIFIED')}
                  className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center gap-1.5"
                >
                  <Check className="h-4 w-4" /> Approve & Execute Runbook
                </button>
                <button
                  onClick={() => setRemediationStatus('IDLE')}
                  className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition-colors"
                >
                  Reject Action
                </button>
              </div>
              {remediationStatus === 'VERIFIED' && (
                <div className="p-3 rounded bg-emerald-950/30 border border-emerald-500/40 text-xs text-emerald-400 flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4" /> Runbook executed successfully. Pool saturation restored to 14%. Postmortem draft generated.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
