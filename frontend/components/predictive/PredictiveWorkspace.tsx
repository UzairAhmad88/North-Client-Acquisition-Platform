"use client";

import React, { useState, useEffect, useCallback } from "react";
import {
  predictiveApi,
  PredictionRecord,
  DecisionSupportRecord,
  ModelGovernance,
} from "@/lib/api/predictive";
import { PredictiveDashboard } from "./PredictiveDashboard";
import { DecisionCenter } from "./DecisionCenter";
import { ModelGovernancePanel } from "./ModelGovernancePanel";
import { ForecastVisualizer } from "./ForecastVisualizer";
import {
  Sparkles,
  ShieldCheck,
  Cpu,
  TrendingUp,
  BrainCircuit,
  AlertCircle,
  RefreshCw,
} from "lucide-react";

export type WorkspaceTab = "dashboard" | "decisions" | "governance" | "forecasts";

export function PredictiveWorkspace() {
  const [activeTab, setActiveTab] = useState<WorkspaceTab>("dashboard");
  const [loading, setLoading] = useState<boolean>(true);
  const [predictions, setPredictions] = useState<PredictionRecord[]>([]);
  const [decisionRecords, setDecisionRecords] = useState<DecisionSupportRecord[]>([]);
  const [models, setModels] = useState<ModelGovernance[]>([]);
  const [forecastData, setForecastData] = useState<any>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [predsRes, decisionsRes, modelsRes, forecastRes] = await Promise.allSettled([
        predictiveApi.listPredictions(),
        predictiveApi.listDecisionSupport(),
        predictiveApi.listModels(),
        predictiveApi.getForecast("default_tenant", "SUPPORT_VOLUME", "30d"),
      ]);

      if (predsRes.status === "fulfilled" && predsRes.value && predsRes.value.length > 0) {
        setPredictions(predsRes.value);
      } else {
        // Fallback sample records for initial display
        setPredictions([
          {
            id: "pred_lead_001",
            tenant_id: "default_tenant",
            model_id: "mod_lead_v1",
            prediction_type: "LEAD_CONVERSION",
            entity_id: "lead_nordic_tech",
            probability: 0.84,
            risk_band: "HIGH",
            confidence_interval: { lower: 0.76, upper: 0.92 },
            model_version: "v1.0-baseline",
            inference_timestamp: new Date().toISOString(),
            created_at: new Date().toISOString(),
            explanation: {
              summary_text: "High alignment with technical stack and immediate budget fit.",
              key_drivers: [
                { feature: "lead_score", value: 92, impact: "+0.46" },
                { feature: "service_fit_score", value: 85, impact: "+0.25" },
                { feature: "client_responded", value: true, impact: "+0.15" },
              ],
              safety_notes: ["Probabilistic estimate. Requires human sales validation."],
            },
          },
          {
            id: "pred_proj_002",
            tenant_id: "default_tenant",
            model_id: "mod_proj_v1",
            prediction_type: "PROJECT_DELAY",
            entity_id: "proj_apex_cloud",
            probability: 0.68,
            risk_band: "HIGH",
            confidence_interval: { lower: 0.61, upper: 0.75 },
            model_version: "v1.0-baseline",
            inference_timestamp: new Date().toISOString(),
            created_at: new Date().toISOString(),
            explanation: {
              summary_text: "Elevated risk of delay due to 2 unresolved external integrations.",
              key_drivers: [
                { feature: "blocked_tasks_count", value: 3, impact: "+0.30" },
                { feature: "unresolved_requirements", value: 2, impact: "+0.16" },
              ],
              safety_notes: ["Decision support only. Milestones are never modified automatically."],
            },
          },
        ]);
      }

      if (decisionsRes.status === "fulfilled" && decisionsRes.value && decisionsRes.value.length > 0) {
        setDecisionRecords(decisionsRes.value);
      } else {
        setDecisionRecords([
          {
            id: "dec_supp_001",
            tenant_id: "default_tenant",
            prediction_id: "pred_proj_002",
            title: "Deterministic Rule Triggered: CRITICAL_DEFECT_RELEASE_BLOCK",
            recommended_action: "Mandatory Action: BLOCK_RELEASE - 1 or more critical QA defects remain open.",
            tradeoff_analysis: "Deterministic safety rule strictly overrides all probabilistic release models.",
            urgency: "CRITICAL",
            state: "PENDING_REVIEW",
            created_at: new Date().toISOString(),
          },
        ]);
      }

      if (modelsRes.status === "fulfilled" && modelsRes.value && modelsRes.value.length > 0) {
        setModels(modelsRes.value);
      } else {
        setModels([
          {
            id: "mod_lead_v1",
            tenant_id: "default_tenant",
            model_key: "lead_conversion_baseline",
            name: "Lead Conversion Calibrated Baseline",
            prediction_type: "LEAD_CONVERSION",
            algorithm: "calibrated_logistic_regression",
            current_version: "v1.0",
            status: "PRODUCTION",
            approved_by: "head_of_ml",
            approved_at: new Date().toISOString(),
            thresholds: { low: 0.39, medium: 0.69, high: 0.89 },
            created_at: new Date().toISOString(),
          },
          {
            id: "mod_proj_v1",
            tenant_id: "default_tenant",
            model_key: "project_schedule_delay_model",
            name: "Project Schedule Delay Overrun Predictor",
            prediction_type: "PROJECT_DELAY",
            algorithm: "gradient_boosted_classifier",
            current_version: "v1.0",
            status: "PRODUCTION",
            approved_by: "delivery_governance_lead",
            approved_at: new Date().toISOString(),
            thresholds: { low: 0.44, medium: 0.74, high: 0.94 },
            created_at: new Date().toISOString(),
          },
        ]);
      }

      if (forecastRes.status === "fulfilled" && forecastRes.value) {
        setForecastData(forecastRes.value);
      } else {
        setForecastData({
          forecast_type: "SUPPORT_VOLUME",
          time_horizon: "30d",
          forecast: {
            "Day 1-7": 24,
            "Day 8-14": 31,
            "Day 15-21": 28,
            "Day 22-30": 35,
          },
          confidence_intervals: {
            "Day 1-7": { lower: 20, upper: 28 },
            "Day 8-14": { lower: 26, upper: 36 },
            "Day 15-21": { lower: 23, upper: 33 },
            "Day 22-30": { lower: 29, upper: 41 },
          },
        });
      }
    } catch (err) {
      console.error("Failed to load predictive workspace data:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleTriggerInference = async () => {
    try {
      setLoading(true);
      await predictiveApi.generatePrediction({
        prediction_type: "LEAD_CONVERSION",
        entity_id: `lead_${Date.now().toString().slice(-4)}`,
        features: {
          lead_score: 88.0,
          service_fit_score: 80.0,
          has_response: true,
          interaction_count: 3,
        },
      });
      await loadData();
    } catch (err) {
      console.error("Inference run error:", err);
      await loadData();
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border border-indigo-800/40 rounded-xl p-6 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 w-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Phase 32 AI/ML Engine
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                Deterministic Rules &gt; Model Output
              </span>
            </div>
            <h1 className="text-2xl font-bold flex items-center gap-3">
              <BrainCircuit className="w-7 h-7 text-indigo-400" />
              Predictive Operations &amp; Decision Intelligence
            </h1>
            <p className="text-slate-300 text-sm mt-1 max-w-2xl">
              Calibrated probabilistic modeling, point-in-time leakage defense, deterministic policy overrides,
              and human-in-the-loop decision auditing.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={loadData}
              disabled={loading}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-750 text-slate-200 border border-slate-700 transition"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
              Refresh
            </button>
            <div className="text-right hidden sm:block">
              <div className="text-xs text-slate-400">Autonomous Deployment</div>
              <div className="text-sm font-semibold text-rose-300 flex items-center gap-1">
                <AlertCircle className="w-3.5 h-3.5" /> Strictly Disabled
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-200 dark:border-slate-800 gap-2">
        <button
          onClick={() => setActiveTab("dashboard")}
          className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "dashboard"
              ? "border-indigo-600 text-indigo-600 dark:text-indigo-400"
              : "border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200"
          }`}
        >
          <Sparkles className="w-4 h-4" />
          Predictive Analytics &amp; Predictions
        </button>

        <button
          onClick={() => setActiveTab("decisions")}
          className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "decisions"
              ? "border-indigo-600 text-indigo-600 dark:text-indigo-400"
              : "border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200"
          }`}
        >
          <ShieldCheck className="w-4 h-4" />
          Decision Center &amp; Human Reviews
        </button>

        <button
          onClick={() => setActiveTab("governance")}
          className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "governance"
              ? "border-indigo-600 text-indigo-600 dark:text-indigo-400"
              : "border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200"
          }`}
        >
          <Cpu className="w-4 h-4" />
          Model Governance &amp; Retraining
        </button>

        <button
          onClick={() => setActiveTab("forecasts")}
          className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "forecasts"
              ? "border-indigo-600 text-indigo-600 dark:text-indigo-400"
              : "border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200"
          }`}
        >
          <TrendingUp className="w-4 h-4" />
          Forecast Visualizer &amp; Scenarios
        </button>
      </div>

      {/* Tab Panels */}
      <div className="pt-2">
        {activeTab === "dashboard" && (
          <PredictiveDashboard
            predictions={predictions}
            loading={loading}
            onRefresh={loadData}
            onTriggerInference={handleTriggerInference}
          />
        )}
        {activeTab === "decisions" && (
          <DecisionCenter
            records={decisionRecords}
            onRefresh={loadData}
          />
        )}
        {activeTab === "governance" && (
          <ModelGovernancePanel
            models={models}
            onRefresh={loadData}
          />
        )}
        {activeTab === "forecasts" && (
          <ForecastVisualizer
            forecastData={forecastData}
          />
        )}
      </div>
    </div>
  );
}

export default PredictiveWorkspace;
