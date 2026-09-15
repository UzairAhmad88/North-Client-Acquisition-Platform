"use client";

import React, { useState, useEffect } from "react";
import {
  marketingApi,
  MarketingOverviewMetrics,
  MarketingAudience,
  MarketingPositioning,
  ContentAsset,
  ContentGap,
  MarketingCampaign,
  MarketingLead,
  FunnelMetrics,
  MarketingRoi,
  MarketingForecast,
  MarketingRisk,
  MarketingFatigue,
} from "@/lib/api/marketing";
import { MarketingOverviewMetricsView } from "./MarketingOverviewMetrics";
import { AudiencePositioningPanel } from "./AudiencePositioningPanel";
import { ContentCommandCenter } from "./ContentCommandCenter";
import { CampaignManager } from "./CampaignManager";
import { LeadScoringFunnel } from "./LeadScoringFunnel";
import { AttributionRoiMatrix } from "./AttributionRoiMatrix";
import { MarketingForecastChart } from "./MarketingForecastChart";
import { MarketingRiskFatigueRadar } from "./MarketingRiskFatigueRadar";
import { MarketingCopilot } from "./MarketingCopilot";

export const MarketingDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<
    "overview" | "audiences" | "content" | "campaigns" | "leads" | "economics" | "copilot"
  >("overview");

  const [metrics, setMetrics] = useState<MarketingOverviewMetrics | null>(null);
  const [audiences, setAudiences] = useState<MarketingAudience[]>([]);
  const [positionings, setPositionings] = useState<MarketingPositioning[]>([]);
  const [content, setContent] = useState<ContentAsset[]>([]);
  const [gaps, setGaps] = useState<ContentGap[]>([]);
  const [campaigns, setCampaigns] = useState<MarketingCampaign[]>([]);
  const [leads, setLeads] = useState<MarketingLead[]>([]);
  const [funnel, setFunnel] = useState<FunnelMetrics | null>(null);
  const [roi, setRoi] = useState<MarketingRoi | null>(null);
  const [forecasts, setForecasts] = useState<MarketingForecast[]>([]);
  const [risks, setRisks] = useState<MarketingRisk[]>([]);
  const [fatigue, setFatigue] = useState<MarketingFatigue[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          overviewData,
          audData,
          posData,
          cntData,
          gapData,
          cmpData,
          ledData,
          fnlData,
          roiData,
          fcData,
          rskData,
          fatData,
        ] = await Promise.all([
          marketingApi.getOverview(),
          marketingApi.getAudiences(),
          marketingApi.getPositioning(),
          marketingApi.getContent(),
          marketingApi.getContentGaps(),
          marketingApi.getCampaigns(),
          marketingApi.getLeads(),
          marketingApi.getFunnel(),
          marketingApi.getRoi(),
          marketingApi.getForecasts(),
          marketingApi.getRisks(),
          marketingApi.getFatigue(),
        ]);

        setMetrics(overviewData);
        setAudiences(audData);
        setPositionings(posData);
        setContent(cntData);
        setGaps(gapData);
        setCampaigns(cmpData);
        setLeads(ledData);
        setFunnel(fnlData);
        setRoi(roiData);
        setForecasts(fcData);
        setRisks(rskData);
        setFatigue(fatData);
      } catch (err) {
        console.error("Failed to load marketing dashboard data", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const tabs = [
    { id: "overview", label: "Executive Overview" },
    { id: "audiences", label: "Audiences & Positioning" },
    { id: "content", label: "Content & Claims" },
    { id: "campaigns", label: "Campaigns & Channels" },
    { id: "leads", label: "Lead Scoring & Funnel" },
    { id: "economics", label: "Attribution & Forecast" },
    { id: "copilot", label: "Marketing Copilot" },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span>Marketing Intelligence & Demand Platform</span>
            <span className="text-xs bg-indigo-950 text-indigo-400 border border-indigo-800 px-2 py-0.5 rounded-full font-mono">
              Phase 59
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Evidence-grounded demand generation, multi-touch attribution, content strategy, and governed automation
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id as any)}
            className={`text-xs px-3.5 py-1.5 rounded-lg transition font-medium ${
              activeTab === t.id
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Top Metric Cards */}
      <MarketingOverviewMetricsView metrics={metrics} />

      {/* Tab Panels */}
      {activeTab === "overview" && (
        <div className="space-y-6">
          <AudiencePositioningPanel audiences={audiences} positionings={positionings} />
          <CampaignManager campaigns={campaigns} />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AttributionRoiMatrix roi={roi} />
            <MarketingForecastChart forecasts={forecasts} />
          </div>
          <MarketingRiskFatigueRadar risks={risks} fatigue={fatigue} />
        </div>
      )}

      {activeTab === "audiences" && (
        <AudiencePositioningPanel audiences={audiences} positionings={positionings} />
      )}

      {activeTab === "content" && (
        <ContentCommandCenter content={content} gaps={gaps} />
      )}

      {activeTab === "campaigns" && (
        <CampaignManager campaigns={campaigns} />
      )}

      {activeTab === "leads" && (
        <LeadScoringFunnel leads={leads} funnel={funnel} />
      )}

      {activeTab === "economics" && (
        <div className="space-y-6">
          <AttributionRoiMatrix roi={roi} />
          <MarketingForecastChart forecasts={forecasts} />
        </div>
      )}

      {activeTab === "copilot" && (
        <div className="max-w-4xl mx-auto">
          <MarketingCopilot />
        </div>
      )}
    </div>
  );
};
