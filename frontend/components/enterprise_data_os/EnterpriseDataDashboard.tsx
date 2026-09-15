"use client";

import React, { useEffect, useState } from "react";
import {
  fetchEnterpriseDataOverview,
  fetchDataDomains,
  fetchDataSources,
  fetchDataPipelines,
  fetchLakehouseDatasets,
  fetchDataContracts,
  fetchDataProducts,
  fetchDataCatalog,
  fetchBusinessGlossary,
  fetchSemanticMetrics,
  fetchDataQualityRules,
  fetchDataLineage,
  fetchFeatures,
  fetchDataFinopsSpend,
  EnterpriseDataOverviewMetrics,
  DataDomainItem,
  DataSourceItem,
  DataPipelineItem,
  LakehouseDatasetItem,
  DataContractItem,
  DataProductItem,
  DataCatalogAssetItem,
  BusinessGlossaryTermItem,
  SemanticMetricItem,
  DataQualityRuleItem,
  DataLineageEdgeItem,
  FeatureStoreItem,
  DataFinopsSpendItem,
} from "@/lib/api/enterpriseDataOs";
import { DataOverviewMetricsView } from "./DataOverviewMetrics";
import { DataSourcesPipelinesPanel } from "./DataSourcesPipelinesPanel";
import { LakehouseDataProductsView } from "./LakehouseDataProductsView";
import { DataContractsQualityRadar } from "./DataContractsQualityRadar";
import { SemanticMetricStoreExplorer } from "./SemanticMetricStoreExplorer";
import { DataLineageGovernanceMatrix } from "./DataLineageGovernanceMatrix";
import { DataCopilotView } from "./DataCopilot";

export const EnterpriseDataDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<EnterpriseDataOverviewMetrics | null>(null);
  const [domains, setDomains] = useState<DataDomainItem[]>([]);
  const [sources, setSources] = useState<DataSourceItem[]>([]);
  const [pipelines, setPipelines] = useState<DataPipelineItem[]>([]);
  const [datasets, setDatasets] = useState<LakehouseDatasetItem[]>([]);
  const [contracts, setContracts] = useState<DataContractItem[]>([]);
  const [products, setProducts] = useState<DataProductItem[]>([]);
  const [catalog, setCatalog] = useState<DataCatalogAssetItem[]>([]);
  const [glossary, setGlossary] = useState<BusinessGlossaryTermItem[]>([]);
  const [semanticMetrics, setSemanticMetrics] = useState<SemanticMetricItem[]>([]);
  const [qualityRules, setQualityRules] = useState<DataQualityRuleItem[]>([]);
  const [lineage, setLineage] = useState<DataLineageEdgeItem[]>([]);
  const [features, setFeatures] = useState<FeatureStoreItem[]>([]);
  const [finops, setFinops] = useState<DataFinopsSpendItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [
          m,
          doms,
          srcs,
          pipes,
          ds,
          cons,
          prods,
          cat,
          gloss,
          sem,
          rules,
          lin,
          feats,
          fin,
        ] = await Promise.all([
          fetchEnterpriseDataOverview(),
          fetchDataDomains(),
          fetchDataSources(),
          fetchDataPipelines(),
          fetchLakehouseDatasets(),
          fetchDataContracts(),
          fetchDataProducts(),
          fetchDataCatalog(),
          fetchBusinessGlossary(),
          fetchSemanticMetrics(),
          fetchDataQualityRules(),
          fetchDataLineage(),
          fetchFeatures(),
          fetchDataFinopsSpend(),
        ]);
        setMetrics(m);
        setDomains(doms);
        setSources(srcs);
        setPipelines(pipes);
        setDatasets(ds);
        setContracts(cons);
        setProducts(prods);
        setCatalog(cat);
        setGlossary(gloss);
        setSemanticMetrics(sem);
        setQualityRules(rules);
        setLineage(lin);
        setFeatures(feats);
        setFinops(fin);
      } catch (err) {
        console.error("Failed to load Enterprise Data OS data:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Enterprise Data Operating System
            </h1>
            <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-indigo-900/60 text-indigo-300 border border-indigo-700/50">
              Phase 62
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Central enterprise data nervous system connecting Lakehouse, Data Products, Governance, Semantic Metrics, and AI Copilot
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs text-slate-400">Data Quality Index</div>
            <div className="text-sm font-bold text-emerald-400 font-mono">
              {metrics ? `${metrics.composite_data_quality_pct}% Completeness & Validity` : "Loading..."}
            </div>
          </div>
        </div>
      </div>

      {/* Top Level KPIs */}
      <DataOverviewMetricsView metrics={metrics} />

      {/* Data Copilot */}
      <DataCopilotView />

      {/* Data Sources, Pipelines & Domains */}
      <DataSourcesPipelinesPanel sources={sources} pipelines={pipelines} domains={domains} />

      {/* Lakehouse Tiers & Data Products */}
      <LakehouseDataProductsView datasets={datasets} products={products} />

      {/* Data Contracts & Quality Rules */}
      <DataContractsQualityRadar contracts={contracts} qualityRules={qualityRules} />

      {/* Semantic Layer, Glossary & Catalog */}
      <SemanticMetricStoreExplorer metrics={semanticMetrics} glossary={glossary} catalog={catalog} />

      {/* Lineage Graph, Feature Store & FinOps */}
      <DataLineageGovernanceMatrix lineage={lineage} features={features} finops={finops} />
    </div>
  );
};
