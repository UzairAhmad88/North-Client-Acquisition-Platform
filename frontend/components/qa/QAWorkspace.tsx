'use client';

import React, { useState, useEffect } from 'react';
import {
  listTestPlans,
  listTestRuns,
  listDefects,
  listUATSessions,
  listReleases,
  getHandoverChecklist,
  evaluateReleaseGate,
  TestPlan,
  TestRun,
  Defect,
  UATSession,
  ReleaseVersion,
  HandoverChecklist,
} from '@/lib/api/qa';
import { QADashboardOverview } from './QADashboardOverview';
import { TestCaseManager } from './TestCaseManager';
import { DefectTracker } from './DefectTracker';
import { UATClientPanel } from './UATClientPanel';
import { ReleaseReadinessChecklist } from './ReleaseReadinessChecklist';
import { HandoverAcceptancePanel } from './HandoverAcceptancePanel';
import { ShieldCheck, CheckCircle2, AlertTriangle, FileCode, Server, Award } from 'lucide-react';

interface QAWorkspaceProps {
  projectId: string;
}

export const QAWorkspace: React.FC<QAWorkspaceProps> = ({ projectId }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'tests' | 'defects' | 'uat' | 'releases' | 'handover'>('overview');

  const [testPlans, setTestPlans] = useState<TestPlan[]>([]);
  const [testRuns, setTestRuns] = useState<TestRun[]>([]);
  const [defects, setDefects] = useState<Defect[]>([]);
  const [uatSessions, setUATSessions] = useState<UATSession[]>([]);
  const [releases, setReleases] = useState<ReleaseVersion[]>([]);
  const [handover, setHandover] = useState<HandoverChecklist | null>(null);

  const [loading, setLoading] = useState(true);
  const [readinessScore, setReadinessScore] = useState(0);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    loadAllQAData();
  }, [projectId]);

  const loadAllQAData = async () => {
    setLoading(true);
    try {
      const [plansData, runsData, defectsData, uatData, relsData, handoverData] = await Promise.allSettled([
        listTestPlans(projectId),
        listTestRuns(projectId),
        listDefects(projectId),
        listUATSessions(projectId),
        listReleases(projectId),
        getHandoverChecklist(projectId),
      ]);

      if (plansData.status === 'fulfilled') setTestPlans(plansData.value);
      if (runsData.status === 'fulfilled') setTestRuns(runsData.value);
      if (defectsData.status === 'fulfilled') setDefects(defectsData.value);
      if (uatData.status === 'fulfilled') setUATSessions(uatData.value);
      if (relsData.status === 'fulfilled') setReleases(relsData.value);
      if (handoverData.status === 'fulfilled') setHandover(handoverData.value);

      // Evaluate release gate if releases exist
      if (relsData.status === 'fulfilled' && relsData.value.length > 0) {
        try {
          const evalRes = await evaluateReleaseGate(relsData.value[0].id);
          setReadinessScore(evalRes.readiness_score);
          setIsReady(evalRes.is_ready_for_release);
        } catch {
          // ignore error on initial load
        }
      }
    } catch (err) {
      console.error('Error loading QA data:', err);
    } finally {
      setLoading(false);
    }
  };

  // Calculations
  const totalRunTests = testRuns.reduce((acc, r) => acc + r.passed_count + r.failed_count + r.blocked_count + r.skipped_count, 0);
  const totalPassed = testRuns.reduce((acc, r) => acc + r.passed_count, 0);
  const passRate = totalRunTests > 0 ? (totalPassed / totalRunTests) * 100 : 100.0;

  const openDefects = defects.filter((d) => !['CLOSED', 'VERIFIED'].includes(d.status));
  const criticalDefects = openDefects.filter((d) => d.severity === 'CRITICAL');
  const uatApproved = uatSessions.some((u) => u.approved_by_client);

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4 sm:p-6 text-slate-100">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-purple-600/10 border border-purple-500/20 rounded-xl text-purple-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-black text-white tracking-tight">QA, UAT & Handover Governance</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Phase 29 — Defect Tracking, Release Gates & Delivery Packaging • Project ID: <code className="text-slate-300">{projectId}</code>
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3 bg-slate-950 px-4 py-2.5 rounded-xl border border-slate-800">
          <Award className="w-5 h-5 text-amber-400" />
          <div className="text-xs">
            <div className="font-semibold text-slate-200">Delivery Status</div>
            <div className="text-[10px] text-slate-400">
              {handover?.signed_off_by_client ? 'COMPLETED & HANDED OVER' : 'QA & ACCEPTANCE IN PROGRESS'}
            </div>
          </div>
        </div>
      </div>

      {/* Overview Cards */}
      <QADashboardOverview
        testRunCount={testRuns.length}
        passRate={passRate}
        openDefectsCount={openDefects.length}
        criticalDefectsCount={criticalDefects.length}
        readinessScore={readinessScore}
        isReadyForRelease={isReady}
        uatApproved={uatApproved}
        onEvaluateGate={loadAllQAData}
      />

      {/* Navigation Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-800 pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition flex items-center space-x-2 ${
            activeTab === 'overview' ? 'bg-purple-600/20 border border-purple-500 text-purple-300' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <ShieldCheck className="w-4 h-4" />
          <span>Executive Overview</span>
        </button>

        <button
          onClick={() => setActiveTab('tests')}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition flex items-center space-x-2 ${
            activeTab === 'tests' ? 'bg-blue-600/20 border border-blue-500 text-blue-300' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileCode className="w-4 h-4" />
          <span>Test Plans & Cases ({testPlans.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('defects')}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition flex items-center space-x-2 ${
            activeTab === 'defects' ? 'bg-red-600/20 border border-red-500 text-red-300' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <AlertTriangle className="w-4 h-4" />
          <span>Defect Tracker ({defects.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('uat')}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition flex items-center space-x-2 ${
            activeTab === 'uat' ? 'bg-emerald-600/20 border border-emerald-500 text-emerald-300' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <CheckCircle2 className="w-4 h-4" />
          <span>Client UAT</span>
        </button>

        <button
          onClick={() => setActiveTab('releases')}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition flex items-center space-x-2 ${
            activeTab === 'releases' ? 'bg-purple-600/20 border border-purple-500 text-purple-300' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Server className="w-4 h-4" />
          <span>Release Gates</span>
        </button>

        <button
          onClick={() => setActiveTab('handover')}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition flex items-center space-x-2 ${
            activeTab === 'handover' ? 'bg-amber-600/20 border border-amber-500 text-amber-300' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Award className="w-4 h-4" />
          <span>Handover Acceptance</span>
        </button>
      </div>

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <TestCaseManager testPlans={testPlans} projectId={projectId} onRefresh={loadAllQAData} />
          <DefectTracker defects={defects} projectId={projectId} onRefresh={loadAllQAData} />
        </div>
      )}

      {activeTab === 'tests' && <TestCaseManager testPlans={testPlans} projectId={projectId} onRefresh={loadAllQAData} />}

      {activeTab === 'defects' && <DefectTracker defects={defects} projectId={projectId} onRefresh={loadAllQAData} />}

      {activeTab === 'uat' && <UATClientPanel uatSessions={uatSessions} projectId={projectId} onRefresh={loadAllQAData} />}

      {activeTab === 'releases' && <ReleaseReadinessChecklist releases={releases} projectId={projectId} onRefresh={loadAllQAData} />}

      {activeTab === 'handover' && <HandoverAcceptancePanel checklist={handover} projectId={projectId} onRefresh={loadAllQAData} />}
    </div>
  );
};
