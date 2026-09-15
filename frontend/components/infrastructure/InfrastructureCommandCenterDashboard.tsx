'use client';

import React, { useState } from 'react';
import {
  Server,
  Cloud,
  Cpu,
  Database,
  Layers,
  Activity,
  AlertTriangle,
  Play,
  CheckCircle2,
  XCircle,
  Clock,
  RotateCcw,
  Terminal,
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
  Settings,
  HardDrive,
  Network,
  Shield,
  RefreshCw,
  Sliders,
  Scale,
  Crosshair,
  TrendingDown
} from 'lucide-react';

export default function InfrastructureCommandCenterDashboard() {
  const [roleView, setRoleView] = useState<'executive' | 'platform' | 'sre' | 'cloud' | 'finops' | 'security' | 'operations'>('platform');
  const [activeTab, setActiveTab] = useState<'overview' | 'k8s_platform' | 'finops' | 'capacity_forecast' | 'blast_radius' | 'dr_failover' | 'agents'>('overview');

  // Cycle simulator state
  const [cycleRunning, setCycleRunning] = useState(false);
  const [cycleStep, setCycleStep] = useState(0);
  const [cycleResult, setCycleResult] = useState<any>(null);

  // Scaling simulator
  const [targetReplicas, setTargetReplicas] = useState(12);
  const [scalingStatus, setScalingStatus] = useState<'IDLE' | 'SIMULATING' | 'APPROVED' | 'SCALED'>('IDLE');

  // DR failover drill state
  const [drRunning, setDrRunning] = useState(false);
  const [drResult, setDrResult] = useState<any>(null);

  // FinOps recommendation approval state
  const [savingsAction, setSavingsAction] = useState<'PENDING' | 'SIMULATED' | 'APPLIED'>('PENDING');

  const infraKpis = [
    { label: 'Cloud Health Index', value: '99.98%', status: 'HEALTHY', change: '+0.04%' },
    { label: 'Active K8s Nodes', value: '184', status: 'STABLE', change: '8 Clusters' },
    { label: 'Monthly Cloud Spend', value: '$42,850', status: 'ON_BUDGET', change: '-12% vs Target' },
    { label: 'Forecasted Savings', value: '$7,420/mo', status: 'IDENTIFIED', change: '24 Recommendations' },
  ];

  const cycleSteps = [
    { id: 1, name: '1. Observe: Multi-Cloud Telemetry Ingestion', agent: 'CloudHealthAgent', status: 'COMPLETED', time: '1.2s' },
    { id: 2, name: '2. Understand: Knowledge Graph Impact Mapping', agent: 'InventoryAgent', status: 'COMPLETED', time: '1.8s' },
    { id: 3, name: '3. Plan: Safe Autoscaling & Right-Sizing Plan', agent: 'ScalingAgent', status: 'COMPLETED', time: '2.4s' },
    { id: 4, name: '4. Simulate: Blast Radius & Cost Diff Calculation', agent: 'CapacityAgent', status: 'COMPLETED', time: '1.5s' },
    { id: 5, name: '5. Approve: Phase 66 Zero-Trust Policy Verification', agent: 'GovernanceGate', status: 'COMPLETED', time: '0.9s' },
    { id: 6, name: '6. Provision: K8s HPA / IaC Reconciliation', agent: 'KubernetesAgent', status: 'COMPLETED', time: '3.1s' },
    { id: 7, name: '7. Monitor: SLO Budget & Error Rate Validation', agent: 'ReliabilityAgent', status: 'COMPLETED', time: '2.0s' },
    { id: 8, name: '8. Optimize: Idle Resource Reclamation & Tagging', agent: 'FinOpsAgent', status: 'COMPLETED', time: '1.7s' },
    { id: 9, name: '9. Recover: DR RPO/RTO Heartbeat & Snapshot Check', agent: 'DisasterRecoveryAgent', status: 'COMPLETED', time: '1.1s' },
    { id: 10, name: '10. Learn: Closed-Loop Capacity Model Calibration', agent: 'OrchestratorAgent', status: 'COMPLETED', time: '0.8s' },
  ];

  const runAutonomousCycle = () => {
    setCycleRunning(true);
    setCycleStep(1);
    setCycleResult(null);

    const interval = setInterval(() => {
      setCycleStep((prev) => {
        if (prev >= 10) {
          clearInterval(interval);
          setCycleRunning(false);
          setCycleResult({
            cycleId: 'cycle_infra_' + Math.floor(Math.random() * 9000 + 1000),
            status: 'HEALTHY_AND_BALANCED',
            duration: '16.5s',
            reclaimedCost: '$380 / month',
            safeReplicas: '14 Pods',
            blastRadius: 'Zero user degradation detected',
            governance: 'Signed by Phase 66 Guardrail',
          });
          return 10;
        }
        return prev + 1;
      });
    }, 400);
  };

  const simulateScaling = () => {
    setScalingStatus('SIMULATING');
    setTimeout(() => {
      setScalingStatus('APPROVED');
      setTimeout(() => {
        setScalingStatus('SCALED');
      }, 1000);
    }, 1200);
  };

  const triggerDrill = () => {
    setDrRunning(true);
    setTimeout(() => {
      setDrRunning(false);
      setDrResult({
        drillId: 'dr_drill_' + Math.floor(Math.random() * 9000 + 1000),
        primaryRegion: 'us-east-1',
        secondaryRegion: 'us-west-2',
        measuredRpo: '42 seconds (Target: < 5 mins)',
        measuredRto: '3.4 minutes (Target: < 15 mins)',
        dataIntegrity: '100% Bit-for-Bit Verified',
        status: 'PASSED_CERTIFIED'
      });
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 backdrop-blur shadow-2xl">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-400">
              <Cloud className="w-7 h-7" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Cloud Operating System & Autonomous Infrastructure
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  Phase 68 Live
                </span>
              </h1>
              <p className="text-sm text-slate-400 mt-1">
                Zero-Trust Multi-Cloud Abstraction • Kubernetes Intelligence • Autonomous FinOps • Governed Blast Radius
              </p>
            </div>
          </div>
        </div>

        {/* Role Switcher */}
        <div className="flex items-center gap-2 bg-slate-950/60 p-1.5 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 font-medium px-2">Role View:</span>
          {(['executive', 'platform', 'sre', 'cloud', 'finops', 'security', 'operations'] as const).map((role) => (
            <button
              key={role}
              onClick={() => setRoleView(role)}
              className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all capitalize ${
                roleView === role
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              {role}
            </button>
          ))}
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {infraKpis.map((kpi, idx) => (
          <div key={idx} className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-xl shadow-lg relative overflow-hidden">
            <div className="text-xs text-slate-400 font-medium">{kpi.label}</div>
            <div className="text-2xl font-bold text-white mt-1">{kpi.value}</div>
            <div className="flex items-center justify-between mt-3 text-xs">
              <span className="text-emerald-400 font-semibold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> {kpi.status}
              </span>
              <span className="text-slate-400">{kpi.change}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'overview', label: 'Command Center', icon: Activity },
          { id: 'k8s_platform', label: 'Kubernetes Intelligence', icon: Server },
          { id: 'finops', label: 'Autonomous FinOps', icon: DollarSign },
          { id: 'capacity_forecast', label: 'Capacity & GPU Intelligence', icon: Cpu },
          { id: 'blast_radius', label: 'Blast Radius Simulator', icon: Crosshair },
          { id: 'dr_failover', label: 'Disaster Recovery & Backup', icon: RotateCcw },
          { id: 'agents', label: '18 Infrastructure Agents', icon: Sparkles },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-all ${
                activeTab === tab.id
                  ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab: Overview (Autonomous Cycle Engine) */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Workflow className="w-5 h-5 text-indigo-400" />
                  10-Stage Autonomous Cloud Operating Cycle
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Observe → Understand → Plan → Simulate → Approve → Provision → Monitor → Optimize → Recover → Learn
                </p>
              </div>
              <button
                disabled={cycleRunning}
                onClick={runAutonomousCycle}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold text-white transition-all ${
                  cycleRunning
                    ? 'bg-slate-700 cursor-not-allowed text-slate-400'
                    : 'bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/30'
                }`}
              >
                {cycleRunning ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" /> Running Autonomous Cycle...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" /> Trigger Optimization Cycle
                  </>
                )}
              </button>
            </div>

            {/* Steps Visualizer */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3">
              {cycleSteps.map((step) => {
                const isActive = cycleRunning && cycleStep === step.id;
                const isPassed = cycleStep > step.id || (!cycleRunning && cycleResult);
                return (
                  <div
                    key={step.id}
                    className={`p-3.5 rounded-xl border transition-all ${
                      isActive
                        ? 'bg-indigo-950/60 border-indigo-500 text-indigo-200 ring-2 ring-indigo-500/30'
                        : isPassed
                        ? 'bg-emerald-950/30 border-emerald-500/40 text-emerald-200'
                        : 'bg-slate-950/40 border-slate-800/80 text-slate-400'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs mb-1">
                      <span className="font-semibold">{step.id}</span>
                      {isPassed ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      ) : isActive ? (
                        <RefreshCw className="w-4 h-4 animate-spin text-indigo-400" />
                      ) : (
                        <Clock className="w-3.5 h-3.5 text-slate-500" />
                      )}
                    </div>
                    <div className="text-xs font-medium line-clamp-2">{step.name}</div>
                    <div className="text-[11px] text-slate-500 mt-2 flex justify-between">
                      <span>{step.agent}</span>
                      <span>{step.time}</span>
                    </div>
                  </div>
                );
              })}
            </div>

            {cycleResult && (
              <div className="mt-6 p-4 rounded-xl bg-emerald-950/40 border border-emerald-500/40 flex items-center justify-between">
                <div>
                  <div className="text-sm font-bold text-emerald-300 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4" /> Cycle Completed: {cycleResult.status}
                  </div>
                  <div className="text-xs text-slate-300 mt-1 flex gap-4">
                    <span>Cycle ID: <b>{cycleResult.cycleId}</b></span>
                    <span>Reclaimed Cost: <b>{cycleResult.reclaimedCost}</b></span>
                    <span>Safe Sizing: <b>{cycleResult.safeReplicas}</b></span>
                    <span>Guardrail: <b>{cycleResult.governance}</b></span>
                  </div>
                </div>
                <span className="text-xs font-mono px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-lg">
                  {cycleResult.duration}
                </span>
              </div>
            )}
          </div>

          {/* Multi-Cloud Inventory Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-3">
                <Cloud className="w-4 h-4 text-sky-400" /> Multi-Cloud Provider Fleet
              </h3>
              <div className="space-y-2.5 text-xs">
                <div className="flex justify-between items-center p-2.5 bg-slate-950/60 rounded-xl border border-slate-800">
                  <span className="font-semibold text-slate-200">AWS (Production Core)</span>
                  <span className="text-emerald-400 font-mono">us-east-1, eu-west-1</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-950/60 rounded-xl border border-slate-800">
                  <span className="font-semibold text-slate-200">GCP (AI & BigQuery Lake)</span>
                  <span className="text-emerald-400 font-mono">us-central1</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-950/60 rounded-xl border border-slate-800">
                  <span className="font-semibold text-slate-200">Azure (Enterprise Identity)</span>
                  <span className="text-emerald-400 font-mono">eastus2</span>
                </div>
              </div>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-3">
                <Shield className="w-4 h-4 text-emerald-400" /> Phase 66 Zero-Trust Gate
              </h3>
              <div className="space-y-2 text-xs text-slate-300">
                <p className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-emerald-400" /> Cloud Credential Vault: Encrypted at Rest
                </p>
                <p className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-emerald-400" /> Destructive Production Deletion: Blocked
                </p>
                <p className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-emerald-400" /> RBAC / ABAC Role-Scoped Action Engine
                </p>
                <p className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-emerald-400" /> Immutable Audit Event Trail Active
                </p>
              </div>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-3">
                <Gauge className="w-4 h-4 text-amber-400" /> Active SRE Error Budgets
              </h3>
              <div className="space-y-2.5 text-xs">
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-300">API Gateway 99.95% SLO</span>
                    <span className="text-emerald-400 font-mono">92% remaining</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5">
                    <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: '92%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-300">Inference Runtime 99.90% SLO</span>
                    <span className="text-amber-400 font-mono">81% remaining</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5">
                    <div className="bg-amber-500 h-1.5 rounded-full" style={{ width: '81%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Kubernetes Intelligence */}
      {activeTab === 'k8s_platform' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Server className="w-5 h-5 text-indigo-400" />
                  Kubernetes Cluster & Workload Fleet
                </h3>
                <p className="text-xs text-slate-400">
                  Real-time node pressure, pod crash loops, and autonomous HPA / VPA autoscaling
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-slate-400">Workload Target:</span>
                <input
                  type="number"
                  value={targetReplicas}
                  onChange={(e) => setTargetReplicas(Number(e.target.value))}
                  className="w-16 px-2 py-1 bg-slate-950 border border-slate-700 rounded-lg text-xs text-white"
                />
                <button
                  onClick={simulateScaling}
                  disabled={scalingStatus === 'SIMULATING'}
                  className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white rounded-lg transition-all"
                >
                  {scalingStatus === 'SIMULATING' ? 'Simulating...' : 'Safe Scale Workload'}
                </button>
              </div>
            </div>

            {scalingStatus === 'SCALED' && (
              <div className="p-3 mb-4 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-xs text-emerald-300 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" /> Workload scaled to {targetReplicas} replicas safely after passing capacity and blast-radius checks.
              </div>
            )}

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="text-[11px] uppercase bg-slate-950/80 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-3">Cluster</th>
                    <th className="p-3">Node Count</th>
                    <th className="p-3">CPU Usage</th>
                    <th className="p-3">Memory Pressure</th>
                    <th className="p-3">Crash Loop Pods</th>
                    <th className="p-3">Health Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  <tr className="hover:bg-slate-800/30">
                    <td className="p-3 font-semibold text-white">prod-k8s-us-east-1</td>
                    <td className="p-3">64 Nodes</td>
                    <td className="p-3 text-emerald-400 font-mono">68.4%</td>
                    <td className="p-3 text-slate-300 font-mono">71.2% (Normal)</td>
                    <td className="p-3 text-emerald-400 font-mono">0</td>
                    <td className="p-3"><span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-semibold">HEALTHY</span></td>
                  </tr>
                  <tr className="hover:bg-slate-800/30">
                    <td className="p-3 font-semibold text-white">ai-infer-gpu-us-central1</td>
                    <td className="p-3">28 Nodes (A100/H100)</td>
                    <td className="p-3 text-amber-400 font-mono">89.2%</td>
                    <td className="p-3 text-amber-400 font-mono">82.5% (High)</td>
                    <td className="p-3 text-emerald-400 font-mono">0</td>
                    <td className="p-3"><span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 font-semibold">LOADED</span></td>
                  </tr>
                  <tr className="hover:bg-slate-800/30">
                    <td className="p-3 font-semibold text-white">staging-k8s-eu-west-1</td>
                    <td className="p-3">12 Nodes</td>
                    <td className="p-3 text-emerald-400 font-mono">31.0%</td>
                    <td className="p-3 text-slate-300 font-mono">38.4% (Normal)</td>
                    <td className="p-3 text-emerald-400 font-mono">0</td>
                    <td className="p-3"><span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-semibold">HEALTHY</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Autonomous FinOps */}
      {activeTab === 'finops' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <DollarSign className="w-5 h-5 text-emerald-400" />
                  FinOps Intelligence & Cost Allocation
                </h3>
                <p className="text-xs text-slate-400">
                  Unit economics, idle resource reclamation, rightsizing, and savings plans
                </p>
              </div>
              <button
                onClick={() => setSavingsAction(savingsAction === 'PENDING' ? 'SIMULATED' : 'APPLIED')}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-xs font-semibold text-white rounded-xl shadow-lg transition-all"
              >
                {savingsAction === 'PENDING' && 'Simulate Idle Reclamation'}
                {savingsAction === 'SIMULATED' && 'Authorize Governed Rightsizing'}
                {savingsAction === 'APPLIED' && 'Rightsizing Complete (-$7,420/mo)'}
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="text-xs text-slate-400">Unit Cost / API Request</div>
                <div className="text-xl font-bold text-white mt-1">$0.000142</div>
                <div className="text-xs text-emerald-400 mt-1">-8.4% this quarter</div>
              </div>
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="text-xs text-slate-400">Unit Cost / AI Model Task</div>
                <div className="text-xl font-bold text-white mt-1">$0.00391</div>
                <div className="text-xs text-emerald-400 mt-1">-14.2% via GPU batching</div>
              </div>
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="text-xs text-slate-400">Identified Monthly Waste</div>
                <div className="text-xl font-bold text-amber-400 mt-1">$7,420.00</div>
                <div className="text-xs text-slate-400 mt-1">14 unattached EBS + 6 idle RDS</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Capacity & GPU Intelligence */}
      {activeTab === 'capacity_forecast' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2 mb-2">
              <Cpu className="w-5 h-5 text-indigo-400" />
              90-Day Predictive Capacity & GPU Scheduling
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              AI-assisted demand extrapolation across CPU, RAM, NVMe storage, and Tensor GPU memory
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <h4 className="text-xs font-bold text-white mb-3">GPU Workload Queues (A100/H100)</h4>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-300">
                    <span>LLM Fine-Tuning Cluster</span>
                    <span className="font-mono text-emerald-400">100% Utilized (32 GPUs)</span>
                  </div>
                  <div className="flex justify-between text-slate-300">
                    <span>Agent Real-Time Inference</span>
                    <span className="font-mono text-indigo-400">74% Utilized (16 GPUs)</span>
                  </div>
                  <div className="flex justify-between text-slate-300">
                    <span>Embedding Vector Generation</span>
                    <span className="font-mono text-sky-400">45% Utilized (8 GPUs)</span>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <h4 className="text-xs font-bold text-white mb-3">Headroom & Exhaustion Horizon</h4>
                <div className="space-y-2 text-xs text-slate-300">
                  <div className="flex justify-between">
                    <span>Kubernetes Cluster Headroom:</span>
                    <span className="font-semibold text-emerald-400">42 Days at current rate</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Primary Database IOPS Headroom:</span>
                    <span className="font-semibold text-emerald-400">86 Days</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Object Storage Growth Rate:</span>
                    <span className="font-semibold text-slate-300">+2.4 TB / month</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Blast Radius Simulator */}
      {activeTab === 'blast_radius' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2 mb-2">
              <Crosshair className="w-5 h-5 text-indigo-400" />
              Deterministic Blast Radius & Impact Simulator
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              Simulate proposed configuration mutations against the full dependency graph before applying changes
            </p>

            <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800 space-y-3 text-xs">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Target Resource:</span>
                <span className="font-mono text-white font-semibold">aurora-pg-cluster-prod-01</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Proposed Action:</span>
                <span className="font-mono text-amber-400">Failover to Replica B (Dry-Run)</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Affected Upstream Services:</span>
                <span className="font-mono text-indigo-300">order-service, auth-api, billing-engine (3)</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Estimated Latency Blip:</span>
                <span className="font-mono text-emerald-400">&lt; 350 ms</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Safety Verdict:</span>
                <span className="px-2.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-semibold">
                  APPROVED_SAFE_FOR_MAINTENANCE_WINDOW
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Disaster Recovery */}
      {activeTab === 'dr_failover' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <RotateCcw className="w-5 h-5 text-sky-400" />
                  Disaster Recovery & Automated Backup Validation
                </h3>
                <p className="text-xs text-slate-400">
                  Continuous backup verification, sandbox restore tests, and cross-region RPO/RTO validation
                </p>
              </div>
              <button
                onClick={triggerDrill}
                disabled={drRunning}
                className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-xs font-semibold text-white rounded-xl shadow-lg transition-all"
              >
                {drRunning ? 'Simulating Failover...' : 'Execute Live DR Drill'}
              </button>
            </div>

            {drResult && (
              <div className="p-4 rounded-xl bg-sky-950/40 border border-sky-500/40 space-y-2 text-xs">
                <div className="text-sm font-bold text-sky-300 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4" /> DR Drill Result: {drResult.status}
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-slate-300">
                  <div>RPO: <b>{drResult.measuredRpo}</b></div>
                  <div>RTO: <b>{drResult.measuredRto}</b></div>
                  <div>Integrity: <b>{drResult.dataIntegrity}</b></div>
                  <div>Secondary: <b>{drResult.secondaryRegion}</b></div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab: 18 Autonomous Agents */}
      {activeTab === 'agents' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { name: 'InfrastructureOrchestrator', role: 'Closed-loop 10-stage execution coordinator' },
            { name: 'InventoryAgent', role: 'Continuous multi-cloud asset cataloging' },
            { name: 'CloudHealthAgent', role: 'Availability & anomaly scoring engine' },
            { name: 'KubernetesAgent', role: 'Cluster topology & pod life-cycle intelligence' },
            { name: 'ScalingAgent', role: 'Policy-governed HPA / VPA autoscaling' },
            { name: 'CapacityAgent', role: 'Predictive 90-day resource forecast' },
            { name: 'FinOpsAgent', role: 'Right-sizing & unit-cost attribution' },
            { name: 'CostAnomalyAgent', role: 'Real-time spike & leak detection' },
            { name: 'NetworkAgent', role: 'VPC topology & cross-AZ egress optimizer' },
            { name: 'StorageAgent', role: 'Volume tiering & snapshot reclamation' },
            { name: 'DatabaseInfrastructureAgent', role: 'IOPS & connection pool tuning' },
            { name: 'GpuAgent', role: 'Tensor memory & inference queue scheduler' },
            { name: 'DriftAgent', role: 'IaC vs real-state continuous diff' },
            { name: 'ReliabilityAgent', role: 'SLO tracking & error budget protector' },
            { name: 'DisasterRecoveryAgent', role: 'RPO/RTO validation & drill execution' },
            { name: 'OptimizationAgent', role: 'End-to-end self-healing engine' },
            { name: 'IncidentAgent', role: 'Automated triage & blast radius bounding' },
            { name: 'RemediationAgent', role: 'Governed runbook application' },
          ].map((agent, idx) => (
            <div key={idx} className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold text-white">{agent.name}</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 font-semibold">
                  ACTIVE
                </span>
              </div>
              <div className="text-xs text-slate-400">{agent.role}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
