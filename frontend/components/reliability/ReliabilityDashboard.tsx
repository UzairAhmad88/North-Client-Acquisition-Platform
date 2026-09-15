'use client';

import React, { useState, useEffect } from 'react';
import {
  reliabilityApi,
  DeepHealthResult,
  CircuitBreakerState,
  SLOMetricSnapshot,
  ReliabilityIncident,
  BackupRecord,
  RestoreVerificationTest,
  DRPlan,
  DRDrill,
  FeatureFlag,
} from '@/lib/api/reliability';

import { HealthOverview } from './HealthOverview';
import { DependencyHealthMatrix } from './DependencyHealthMatrix';
import { SLOErrorBudgetCard } from './SLOErrorBudgetCard';
import { IncidentManager } from './IncidentManager';
import { BackupRestoreStatus } from './BackupRestoreStatus';
import { DisasterRecoveryPlanViewer } from './DisasterRecoveryPlanViewer';
import { FeatureFlagController } from './FeatureFlagController';

export function ReliabilityDashboard() {
  const [activeTab, setActiveTab] = useState<
    'overview' | 'dependencies' | 'slos' | 'incidents' | 'backups' | 'dr' | 'flags'
  >('overview');

  const [health, setHealth] = useState<DeepHealthResult | null>(null);
  const [circuits, setCircuits] = useState<CircuitBreakerState[]>([]);
  const [slos, setSlos] = useState<SLOMetricSnapshot[]>([]);
  const [incidents, setIncidents] = useState<ReliabilityIncident[]>([]);
  const [backups, setBackups] = useState<BackupRecord[]>([]);
  const [restoreTests, setRestoreTests] = useState<RestoreVerificationTest[]>([]);
  const [plans, setPlans] = useState<DRPlan[]>([]);
  const [drills, setDrills] = useState<DRDrill[]>([]);
  const [flags, setFlags] = useState<FeatureFlag[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadAllData = async () => {
    setIsLoading(true);
    try {
      const [
        healthRes,
        circuitsRes,
        slosRes,
        incidentsRes,
        backupsRes,
        restoreTestsRes,
        plansRes,
        drillsRes,
        flagsRes,
      ] = await Promise.all([
        reliabilityApi.getDeepHealth().catch(() => null),
        reliabilityApi.listCircuits().catch(() => []),
        reliabilityApi.getSLODashboard().catch(() => ({ slos: [] })),
        reliabilityApi.listIncidents().catch(() => []),
        reliabilityApi.listBackups().catch(() => []),
        reliabilityApi.listRestoreTests().catch(() => []),
        reliabilityApi.listDRPlans().catch(() => []),
        reliabilityApi.listDRDrills().catch(() => []),
        reliabilityApi.listFeatureFlags().catch(() => []),
      ]);

      if (healthRes) setHealth(healthRes);
      if (circuitsRes) setCircuits(circuitsRes);
      if (slosRes?.slos) setSlos(slosRes.slos);
      if (incidentsRes) setIncidents(incidentsRes);
      if (backupsRes) setBackups(backupsRes);
      if (restoreTestsRes) setRestoreTests(restoreTestsRes);
      if (plansRes) setPlans(plansRes);
      if (drillsRes) setDrills(drillsRes);
      if (flagsRes) setFlags(flagsRes);
    } catch (err) {
      console.error('Failed to load reliability telemetry', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  const handleResetCircuit = async (serviceName: string) => {
    try {
      await reliabilityApi.resetCircuit(serviceName);
      loadAllData();
    } catch (err) {
      console.error('Failed to reset circuit', err);
    }
  };

  const handleDeclareIncident = async (data: Partial<ReliabilityIncident>) => {
    try {
      await reliabilityApi.declareIncident(data);
      loadAllData();
    } catch (err) {
      console.error('Failed to declare incident', err);
    }
  };

  const handleAcknowledge = async (id: string) => {
    try {
      await reliabilityApi.acknowledgeIncident(id);
      loadAllData();
    } catch (err) {
      console.error('Failed to acknowledge incident', err);
    }
  };

  const handleMitigate = async (id: string) => {
    try {
      await reliabilityApi.mitigateIncident(id);
      loadAllData();
    } catch (err) {
      console.error('Failed to mitigate incident', err);
    }
  };

  const handleResolve = async (id: string) => {
    try {
      await reliabilityApi.resolveIncident(id);
      loadAllData();
    } catch (err) {
      console.error('Failed to resolve incident', err);
    }
  };

  const handleTriggerBackup = async () => {
    try {
      await reliabilityApi.triggerBackup();
      loadAllData();
    } catch (err) {
      console.error('Failed to trigger backup', err);
    }
  };

  const handleRunRestoreTest = async (backupId: string) => {
    try {
      await reliabilityApi.runRestoreTest(backupId);
      loadAllData();
    } catch (err) {
      console.error('Failed to run restore test', err);
    }
  };

  const handleRunDrill = async (scenario: string, initiatedBy: string) => {
    try {
      await reliabilityApi.runDRDrill(scenario, initiatedBy);
      loadAllData();
    } catch (err) {
      console.error('Failed to run DR drill', err);
    }
  };

  const handleToggleFlag = async (flag: FeatureFlag) => {
    try {
      await reliabilityApi.setFeatureFlag(flag);
      loadAllData();
    } catch (err) {
      console.error('Failed to toggle flag', err);
    }
  };

  const handleUpdateRollout = async (flag: FeatureFlag, newPct: number) => {
    try {
      await reliabilityApi.setFeatureFlag({ ...flag, percentage_rollout: newPct });
      loadAllData();
    } catch (err) {
      console.error('Failed to update flag rollout', err);
    }
  };

  return (
    <div className="space-y-6 text-slate-100">
      {/* Header Banner */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <span>🛡️</span> Platform Reliability, SRE & Disaster Recovery
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Expected, detected, contained, recovered, and audited. Multi-layer resilience and business continuity.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={loadAllData}
            disabled={isLoading}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition flex items-center gap-2"
          >
            <span>🔄</span> {isLoading ? 'Refreshing...' : 'Refresh All'}
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800">
        {[
          { id: 'overview', label: 'Health Overview', icon: '📊' },
          { id: 'dependencies', label: 'Circuit Breakers & Probes', icon: '⚡' },
          { id: 'slos', label: 'SLOs & Error Budgets', icon: '🎯' },
          { id: 'incidents', label: 'Incident Command', icon: '🚨' },
          { id: 'backups', label: 'Backups & Sandbox Restores', icon: '💾' },
          { id: 'dr', label: '14-Step DR & Drills', icon: '🔥' },
          { id: 'flags', label: 'Feature Flags & Operations', icon: '🚩' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 text-xs font-semibold rounded-xl transition flex items-center gap-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-lg shadow-cyan-950/40'
                : 'text-slate-400 hover:text-white hover:bg-slate-900 border border-transparent'
            }`}
          >
            <span>{tab.icon}</span> {tab.label}
          </button>
        ))}
      </div>

      {/* Active Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <HealthOverview health={health} onRefresh={loadAllData} isLoading={isLoading} />
          <SLOErrorBudgetCard slos={slos} />
          <DependencyHealthMatrix
            components={health?.components || {}}
            circuits={circuits}
            onResetCircuit={handleResetCircuit}
          />
        </div>
      )}

      {activeTab === 'dependencies' && (
        <DependencyHealthMatrix
          components={health?.components || {}}
          circuits={circuits}
          onResetCircuit={handleResetCircuit}
        />
      )}

      {activeTab === 'slos' && <SLOErrorBudgetCard slos={slos} />}

      {activeTab === 'incidents' && (
        <IncidentManager
          incidents={incidents}
          onDeclareIncident={handleDeclareIncident}
          onAcknowledge={handleAcknowledge}
          onMitigate={handleMitigate}
          onResolve={handleResolve}
          onViewPostmortem={(id) => {
            alert(`Opening postmortem report for incident ${id}`);
          }}
        />
      )}

      {activeTab === 'backups' && (
        <BackupRestoreStatus
          backups={backups}
          restoreTests={restoreTests}
          onTriggerBackup={handleTriggerBackup}
          onRunRestoreTest={handleRunRestoreTest}
          isLoading={isLoading}
        />
      )}

      {activeTab === 'dr' && (
        <DisasterRecoveryPlanViewer
          plans={plans}
          drills={drills}
          onRunDrill={handleRunDrill}
          isLoading={isLoading}
        />
      )}

      {activeTab === 'flags' && (
        <FeatureFlagController
          flags={flags}
          onToggleFlag={handleToggleFlag}
          onUpdateRollout={handleUpdateRollout}
        />
      )}
    </div>
  );
}
