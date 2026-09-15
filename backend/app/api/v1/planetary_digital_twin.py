"""
Phase 94 — Global Intelligence Infrastructure, Planetary Digital Twin & Long-Horizon Strategic Foresight REST API Router
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.services.planetary_digital_twin import (
    PlanetaryKnowledgeFabricService,
    GeospatialInfrastructureService,
    ClimateEnvironmentSimulationService,
    MacroEconomicDemographicsService,
    StrategicForesightEngineService,
    PolicyCrisisSimulationService,
    PlanetaryTwinAnalyticsService,
)

router = APIRouter(prefix="/planetary-twin", tags=["Planetary Digital Twin OS"])

class HistoricalReconstructPayload(BaseModel):
    entity_id: str = Field("node-us-001")
    year: int = Field(2020)

class InfraCascadePayload(BaseModel):
    infrastructure_id: str = Field("infra-grid-alpha")

class ClimateSimPayload(BaseModel):
    scenario_code: str = Field("SSP2_4.5")
    horizon_year: int = Field(2050)

class FinancialContagionPayload(BaseModel):
    source: str = Field("Major Commercial Bank Default")

class ForesightHorizonPayload(BaseModel):
    horizon_years: int = Field(25)

class PolicyRedBluePayload(BaseModel):
    title: str = Field("Global Carbon Border Adjustment Mechanism (CBAM)")
    author: str = Field("Climate Policy Taskforce")

class CrisisCascadePayload(BaseModel):
    crisis_type: str = Field("PANDEMIC_LOGISTICS")

class CounterfactualPayload(BaseModel):
    query: str = Field("What if global renewable energy adoption accelerates to 80% by 2030?")

# --- API Endpoints ---

@router.get("/planetary/graph", response_model=Dict[str, Any])
def get_planetary_graph(
    scale_level: str = Query("NATIONAL", example="NATIONAL"),
    entity_type: str = Query("COUNTRY", example="COUNTRY")
):
    """Queries the multi-scale planetary knowledge graph with data provenance and missing data handling."""
    return PlanetaryKnowledgeFabricService.get_planetary_entity_graph(scale_level, entity_type)

@router.post("/historical/reconstruct", response_model=Dict[str, Any])
def reconstruct_historical(payload: HistoricalReconstructPayload):
    """Reconstructs historical planetary or institutional state with full provenance."""
    return PlanetaryKnowledgeFabricService.reconstruct_historical_state(payload.entity_id, payload.year)

@router.post("/infrastructure/cascade", response_model=Dict[str, Any])
def simulate_infra_cascade(payload: InfraCascadePayload):
    """Simulates cascading failures across dependent infrastructure sectors and recovery pathways."""
    return GeospatialInfrastructureService.simulate_cascading_infrastructure_failure(payload.infrastructure_id)

@router.get("/trade/network", response_model=Dict[str, Any])
def get_trade_network():
    """Models global trade network relationships, chokepoints, and single points of failure."""
    return GeospatialInfrastructureService.get_trade_network_model()

@router.post("/climate/impact", response_model=Dict[str, Any])
def simulate_climate_impact(payload: ClimateSimPayload):
    """Runs climate impact simulations for extreme events, ecosystem feedback, and adaptation."""
    return ClimateEnvironmentSimulationService.run_climate_impact_simulation(payload.scenario_code, payload.horizon_year)

@router.post("/economic/contagion", response_model=Dict[str, Any])
def simulate_economic_contagion(payload: FinancialContagionPayload):
    """Simulates macroeconomic contagion, liquidity stress, and trade policy impacts."""
    return MacroEconomicDemographicsService.simulate_financial_contagion(payload.dict())

@router.get("/macro/labor-compute", response_model=Dict[str, Any])
def get_labor_compute_trajectory():
    """Models AI adoption impact on labor markets, skill transformation, and compute capacity."""
    return MacroEconomicDemographicsService.evaluate_ai_labor_compute_trajectory()

@router.post("/foresight/horizon", response_model=Dict[str, Any])
def generate_foresight(payload: ForesightHorizonPayload):
    """Generates strategic foresight scenarios (5, 10, 25, 50, 100 years) with megatrend signals."""
    return StrategicForesightEngineService.generate_long_horizon_scenarios(payload.horizon_years)

@router.post("/policy/redblue", response_model=Dict[str, Any])
def simulate_policy(payload: PolicyRedBluePayload):
    """Runs global policy simulations with side-effect analysis, trade-offs, and Red/Blue synthesis."""
    return PolicyCrisisSimulationService.run_policy_red_blue_simulation(payload.dict())

@router.post("/crisis/cascade", response_model=Dict[str, Any])
def simulate_crisis_cascade(payload: CrisisCascadePayload):
    """Simulates global crisis cascades across health, transport, food, and cyber systems."""
    return PolicyCrisisSimulationService.run_crisis_cascade_simulation(payload.crisis_type)

@router.post("/twin/counterfactual", response_model=Dict[str, Any])
def run_counterfactual(payload: CounterfactualPayload):
    """Runs counterfactual 'what-if' scenario engine with explicit model assumptions."""
    return PlanetaryTwinAnalyticsService.run_counterfactual_scenario(payload.dict())

@router.get("/analytics/calibration", response_model=Dict[str, Any])
def get_model_calibration():
    """Tracks forecast vs reality observations, calibration accuracy, and evidence changes."""
    return PlanetaryTwinAnalyticsService.get_forecast_vs_reality_calibration()
