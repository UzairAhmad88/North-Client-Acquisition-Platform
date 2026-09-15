import { api } from './client';

export interface PredictionExplanation {
  summary_text: string;
  key_drivers: Array<{ feature: string; value: any; impact: string }>;
  safety_notes: string[];
}

export interface PredictionOutcome {
  actual_numeric_outcome: number;
  outcome_label: string;
  error_magnitude?: number;
  recorded_by: string;
  recorded_at: string;
}

export interface PredictionRecord {
  id: string;
  tenant_id: string;
  model_id: string;
  prediction_type: string;
  entity_id: string;
  probability: number;
  risk_band: string;
  confidence_interval: { lower: number; upper: number };
  model_version: string;
  inference_timestamp: string;
  created_at: string;
  explanation?: PredictionExplanation;
  outcome?: PredictionOutcome;
}

export interface DecisionOverride {
  id: string;
  original_recommendation: string;
  chosen_action: string;
  override_reason: string;
  operator: string;
  created_at: string;
}

export interface DecisionSupportRecord {
  id: string;
  tenant_id: string;
  prediction_id: string;
  title: string;
  recommended_action: string;
  tradeoff_analysis: string;
  urgency: string;
  state: string;
  reviewed_by?: string;
  reviewed_at?: string;
  created_at: string;
  overrides?: DecisionOverride[];
}

export interface ModelGovernance {
  id: string;
  tenant_id: string;
  model_key: string;
  name: string;
  prediction_type: string;
  algorithm: string;
  current_version: string;
  status: string;
  thresholds: Record<string, any>;
  approved_by?: string;
  approved_at?: string;
  created_at: string;
}

export interface ForecastResponse {
  id: string;
  tenant_id: string;
  forecast_type: string;
  time_horizon: string;
  model_version: string;
  predictions_payload: Record<string, any>;
  confidence_intervals: Record<string, any>;
  created_at: string;
}

export interface ModelDriftEvent {
  id: string;
  tenant_id: string;
  model_key: string;
  drift_type: string;
  drift_metric_value: number;
  drift_status: string;
  details: Record<string, any>;
  detected_at: string;
}

export const predictiveApi = {
  listPredictions: (tenantId: string = 'default_tenant', predictionType?: string, riskBand?: string): Promise<PredictionRecord[]> => {
    const params = new URLSearchParams({ tenant_id: tenantId });
    if (predictionType) params.append('prediction_type', predictionType);
    if (riskBand) params.append('risk_band', riskBand);
    return api<PredictionRecord[]>(`/predictive/predictions?${params.toString()}`);
  },

  getPrediction: (predictionId: string): Promise<PredictionRecord> =>
    api<PredictionRecord>(`/predictive/predictions/${predictionId}`),

  generatePrediction: (data: { prediction_type: string; entity_id: string; features: Record<string, any> }, tenantId: string = 'default_tenant'): Promise<any> =>
    api<any>(`/predictive/predictions?tenant_id=${tenantId}`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  recordOutcome: (predictionId: string, data: { actual_numeric_outcome: number; outcome_label: string; recorded_by?: string }): Promise<any> =>
    api<any>(`/predictive/predictions/${predictionId}/outcome`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  listDecisionSupport: (tenantId: string = 'default_tenant', state?: string): Promise<DecisionSupportRecord[]> => {
    const params = new URLSearchParams({ tenant_id: tenantId });
    if (state) params.append('state', state);
    return api<DecisionSupportRecord[]>(`/predictive/decision-support?${params.toString()}`);
  },

  reviewDecisionSupport: (recordId: string, data: { action: string; reviewer?: string; notes?: string; override_reason?: string; chosen_action?: string }): Promise<DecisionSupportRecord> =>
    api<DecisionSupportRecord>(`/predictive/decision-support/${recordId}/review`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  listModels: (tenantId: string = 'default_tenant'): Promise<ModelGovernance[]> =>
    api<ModelGovernance[]>(`/predictive/models?tenant_id=${tenantId}`),

  approveModel: (modelId: string, approvedBy: string = 'user'): Promise<ModelGovernance> =>
    api<ModelGovernance>(`/predictive/models/${modelId}/approve`, {
      method: 'POST',
      body: JSON.stringify({ approved_by: approvedBy }),
    }),

  getForecast: (tenantId: string = 'default_tenant', forecastType: string = 'WORKLOAD_DEMAND', timeHorizon: string = '30d'): Promise<any> =>
    api<any>(`/predictive/forecasts?tenant_id=${tenantId}&forecast_type=${forecastType}&time_horizon=${timeHorizon}`),

  getDriftSummary: (tenantId: string = 'default_tenant'): Promise<any> =>
    api<any>(`/predictive/model-monitoring/drift?tenant_id=${tenantId}`),
};
