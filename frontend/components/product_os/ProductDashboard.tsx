"use client";

import React, { useState, useEffect } from "react";
import {
  fetchProductOverview,
  fetchPortfolio,
  createProduct,
  fetchProblems,
  fetchOpportunities,
  fetchRoadmapBoard,
  fetchTraceabilityMatrix,
  fetchHealthScorecards,
  ProductOverviewMetrics,
  ProductItem,
  ProductProblem,
  ProductOpportunity,
  RoadmapBoard,
  TraceabilityEntry,
  ProductHealthScorecard,
} from "@/lib/api/productOs";

import { ProductOverviewMetricsView } from "./ProductOverviewMetrics";
import { PortfolioStrategyPanelView } from "./PortfolioStrategyPanel";
import { ProblemOpportunityTreeView } from "./ProblemOpportunityTree";
import { PrioritizationRoadmapBoardView } from "./PrioritizationRoadmapBoard";
import { RequirementsTraceabilityMatrixView } from "./RequirementsTraceabilityMatrix";
import { ProductHealthAnalyticsRadarView } from "./ProductHealthAnalyticsRadar";
import { ProductCopilotView } from "./ProductCopilot";

export const ProductDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<
    "overview" | "portfolio" | "discovery" | "roadmap" | "traceability" | "health" | "copilot"
  >("overview");

  const [metrics, setMetrics] = useState<ProductOverviewMetrics | null>(null);
  const [portfolio, setPortfolio] = useState<ProductItem[]>([]);
  const [problems, setProblems] = useState<ProductProblem[]>([]);
  const [opportunities, setOpportunities] = useState<ProductOpportunity[]>([]);
  const [roadmap, setRoadmap] = useState<RoadmapBoard | null>(null);
  const [matrix, setMatrix] = useState<TraceabilityEntry[]>([]);
  const [healthScorecards, setHealthScorecards] = useState<ProductHealthScorecard[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const [m, p, probs, opps, rdm, mat, hlth] = await Promise.all([
        fetchProductOverview(),
        fetchPortfolio(),
        fetchProblems(),
        fetchOpportunities(),
        fetchRoadmapBoard(),
        fetchTraceabilityMatrix(),
        fetchHealthScorecards(),
      ]);
      setMetrics(m);
      setPortfolio(p);
      setProblems(probs);
      setOpportunities(opps);
      setRoadmap(rdm);
      setMatrix(mat);
      setHealthScorecards(hlth);
    } catch (err) {
      console.error("Failed to load Product OS data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateProduct = async (payload: any) => {
    await createProduct(payload);
    await loadData();
  };

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-100 tracking-tight">
              Unified Product Management & Lifecycle OS
            </h1>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-950 text-indigo-400 border border-indigo-800 font-mono">
              Phase 60
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Closed-loop operating system connecting Market, Problems, Roadmap, Engineering, Adoption, and Realized Customer Value.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => loadData()}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs rounded-lg transition border border-slate-700"
          >
            Refresh Telemetry
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      <ProductOverviewMetricsView metrics={metrics} />

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-1 overflow-x-auto text-xs">
        {[
          { key: "overview", label: "Overview & Copilot" },
          { key: "portfolio", label: "Portfolio & Vision" },
          { key: "discovery", label: "Discovery & Opportunities" },
          { key: "roadmap", label: "Roadmap & Prioritization" },
          { key: "traceability", label: "Requirements & Traceability" },
          { key: "health", label: "7-Factor Health Scorecards" },
          { key: "copilot", label: "Product Copilot" },
        ].map((t) => (
          <button
            key={t.key}
            onClick={() => setActiveTab(t.key as any)}
            className={`px-4 py-2.5 font-medium border-b-2 transition whitespace-nowrap ${
              activeTab === t.key
                ? "border-indigo-500 text-indigo-400 bg-slate-900/40"
                : "border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab Panels */}
      {loading ? (
        <div className="p-8 text-center text-xs text-slate-500 animate-pulse">
          Synchronizing product lifecycle telemetry...
        </div>
      ) : (
        <div className="space-y-6">
          {activeTab === "overview" && (
            <div className="space-y-6">
              <ProductCopilotView />
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <PortfolioStrategyPanelView
                  products={portfolio}
                  onCreateProduct={handleCreateProduct}
                />
                <ProductHealthAnalyticsRadarView scorecards={healthScorecards} />
              </div>
            </div>
          )}

          {activeTab === "portfolio" && (
            <PortfolioStrategyPanelView
              products={portfolio}
              onCreateProduct={handleCreateProduct}
            />
          )}

          {activeTab === "discovery" && (
            <ProblemOpportunityTreeView
              problems={problems}
              opportunities={opportunities}
            />
          )}

          {activeTab === "roadmap" && (
            <PrioritizationRoadmapBoardView roadmap={roadmap} />
          )}

          {activeTab === "traceability" && (
            <RequirementsTraceabilityMatrixView matrix={matrix} />
          )}

          {activeTab === "health" && (
            <ProductHealthAnalyticsRadarView scorecards={healthScorecards} />
          )}

          {activeTab === "copilot" && <ProductCopilotView />}
        </div>
      )}
    </div>
  );
};
