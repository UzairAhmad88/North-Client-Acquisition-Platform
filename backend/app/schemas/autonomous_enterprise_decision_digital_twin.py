"""
Phase 75: Autonomous Enterprise Simulation, Digital Twin, Predictive Intelligence,
Scenario Planning & Strategic Decision Intelligence Schemas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -------------------------------------------------------------------
# 1. Strategic Decision Command Center & 14-Stage Loop
# -------------------------------------------------------------------
class DecisionControlCenterSummaryResponse(BaseModel):
    decision_intelligence_score: float
    forecast_calibration_accuracy_pct: float
    active_digital_twin_entities_count: int
    active_strategic_scenarios_count: int
    running_simulations_count: int
    pareto_optimal_options_count: int
    open_strategic_decisions_count: int
    early_warning_signals_count: int
    active_war_rooms_count: int
    simulated_capital_at_risk: float
    currency: str = "USD"


class DecisionOperatingCycleExecutionResponse(BaseModel):
    cycle_run_id: str
    stages_executed: List[str]
    overall_status: str
    forecasts_generated: int
    scenarios_evaluated: int
    monte_carlo_iterations: int
    pareto_tradeoffs_calculated: int
    actions_requiring_human_approval: int
    lessons_learned_recorded: int


# -------------------------------------------------------------------
# 2. Digital Twin Entities & State
# -------------------------------------------------------------------
class DecisionTwinEntityCreate(BaseModel):
    entity_code: str
    entity_type: str
    name: str
    current_state: Dict[str, Any]
    owner: str = "Executive Leadership"
    source_system: str = "ENTERPRISE_EVENT_BUS"


class DecisionTwinEntityResponse(BaseModel):
    id: str
    entity_code: str
    entity_type: str
    name: str
    current_state: Dict[str, Any]
    confidence_score: float
    owner: str
    source_system: str
    is_active: bool
    last_updated: datetime


# -------------------------------------------------------------------
# 3. Forecasts & Causal Driver Trees
# -------------------------------------------------------------------
class DecisionForecastRequest(BaseModel):
    metric_name: str
    forecast_horizon_days: int = 90
    scenario_code: str = "BASE_CASE"


class DecisionForecastResponse(BaseModel):
    id: str
    metric_name: str
    model_algorithm: str
    forecast_horizon_days: int
    point_estimate: float
    prediction_interval_p10: float
    prediction_interval_p50: float
    prediction_interval_p90: float
    confidence_level: float
    created_at: datetime


class DecisionDriverTreeResponse(BaseModel):
    target_metric: str
    current_value: float
    currency: str
    primary_drivers: List[Dict[str, Any]]
    elasticity_weights: Dict[str, float]


# -------------------------------------------------------------------
# 4. Scenarios & Monte Carlo Simulations
# -------------------------------------------------------------------
class DecisionScenarioCreate(BaseModel):
    scenario_code: str
    name: str
    category: str = "MACROECONOMIC"
    assumptions_summary: str
    variables_mutated: Dict[str, Any]
    time_horizon_months: int = 12


class DecisionScenarioResponse(BaseModel):
    id: str
    scenario_code: str
    name: str
    category: str
    assumptions_summary: str
    variables_mutated: Dict[str, Any]
    time_horizon_months: int
    status: str
    created_at: datetime


class DecisionMonteCarloRequest(BaseModel):
    scenario_code: str
    iterations_count: int = 10000
    random_seed: int = 42


class DecisionMonteCarloResponse(BaseModel):
    simulation_id: str
    scenario_code: str
    iterations_count: int
    mean_outcome: float
    var_95_percentile: float
    cvar_expected_shortfall: float
    confidence_interval_90: Dict[str, float]
    reproducibility_hash: str
    status: str


# -------------------------------------------------------------------
# 5. Multi-Objective Decision Optimization & Pareto
# -------------------------------------------------------------------
class DecisionOptimizationRequest(BaseModel):
    objectives: List[str]  # e.g. ["profit", "risk", "customer_experience"]
    constraints: Dict[str, float] = {}  # e.g. {"max_capital": 500000.0}



class DecisionParetoPoint(BaseModel):
    option_name: str
    profit_score: float
    risk_score: float
    customer_experience_score: float
    is_pareto_optimal: bool


class DecisionOptimizationResponse(BaseModel):
    optimization_code: str
    objectives_list: List[str]
    pareto_frontier: List[DecisionParetoPoint]
    recommended_option: str
    tradeoff_explanation: str


# -------------------------------------------------------------------
# 6. Strategic Decisions & Briefs
# -------------------------------------------------------------------
class DecisionBriefResponse(BaseModel):
    decision_code: str
    title: str
    situation: str
    decision_required: str
    options_evaluated: List[Dict[str, Any]]
    recommended_option: str
    key_assumptions: List[str]
    critical_risks: List[str]
    tradeoffs_summary: str
    governance_approval_required: str


# -------------------------------------------------------------------
# 7. OKRs & Early Warnings
# -------------------------------------------------------------------
class DecisionOkrResponse(BaseModel):
    id: str
    objective_title: str
    key_result: str
    baseline_value: float
    target_value: float
    current_value: float
    progress_pct: float
    confidence_level: str
    owner: str


class DecisionEarlyWarningResponse(BaseModel):
    id: str
    signal_code: str
    category: str
    severity: str
    signal_description: str
    confidence: float
    recommended_action: Optional[str] = None
    detected_at: datetime


# -------------------------------------------------------------------
# 8. Crisis Management & Executive War Room
# -------------------------------------------------------------------
class DecisionWarRoomResponse(BaseModel):
    case_code: str
    crisis_type: str
    title: str
    containment_status: str
    financial_exposure_estimate: float
    impacted_business_units: List[str]
    war_room_lead: str
    containment_actions_active: int
