'use client';

import React, { useState } from 'react';
import {
  Cpu,
  Activity,
  AlertTriangle,
  Play,
  CheckCircle2,
  XCircle,
  Clock,
  RotateCcw,
  Zap,
  TrendingUp,
  Workflow,
  Search,
  BookOpen,
  Gauge,
  Sparkles,
  BarChart3,
  Check,
  ChevronRight,
  Eye,
  Settings,
  Shield,
  RefreshCw,
  Radio,
  MapPin,
  Thermometer,
  BatteryCharging,
  Bot,
  Factory,
  Wrench,
  Boxes,
  Compass,
  Sliders,
  Power
} from 'lucide-react';

export default function CyberPhysicalCommandCenterDashboard() {
  const [roleView, setRoleView] = useState<'executive' | 'plant_manager' | 'robotics_lead' | 'safety_engineer' | 'maintenance_tech'>('plant_manager');
  const [activeTab, setActiveTab] = useState<'overview' | 'facilities' | 'robot_fleet' | 'machines_oee' | 'digital_twin' | 'safety_interlocks' | 'maintenance' | 'agents'>('overview');

  // Closed-loop 12-stage cycle simulator
  const [cycleRunning, setCycleRunning] = useState(false);
  const [cycleStep, setCycleStep] = useState(0);
  const [cycleResult, setCycleResult] = useState<any>(null);

  // E-stop simulator state
  const [eStopEngaged, setEStopEngaged] = useState(false);

  const runOperatingCycle = () => {
    setCycleRunning(true);
    setCycleStep(1);
    setCycleResult(null);

    const timer = setInterval(() => {
      setCycleStep((prev) => {
        if (prev >= 12) {
          clearInterval(timer);
          setCycleRunning(false);
          setCycleResult({
            cycleId: `cps_cyc_${Math.random().toString(36).substring(2, 8)}`,
            status: 'COMPLETED',
            actions: [
              'Sensed 420 industrial telemetry streams',
              'Ingested vibration RMS at 1.82 mm/s (VALID)',
              'Synchronized KUKA Arm Digital Twin state (drift: 0.0%)',
              'Checked thermal safety ceilings (within safe limits)',
              'Forecasted CNC spindle bearing RUL: 4,600 operating hours',
              'Verified dual-authorization interlock for Line 1'
            ]
          });
          return 12;
        }
        return prev + 1;
      });
    }, 350);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header & Role Bar */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-400">
              <Factory className="w-7 h-7" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
                Cyber-Physical Operations Command Center
              </h1>
              <p className="text-sm text-slate-400">
                Phase 70 &bull; Autonomous IoT, Robotics Infrastructure, Digital Twins &amp; Real-World AI Operations
              </p>
            </div>
          </div>
        </div>

        {/* E-Stop and Role selector */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setEStopEngaged(!eStopEngaged)}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl font-semibold transition-all shadow-lg ${
              eStopEngaged
                ? 'bg-red-600 text-white animate-pulse shadow-red-600/50'
                : 'bg-red-950/40 text-red-400 border border-red-800/60 hover:bg-red-900/60'
            }`}
          >
            <Power className="w-5 h-5" />
            {eStopEngaged ? 'EMERGENCY STOP ENGAGED' : 'E-STOP SYSTEM ARMED'}
          </button>

          <div className="flex bg-slate-900 border border-slate-800 rounded-xl p-1 text-xs">
            {(['plant_manager', 'robotics_lead', 'safety_engineer', 'executive'] as const).map((r) => (
              <button
                key={r}
                onClick={() => setRoleView(r)}
                className={`px-3 py-1.5 rounded-lg capitalize transition-all ${
                  roleView === r ? 'bg-emerald-600 text-white font-medium shadow' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {r.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        {[
          { label: 'Overall OEE', val: '90.2%', icon: Gauge, color: 'text-emerald-400', sub: 'World Class >= 85%' },
          { label: 'Active Assets', val: '148', icon: Boxes, color: 'text-teal-400', sub: 'Across 4 Facilities' },
          { label: 'IoT Devices', val: '340', icon: Radio, color: 'text-cyan-400', sub: '99.8% Online' },
          { label: 'Robot Fleet', val: '24 AMRs', icon: Bot, color: 'text-indigo-400', sub: '18 Active / 2 Chg' },
          { label: 'Twin Sync', val: '32 ms', icon: RefreshCw, color: 'text-sky-400', sub: 'Drift: 0.00%' },
          { label: 'Safety Interlocks', val: 'ALL ARMED', icon: Shield, color: 'text-emerald-400', sub: '0 Breaches' },
          { label: 'Power Demand', val: '1,840 kW', icon: Zap, color: 'text-amber-400', sub: 'PF: 0.97 Optimal' },
          { label: 'Active CPS Agents', val: '19 AI', icon: Sparkles, color: 'text-purple-400', sub: 'Zero Bypass Gate' },
        ].map((k, i) => (
          <div key={i} className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-3.5 flex flex-col justify-between">
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-xs font-medium">{k.label}</span>
              <k.icon className={`w-4 h-4 ${k.color}`} />
            </div>
            <div>
              <div className={`text-xl font-bold tracking-tight ${k.color}`}>{k.val}</div>
              <div className="text-[10px] text-slate-500 mt-0.5">{k.sub}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 space-x-1 overflow-x-auto pb-1 text-sm">
        {[
          { id: 'overview', label: '12-Stage Cycle & Telemetry', icon: Activity },
          { id: 'facilities', label: 'Facilities & Zones', icon: Factory },
          { id: 'robot_fleet', label: 'Robotics & Missions', icon: Bot },
          { id: 'machines_oee', label: 'Machinery & OEE', icon: Gauge },
          { id: 'digital_twin', label: 'Digital Twins & What-If', icon: RefreshCw },
          { id: 'safety_interlocks', label: 'Safety Policies & E-Stop', icon: Shield },
          { id: 'maintenance', label: 'Predictive Maintenance', icon: Wrench },
          { id: 'agents', label: '19 Autonomous Agents', icon: Sparkles },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-t-xl font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-slate-900 text-emerald-400 border-t-2 border-emerald-400 border-x border-slate-800'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Main Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* 12-Stage Real-World Operating Cycle */}
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
              <div>
                <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
                  <Workflow className="w-5 h-5 text-emerald-400" />
                  Closed-Loop 12-Stage Cyber-Physical Operating Cycle
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Sense &rarr; Ingest &rarr; Understand &rarr; Detect &rarr; Predict &rarr; Simulate &rarr; Plan &rarr; Safety Check &rarr; Authorize &rarr; Act &rarr; Verify &rarr; Learn
                </p>
              </div>
              <button
                onClick={runOperatingCycle}
                disabled={cycleRunning}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium text-sm transition-all shadow-lg ${
                  cycleRunning
                    ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white shadow-emerald-900/30'
                }`}
              >
                {cycleRunning ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    Executing Stage {cycleStep}/12...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-white" />
                    Execute Closed-Loop Cycle
                  </>
                )}
              </button>
            </div>

            {/* Step visualization */}
            <div className="grid grid-cols-2 md:grid-cols-6 lg:grid-cols-12 gap-2 mt-4">
              {[
                '1. Sense',
                '2. Ingest',
                '3. Understand',
                '4. Detect',
                '5. Predict',
                '6. Simulate',
                '7. Plan',
                '8. Safety Check',
                '9. Authorize',
                '10. Act',
                '11. Verify',
                '12. Learn'
              ].map((st, i) => {
                const stepNum = i + 1;
                const isCurrent = cycleRunning && cycleStep === stepNum;
                const isDone = cycleStep > stepNum || cycleResult;
                return (
                  <div
                    key={i}
                    className={`p-2.5 rounded-xl border text-center transition-all ${
                      isCurrent
                        ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 animate-pulse'
                        : isDone
                        ? 'bg-emerald-950/30 border-emerald-800/60 text-emerald-400'
                        : 'bg-slate-950/40 border-slate-800/60 text-slate-500'
                    }`}
                  >
                    <div className="text-[11px] font-semibold">{st}</div>
                    <div className="text-[9px] mt-1">
                      {isCurrent ? 'Running' : isDone ? 'Verified' : 'Standby'}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Cycle Result Output */}
            {cycleResult && (
              <div className="mt-5 p-4 bg-emerald-950/20 border border-emerald-800/50 rounded-xl space-y-2">
                <div className="flex items-center justify-between text-xs text-emerald-400 font-semibold">
                  <span className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4" /> Cycle ID: {cycleResult.cycleId} — Status: {cycleResult.status}
                  </span>
                  <span className="text-slate-400">All Hard Safety Interlocks Passed</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-slate-300">
                  {cycleResult.actions.map((act: string, idx: number) => (
                    <div key={idx} className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                      <span>{act}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Plant Telemetry & Live Streams */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-4">
              <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                <Radio className="w-4 h-4 text-cyan-400" />
                Live Industrial Sensor Ingestion
              </h3>
              <div className="space-y-2.5">
                {[
                  { sensor: 'VIB-SPINDLE-01', asset: 'CNC Mill 01', val: '1.82 mm/s', grade: 'PRISTINE', status: 'HEALTHY' },
                  { sensor: 'TEMP-BEARING-02', asset: 'KUKA Titan Arm', val: '58.4 °C', grade: 'PRISTINE', status: 'HEALTHY' },
                  { sensor: 'PRES-HYDRAULIC-04', asset: 'Stamping Press 02', val: '210.4 Bar', grade: 'PRISTINE', status: 'HEALTHY' },
                  { sensor: 'CURR-MOTOR-DRIVE-03', asset: 'Coolant Pump A', val: '42.8 A', grade: 'PRISTINE', status: 'HEALTHY' }
                ].map((s, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-slate-950/60 border border-slate-800/80 rounded-xl text-xs">
                    <div>
                      <div className="font-semibold text-slate-200">{s.sensor}</div>
                      <div className="text-[11px] text-slate-400">{s.asset}</div>
                    </div>
                    <div className="text-right">
                      <div className="font-mono text-cyan-400 font-bold">{s.val}</div>
                      <div className="text-[10px] text-emerald-400 font-medium">{s.grade} &bull; {s.status}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-4">
              <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                <Bot className="w-4 h-4 text-indigo-400" />
                Autonomous Robotics Fleet Health
              </h3>
              <div className="space-y-2.5">
                {[
                  { id: 'AMR-OTTO-1500', zone: 'ZONE-A Staging', battery: '92.5%', mission: 'MATERIAL_TRANSPORT', state: 'AVAILABLE' },
                  { id: 'AMR-FETCH-500', zone: 'ZONE-C Inspection', battery: '88.0%', mission: 'QUALITY_SCAN', state: 'ACTIVE' },
                  { id: 'ARM-FANUC-M20', zone: 'ZONE-B Assembly', battery: '100.0%', mission: 'PRECISION_WELDING', state: 'ACTIVE' },
                  { id: 'FORKLIFT-AGV-01', zone: 'ZONE-D Dock', battery: '24.0%', mission: 'AUTO_CHARGING', state: 'CHARGING' }
                ].map((r, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-slate-950/60 border border-slate-800/80 rounded-xl text-xs">
                    <div>
                      <div className="font-semibold text-slate-200">{r.id}</div>
                      <div className="text-[11px] text-slate-400">{r.zone} &bull; {r.mission}</div>
                    </div>
                    <div className="text-right">
                      <div className="font-mono text-indigo-300 font-bold">{r.battery}</div>
                      <div className="text-[10px] text-emerald-400 font-medium">{r.state}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Facilities Tab */}
      {activeTab === 'facilities' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-4">
          <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
            <Factory className="w-5 h-5 text-emerald-400" />
            Global Smart Facilities &amp; Safety Zones
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { code: 'FAC-DET-01', name: 'Detroit Advanced Robotics Assembly', area: '45,000 sqm', zones: 8, assets: 74, oee: '91.4%' },
              { code: 'FAC-MUC-01', name: 'Munich Precision Engineering Gigafactory', area: '38,000 sqm', zones: 6, assets: 62, oee: '89.2%' }
            ].map((f, i) => (
              <div key={i} className="p-4 bg-slate-950/80 border border-slate-800 rounded-xl space-y-2">
                <div className="flex justify-between items-center">
                  <div className="font-bold text-slate-200">{f.name}</div>
                  <span className="px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs rounded-lg font-mono">
                    {f.code}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-2 text-xs text-slate-400 pt-2 border-t border-slate-900">
                  <div>Area: <span className="text-slate-200 font-medium">{f.area}</span></div>
                  <div>Assets: <span className="text-slate-200 font-medium">{f.assets}</span></div>
                  <div>OEE: <span className="text-emerald-400 font-bold">{f.oee}</span></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Other tab fallbacks */}
      {['robot_fleet', 'machines_oee', 'digital_twin', 'safety_interlocks', 'maintenance', 'agents'].includes(activeTab) && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 text-center space-y-3">
          <h3 className="text-lg font-bold text-slate-200 capitalize">
            {activeTab.replace('_', ' ')} Intelligence Plane
          </h3>
          <p className="text-sm text-slate-400 max-w-xl mx-auto">
            Real-time telemetry, autonomous agents, and deterministic safety interlocks are continuously synchronized with Phase 70 cyber-physical operating services.
          </p>
          <div className="pt-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs rounded-full font-medium">
              <CheckCircle2 className="w-3.5 h-3.5" /> All System Interlocks Operational
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
