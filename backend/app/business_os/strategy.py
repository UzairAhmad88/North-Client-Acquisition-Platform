"""Strategic Objectives, OKR Management, Initiatives, and Milestone Dependencies."""

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional
import uuid

from app.business_os.base import (
    InitiativeStatus,
    KeyResultStatus,
    ObjectivePriority,
    ObjectiveStatus,
    StrategicDependencyState,
)


class StrategicKeyResult:
    """Measurable Key Result attached to a Strategic Objective."""

    def __init__(
        self,
        kr_id: str,
        objective_id: str,
        title: str,
        target_value: Decimal,
        current_value: Decimal = Decimal("0.00"),
        unit: str = "%",
        status: KeyResultStatus = KeyResultStatus.NOT_STARTED,
        owner: str = "",
    ):
        self.kr_id = kr_id
        self.objective_id = objective_id
        self.title = title
        self.target_value = target_value
        self.current_value = current_value
        self.unit = unit
        self.status = status
        self.owner = owner

    @property
    def progress_pct(self) -> Decimal:
        if self.target_value <= Decimal("0.00"):
            return Decimal("100.00") if self.current_value >= Decimal("0.00") else Decimal("0.00")
        pct = (self.current_value / self.target_value) * Decimal("100.00")
        return min(Decimal("100.00"), max(Decimal("0.00"), pct.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)))

    def update_value(self, new_val: Decimal) -> None:
        self.current_value = new_val
        prog = self.progress_pct
        if prog >= Decimal("100.00"):
            self.status = KeyResultStatus.ACHIEVED
        elif prog >= Decimal("70.00"):
            self.status = KeyResultStatus.ON_TRACK
        elif prog >= Decimal("40.00"):
            self.status = KeyResultStatus.AT_RISK
        else:
            self.status = KeyResultStatus.OFF_TRACK


class StrategicInitiative:
    """Execution vehicle converting strategy into actionable delivery milestones."""

    def __init__(
        self,
        initiative_id: str,
        objective_id: str,
        title: str,
        owner: str,
        budget: Decimal = Decimal("0.00"),
        priority: ObjectivePriority = ObjectivePriority.P1_HIGH,
        status: InitiativeStatus = InitiativeStatus.PLANNED,
        dependencies: Optional[List[Dict[str, Any]]] = None,
        milestones: Optional[List[Dict[str, Any]]] = None,
    ):
        self.initiative_id = initiative_id
        self.objective_id = objective_id
        self.title = title
        self.owner = owner
        self.budget = budget
        self.priority = priority
        self.status = status
        self.dependencies = dependencies or []
        self.milestones = milestones or []

    @property
    def progress_pct(self) -> Decimal:
        if not self.milestones:
            return Decimal("100.00") if self.status == InitiativeStatus.COMPLETED else Decimal("0.00")
        completed = sum(1 for m in self.milestones if m.get("completed", False))
        return (Decimal(completed) / Decimal(len(self.milestones)) * Decimal("100.00")).quantize(
            Decimal("0.1"), rounding=ROUND_HALF_UP
        )

    def add_milestone(self, title: str, due_date: str, completed: bool = False) -> None:
        self.milestones.append({
            "id": str(uuid.uuid4()),
            "title": title,
            "due_date": due_date,
            "completed": completed,
        })

    def add_dependency(self, name: str, dependency_type: str, state: StrategicDependencyState) -> None:
        self.dependencies.append({
            "id": str(uuid.uuid4()),
            "name": name,
            "type": dependency_type,
            "state": state.value,
        })


class StrategicObjective:
    """High-level organizational objective grouping OKRs and initiatives."""

    def __init__(
        self,
        objective_id: str,
        title: str,
        description: str,
        timeframe: str,
        owner: str,
        priority: ObjectivePriority = ObjectivePriority.P1_HIGH,
        status: ObjectiveStatus = ObjectiveStatus.ACTIVE,
        key_results: Optional[List[StrategicKeyResult]] = None,
        initiatives: Optional[List[StrategicInitiative]] = None,
    ):
        self.objective_id = objective_id
        self.title = title
        self.description = description
        self.timeframe = timeframe
        self.owner = owner
        self.priority = priority
        self.status = status
        self.key_results = key_results or []
        self.initiatives = initiatives or []

    @property
    def overall_progress_pct(self) -> Decimal:
        """Computes evidence-based overall progress across key results and initiatives."""
        components: List[Decimal] = []
        for kr in self.key_results:
            components.append(kr.progress_pct)
        for init in self.initiatives:
            components.append(init.progress_pct)

        if not components:
            return Decimal("0.00")
        avg = sum(components) / Decimal(len(components))
        return avg.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


class StrategyManager:
    """Manages organizational strategic roadmap, OKR tracking, and initiative dependencies."""

    def __init__(self):
        self._objectives: Dict[str, StrategicObjective] = {}
        self._seed_default_strategy()

    def _seed_default_strategy(self) -> None:
        obj1 = StrategicObjective(
            objective_id="obj_sustainable_growth",
            title="Scale High-Margin AI Solutions & Sustainable Retainer Base",
            description="Expand AI consulting & client operations retainer portfolio while preserving 65%+ gross margin.",
            timeframe="FY2026 - Q3/Q4",
            owner="Executive Team",
            priority=ObjectivePriority.P0_CRITICAL,
            status=ObjectiveStatus.ACTIVE,
        )
        obj1.key_results = [
            StrategicKeyResult("kr_mrr", obj1.objective_id, "Reach PKR 5,000,000 Monthly Recurring Revenue", Decimal("5000000.00"), Decimal("3800000.00"), "PKR", KeyResultStatus.ON_TRACK, "Finance"),
            StrategicKeyResult("kr_retention", obj1.objective_id, "Maintain 95%+ Net Client Retention Rate", Decimal("95.00"), Decimal("92.50"), "%", KeyResultStatus.ON_TRACK, "Customer Success"),
            StrategicKeyResult("kr_delivery_ontime", obj1.objective_id, "Achieve 90%+ On-Time Milestone Delivery", Decimal("90.00"), Decimal("88.00"), "%", KeyResultStatus.ON_TRACK, "Delivery"),
        ]

        init1 = StrategicInitiative(
            initiative_id="init_autonomous_client_intelligence",
            objective_id=obj1.objective_id,
            title="Unified Client Intelligence & Automated Value Realization Engine",
            owner="VP Engineering",
            budget=Decimal("500000.00"),
            status=InitiativeStatus.IN_PROGRESS,
        )
        init1.add_milestone("Deploy Client 360 Health Synthesis", "2026-10-15", completed=True)
        init1.add_milestone("Launch Closed-Loop Renewal Forecaster", "2026-11-01", completed=True)
        init1.add_milestone("Executive Decision Queue Integration", "2026-11-15", completed=False)
        init1.add_dependency("Engineering Capacity Allocation", "PEOPLE", StrategicDependencyState.AVAILABLE)
        init1.add_dependency("Double-Entry Ledger Synchronization", "TECHNOLOGY", StrategicDependencyState.RESOLVED)

        obj1.initiatives = [init1]
        self._objectives[obj1.objective_id] = obj1

    def create_objective(self, objective: StrategicObjective) -> StrategicObjective:
        self._objectives[objective.objective_id] = objective
        return objective

    def get_objective(self, objective_id: str) -> Optional[StrategicObjective]:
        return self._objectives.get(objective_id)

    def list_objectives(self) -> List[StrategicObjective]:
        return list(self._objectives.values())

    def update_key_result(self, objective_id: str, kr_id: str, new_value: Decimal) -> Optional[StrategicKeyResult]:
        obj = self.get_objective(objective_id)
        if not obj:
            return None
        for kr in obj.key_results:
            if kr.kr_id == kr_id:
                kr.update_value(new_value)
                return kr
        return None
