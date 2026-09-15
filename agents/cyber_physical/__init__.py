"""Phase 70: Autonomous Cyber-Physical Systems AI Agents."""

from agents.cyber_physical.cps_orchestrator import CpsOrchestratorAgent
from agents.cyber_physical.iot_agent import IotAgent
from agents.cyber_physical.telemetry_agent import TelemetryAgent
from agents.cyber_physical.device_health_agent import DeviceHealthAgent
from agents.cyber_physical.sensor_agent import SensorAgent
from agents.cyber_physical.anomaly_agent import AnomalyAgent
from agents.cyber_physical.maintenance_agent import MaintenanceAgent
from agents.cyber_physical.predictive_maintenance_agent import PredictiveMaintenanceAgent
from agents.cyber_physical.robot_fleet_agent import RobotFleetAgent
from agents.cyber_physical.robot_mission_agent import RobotMissionAgent
from agents.cyber_physical.machine_agent import MachineAgent
from agents.cyber_physical.energy_agent import PhysicalEnergyAgent
from agents.cyber_physical.facility_agent import FacilityAgent
from agents.cyber_physical.digital_twin_agent import DigitalTwinAgent
from agents.cyber_physical.simulation_agent import SimulationAgent
from agents.cyber_physical.safety_agent import SafetyAgent
from agents.cyber_physical.incident_agent import PhysicalIncidentAgent
from agents.cyber_physical.asset_lifecycle_agent import AssetLifecycleAgent
from agents.cyber_physical.physical_operations_agent import PhysicalOperationsAgent

# Prompt naming aliases
EnergyAgent = PhysicalEnergyAgent
IncidentAgent = PhysicalIncidentAgent

__all__ = [
    "CpsOrchestratorAgent",
    "IotAgent",
    "TelemetryAgent",
    "DeviceHealthAgent",
    "SensorAgent",
    "AnomalyAgent",
    "MaintenanceAgent",
    "PredictiveMaintenanceAgent",
    "RobotFleetAgent",
    "RobotMissionAgent",
    "MachineAgent",
    "PhysicalEnergyAgent",
    "FacilityAgent",
    "DigitalTwinAgent",
    "SimulationAgent",
    "SafetyAgent",
    "PhysicalIncidentAgent",
    "AssetLifecycleAgent",
    "PhysicalOperationsAgent",
    "EnergyAgent",
    "IncidentAgent",
]
