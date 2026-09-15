'use client';

import React, { useEffect, useState } from 'react';
import {
  TrendingUp,
  RefreshCw,
  DollarSign,
  Compass,
  Layers,
  Sparkles,
} from 'lucide-react';
import {
  revenueGrowthApi,
  RevenueOverviewMetrics as MetricsType,
  SalesOpportunityItem,
  SalesForecastItem,
  RevenueWaterfallItem,
  PricingTierItem,
  DiscountRequestItem,
  DealRiskItem,
  GrowthOpportunityItem,
  MarketCoverageItem,
  TargetAccountItem,
} from '../../lib/api/revenueGrowth';
import { RevenueOverviewMetrics } from './RevenueOverviewMetrics';
import { PipelineStageBoard } from './PipelineStageBoard';
import { RevenueForecastChart } from './RevenueForecastChart';
import { GtmCoveragePanel } from './GtmCoveragePanel';
import { RevenueWaterfallChart } from './RevenueWaterfallChart';
import { PricingDiscountManager } from './PricingDiscountManager';
import { DealRiskRadar } from './DealRiskRadar';
import { RevenueGrowthOpportunities } from './RevenueGrowthOpportunities';
import { RevenueCopilot } from './RevenueCopilot';

export const RevenueDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricsType | null>(null);
  const [opportunities, setOpportunities] = useState<SalesOpportunityItem[]>([]);
  const [forecasts, setForecasts] = useState<SalesForecastItem[]>([]);
  const [waterfalls, setWaterfalls] = useState<RevenueWaterfallItem[]>([]);
  const [pricing, setPricing] = useState<PricingTierItem[]>([]);
  const [discounts, setDiscounts] = useState<DiscountRequestItem[]>([]);
  const [risks, setRisks] = useState<DealRiskItem[]>([]);
  const [growth, setGrowth] = useState<GrowthOpportunityItem[]>([]);
  const [coverage, setCoverage] = useState<MarketCoverageItem[]>([]);
  const [accounts, setAccounts] = useState<TargetAccountItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [ovRes, oppRes, fcRes, watRes, prcRes, dscRes, rskRes, grwRes, covRes, accRes] = await Promise.all([
        revenueGrowthApi.getOverview(),
        revenueGrowthApi.listOpportunities(),
        revenueGrowthApi.getForecasts(),
        revenueGrowthApi.getWaterfalls(),
        revenueGrowthApi.listPricingTiers(),
        revenueGrowthApi.listDiscounts(),
        revenueGrowthApi.listDealRisks(),
        revenueGrowthApi.listGrowthOpportunities(),
        revenueGrowthApi.getMarketCoverage(),
        revenueGrowthApi.listTargetAccounts(),
      ]);

      setMetrics(ovRes);
      setOpportunities(oppRes);
      setForecasts(fcRes);
      setWaterfalls(watRes);
      setPricing(prcRes);
      setDiscounts(dscRes);
      setRisks(rskRes);
      setGrowth(grwRes);
      setCoverage(covRes);
      setAccounts(accRes);
    } catch (err) {
      console.error('Error fetching revenue data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading && !metrics) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex items-center gap-3 text-sm text-slate-400">
          <RefreshCw className="h-5 w-5 animate-spin text-emerald-400" />
          Loading Unified Revenue Growth & Go-to-Market Platform...
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
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-semibold">
              Phase 58 Platform
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-semibold">
              Evidence Grounded
            </span>
          </div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <TrendingUp className="h-6 w-6 text-emerald-400" />
            Unified Revenue Growth, GTM Intelligence & Commercial Optimization
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Probabilistic revenue forecasting, sales pipeline matrix, ARR waterfall, and commercial governance.
          </p>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition-colors self-start md:self-auto"
        >
          <RefreshCw className="h-3.5 w-3.5 text-emerald-400" />
          Refresh Revenue Data
        </button>
      </div>

      {/* Top Metric Cards */}
      {metrics && <RevenueOverviewMetrics metrics={metrics} />}

      {/* Pipeline Board */}
      <PipelineStageBoard opportunities={opportunities} />

      {/* Grid: Forecast & Waterfall */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <RevenueForecastChart forecasts={forecasts} />
        {waterfalls.length > 0 && <RevenueWaterfallChart waterfall={waterfalls[0]} />}
      </div>

      {/* Grid: Coverage & Pricing */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GtmCoveragePanel coverage={coverage} accounts={accounts} />
        <PricingDiscountManager pricingTiers={pricing} discounts={discounts} />
      </div>

      {/* Grid: Deal Risk & Growth Opportunities */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <DealRiskRadar risks={risks} />
        <RevenueGrowthOpportunities opportunities={growth} />
      </div>

      {/* Revenue Intelligence Copilot */}
      <RevenueCopilot />
    </div>
  );
};
