"""
Phase 65: Data Simulation Service
Executes what-if synthetic simulations on enterprise data and architecture.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import DataSimulationModel


class DataSimulationService:
    def __init__(self, db: Session):
        self.db = db

    def run_simulation(
        self,
        tenant_id: str,
        scenario_name: str,
        parameters: Dict[str, Any]
    ) -> DataSimulationModel:
        """
        Simulates impacts of parameter variations, e.g.
        parameters: {"traffic_multiplier": 2.5, "data_volume_gb": 5000}
        """
        multiplier = float(parameters.get("traffic_multiplier", 1.0))
        volume_gb = float(parameters.get("data_volume_gb", 1000.0))

        simulated_results = {
            "estimated_monthly_cost_usd": round(volume_gb * multiplier * 0.08, 2),
            "estimated_p99_latency_ms": round(45.0 * (multiplier ** 0.5), 1),
            "projected_pipeline_throughput_rps": int(1200 * multiplier),
            "storage_headroom_remaining_pct": max(0.0, round(100.0 - (multiplier * 22.0), 1)),
            "recommended_scale_tier": "ENTERPRISE_L" if multiplier > 2.0 else "STANDARD_M"
        }

        sim = DataSimulationModel(
            tenant_id=tenant_id,
            scenario_name=scenario_name,
            parameters=parameters,
            results=simulated_results,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(sim)
        self.db.commit()
        self.db.refresh(sim)
        return sim

    def list_simulations(self, tenant_id: str) -> List[DataSimulationModel]:
        return self.db.query(DataSimulationModel).filter(
            DataSimulationModel.tenant_id == tenant_id
        ).order_by(DataSimulationModel.created_at.desc()).all()
