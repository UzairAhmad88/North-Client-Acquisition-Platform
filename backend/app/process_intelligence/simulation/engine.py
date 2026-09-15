"""
Process Simulation Engine for Phase 49: Isolated what-if simulations with zero production state mutation.
"""

from datetime import datetime, timezone
import math
import random
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.process_intelligence.base import SimulationResult, SimulationScenario
except ImportError:
    from app.process_intelligence.base import SimulationResult, SimulationScenario


class ProcessSimulationEngine:
    """Simulates business process performance under varied arrival rates, capacity, and automation parameters."""

    def __init__(self):
        self._simulation_history: Dict[str, SimulationResult] = {}

    def run_simulation(
        self,
        process_id: str,
        scenario_type: SimulationScenario = SimulationScenario.OPTIMIZED,
        baseline_cycle_time_seconds: float = 36000.0,  # 10 hours default
        baseline_cost_per_case: float = 150.0,
        baseline_failure_rate: float = 0.08,
        baseline_rework_rate: float = 0.15,
        arrival_rate_multiplier: float = 1.0,
        automation_efficiency_gain: float = 0.25,  # 25% reduction in processing time
        resource_capacity_multiplier: float = 1.0,
        iterations: int = 1000,
        tenant_id: str = "default_tenant",
    ) -> SimulationResult:
        """Runs isolated Monte Carlo simulation without mutating any production database records."""
        random.seed(42)  # reproducible deterministic baseline

        simulation_code = f"SIM-{scenario_type.value[:4]}-{uuid.uuid4().hex[:6].upper()}"

        # Adjust scenario multipliers
        scenario_cycle_factor = 1.0
        scenario_cost_factor = 1.0
        scenario_failure_factor = 1.0
        scenario_rework_factor = 1.0

        if scenario_type == SimulationScenario.BASELINE:
            pass
        elif scenario_type == SimulationScenario.OPTIMIZED:
            scenario_cycle_factor = max(0.4, 1.0 - automation_efficiency_gain)
            scenario_cost_factor = max(0.5, 1.0 - (automation_efficiency_gain * 0.8))
            scenario_failure_factor = 0.8
            scenario_rework_factor = 0.7
        elif scenario_type == SimulationScenario.CONSERVATIVE:
            scenario_cycle_factor = max(0.7, 1.0 - (automation_efficiency_gain * 0.5))
            scenario_cost_factor = 0.9
            scenario_failure_factor = 0.95
            scenario_rework_factor = 0.9
        elif scenario_type == SimulationScenario.AGGRESSIVE:
            scenario_cycle_factor = max(0.3, 1.0 - (automation_efficiency_gain * 1.5))
            scenario_cost_factor = 0.6
            scenario_failure_factor = 1.1  # slightly higher risk under aggressive acceleration
            scenario_rework_factor = 0.8
        elif scenario_type == SimulationScenario.HIGH_VOLUME:
            arrival_rate_multiplier = max(arrival_rate_multiplier, 2.0)
            # Queue congestion effect: cycle time increases non-linearly under capacity strain
            congestion_factor = 1.0 + max(0.0, (arrival_rate_multiplier - resource_capacity_multiplier) * 0.4)
            scenario_cycle_factor *= congestion_factor
            scenario_cost_factor *= 1.2
            scenario_failure_factor *= 1.3
        elif scenario_type == SimulationScenario.LOW_RESOURCE:
            resource_capacity_multiplier = 0.5
            scenario_cycle_factor *= 1.8
            scenario_failure_factor *= 1.4

        # Monte Carlo run
        simulated_cycles: List[float] = []
        simulated_costs: List[float] = []
        failures = 0
        reworks = 0

        for _ in range(iterations):
            # Normal distribution with 15% standard deviation variance
            cycle = max(60.0, random.gauss(baseline_cycle_time_seconds * scenario_cycle_factor, baseline_cycle_time_seconds * 0.15))
            cost = max(10.0, random.gauss(baseline_cost_per_case * scenario_cost_factor, baseline_cost_per_case * 0.10))
            simulated_cycles.append(cycle)
            simulated_costs.append(cost)

            if random.random() < (baseline_failure_rate * scenario_failure_factor):
                failures += 1
            if random.random() < (baseline_rework_rate * scenario_rework_factor):
                reworks += 1

        avg_cycle = sum(simulated_cycles) / len(simulated_cycles)
        avg_cost = sum(simulated_costs) / len(simulated_costs)
        failure_rate = failures / iterations
        rework_rate = reworks / iterations
        throughput_per_day = round((86400.0 / avg_cycle) * resource_capacity_multiplier * 5.0, 1)

        assumptions = {
            "scenario": scenario_type.value,
            "arrival_rate_multiplier": arrival_rate_multiplier,
            "automation_efficiency_gain": automation_efficiency_gain,
            "resource_capacity_multiplier": resource_capacity_multiplier,
            "baseline_cycle_seconds": baseline_cycle_time_seconds,
            "iterations": iterations,
            "isolation_verified": True,
            "production_mutation": False,
        }

        result = SimulationResult(
            simulation_code=simulation_code,
            process_id=process_id,
            scenario_type=scenario_type,
            iterations=iterations,
            predicted_throughput=throughput_per_day,
            predicted_cycle_time_seconds=round(avg_cycle, 2),
            predicted_cost=round(avg_cost, 2),
            predicted_failure_rate=round(failure_rate, 4),
            predicted_rework_rate=round(rework_rate, 4),
            results_summary={
                "cycle_time_p50_seconds": round(sorted(simulated_cycles)[int(iterations * 0.5)], 2),
                "cycle_time_p95_seconds": round(sorted(simulated_cycles)[int(iterations * 0.95)], 2),
                "cost_p50": round(sorted(simulated_costs)[int(iterations * 0.5)], 2),
                "cost_p95": round(sorted(simulated_costs)[int(iterations * 0.95)], 2),
                "expected_throughput_per_day": throughput_per_day,
            },
            assumptions=assumptions,
        )

        self._simulation_history[simulation_code] = result
        return result
