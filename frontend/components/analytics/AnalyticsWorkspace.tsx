'use client';

import React, { useState, useEffect } from 'react';
import {
  ExecutiveOverview,
  SalesIntelligence,
  DeliveryIntelligence,
  SupportIntelligence,
  BusinessInsight,
  BusinessRecommendation,
  Experiment,
  analyticsApi,
} from '@/lib/api/analytics';
import { ExecutiveDashboard } from './ExecutiveDashboard';
import { SalesIntelligencePanel } from './SalesIntelligencePanel';
import { DeliveryIntelligencePanel } from './DeliveryIntelligencePanel';
import { OrganizationalLearningHub } from './OrganizationalLearningHub';
import { NaturalLanguageAnalyticsBar } from './NaturalLanguageAnalyticsBar';

export const AnalyticsWorkspace: React.FC = () => {
  const [activeDomain, setActiveDomain] = useState<'executive' | 'sales' | 'delivery' | 'learning'>('executive');
  const [loading, setLoading] = useState(true);

  const [overview, setOverview] = useState<ExecutiveOverview | null>(null);
  const [salesData, setSalesData] = useState<SalesIntelligence | null>(null);
  const [deliveryData, setDeliveryData] = useState<DeliveryIntelligence | null>(null);
  const [supportData, setSupportData] = useState<SupportIntelligence | null>(null);
  const [insights, setInsights] = useState<BusinessInsight[]>([]);
  const [recommendations, setRecommendations] = useState<BusinessRecommendation[]>([]);
  const [experiments, setExperiments] = useState<Experiment[]>([]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [ov, sl, dl, sp, ins, rec, exp] = await Promise.all([
        analyticsApi.getOverview(),
        analyticsApi.getSalesIntelligence(),
        analyticsApi.getDeliveryIntelligence(),
        analyticsApi.getSupportIntelligence(),
        analyticsApi.listInsights(),
        analyticsApi.listRecommendations(),
        analyticsApi.listExperiments(),
      ]);
      setOverview(ov);
      setSalesData(sl);
      setDeliveryData(dl);
      setSupportData(sp);
      setInsights(ins);
      setRecommendations(rec);
      setExperiments(exp);
    } catch (err) {
      console.error('Failed to load analytics workspace data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRunLearningCycle = async () => {
    setLoading(true);
    try {
      await analyticsApi.runLearningCycle();
      await loadData();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Natural Language Query Bar */}
      <NaturalLanguageAnalyticsBar />

      {/* Main Workspace Navigation */}
      <div className="flex items-center gap-2 border-b border-zinc-800 pb-2">
        <button
          onClick={() => setActiveDomain('executive')}
          className={`px-4 py-2 text-sm font-semibold rounded-lg transition-colors ${
            activeDomain === 'executive'
              ? 'bg-indigo-600 text-white shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60'
          }`}
        >
          Executive Overview
        </button>
        <button
          onClick={() => setActiveDomain('sales')}
          className={`px-4 py-2 text-sm font-semibold rounded-lg transition-colors ${
            activeDomain === 'sales'
              ? 'bg-indigo-600 text-white shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60'
          }`}
        >
          Sales & Funnel Intelligence
        </button>
        <button
          onClick={() => setActiveDomain('delivery')}
          className={`px-4 py-2 text-sm font-semibold rounded-lg transition-colors ${
            activeDomain === 'delivery'
              ? 'bg-indigo-600 text-white shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60'
          }`}
        >
          Delivery & Variance Intelligence
        </button>
        <button
          onClick={() => setActiveDomain('learning')}
          className={`px-4 py-2 text-sm font-semibold rounded-lg transition-colors ${
            activeDomain === 'learning'
              ? 'bg-indigo-600 text-white shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60'
          }`}
        >
          Organizational Learning Hub ({insights.length})
        </button>
      </div>

      {/* Active Panel View */}
      {activeDomain === 'executive' && (
        <ExecutiveDashboard
          overview={overview}
          loading={loading}
          onRefresh={loadData}
          onRunLearningCycle={handleRunLearningCycle}
        />
      )}

      {activeDomain === 'sales' && <SalesIntelligencePanel data={salesData} loading={loading} />}

      {activeDomain === 'delivery' && <DeliveryIntelligencePanel data={deliveryData} loading={loading} />}

      {activeDomain === 'learning' && (
        <OrganizationalLearningHub
          insights={insights}
          recommendations={recommendations}
          experiments={experiments}
          onRefresh={loadData}
        />
      )}
    </div>
  );
};
