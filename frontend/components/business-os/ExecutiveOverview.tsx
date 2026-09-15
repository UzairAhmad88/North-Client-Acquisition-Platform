'use client';

import React, { useEffect, useState } from 'react';
import {
  BusinessHealthReport,
  DecisionRecord,
  ExecutiveBriefing,
  OrganizationalRisk,
  StrategicObjective,
  businessOSApi,
} from '@/lib/api/business_os';
import { BusinessHealth } from './BusinessHealth';
import { DecisionQueue } from './DecisionQueue';
import { RiskOverview } from './RiskOverview';
import { ScenarioBuilder } from './ScenarioBuilder';
import { ExecutiveAssistant } from './ExecutiveAssistant';
import { ExecutiveBriefingComponent } from './ExecutiveBriefing';
import { StrategyProgress } from './StrategyProgress';

export const ExecutiveOverview: React.FC = () => {
  const [overviewData, setOverviewData] = useState<any>(null);
  const [healthData, setHealthData] = useState<BusinessHealthReport | null>(null);
  const [briefingData, setBriefingData] = useState<ExecutiveBriefing | null>(null);
  const [decisions, setDecisions] = useState<DecisionRecord[]>([]);
  const [risks, setRisks] = useState<OrganizationalRisk[]>([]);
  const [objectives, setObjectives] = useState<StrategicObjective[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<string>('360_overview');

  const loadData = async () => {
    try {
      setIsLoading(true);
      const [ov, hl, br, dec, rk, obj] = await Promise.all([
        businessOSApi.getOverview(),
        businessOSApi.getHealth(),
        businessOSApi.getBriefing('DAILY'),
        businessOSApi.listDecisions(),
        businessOSApi.listRisks(),
        businessOSApi.listObjectives(),
      ]);
      setOverviewData(ov);
      setHealthData(hl);
      setBriefingData(br);
      setDecisions(dec);
      setRisks(rk);
      setObjectives(obj);
    } catch (e) {
      console.error('Error loading Business OS data', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (isLoading || !healthData || !briefingData) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-slate-400 text-sm animate-pulse">Loading Executive Command Center Intelligence...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-xl p-6 shadow-2xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-black text-white">Uzaii Business OS — Executive Command Center</h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              OPERATIONAL 360
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1 max-w-3xl">
            Unifying 41 operational domains into strategic intelligence, OKR alignment, 10-dimension health scoring,
            decision governance, and grounded scenario planning.
          </p>
        </div>
        <button
          onClick={loadData}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold border border-slate-700 transition-all"
        >
          ↻ Refresh Intelligence
        </button>
      </div>

      {/* Navigation Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-3">
        {[
          { id: '360_overview', label: 'Executive 360 Overview' },
          { id: 'health', label: '10-Dimension Health' },
          { id: 'strategy', label: 'Strategy & OKRs' },
          { id: 'decisions', label: 'Decision Queue' },
          { id: 'risks', label: 'Enterprise Risk Matrix' },
          { id: 'scenarios', label: 'Scenario Simulator' },
          { id: 'assistant', label: 'Executive AI Copilot' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
              activeTab === tab.id
                ? 'bg-indigo-600 text-white shadow-lg'
                : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      {activeTab === '360_overview' && (
        <div className="space-y-6">
          <ExecutiveBriefingComponent initialBriefing={briefingData} />

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-xs text-slate-400 font-medium">Monthly Recurring Revenue</div>
              <div className="text-xl font-black text-emerald-400 mt-1">PKR 3.80M</div>
              <div className="text-[11px] text-emerald-500 font-semibold mt-0.5">↑ 10.1% vs prev period</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-xs text-slate-400 font-medium">Gross Profit Margin</div>
              <div className="text-xl font-black text-indigo-400 mt-1">65.4%</div>
              <div className="text-[11px] text-indigo-400 font-semibold mt-0.5">Target: 65.0%</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-xs text-slate-400 font-medium">Net Client Retention</div>
              <div className="text-xl font-black text-emerald-400 mt-1">94.5%</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Target: 95.0%</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-xs text-slate-400 font-medium">Platform Availability</div>
              <div className="text-xl font-black text-emerald-400 mt-1">99.95%</div>
              <div className="text-[11px] text-emerald-500 font-semibold mt-0.5">Zero critical outages</div>
            </div>
          </div>

          <BusinessHealth healthReport={healthData} />
          <DecisionQueue decisions={decisions} onDecisionUpdated={loadData} />
        </div>
      )}

      {activeTab === 'health' && <BusinessHealth healthReport={healthData} />}
      {activeTab === 'strategy' && <StrategyProgress objectives={objectives} />}
      {activeTab === 'decisions' && <DecisionQueue decisions={decisions} onDecisionUpdated={loadData} />}
      {activeTab === 'risks' && <RiskOverview risks={risks} />}
      {activeTab === 'scenarios' && <ScenarioBuilder />}
      {activeTab === 'assistant' && <ExecutiveAssistant />}
    </div>
  );
};
