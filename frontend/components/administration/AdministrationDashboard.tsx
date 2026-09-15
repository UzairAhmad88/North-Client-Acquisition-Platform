'use client';

import React, { useState, useEffect } from 'react';
import {
  administrationApi,
  AdminHealthReport,
  ConfigItem,
  PolicyItem,
  FeatureFlagItem,
  EnvironmentDefinition,
  ProviderConfiguration,
  KillSwitchItem,
  MaintenanceState,
  DriftItem,
} from '@/lib/api/administration';

import { ConfigurationManagerView } from './ConfigurationManagerView';
import { PolicyEngineView } from './PolicyEngineView';
import { SystemControlsView } from './SystemControlsView';
import { FeatureFlagsView } from './FeatureFlagsView';
import { EnvironmentsView } from './EnvironmentsView';
import { IntegrationsView } from './IntegrationsView';
import { MaintenanceView } from './MaintenanceView';
import { DriftDetectorView } from './DriftDetectorView';

export function AdministrationDashboard() {
  const [activeTab, setActiveTab] = useState<
    'overview' | 'configs' | 'policies' | 'controls' | 'flags' | 'environments' | 'integrations' | 'maintenance' | 'drift'
  >('overview');

  const [health, setHealth] = useState<AdminHealthReport | null>(null);
  const [configs, setConfigs] = useState<ConfigItem[]>([]);
  const [policies, setPolicies] = useState<PolicyItem[]>([]);
  const [flags, setFlags] = useState<FeatureFlagItem[]>([]);
  const [environments, setEnvironments] = useState<EnvironmentDefinition[]>([]);
  const [integrations, setIntegrations] = useState<ProviderConfiguration[]>([]);
  const [controls, setControls] = useState<KillSwitchItem[]>([]);
  const [maintenance, setMaintenance] = useState<MaintenanceState | null>(null);
  const [drifts, setDrifts] = useState<DriftItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadAllData = async () => {
    setIsLoading(true);
    try {
      const [
        healthRes,
        configsRes,
        policiesRes,
        flagsRes,
        environmentsRes,
        integrationsRes,
        controlsRes,
        maintenanceRes,
        driftsRes,
      ] = await Promise.all([
        administrationApi.getHealth().catch(() => null),
        administrationApi.listConfigs().catch(() => []),
        administrationApi.listPolicies().catch(() => []),
        administrationApi.listFeatureFlags().catch(() => []),
        administrationApi.listEnvironments().catch(() => []),
        administrationApi.listIntegrations().catch(() => []),
        administrationApi.listSystemControls().catch(() => []),
        administrationApi.getMaintenanceState().catch(() => null),
        administrationApi.listDrifts().catch(() => []),
      ]);

      setHealth(healthRes);
      setConfigs(configsRes || []);
      setPolicies(policiesRes || []);
      setFlags(flagsRes || []);
      setEnvironments(environmentsRes || []);
      setIntegrations(integrationsRes || []);
      setControls(controlsRes || []);
      setMaintenance(maintenanceRes);
      setDrifts(driftsRes || []);
    } catch (err) {
      console.error('Failed to load administration data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Platform Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur shadow-2xl">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🎛️</span>
            <div>
              <h1 className="text-2xl font-black tracking-tight text-white">
                Platform Administration & Control Center
              </h1>
              <p className="text-xs text-slate-400">
                Centralized runtime configuration, enterprise policy engine, feature flags, environments, and emergency controls
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-slate-950 px-3.5 py-2 rounded-xl border border-slate-800">
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                health?.status === 'HEALTHY'
                  ? 'bg-emerald-500 animate-pulse'
                  : health?.status === 'STABLE'
                  ? 'bg-cyan-500'
                  : 'bg-rose-500 animate-ping'
              }`}
            />
            <span className="text-xs font-bold font-mono uppercase tracking-wider text-slate-200">
              {health?.status || 'HEALTHY'}
            </span>
          </div>

          <button
            onClick={loadAllData}
            disabled={isLoading}
            className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-4 py-2 rounded-xl text-xs shadow-lg transition flex items-center gap-2"
          >
            <span>{isLoading ? '⏳' : '🔄'}</span>
            <span>{isLoading ? 'Refreshing...' : 'Refresh All'}</span>
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'overview', label: '📊 Overview & Health', badge: null },
          { id: 'configs', label: '⚙️ Configurations', badge: configs.length },
          { id: 'policies', label: '📜 Policy Engine', badge: policies.length },
          { id: 'controls', label: '🛑 System Controls & Kill Switches', badge: controls.filter((c) => c.state === 'ACTIVE').length || null },
          { id: 'flags', label: '🚩 Feature Flags', badge: flags.length },
          { id: 'environments', label: '🌐 Environments', badge: environments.length },
          { id: 'integrations', label: '🔌 Integrations', badge: integrations.length },
          { id: 'maintenance', label: '🚧 Maintenance Mode', badge: maintenance?.current_mode !== 'NORMAL' ? 'ACTIVE' : null },
          { id: 'drift', label: '🔍 Drift Detector', badge: drifts.length || null },
        ].map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'bg-slate-900/60 text-slate-400 hover:bg-slate-800 hover:text-white border border-slate-800/80'
              }`}
            >
              <span>{tab.label}</span>
              {tab.badge !== null && (
                <span
                  className={`text-[10px] px-1.5 py-0.5 rounded-full font-mono ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : typeof tab.badge === 'string'
                      ? 'bg-amber-500 text-black font-extrabold'
                      : 'bg-slate-800 text-slate-300'
                  }`}
                >
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <div className="mt-4">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Health Scorecards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 backdrop-blur space-y-1">
                <span className="text-[11px] text-slate-400 font-semibold uppercase block">
                  Configuration Validity
                </span>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-black font-mono text-emerald-400">
                    {health?.configuration_validity_score ?? 100}%
                  </span>
                </div>
                <span className="text-[10px] text-slate-500 block">Strict type & schema conformance</span>
              </div>

              <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 backdrop-blur space-y-1">
                <span className="text-[11px] text-slate-400 font-semibold uppercase block">
                  Policy Consistency
                </span>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-black font-mono text-cyan-400">
                    {health?.policy_consistency_score ?? 100}%
                  </span>
                </div>
                <span className="text-[10px] text-slate-500 block">Cross-domain rule alignment</span>
              </div>

              <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 backdrop-blur space-y-1">
                <span className="text-[11px] text-slate-400 font-semibold uppercase block">
                  Integration Health
                </span>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-black font-mono text-indigo-400">
                    {health?.integration_health_score ?? 100}%
                  </span>
                </div>
                <span className="text-[10px] text-slate-500 block">Upstream provider gateways</span>
              </div>

              <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 backdrop-blur space-y-1">
                <span className="text-[11px] text-slate-400 font-semibold uppercase block">
                  Active Kill Switches
                </span>
                <div className="flex items-baseline gap-2">
                  <span
                    className={`text-3xl font-black font-mono ${
                      (health?.active_kill_switches_count || 0) > 0 ? 'text-rose-400' : 'text-slate-300'
                    }`}
                  >
                    {health?.active_kill_switches_count ?? 0}
                  </span>
                </div>
                <span className="text-[10px] text-slate-500 block">Subsystem circuit disconnections</span>
              </div>
            </div>

            {/* Quick Actions & Status Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="md:col-span-2 bg-slate-900/40 border border-slate-800 rounded-2xl p-6 backdrop-blur space-y-4">
                <h3 className="text-base font-bold text-white">Platform Subsystems Summary</h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                  <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
                    <span className="text-slate-500 block text-[10px] uppercase">Registered Configs</span>
                    <span className="text-lg font-bold text-white font-mono">{configs.length}</span>
                  </div>
                  <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
                    <span className="text-slate-500 block text-[10px] uppercase">Active Policies</span>
                    <span className="text-lg font-bold text-white font-mono">{policies.length}</span>
                  </div>
                  <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
                    <span className="text-slate-500 block text-[10px] uppercase">Feature Flags</span>
                    <span className="text-lg font-bold text-white font-mono">{flags.length}</span>
                  </div>
                  <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
                    <span className="text-slate-500 block text-[10px] uppercase">Environments</span>
                    <span className="text-lg font-bold text-white font-mono">{environments.length}</span>
                  </div>
                  <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
                    <span className="text-slate-500 block text-[10px] uppercase">Upstream Providers</span>
                    <span className="text-lg font-bold text-white font-mono">{integrations.length}</span>
                  </div>
                  <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
                    <span className="text-slate-500 block text-[10px] uppercase">Unresolved Drifts</span>
                    <span
                      className={`text-lg font-bold font-mono ${
                        drifts.length > 0 ? 'text-rose-400' : 'text-emerald-400'
                      }`}
                    >
                      {drifts.length}
                    </span>
                  </div>
                </div>
              </div>

              {/* Maintenance State Widget */}
              <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 backdrop-blur space-y-3 flex flex-col justify-between">
                <div>
                  <h3 className="text-base font-bold text-white">Maintenance Mode</h3>
                  <p className="text-xs text-slate-400 mt-1">
                    Current Platform Status:{' '}
                    <strong className="text-white">{maintenance?.current_mode || 'NORMAL'}</strong>
                  </p>
                  <div className="mt-4 bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs space-y-1">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Mutations:</span>
                      <span className={maintenance?.is_mutation_allowed ? 'text-emerald-400' : 'text-rose-400'}>
                        {maintenance?.is_mutation_allowed ? 'Permitted' : 'Locked (Read-Only)'}
                      </span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => setActiveTab('maintenance')}
                  className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold py-2.5 px-4 rounded-xl border border-slate-700 transition"
                >
                  Manage Maintenance Windows
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'configs' && (
          <ConfigurationManagerView configs={configs} onRefresh={loadAllData} />
        )}

        {activeTab === 'policies' && (
          <PolicyEngineView policies={policies} onRefresh={loadAllData} />
        )}

        {activeTab === 'controls' && (
          <SystemControlsView switches={controls} onRefresh={loadAllData} />
        )}

        {activeTab === 'flags' && (
          <FeatureFlagsView flags={flags} onRefresh={loadAllData} />
        )}

        {activeTab === 'environments' && (
          <EnvironmentsView environments={environments} onRefresh={loadAllData} />
        )}

        {activeTab === 'integrations' && (
          <IntegrationsView providers={integrations} onRefresh={loadAllData} />
        )}

        {activeTab === 'maintenance' && (
          <MaintenanceView maintenance={maintenance} onRefresh={loadAllData} />
        )}

        {activeTab === 'drift' && (
          <DriftDetectorView drifts={drifts} onRefresh={loadAllData} />
        )}
      </div>
    </div>
  );
}
