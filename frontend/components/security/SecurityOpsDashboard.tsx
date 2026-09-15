'use client';

import React, { useEffect, useState } from 'react';
import {
  securityOpsApi,
  SecurityExecutiveOverview,
  SecurityEventItem,
  SecurityDetectionItem,
  SecurityAlertItem,
  SecurityIncidentItem,
  InvestigationWorkspaceData,
  BlastRadiusData,
  ThreatIndicatorItem,
  RiskHeatmapItem,
} from '@/lib/api/securityOps';
import SecurityOverview from './SecurityOverview';
import SecurityHealth from './SecurityHealth';
import SecurityEventTable from './SecurityEventTable';
import DetectionTable from './DetectionTable';
import AlertTable from './AlertTable';
import IncidentTable from './IncidentTable';
import InvestigationPanel from './InvestigationPanel';
import BlastRadiusView from './BlastRadiusView';
import RiskScore from './RiskScore';
import ThreatIndicatorTable from './ThreatIndicatorTable';
import RemediationPanel from './RemediationPanel';
import SecurityCopilot from './SecurityCopilot';
import { Shield, Activity, Crosshair, AlertTriangle, ShieldAlert, TrendingUp, Globe, Bot, Lock, RefreshCw } from 'lucide-react';

export default function SecurityOpsDashboard() {
  const [activeTab, setActiveTab] = useState<'overview' | 'incidents' | 'alerts' | 'detections' | 'events' | 'risk' | 'intelligence' | 'copilot' | 'emergency'>('overview');

  // State data
  const [overview, setOverview] = useState<SecurityExecutiveOverview | null>(null);
  const [events, setEvents] = useState<SecurityEventItem[]>([]);
  const [detections, setDetections] = useState<SecurityDetectionItem[]>([]);
  const [alerts, setAlerts] = useState<SecurityAlertItem[]>([]);
  const [incidents, setIncidents] = useState<SecurityIncidentItem[]>([]);
  const [indicators, setIndicators] = useState<ThreatIndicatorItem[]>([]);
  const [heatmap, setHeatmap] = useState<RiskHeatmapItem[]>([]);
  const [emergencyControls, setEmergencyControls] = useState<Record<string, boolean>>({});

  // Active modals / workspaces
  const [selectedIncidentWorkspace, setSelectedIncidentWorkspace] = useState<InvestigationWorkspaceData | null>(null);
  const [selectedBlastRadius, setSelectedBlastRadius] = useState<BlastRadiusData | null>(null);
  const [selectedAlertForRemediation, setSelectedAlertForRemediation] = useState<SecurityAlertItem | null>(null);

  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [ovData, evData, detData, alData, incData, indData, riskData, emData] = await Promise.all([
        securityOpsApi.getOverview().catch(() => null),
        securityOpsApi.listEvents().catch(() => []),
        securityOpsApi.listDetections().catch(() => []),
        securityOpsApi.listAlerts().catch(() => []),
        securityOpsApi.listIncidents().catch(() => []),
        securityOpsApi.listThreatIndicators().catch(() => []),
        securityOpsApi.getRisk().catch(() => ({ assessment: null, heatmap: [] })),
        securityOpsApi.getEmergencyControls().catch(() => ({})),
      ]);

      if (ovData) setOverview(ovData);
      setEvents(evData);
      setDetections(detData);
      setAlerts(alData);
      setIncidents(incData);
      setIndicators(indData);
      if (riskData?.heatmap) setHeatmap(riskData.heatmap);
      setEmergencyControls(emData);
    } catch (err) {
      console.error('Error loading Security Operations data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 20000); // Poll every 20s
    return () => clearInterval(interval);
  }, []);

  const handleOpenWorkspace = async (incidentId: string) => {
    try {
      const data = await securityOpsApi.getInvestigationWorkspace(incidentId);
      setSelectedIncidentWorkspace(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleOpenBlastRadius = async (incidentId: string) => {
    try {
      const data = await securityOpsApi.getBlastRadius(incidentId);
      setSelectedBlastRadius(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpdateAlertStatus = async (alertId: string, newStatus: string) => {
    try {
      await securityOpsApi.updateAlertStatus(alertId, newStatus);
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleEmergencyControl = async (control: string, currentVal: boolean) => {
    try {
      await securityOpsApi.toggleEmergencyControl(control, !currentVal, 'soc_lead', 'Administrative SOC override');
      const updated = await securityOpsApi.getEmergencyControls();
      setEmergencyControls(updated);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Sub-navigation Tabs */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 pb-3">
        <div className="flex flex-wrap items-center gap-2">
          {[
            { id: 'overview', label: 'Overview & Health', icon: Shield },
            { id: 'incidents', label: 'Incidents', icon: ShieldAlert, badge: incidents.length },
            { id: 'alerts', label: 'Alerts', icon: AlertTriangle, badge: alerts.length },
            { id: 'detections', label: 'Threat Detections', icon: Crosshair },
            { id: 'events', label: 'Telemetry Stream', icon: Activity },
            { id: 'risk', label: 'Risk Heatmap', icon: TrendingUp },
            { id: 'intelligence', label: 'Threat Intel (IOCs)', icon: Globe },
            { id: 'copilot', label: 'AI Copilot', icon: Bot },
            { id: 'emergency', label: 'Emergency Controls', icon: Lock },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                  isActive
                    ? 'bg-slate-900 text-white shadow-xs'
                    : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
                {tab.badge !== undefined && tab.badge > 0 && (
                  <span
                    className={`ml-1 text-[10px] px-1.5 py-0.2 rounded-full font-bold ${
                      isActive ? 'bg-indigo-500 text-white' : 'bg-slate-100 text-slate-700'
                    }`}
                  >
                    {tab.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>

        <button
          onClick={loadData}
          className="p-1.5 rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 text-xs font-medium flex items-center gap-1 shadow-2xs"
        >
          <RefreshCw className="w-3.5 h-3.5" /> Refresh
        </button>
      </div>

      {/* Active Workspaces & Overlays */}
      {selectedIncidentWorkspace && (
        <InvestigationPanel
          data={selectedIncidentWorkspace}
          loading={false}
          onClose={() => setSelectedIncidentWorkspace(null)}
        />
      )}

      {selectedBlastRadius && (
        <BlastRadiusView
          data={selectedBlastRadius}
          loading={false}
          onClose={() => setSelectedBlastRadius(null)}
        />
      )}

      {selectedAlertForRemediation && (
        <RemediationPanel
          alert={selectedAlertForRemediation}
          onClose={() => setSelectedAlertForRemediation(null)}
          onSuccess={() => {
            loadData();
          }}
        />
      )}

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <SecurityOverview overview={overview} loading={loading} onRefresh={loadData} />
          {overview && <SecurityHealth domainBreakdown={overview.domain_breakdown} />}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <IncidentTable
              incidents={incidents.slice(0, 5)}
              loading={loading}
              onOpenWorkspace={handleOpenWorkspace}
              onOpenBlastRadius={handleOpenBlastRadius}
            />
            <AlertTable
              alerts={alerts.slice(0, 5)}
              loading={loading}
              onUpdateStatus={handleUpdateAlertStatus}
              onSelectAlertForRemediation={(alt) => setSelectedAlertForRemediation(alt)}
            />
          </div>
        </div>
      )}

      {activeTab === 'incidents' && (
        <IncidentTable
          incidents={incidents}
          loading={loading}
          onOpenWorkspace={handleOpenWorkspace}
          onOpenBlastRadius={handleOpenBlastRadius}
        />
      )}

      {activeTab === 'alerts' && (
        <AlertTable
          alerts={alerts}
          loading={loading}
          onUpdateStatus={handleUpdateAlertStatus}
          onSelectAlertForRemediation={(alt) => setSelectedAlertForRemediation(alt)}
        />
      )}

      {activeTab === 'detections' && (
        <DetectionTable detections={detections} loading={loading} onRefresh={loadData} />
      )}

      {activeTab === 'events' && (
        <SecurityEventTable events={events} loading={loading} onRefresh={loadData} />
      )}

      {activeTab === 'risk' && (
        <RiskScore heatmap={heatmap} loading={loading} />
      )}

      {activeTab === 'intelligence' && (
        <ThreatIndicatorTable indicators={indicators} loading={loading} onRefresh={loadData} />
      )}

      {activeTab === 'copilot' && (
        <SecurityCopilot />
      )}

      {activeTab === 'emergency' && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
          <div className="flex justify-between items-center border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Lock className="w-5 h-5 text-rose-600" />
                Emergency Security Controls & Kill Switches
              </h3>
              <p className="text-xs text-slate-500">
                Coordinated containment controls with Phase 44 Administration (Section 28)
              </p>
            </div>
            <span className="text-xs font-bold text-rose-700 bg-rose-50 px-2.5 py-1 rounded-full border border-rose-200">
              SOC Lead Authorized Only
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(emergencyControls).map(([ctrl, isEnabled]) => (
              <div
                key={ctrl}
                className={`p-4 rounded-xl border transition-colors flex justify-between items-center ${
                  isEnabled
                    ? 'bg-rose-50 border-rose-200 text-rose-900'
                    : 'bg-slate-50/70 border-slate-200 text-slate-800'
                }`}
              >
                <div>
                  <div className="font-mono text-xs font-bold">{ctrl}</div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    State: <span className="font-bold">{isEnabled ? 'ENGAGED (LOCKED)' : 'DISENGAGED (NORMAL)'}</span>
                  </div>
                </div>

                <button
                  onClick={() => handleToggleEmergencyControl(ctrl, isEnabled)}
                  className={`px-3 py-1.5 text-xs font-semibold rounded-lg shadow-xs transition-colors ${
                    isEnabled
                      ? 'bg-emerald-600 text-white hover:bg-emerald-700'
                      : 'bg-rose-600 text-white hover:bg-rose-700'
                  }`}
                >
                  {isEnabled ? 'Disengage' : 'ENGAGE LOCK'}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
