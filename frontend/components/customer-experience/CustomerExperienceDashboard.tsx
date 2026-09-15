'use client';

import React, { useEffect, useState } from 'react';
import {
  Compass,
  Activity,
  HeartHandshake,
  TrendingDown,
  AlertTriangle,
  Layers,
  Sparkles,
  RefreshCw,
  Zap,
} from 'lucide-react';
import {
  customerExperienceApi,
  Customer360Profile as Customer360Type,
  CustomerJourneyItem,
  FrictionPointItem,
  EffortRecordItem,
  ExperienceHealthItem,
  VoiceThemeItem,
  ExpectationGapItem,
  OverviewMetrics,
} from '../../lib/api/customerExperience';
import { Customer360Profile } from './Customer360Profile';
import { JourneyTimelineMap } from './JourneyTimelineMap';
import { FrictionHeatmap } from './FrictionHeatmap';
import { CustomerEffortGauge } from './CustomerEffortGauge';
import { ExperienceHealthCard } from './ExperienceHealthCard';
import { VoiceOfCustomerPanel } from './VoiceOfCustomerPanel';
import { ExpectationGapViewer } from './ExpectationGapViewer';
import { CustomerJourneyCopilot } from './CustomerJourneyCopilot';

export const CustomerExperienceDashboard: React.FC = () => {
  const [overview, setOverview] = useState<OverviewMetrics | null>(null);
  const [profile, setProfile] = useState<Customer360Type | null>(null);
  const [journeys, setJourneys] = useState<CustomerJourneyItem[]>([]);
  const [frictions, setFrictions] = useState<FrictionPointItem[]>([]);
  const [efforts, setEfforts] = useState<EffortRecordItem[]>([]);
  const [health, setHealth] = useState<ExperienceHealthItem | null>(null);
  const [vocThemes, setVocThemes] = useState<VoiceThemeItem[]>([]);
  const [vocRecords, setVocRecords] = useState<any[]>([]);
  const [gaps, setGaps] = useState<ExpectationGapItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [ovRes, profRes, jrnyRes, fricRes, effRes, hlthRes, vocRes, gapRes] = await Promise.all([
        customerExperienceApi.getOverview(),
        customerExperienceApi.getCustomer360('cust-demo-001'),
        customerExperienceApi.listJourneys('cust-demo-001'),
        customerExperienceApi.listFrictions('cust-demo-001'),
        customerExperienceApi.listEfforts('cust-demo-001'),
        customerExperienceApi.getHealth('cust-demo-001'),
        customerExperienceApi.getVoiceOfCustomer(),
        customerExperienceApi.listExpectationGaps('cust-demo-001'),
      ]);

      setOverview(ovRes);
      setProfile(profRes);
      setJourneys(jrnyRes);
      setFrictions(fricRes);
      setEfforts(effRes);
      setHealth(hlthRes);
      setVocThemes(vocRes.themes);
      setVocRecords(vocRes.records);
      setGaps(gapRes);
    } catch (err) {
      console.error('Error fetching CX data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading && !profile) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex items-center gap-3 text-sm text-slate-400">
          <RefreshCw className="h-5 w-5 animate-spin text-indigo-400" />
          Loading Unified Customer Experience & Journey Intelligence Platform...
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-semibold">
              Phase 57 Platform
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-semibold">
              Evidence Grounded
            </span>
          </div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Compass className="h-6 w-6 text-indigo-400" />
            Unified Customer Experience & Journey Intelligence
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time journey reconstruction, friction detection, customer effort scoring, and expectation alignment.
          </p>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition-colors self-start md:self-auto"
        >
          <RefreshCw className="h-3.5 w-3.5 text-indigo-400" />
          Refresh Intelligence
        </button>
      </div>

      {/* Top Stat Cards */}
      {overview && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
              <span>Active Journeys</span>
              <Layers className="h-4 w-4 text-indigo-400" />
            </div>
            <div className="text-2xl font-bold text-white font-mono">{overview.active_journeys_count}</div>
            <div className="text-[11px] text-emerald-400 mt-1 font-mono">
              Completion: {Math.round(overview.journey_completion_rate * 100)}%
            </div>
          </div>

          <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
              <span>Experience Health</span>
              <Activity className="h-4 w-4 text-purple-400" />
            </div>
            <div className="text-2xl font-bold text-white font-mono">{overview.overall_experience_health}</div>
            <div className="text-[11px] text-purple-400 mt-1 font-mono">Composite Index</div>
          </div>

          <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
              <span>Avg Effort (CES)</span>
              <Zap className="h-4 w-4 text-emerald-400" />
            </div>
            <div className="text-2xl font-bold text-white font-mono">{overview.avg_customer_effort_score}</div>
            <div className="text-[11px] text-emerald-400 mt-1 font-mono">Low Effort Tier</div>
          </div>

          <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
              <span>Identified Expansion</span>
              <HeartHandshake className="h-4 w-4 text-cyan-400" />
            </div>
            <div className="text-2xl font-bold text-white font-mono">
              ${overview.identified_expansion_arr_usd.toLocaleString()}
            </div>
            <div className="text-[11px] text-cyan-400 mt-1 font-mono">Pipeline ARR Lift</div>
          </div>
        </div>
      )}

      {/* Customer 360 & Timeline */}
      {profile && <Customer360Profile profile={profile} />}
      {journeys.length > 0 && <JourneyTimelineMap journey={journeys[0]} />}

      {/* Grid: Health & Effort */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {health && <ExperienceHealthCard health={health} />}
        <CustomerEffortGauge effortRecords={efforts} />
      </div>

      {/* Grid: Friction & Expectations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <FrictionHeatmap frictions={frictions} />
        <ExpectationGapViewer gaps={gaps} />
      </div>

      {/* Grid: VoC & Copilot */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <VoiceOfCustomerPanel themes={vocThemes} records={vocRecords} />
        <CustomerJourneyCopilot customerId={profile?.customer_id} />
      </div>
    </div>
  );
};
