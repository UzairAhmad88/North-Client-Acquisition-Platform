"use client";

import React, { useEffect, useState } from "react";
import {
  fetchEngineeringOverview,
  fetchRepositories,
  fetchPullRequests,
  fetchServices,
  fetchPipelines,
  fetchDeployments,
  fetchReleaseReadiness,
  fetchIncidents,
  fetchChanges,
  fetchVulnerabilities,
  fetchTechnicalDebt,
  fetchFinopsCosts,
  EngineeringOverviewMetrics,
  EngineeringRepository,
  EngineeringPullRequest,
  ServiceCatalogItem,
  CicdPipelineRecord,
  DeploymentRecord,
  ReleaseReadinessCheck,
  IncidentRecord,
  ChangeManagementRecord,
  DependencyVulnerabilityItem,
  TechnicalDebtItem,
  FinOpsCostSummary,
} from "@/lib/api/engineeringOs";
import { EngineeringOverviewMetricsView } from "./EngineeringOverviewMetrics";
import { RepositoryPrCodeQualityPanel } from "./RepositoryPrCodeQualityPanel";
import { ServiceApiArchitectureMap } from "./ServiceApiArchitectureMap";
import { CicdDeploymentReleaseBoard } from "./CicdDeploymentReleaseBoard";
import { IncidentSreObservabilityRadar } from "./IncidentSreObservabilityRadar";
import { SecuritySupplyChainFinopsView } from "./SecuritySupplyChainFinopsView";
import { DeveloperCopilotView } from "./DeveloperCopilot";

export const EngineeringDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<EngineeringOverviewMetrics | null>(null);
  const [repositories, setRepositories] = useState<EngineeringRepository[]>([]);
  const [pullRequests, setPullRequests] = useState<EngineeringPullRequest[]>([]);
  const [services, setServices] = useState<ServiceCatalogItem[]>([]);
  const [pipelines, setPipelines] = useState<CicdPipelineRecord[]>([]);
  const [deployments, setDeployments] = useState<DeploymentRecord[]>([]);
  const [readiness, setReadiness] = useState<ReleaseReadinessCheck | null>(null);
  const [incidents, setIncidents] = useState<IncidentRecord[]>([]);
  const [changes, setChanges] = useState<ChangeManagementRecord[]>([]);
  const [vulnerabilities, setVulnerabilities] = useState<DependencyVulnerabilityItem[]>([]);
  const [technicalDebt, setTechnicalDebt] = useState<TechnicalDebtItem[]>([]);
  const [finops, setFinops] = useState<FinOpsCostSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [
          m,
          repos,
          prs,
          svcs,
          pipes,
          deps,
          relReadiness,
          incs,
          chgs,
          vulns,
          debts,
          fin,
        ] = await Promise.all([
          fetchEngineeringOverview(),
          fetchRepositories(),
          fetchPullRequests(),
          fetchServices(),
          fetchPipelines(),
          fetchDeployments(),
          fetchReleaseReadiness(),
          fetchIncidents(),
          fetchChanges(),
          fetchVulnerabilities(),
          fetchTechnicalDebt(),
          fetchFinopsCosts(),
        ]);
        setMetrics(m);
        setRepositories(repos);
        setPullRequests(prs);
        setServices(svcs);
        setPipelines(pipes);
        setDeployments(deps);
        setReadiness(relReadiness);
        setIncidents(incs);
        setChanges(chgs);
        setVulnerabilities(vulns);
        setTechnicalDebt(debts);
        setFinops(fin);
      } catch (err) {
        console.error("Failed to load Engineering OS data:", err);
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
              Engineering & Technical Operations Operating System
            </h1>
            <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-indigo-900/60 text-indigo-300 border border-indigo-700/50">
              Phase 61
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            End-to-end continuous engineering lifecycle: Product → Requirement → Code → CI/CD → Test → Security → Deploy → Release → Observe → Incident → Learning
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs text-slate-400">DORA Deployment Frequency</div>
            <div className="text-sm font-bold text-emerald-400 font-mono">
              {metrics ? `${metrics.dora_metrics.deployment_frequency_per_day} deploys / day` : "Loading..."}
            </div>
          </div>
        </div>
      </div>

      {/* Top Level KPIs */}
      <EngineeringOverviewMetricsView metrics={metrics} />

      {/* Developer Copilot */}
      <DeveloperCopilotView />

      {/* Repositories & PRs */}
      <RepositoryPrCodeQualityPanel repositories={repositories} pullRequests={pullRequests} />

      {/* Services & Architecture */}
      <ServiceApiArchitectureMap services={services} />

      {/* CI/CD & Deployments & Release Gate */}
      <CicdDeploymentReleaseBoard
        pipelines={pipelines}
        deployments={deployments}
        readiness={readiness}
      />

      {/* SRE, Observability & Incidents */}
      <IncidentSreObservabilityRadar incidents={incidents} />

      {/* Security, Debt & FinOps */}
      <SecuritySupplyChainFinopsView
        vulnerabilities={vulnerabilities}
        technicalDebt={technicalDebt}
        finops={finops}
        changes={changes}
      />
    </div>
  );
};
