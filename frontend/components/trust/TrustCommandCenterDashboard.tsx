'use client';

import React, { useState } from 'react';
import {
  ShieldCheck,
  Scale,
  FileText,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Play,
  Layers,
  BarChart3,
  Globe,
  Lock,
  Search,
  Check,
  ChevronRight,
  Bot,
  Zap,
  Sliders,
  Eye,
  RefreshCw,
  FileCode,
  Landmark,
  UserCheck,
  FileCheck,
  BookOpen,
  Key,
  Database
} from 'lucide-react';

export default function TrustCommandCenterDashboard() {
  const [activeTab, setActiveTab] = useState<
    'command-center' | 'regulations' | 'contracts' | 'controls' | 'privacy' | 'ai-gov' | 'investigations' | 'agents'
  >('command-center');

  // Closed loop 11-stage cycle simulator
  const [cycleRunning, setCycleRunning] = useState(false);
  const [cycleStep, setCycleStep] = useState(0);
  const [cycleCompleted, setCycleCompleted] = useState(false);

  // Clause Scanner State
  const [clauseInput, setClauseInput] = useState<string>(
    'Counterparty liability shall be uncapped for indirect, punitive, or consequential damages resulting from platform incidents.'
  );
  const [clauseScanResult, setClauseScanResult] = useState<any>(null);
  const [scanningClause, setScanningClause] = useState(false);

  // Dual Approval Legal Commitments
  const [pendingApprovals, setPendingApprovals] = useState([
    { id: 'CTR-REV-901', title: 'Global SaaS Master Services Agreement - Uncapped Indemnity Clause', counterparty: 'Apex Cloud Systems', value: '$850,000', signedLegal: true, signedExec: false },
    { id: 'EXC-AI-042', title: 'Policy Exception: High-Autonomy Physical Robotics Dispatch Sandbox', counterparty: 'Internal R&D', value: 'N/A', signedLegal: false, signedExec: false }
  ]);

  const stages = [
    'Observe', 'Classify', 'Map', 'Assess',
    'Identify Gap', 'Recommend', 'Request Approval', 'Execute Approved Action',
    'Collect Evidence', 'Verify', 'Audit'
  ];

  const run11StageCycle = () => {
    setCycleRunning(true);
    setCycleStep(1);
    setCycleCompleted(false);

    const timer = setInterval(() => {
      setCycleStep((prev) => {
        if (prev >= 11) {
          clearInterval(timer);
          setCycleRunning(false);
          setCycleCompleted(true);
          return 11;
        }
        return prev + 1;
      });
    }, 450);
  };

  const handleApproveCommitment = (id: string) => {
    setPendingApprovals((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, signedExec: true } : item
      )
    );
  };

  const handleScanClause = () => {
    setScanningClause(true);
    setTimeout(() => {
      const isUncapped = clauseInput.toLowerCase().includes('uncapped') || clauseInput.toLowerCase().includes('unlimited');
      setClauseScanResult({
        riskLevel: isUncapped ? 'CRITICAL' : 'LOW',
        isStandard: !isUncapped,
        finding: isUncapped
          ? 'Deviation from Standard Mutual Cap: Detected uncapped liability exposure for consequential damages.'
          : 'Clause conforms with approved template mutual liability guidelines.',
        recommendation: isUncapped
          ? 'Counter-propose mutual liability limitation capped at 12 months fees paid under Section 14.2.'
          : 'Ready for standard legal sign-off without escalation.'
      });
      setScanningClause(false);
    }, 600);
  };

  return (
    <div className="space-y-6 text-slate-100 min-h-screen pb-16">
      {/* Header Banner */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 p-6 bg-slate-900/80 border border-slate-800 rounded-2xl backdrop-blur-xl shadow-2xl">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2.5 bg-blue-500/10 border border-blue-500/30 rounded-xl">
              <ShieldCheck className="w-6 h-6 text-blue-400" />
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Enterprise Trust & Governance Operating System
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/30 rounded-full flex items-center gap-1">
              <Scale className="w-3 h-3" /> Governed Legal & Compliance
            </span>
          </div>
          <p className="text-sm text-slate-400">
            Phase 73: Regulatory Intelligence, CLM Contract Intelligence, Privacy OS, AI Governance & Autonomous 11-Stage Trust Operating Loop
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-4 py-2 bg-slate-800/80 border border-slate-700/60 rounded-xl text-xs flex items-center gap-2">
            <Lock className="w-4 h-4 text-emerald-400" />
            <span>Composite Trust Score:</span>
            <span className="font-mono text-emerald-400 font-bold">94.8 / 100 (Exemplary)</span>
          </div>

          <button
            onClick={run11StageCycle}
            disabled={cycleRunning}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition-all shadow-lg shadow-blue-600/20"
          >
            {cycleRunning ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Running Stage {cycleStep}/11...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Execute Trust Loop</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* 11-Stage Interactive Closed Loop Tracker */}
      <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl">
        <div className="flex items-center justify-between mb-3 text-xs">
          <span className="font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
            <Zap className="w-4 h-4 text-amber-400" /> Autonomous 11-Stage Trust Loop
          </span>
          <span className="text-slate-400 font-mono">
            {cycleRunning ? `Stage ${cycleStep}: ${stages[cycleStep - 1]}` : (cycleCompleted ? 'Cycle Complete (Evidence Logged)' : 'Ready (Awaiting Horizon Trigger)')}
          </span>
        </div>
        <div className="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-11 gap-2">
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
                    ? 'bg-blue-500/10 border-blue-500/40 text-blue-400'
                    : 'bg-slate-950/60 border-slate-800 text-slate-500'
                }`}
              >
                <div className="text-[10px] font-mono opacity-70 mb-1">0{stepNum}</div>
                <div className="text-xs truncate">{stage}</div>
                <div className="mt-1 flex justify-center">
                  {isDone ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-blue-400" />
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
        {/* Compliance Posture */}
        <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Compliance Posture</span>
            <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-400">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white font-mono">98.2%</div>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-400">286 Controls Tested</span>
            <span className="text-emerald-400 font-semibold">SOC 2 / ISO / GDPR</span>
          </div>
        </div>

        {/* Contract Lifecycle Management */}
        <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Active Contracts & CLM</span>
            <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
              <FileText className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white font-mono">184 Active</div>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-400">5 Renewals in 30d</span>
            <span className="text-amber-400 font-semibold">2 Flagged Clauses</span>
          </div>
        </div>

        {/* Privacy OS & Legal Holds */}
        <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Privacy OS & Holds</span>
            <div className="p-2 bg-purple-500/10 rounded-lg text-purple-400">
              <Key className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white font-mono">1 Legal Hold</div>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-400">2 Pending DSARs</span>
            <span className="text-purple-400 font-semibold">100% SLA Met</span>
          </div>
        </div>

        {/* AI Governance & Ethics */}
        <div className="p-5 bg-slate-900/60 border border-slate-800/80 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">AI Governance & Models</span>
            <div className="p-2 bg-amber-500/10 rounded-lg text-amber-400">
              <Bot className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white font-mono">19 AI Systems</div>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-400">2 High-Risk (EU Act)</span>
            <span className="text-emerald-400 font-semibold">0 Open Incidents</span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto text-sm">
        {[
          { id: 'command-center', label: 'Executive Trust Command', icon: Landmark },
          { id: 'regulations', label: 'Regulatory Intelligence', icon: Globe },
          { id: 'contracts', label: 'Contract Intelligence & CLM', icon: FileText },
          { id: 'controls', label: 'Compliance & Controls', icon: ShieldCheck },
          { id: 'privacy', label: 'Privacy OS & DSAR', icon: Lock },
          { id: 'ai-gov', label: 'AI Governance & Ethics', icon: Bot },
          { id: 'investigations', label: 'Evidence & Investigations', icon: FileCheck },
          { id: 'agents', label: '16 Trust AI Agents', icon: UserCheck }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl whitespace-nowrap font-medium transition-all ${
                isActive
                  ? 'bg-slate-800 text-blue-400 border border-slate-700 shadow-md'
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
          {/* Left 2 Cols: Dual-Control Sign-off & Regulatory Changes */}
          <div className="lg:col-span-2 space-y-6">
            {/* Dual Control Sign-off */}
            <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Scale className="w-5 h-5 text-amber-400" />
                  <h2 className="text-base font-semibold text-white">
                    Mandatory Dual-Control Legal Authorization Queue
                  </h2>
                </div>
                <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded-full">
                  Policy Enforced
                </span>
              </div>

              <div className="space-y-3">
                {pendingApprovals.map((p) => {
                  const fullyApproved = p.signedLegal && p.signedExec;
                  return (
                    <div
                      key={p.id}
                      className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl flex items-center justify-between"
                    >
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-sm font-bold text-white">{p.id}</span>
                          <span className="text-sm text-slate-300 font-medium">{p.title}</span>
                        </div>
                        <div className="text-xs text-slate-400 mt-1 flex items-center gap-3">
                          <span>Party: <strong className="text-white">{p.counterparty}</strong></span>
                          <span>Value: {p.value}</span>
                          <span className="text-amber-400">
                            Legal Sign-off: {p.signedLegal ? 'Approved' : 'Pending'} | Exec Sign-off: {p.signedExec ? 'Approved' : 'Pending'}
                          </span>
                        </div>
                      </div>

                      <div>
                        {fullyApproved ? (
                          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs rounded-lg font-medium flex items-center gap-1">
                            <Check className="w-3.5 h-3.5" /> Authorized
                          </span>
                        ) : (
                          <button
                            onClick={() => handleApproveCommitment(p.id)}
                            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs rounded-lg font-semibold flex items-center gap-1.5 transition-all"
                          >
                            <ShieldCheck className="w-3.5 h-3.5" /> Authorize Dual Control
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Regulatory Horizon Radar */}
            <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl">
              <h2 className="text-base font-semibold text-white mb-4 flex items-center gap-2">
                <Globe className="w-5 h-5 text-blue-400" />
                Active Regulatory Horizon & Statutory Changes
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400">EU AI Act (Regulation 2024/1689)</div>
                  <div className="text-sm font-bold text-blue-400 mt-1">IN CONFORMITY</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">High-Risk Model Audited</div>
                </div>
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400">SEC Cybersecurity Incident Disclosure</div>
                  <div className="text-sm font-bold text-emerald-400 mt-1">4-DAY PLAYBOOK PASS</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Automated SOC Telemetry</div>
                </div>
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400">GDPR Cross-Border Data Transfers</div>
                  <div className="text-sm font-bold text-emerald-400 mt-1">STANDARD CLAUSES VERIFIED</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">DPA Annex Updated</div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Col: Interactive Clause Deviation Scanner */}
          <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
            <div className="flex items-center gap-2">
              <FileCode className="w-5 h-5 text-purple-400" />
              <h2 className="text-base font-semibold text-white">Clause Risk & Deviation Scanner</h2>
            </div>
            <p className="text-xs text-slate-400">
              Scan inbound contractual language against approved standard template baselines to flag unreviewed exposure.
            </p>

            <div className="space-y-2">
              <textarea
                value={clauseInput}
                onChange={(e) => setClauseInput(e.target.value)}
                rows={4}
                className="w-full p-3 bg-slate-950/80 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-blue-500"
              />

              <button
                onClick={handleScanClause}
                disabled={scanningClause}
                className="w-full py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-semibold transition-all flex items-center justify-center gap-2"
              >
                {scanningClause ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5" />}
                <span>Scan Contractual Language</span>
              </button>
            </div>

            {clauseScanResult && (
              <div className="p-3.5 bg-purple-950/30 border border-purple-800/40 rounded-xl space-y-2 mt-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-purple-300">Scan Assessment:</span>
                  <span className={`px-2 py-0.5 rounded font-mono font-bold text-[10px] ${
                    clauseScanResult.riskLevel === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                  }`}>
                    {clauseScanResult.riskLevel} RISK
                  </span>
                </div>
                <div className="text-xs text-slate-300">{clauseScanResult.finding}</div>
                <div className="text-[11px] text-slate-400">
                  <strong className="text-purple-300">Advisory Recommendation: </strong>
                  {clauseScanResult.recommendation}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab 2: Regulatory Intelligence */}
      {activeTab === 'regulations' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-blue-400" />
            Global Regulatory Intelligence & Horizon Scanning
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-950/60 text-xs uppercase text-slate-400">
                <tr>
                  <th className="p-3">Regulation Code</th>
                  <th className="p-3">Title</th>
                  <th className="p-3">Authority</th>
                  <th className="p-3">Jurisdiction</th>
                  <th className="p-3">Category</th>
                  <th className="p-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {[
                  { code: 'EU_GDPR', title: 'General Data Protection Regulation (2016/679)', auth: 'European Parliament', jur: 'EU', cat: 'DATA_PRIVACY', status: 'COMPLIANT' },
                  { code: 'EU_AI_ACT', title: 'European Union Artificial Intelligence Act', auth: 'European Commission', jur: 'EU', cat: 'AI_GOVERNANCE', status: 'IN_CONFORMITY' },
                  { code: 'SEC_CYBER', title: 'SEC Cybersecurity Incident & Risk Management', auth: 'US SEC', jur: 'US_FEDERAL', cat: 'CYBERSECURITY', status: 'COMPLIANT' },
                  { code: 'SOX_404', title: 'Sarbanes-Oxley Act Section 404 Controls', auth: 'PCAOB', jur: 'US_FEDERAL', cat: 'FINANCIAL_REPORTING', status: 'VERIFIED' }
                ].map((row) => (
                  <tr key={row.code} className="hover:bg-slate-800/30">
                    <td className="p-3 font-mono font-bold text-blue-400">{row.code}</td>
                    <td className="p-3 font-medium text-white">{row.title}</td>
                    <td className="p-3 text-xs">{row.auth}</td>
                    <td className="p-3 font-mono text-xs">{row.jur}</td>
                    <td className="p-3 text-xs"><span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">{row.cat}</span></td>
                    <td className="p-3 text-center text-xs text-emerald-400">{row.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 3: Contract Intelligence & CLM */}
      {activeTab === 'contracts' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-400" />
            Contract Lifecycle Management (CLM) & Obligation Graph
          </h2>
          <p className="text-xs text-slate-400">
            Version-preserving repository linking contracts directly with Phase 72 financial billing milestones and statutory obligations.
          </p>
        </div>
      )}

      {/* Tab 4: Compliance & Controls */}
      {activeTab === 'controls' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Unified Control Library & Automated Effectiveness Testing
          </h2>
          <p className="text-xs text-slate-400">
            Multi-framework control mappings (SOC 2, ISO 27001, NIST, GDPR) with continuous design and operating effectiveness sampling.
          </p>
        </div>
      )}

      {/* Tab 5: Privacy OS & DSAR */}
      {activeTab === 'privacy' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Lock className="w-5 h-5 text-purple-400" />
            Privacy Operating System, DSAR Fulfillment & Active Legal Holds
          </h2>
          <p className="text-xs text-slate-400">
            Data processing register, positive consent tracking, and legal hold locks preventing automated record deletion.
          </p>
        </div>
      )}

      {/* Tab 6: AI Governance & Ethics */}
      {activeTab === 'ai-gov' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Bot className="w-5 h-5 text-amber-400" />
            AI Governance Operating System & EU AI Act Conformity
          </h2>
          <p className="text-xs text-slate-400">
            System risk tiering, bias evaluations, factuality benchmarks, and explicit agent permission boundaries.
          </p>
        </div>
      )}

      {/* Tab 7: Evidence & Investigations */}
      {activeTab === 'investigations' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <FileCheck className="w-5 h-5 text-emerald-400" />
            Confidential Ethics Investigations & Evidence Chain-of-Custody
          </h2>
          <p className="text-xs text-slate-400">
            Immutable SHA-256 evidence digests, encrypted vaults, and privileged legal work product protection.
          </p>
        </div>
      )}

      {/* Tab 8: 16 Governed Autonomous Trust AI Agents */}
      {activeTab === 'agents' && (
        <div className="p-6 bg-slate-900/60 border border-slate-800/80 rounded-2xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-blue-400" />
            16 Governed Autonomous Trust, Legal & Compliance AI Agents
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {[
              { name: 'Trust Orchestrator', desc: '11-stage autonomous trust loop coordinator' },
              { name: 'Compliance Agent', desc: 'Framework mapping & control gap analysis' },
              { name: 'Regulatory Intelligence', desc: 'Global regulatory notice horizon scanning' },
              { name: 'Contract Agent', desc: 'CLM intake, version control & milestones' },
              { name: 'Clause Analysis Agent', desc: 'Template deviation & liability risk scanner' },
              { name: 'Obligation Agent', desc: 'Contractual & statutory deadline tracking' },
              { name: 'Policy Agent', desc: 'Policy lifecycle & employee acknowledgements' },
              { name: 'Privacy Agent', desc: 'ROPA inventory, DSAR pipeline & holds' },
              { name: 'AI Governance Agent', desc: 'Model risk tiering & agent boundaries' },
              { name: 'Audit Agent', desc: 'Audit fieldwork & finding remediation' },
              { name: 'Evidence Agent', desc: 'Cryptographic SHA-256 chain of custody' },
              { name: 'Third Party Risk Agent', desc: 'Vendor due diligence & sanctions' },
              { name: 'Investigation Agent', desc: 'Confidential whistleblower case workflow' },
              { name: 'Legal Matter Agent', desc: 'Litigation calendar & outside counsel spend' },
              { name: 'Licensing Agent', desc: 'Corporate licenses & insurance policies' },
              { name: 'Governance Agent', desc: 'Board resolutions & conflict registers' }
            ].map((agent, i) => (
              <div key={agent.name} className="p-3.5 bg-slate-950/60 border border-slate-800 rounded-xl">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-blue-400 font-semibold">0{i+1}.</span>
                  <span className="text-[10px] px-2 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/30 rounded-full font-mono">
                    ADVISORY
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
