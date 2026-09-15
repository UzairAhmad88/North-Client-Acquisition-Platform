"""Departmental & Organization Scorecard Generation and Threshold Tracking."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.business_os.base import KPICategory, KPISnapshot, ScorecardStatus
from app.business_os.kpi import KPIRegistry


class ScorecardItem(BaseModel):
    kpi_id: str
    name: str
    category: KPICategory
    target: Decimal
    actual: Decimal
    variance: Decimal
    variance_pct: Optional[Decimal]
    unit: str
    currency: str
    trend: str  # UP, DOWN, STABLE
    status: ScorecardStatus
    owner: str


class DepartmentScorecard(BaseModel):
    department_name: str
    category: KPICategory
    overall_status: ScorecardStatus
    scorecard_items: List[ScorecardItem]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ScorecardEngine:
    """Generates organizational and functional scorecards."""

    def __init__(self, kpi_registry: Optional[KPIRegistry] = None):
        self.registry = kpi_registry or KPIRegistry()

    def generate_department_scorecard(
        self,
        department_name: str,
        category: KPICategory,
        metric_values: Dict[str, Decimal],
        previous_values: Optional[Dict[str, Decimal]] = None,
        owners_map: Optional[Dict[str, str]] = None,
    ) -> DepartmentScorecard:
        definitions = self.registry.list_definitions(category=category)
        items: List[ScorecardItem] = []
        statuses: List[ScorecardStatus] = []

        owners = owners_map or {
            KPICategory.FINANCIAL: "Head of Finance",
            KPICategory.SALES: "VP Sales & Growth",
            KPICategory.CLIENT: "Head of Customer Success",
            KPICategory.DELIVERY: "VP Engineering & Delivery",
            KPICategory.SUPPORT: "Support Lead",
            KPICategory.AI: "Lead AI Architect",
            KPICategory.OPERATIONS: "Director of Operations",
        }

        for defn in definitions:
            actual = metric_values.get(defn.kpi_id, Decimal("0.00"))
            prev = (previous_values or {}).get(defn.kpi_id)
            snapshot = self.registry.calculate_snapshot(defn.kpi_id, actual, previous_value=prev)

            trend = "STABLE"
            if prev is not None:
                if actual > prev:
                    trend = "UP"
                elif actual < prev:
                    trend = "DOWN"

            owner = owners.get(defn.category, "Executive Office")

            item = ScorecardItem(
                kpi_id=snapshot.kpi_id,
                name=snapshot.name,
                category=snapshot.category,
                target=snapshot.target_value or Decimal("0.00"),
                actual=snapshot.value,
                variance=snapshot.variance or Decimal("0.00"),
                variance_pct=snapshot.variance_pct,
                unit=snapshot.unit,
                currency=snapshot.currency,
                trend=trend,
                status=snapshot.status,
                owner=owner,
            )
            items.append(item)
            statuses.append(snapshot.status)

        # Overall department status
        if ScorecardStatus.OFF_TRACK in statuses:
            dept_status = ScorecardStatus.OFF_TRACK
        elif ScorecardStatus.AT_RISK in statuses:
            dept_status = ScorecardStatus.AT_RISK
        elif all(s == ScorecardStatus.EXCEEDING for s in statuses):
            dept_status = ScorecardStatus.EXCEEDING
        else:
            dept_status = ScorecardStatus.ON_TRACK

        return DepartmentScorecard(
            department_name=department_name,
            category=category,
            overall_status=dept_status,
            scorecard_items=items,
        )

    def generate_all_scorecards(
        self,
        metrics_by_kpi: Dict[str, Decimal],
        previous_by_kpi: Optional[Dict[str, Decimal]] = None,
    ) -> List[DepartmentScorecard]:
        scorecards: List[DepartmentScorecard] = []
        departments = [
            ("Financial Performance Scorecard", KPICategory.FINANCIAL),
            ("Sales & Revenue Pipeline Scorecard", KPICategory.SALES),
            ("Customer Success & Retention Scorecard", KPICategory.CLIENT),
            ("Project & Delivery Excellence Scorecard", KPICategory.DELIVERY),
            ("Customer Support & SLA Scorecard", KPICategory.SUPPORT),
            ("AI Systems & Autonomy Scorecard", KPICategory.AI),
            ("Operations & Platform Reliability Scorecard", KPICategory.OPERATIONS),
        ]

        for dept_name, cat in departments:
            sc = self.generate_department_scorecard(
                department_name=dept_name,
                category=cat,
                metric_values=metrics_by_kpi,
                previous_values=previous_by_kpi,
            )
            scorecards.append(sc)

        return scorecards
