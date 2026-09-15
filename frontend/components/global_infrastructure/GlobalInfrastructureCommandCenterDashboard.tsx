'use client';

import React, { useState } from 'react';
import {
  Globe,
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
  TrendingDown,
  Radio,
  MapPin,
  Compass,
  Thermometer,
  BatteryCharging
} from 'lucide-react';

export default function GlobalInfrastructureCommandCenterDashboard() {
  const [roleView, setRoleView] = useState<'executive' | 'global_sre' | 'dc_ops' | 'edge_architect' | 'network_engineer'>('global_sre');
  const [activeTab, setActiveTab] = useState<'overview' | 'global_map' | 'data_centers' | 'edge_computing' | 'traffic_steering' | 'chaos_dr' | 'digital_twin' | 'agents'>('overview');

  // Planetary Cycle Simulator
  const [cycleRunning, setCycleRunning] = useState(false);
  const [cycleStep, setCycleStep] = useState(0);
  const [cycleResult, setCycleResult] = useState<any>(null);

  // Traffic shift simulator state
  const [trafficShiftPct, setTrafficShiftPct] = useState(25);
  const [shiftStatus, setShiftStatus] = useState<'IDLE' | 'SIMULATING' | 'APPROVED' | 'DIVERTED'>('IDLE');

  // Chaos injection state
  const [chaosRunning, setChaosRunning] = useState(false);
  const [chaosResult, setChaosResult] = useState<any>(null);

  // What-If Simulator state
  const [whatIfScenario, setWhatIfScenario] = useState('DATACENTER_IAD_OUTAGE');
  const [simRunning, setSimRunning] = useState(false);
  const [simResult, setSimResult] = useState<any>(null);

  const planetaryKpis = [
    { label: 'Global Health Score', value: '99.4%', status: 'OPTIMAL', change: '+0.12%' },
    { label: 'Planetary Ingress RPS', value: '142,000 /s', status: 'PEAK_LOAD', change: '84.6 Gbps' },
    { label: 'Avg Global Latency (p95)', value: '22.4 ms', status: 'WITHIN_SLO', change: 'p99: 108ms' },
    { label: 'Avg Data Center PUE', value: '1.15', status: 'TIER_4_EFFICIENCY', change: '86% Renewable' },
  ];

  const planetaryCycleSteps = [
    { id: 1, name: '1. Observe: Continental Ingress & BGP Latency', agent: 'RegionHealthAgent', time: '1.4s' },
    { id: 2, name: '2. Understand: Cross-Region Topology Mapping', agent: 'GlobalNetworkAgent', time: '1.8s' },
    { id: 3, name: '3. Predict: Predictive Hardware Failure & SMART', agent: 'HardwareAgent', time: '2.1s' },
    { id: 4, name: '4. Simulate: Digital Twin Disaster Scenario', agent: 'DigitalTwinService', time: '1.6s' },
    { id: 5, name: '5. Plan: 7-Factor Workload Placement Matrix', agent: 'PlacementAgent', time: '2.5s' },
    { id: 6, name: '6. Policy Check: Zero-Trust Blast Radius Gate', agent: 'ValidationService', time: '0.8s' },
    { id: 7, name: '7. Approval: Two-Person Rule Gatekeeper', agent: 'IncidentCommander', time: '1.1s' },
    { id: 8, name: '8. Execute: Dynamic Anycast Steering Shift', agent: 'TrafficAgent', time: '3.2s' },
    { id: 9, name: '9. Verify: Distributed SLO & Error Budget', agent: 'GlobalReliabilityAgent', time: '1.9s' },
    { id: 10, name: '10. Optimize: Thermal Cooling & PUE Tuning', agent: 'EnergyAgent', time: '1.5s' },
    { id: 11, name: '11. Recover: Multi-Region RPO/RTO Checkpoint', agent: 'DisasterRecoveryAgent', time: '1.2s' },
    { id: 12, name: '12. Learn: Planetary Closed-Loop Calibration', agent: 'GlobalOrchestrator', time: '0.9s' },
  ];

  const runPlanetaryCycle = () => {
    setCycleRunning(true);
    setCycleStep(1);
    setCycleResult(null);

    const interval = setInterval(() => {
      setCycleStep((prev) => {
        if (prev >= 12) {
          clearInterval(interval);
          setCycleRunning(false);
          setCycleResult({
            cycleId: 'cyc_global_' + Math.floor(Math.random() * 9000 + 1000),
            status: 'PLANETARY_EQUILIBRIUM_VERIFIED',
            duration: '21.4s',
            divertedCapacity: '0.0% Deficit',
            measuredRpo: '18 seconds',
            measuredRto: '184 seconds',
            governance: 'Verified via Phase 66 Zero-Trust Boundary',
          });
          return 12;
        }
        return prev + 1;
      });
    }, 380);
  };

  const simulateTrafficShift = () => {
    setShiftStatus('SIMULATING');
    setTimeout(() => {
      setShiftStatus('APPROVED');
      setTimeout(() => {
        setShiftStatus('DIVERTED');
      }, 1000);
    }, 1200);
  };

  const runChaosInjection = () => {
    setChaosRunning(true);
    setTimeout(() => {
      setChaosRunning(false);
      setChaosResult({
        experimentId: 'exp_chaos_' + Math.floor(Math.random() * 9000 + 1000),
        faultType: 'PACKET_LOSS_INJECTION',
        targetRegion: 'eu-west-1',
        blastRadius: '3.4% of non-critical traffic',
        recoveryTime: '4.2 seconds via BGP Anycast fallback',
        status: 'PASSED_RESILIENT'
      });
    }, 1500);
  };

  const runWhatIfSimulation = () => {
    setSimRunning(true);
    setTimeout(() => {
      setSimRunning(false);
      setSimResult({
        scenario: whatIfScenario,
        survivingCapacity: '82.4%',
        impactedUsers: '0.0% (Zero dropped requests)',
        estimatedRto: '3.1 minutes',
        costImpact: '+$480/day burst capacity',
        verdict: 'SAFE_AND_CONTAINED'
      });
    }, 1400);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 backdrop-blur shadow-2xl">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-sky-500/10 border border-sky-500/20 rounded-xl text-sky-400">
              <Globe className="w-7 h-7" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Global Infrastructure & Planet-Scale Reliability
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">
                  Phase 69 Live
                </span>
              </h1>
              <p className="text-sm text-slate-400 mt-1">
                Data Center Facilities • Edge Computing • Planet-Scale Traffic • Digital Twin • Chaos Resilience
              </p>
            </div>
          </div>
        </div>

        {/* Role Switcher */}
        <div className="flex items-center gap-2 bg-slate-950/60 p-1.5 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 font-medium px-2">Role:</span>
          {(['executive', 'global_sre', 'dc_ops', 'edge_architect', 'network_engineer'] as const).map((role) => (
            <button
              key={role}
              onClick={() => setRoleView(role)}
              className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all capitalize ${
                roleView === role
                  ? 'bg-sky-600 text-white shadow-md shadow-sky-600/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              {role.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {planetaryKpis.map((kpi, idx) => (
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
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: 'overview', label: 'Planetary Operating Loop', icon: Activity },
          { id: 'global_map', label: 'Global Map & POPs', icon: Globe },
          { id: 'data_centers', label: 'Data Centers & PUE', icon: Server },
          { id: 'edge_computing', label: 'Edge Nodes & Fleet', icon: Radio },
          { id: 'traffic_steering', label: 'Global Traffic Steering', icon: Network },
          { id: 'chaos_dr', label: 'Chaos & Failover Drills', icon: Zap },
          { id: 'digital_twin', label: 'Digital Twin What-If', icon: Crosshair },
          { id: 'agents', label: '20 Planetary Agents', icon: Sparkles },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-sky-600/20 text-sky-400 border border-sky-500/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab: Overview (12-Stage Planetary Loop) */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Workflow className="w-5 h-5 text-sky-400" />
                  12-Stage Closed-Loop Planet-Scale Operating Cycle
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Observe → Understand → Predict → Simulate → Plan → Policy Check → Approval → Execute → Verify → Optimize → Recover → Learn
                </p>
              </div>
              <button
                disabled={cycleRunning}
                onClick={runPlanetaryCycle}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold text-white transition-all ${
                  cycleRunning
                    ? 'bg-slate-700 cursor-not-allowed text-slate-400'
                    : 'bg-sky-600 hover:bg-sky-500 shadow-lg shadow-sky-600/30'
                }`}
              >
                {cycleRunning ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" /> Executing Planet-Scale Cycle...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" /> Trigger Planetary Cycle
                  </>
                )}
              </button>
            </div>

            {/* Steps Visualizer */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-3">
              {planetaryCycleSteps.map((step) => {
                const isActive = cycleRunning && cycleStep === step.id;
                const isPassed = cycleStep > step.id || (!cycleRunning && cycleResult);
                return (
                  <div
                    key={step.id}
                    className={`p-3 rounded-xl border transition-all ${
                      isActive
                        ? 'bg-sky-950/60 border-sky-500 text-sky-200 ring-2 ring-sky-500/30'
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
                        <RefreshCw className="w-4 h-4 animate-spin text-sky-400" />
                      ) : (
                        <Clock className="w-3.5 h-3.5 text-slate-500" />
                      )}
                    </div>
                    <div className="text-xs font-medium line-clamp-2">{step.name}</div>
                    <div className="text-[10px] text-slate-500 mt-2 flex justify-between">
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
                    <CheckCircle2 className="w-4 h-4" /> Planetary Cycle Completed: {cycleResult.status}
                  </div>
                  <div className="text-xs text-slate-300 mt-1 flex gap-4">
                    <span>Cycle ID: <b>{cycleResult.cycleId}</b></span>
                    <span>Deficit: <b>{cycleResult.divertedCapacity}</b></span>
                    <span>Verified RPO: <b>{cycleResult.measuredRpo}</b></span>
                    <span>Guardrail: <b>{cycleResult.governance}</b></span>
                  </div>
                </div>
                <span className="text-xs font-mono px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-lg">
                  {cycleResult.duration}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab: Global Map & POPs */}
      {activeTab === 'global_map' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2 mb-2">
              <Globe className="w-5 h-5 text-sky-400" />
              Planetary Topological Presence & Transit Latencies
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              Global backbone transits connecting 3 Cloud Regions, 2 Physical Data Centers, and 42 Edge Metro POPs
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-white">Americas Core (IAD Hub)</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-semibold">ONLINE</span>
                </div>
                <div className="text-xs text-slate-400 space-y-1">
                  <div>Facilities: Equinix Ashburn Campus (DC-IAD-01)</div>
                  <div>Edge POPs: NYC, CHI, MIA, SFO, LAX (14 POPs)</div>
                  <div>P95 Transit Latency: <b className="text-emerald-400">11.2 ms</b></div>
                </div>
              </div>

              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-white">Europe Core (FRA Hub)</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-semibold">ONLINE</span>
                </div>
                <div className="text-xs text-slate-400 space-y-1">
                  <div>Facilities: Interxion Frankfurt (DC-FRA-01)</div>
                  <div>Edge POPs: LHR, CDG, AMS, MXP, MAD (16 POPs)</div>
                  <div>P95 Transit Latency: <b className="text-emerald-400">14.8 ms</b></div>
                </div>
              </div>

              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-white">Asia-Pacific Hub (NRT / TPE)</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-semibold">ONLINE</span>
                </div>
                <div className="text-xs text-slate-400 space-y-1">
                  <div>Facilities: Google Cloud Asia-East1 + Colocation</div>
                  <div>Edge POPs: TYO, SIN, HKG, SYD (12 POPs)</div>
                  <div>P95 Transit Latency: <b className="text-emerald-400">24.5 ms</b></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Data Centers & PUE */}
      {activeTab === 'data_centers' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2 mb-2">
              <Server className="w-5 h-5 text-sky-400" />
              Physical Data Center Telemetry & PUE Optimization
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              Thermal loads, rack capacities, Power Usage Effectiveness, and predictive SMART hardware diagnostics
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="p-5 bg-slate-950/60 rounded-xl border border-slate-800 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Facility:</span>
                  <span className="text-xs font-bold text-white">Equinix Ashburn (DC-IAD-01)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Power Usage Effectiveness (PUE):</span>
                  <span className="text-xs font-mono font-bold text-emerald-400">1.16 (Elite Tier)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Active Power Draw:</span>
                  <span className="text-xs font-mono text-slate-200">2,840 kW / 4,500 kW (63.1%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Average Ambient Temperature:</span>
                  <span className="text-xs font-mono text-emerald-400">21.2 °C (In-Range)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">30-Day Hardware Failure Risk:</span>
                  <span className="text-xs font-mono text-emerald-400">0.008 (Low Risk)</span>
                </div>
              </div>

              <div className="p-5 bg-slate-950/60 rounded-xl border border-slate-800 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Facility:</span>
                  <span className="text-xs font-bold text-white">Interxion Frankfurt (DC-FRA-01)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Power Usage Effectiveness (PUE):</span>
                  <span className="text-xs font-mono font-bold text-emerald-400">1.14 (Elite Tier)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Active Power Draw:</span>
                  <span className="text-xs font-mono text-slate-200">2,100 kW / 3,200 kW (65.6%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Average Ambient Temperature:</span>
                  <span className="text-xs font-mono text-emerald-400">20.8 °C (In-Range)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Renewable Energy Mix:</span>
                  <span className="text-xs font-mono text-emerald-400">92.4% Hydro & Wind</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Edge Computing */}
      {activeTab === 'edge_computing' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2 mb-2">
              <Radio className="w-5 h-5 text-sky-400" />
              Distributed Edge Computing Fleet & Offline Synchronization
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              Sub-10ms edge processing, local state reconciliation, and 2,500+ managed device endpoints
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="text-xs text-slate-400">Edge POPs Active</div>
                <div className="text-2xl font-bold text-white mt-1">42 Locations</div>
                <div className="text-xs text-emerald-400 mt-2">100% Online</div>
              </div>

              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="text-xs text-slate-400">Connected Device Fleet</div>
                <div className="text-2xl font-bold text-white mt-1">2,480 Gateways</div>
                <div className="text-xs text-slate-400 mt-2">99.6% Compliance</div>
              </div>

              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="text-xs text-slate-400">Edge Offline Buffer Queues</div>
                <div className="text-2xl font-bold text-emerald-400 mt-1">0 Events Queued</div>
                <div className="text-xs text-slate-400 mt-2">Real-time In Sync</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Global Traffic Steering */}
      {activeTab === 'traffic_steering' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Network className="w-5 h-5 text-sky-400" />
                  Policy-Driven Global Traffic Steering & Evacuation
                </h3>
                <p className="text-xs text-slate-400">
                  Perform controlled traffic migrations with capacity validation and SLO error budget preservation
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-slate-400">Shift Volume:</span>
                <input
                  type="number"
                  value={trafficShiftPct}
                  onChange={(e) => setTrafficShiftPct(Number(e.target.value))}
                  className="w-16 px-2 py-1 bg-slate-950 border border-slate-700 rounded-lg text-xs text-white"
                />
                <span className="text-xs text-slate-400">%</span>
                <button
                  onClick={simulateTrafficShift}
                  disabled={shiftStatus === 'SIMULATING'}
                  className="px-3.5 py-1.5 bg-sky-600 hover:bg-sky-500 text-xs font-semibold text-white rounded-lg transition-all"
                >
                  {shiftStatus === 'SIMULATING' ? 'Simulating...' : 'Simulate Traffic Shift'}
                </button>
              </div>
            </div>

            {shiftStatus === 'DIVERTED' && (
              <div className="p-3 mb-4 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-xs text-emerald-300 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" /> Shift of {trafficShiftPct}% traffic simulated safely with 0% latency penalty and verified destination headroom.
              </div>
            )}

            <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800 space-y-2 text-xs text-slate-300">
              <div className="flex justify-between">
                <span>Active Routing Strategy:</span>
                <span className="font-semibold text-emerald-400 font-mono">LATENCY_OPTIMIZED_ANYCAST</span>
              </div>
              <div className="flex justify-between">
                <span>Failover Latency Threshold:</span>
                <span className="font-semibold text-slate-200 font-mono">220 ms</span>
              </div>
              <div className="flex justify-between">
                <span>Data Residency Filter:</span>
                <span className="font-semibold text-sky-300 font-mono">GDPR_EU_STRICT_PINNING_ENABLED</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Chaos & Failover Drills */}
      {activeTab === 'chaos_dr' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Zap className="w-5 h-5 text-amber-400" />
                  Controlled Chaos Engineering & Planetary DR Readiness
                </h3>
                <p className="text-xs text-slate-400">
                  Fault injection under blast-radius bounds with automatic abort trip gates
                </p>
              </div>
              <button
                onClick={runChaosInjection}
                disabled={chaosRunning}
                className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-xs font-semibold text-white rounded-xl shadow-lg transition-all"
              >
                {chaosRunning ? 'Injecting Chaos Fault...' : 'Run Chaos Experiment'}
              </button>
            </div>

            {chaosResult && (
              <div className="p-4 rounded-xl bg-amber-950/40 border border-amber-500/40 space-y-2 text-xs">
                <div className="text-sm font-bold text-amber-300 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4" /> Chaos Experiment Completed: {chaosResult.status}
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-slate-300">
                  <div>Fault: <b>{chaosResult.faultType}</b></div>
                  <div>Target: <b>{chaosResult.targetRegion}</b></div>
                  <div>Blast Radius: <b>{chaosResult.blastRadius}</b></div>
                  <div>Recovery: <b>{chaosResult.recoveryTime}</b></div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab: Digital Twin What-If */}
      {activeTab === 'digital_twin' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Crosshair className="w-5 h-5 text-sky-400" />
                  Planet-Scale Digital Twin & What-If Engine
                </h3>
                <p className="text-xs text-slate-400">
                  Simulate hypothetical regional blackouts, traffic surges, and GPU hardware supply shocks
                </p>
              </div>
              <div className="flex items-center gap-3">
                <select
                  value={whatIfScenario}
                  onChange={(e) => setWhatIfScenario(e.target.value)}
                  className="px-3 py-1.5 bg-slate-950 border border-slate-700 rounded-lg text-xs text-white"
                >
                  <option value="DATACENTER_IAD_OUTAGE">What if Equinix Ashburn (DC-IAD-01) suffers a blackout?</option>
                  <option value="TRAFFIC_DOUBLING_PEAK">What if European traffic doubles during peak hours?</option>
                  <option value="SUBSEA_CABLE_CUT">What if transatlantic undersea fiber cuts?</option>
                </select>
                <button
                  onClick={runWhatIfSimulation}
                  disabled={simRunning}
                  className="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-xs font-semibold text-white rounded-lg transition-all"
                >
                  {simRunning ? 'Simulating...' : 'Run What-If Simulation'}
                </button>
              </div>
            </div>

            {simResult && (
              <div className="p-4 rounded-xl bg-sky-950/40 border border-sky-500/40 space-y-2 text-xs">
                <div className="text-sm font-bold text-sky-300 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4" /> Simulation Result: {simResult.verdict}
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-slate-300">
                  <div>Surviving Capacity: <b>{simResult.survivingCapacity}</b></div>
                  <div>Impacted Users: <b>{simResult.impactedUsers}</b></div>
                  <div>Projected RTO: <b>{simResult.estimatedRto}</b></div>
                  <div>Cost Delta: <b>{simResult.costImpact}</b></div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab: 20 Planetary Agents */}
      {activeTab === 'agents' && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            { name: 'GlobalOrchestratorAgent', role: '12-stage planetary loop coordinator' },
            { name: 'RegionHealthAgent', role: 'Multi-cloud regional interconnect telemetry' },
            { name: 'DataCenterAgent', role: 'Power usage effectiveness (PUE) & cooling' },
            { name: 'EdgeAgent', role: 'Offline queuing & POP synchronization' },
            { name: 'HardwareAgent', role: 'Bare-metal SMART failure prediction' },
            { name: 'GlobalNetworkAgent', role: 'Planetary backbone transit & BGP health' },
            { name: 'TrafficAgent', role: 'Policy-driven geo-steering & Anycast' },
            { name: 'LatencyAgent', role: 'Empirical p50/p95/p99 latency matrices' },
            { name: 'GlobalCapacityAgent', role: 'Multi-region headroom & exhaustion' },
            { name: 'PlacementAgent', role: '7-factor multi-objective placement' },
            { name: 'MigrationAgent', role: 'Zero-downtime cross-region migration' },
            { name: 'ReplicationAgent', role: 'Cross-region DB replication & lag' },
            { name: 'ConsistencyAgent', role: 'Consensus quorum & partition detector' },
            { name: 'GlobalDisasterRecoveryAgent', role: 'Planetary RPO/RTO validation' },
            { name: 'ChaosAgent', role: 'Safe blast-radius-bounded chaos' },
            { name: 'IncidentCommanderAgent', role: 'Global incident triage & blast containment' },
            { name: 'RootCauseAgent', role: 'Systemic dependency timeline RCA' },
            { name: 'GlobalRemediationAgent', role: 'Governed runbook self-healing' },
            { name: 'EnergyAgent', role: 'Carbon intensity & sustainability tracking' },
            { name: 'GlobalReliabilityAgent', role: 'Planetary SLO & error budget defender' },
          ].map((agent, idx) => (
            <div key={idx} className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold text-white truncate">{agent.name}</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-sky-500/20 text-sky-400 font-semibold">
                  ACTIVE
                </span>
              </div>
              <div className="text-xs text-slate-400 line-clamp-2">{agent.role}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
