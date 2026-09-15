"""Portfolio Health Management, Workload Intelligence, and Engineering Capacity Planning."""

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProjectPortfolioItem(BaseModel):
    project_id: str
    project_name: str
    client_name: str
    stage: str
    health_status: str  # HEALTHY, AT_RISK, CRITICAL, BLOCKED, COMPLETED
    contract_value: Decimal
    incurred_cost: Decimal
    gross_margin_pct: Decimal
    progress_pct: Decimal
    completion_target_date: str
    delay_days: int = 0
    active_risks_count: int = 0
    assigned_lead: str = ""


class PortfolioSummary(BaseModel):
    total_projects: int
    active_projects: int
    healthy_projects: int
    at_risk_projects: int
    critical_projects: int
    completed_projects: int
    on_time_delivery_rate_pct: Decimal
    portfolio_average_margin_pct: Decimal
    total_portfolio_value: Decimal
    total_incurred_cost: Decimal
    projects: List[ProjectPortfolioItem] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TeamCapacityItem(BaseModel):
    member_id: str
    name: str
    role: str
    primary_skills: List[str]
    capacity_weekly_hours: Decimal
    assigned_weekly_hours: Decimal
    utilization_pct: Decimal
    workload_status: str  # OPTIMAL, UNDERUTILIZED, OVERLOADED
    active_projects_count: int


class CapacityPlanningSummary(BaseModel):
    total_team_members: int
    total_available_capacity_hours: Decimal
    total_committed_hours: Decimal
    aggregate_utilization_pct: Decimal
    overloaded_members_count: int
    underutilized_members_count: int
    capacity_risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    recommendations: List[str] = Field(default_factory=list)
    team_members: List[TeamCapacityItem] = Field(default_factory=list)


class PortfolioCapacityManager:
    """Manages cross-project portfolio health and organizational capacity intelligence."""

    def __init__(self):
        pass

    def evaluate_portfolio(self, raw_projects: Optional[List[Dict[str, Any]]] = None) -> PortfolioSummary:
        projects_data = raw_projects or [
            {
                "project_id": "proj_alpha",
                "project_name": "Autonomous ERP Integration",
                "client_name": "Acme Global Logistics",
                "stage": "EXECUTION",
                "health_status": "HEALTHY",
                "contract_value": Decimal("4500000.00"),
                "incurred_cost": Decimal("1350000.00"),
                "progress_pct": Decimal("65.0"),
                "completion_target_date": "2026-11-30",
                "delay_days": 0,
                "active_risks_count": 1,
                "assigned_lead": "Lead Architect A",
            },
            {
                "project_id": "proj_beta",
                "project_name": "Predictive Supply Chain Copilot",
                "client_name": "Zenith Retail Corp",
                "stage": "UAT_HANDOVER",
                "health_status": "AT_RISK",
                "contract_value": Decimal("3200000.00"),
                "incurred_cost": Decimal("1280000.00"),
                "progress_pct": Decimal("88.0"),
                "completion_target_date": "2026-10-15",
                "delay_days": 4,
                "active_risks_count": 2,
                "assigned_lead": "Senior Tech Lead B",
            },
            {
                "project_id": "proj_gamma",
                "project_name": "Customer 360 AI Analytics Suite",
                "client_name": "Apex Financial",
                "stage": "INITIATION",
                "health_status": "HEALTHY",
                "contract_value": Decimal("2800000.00"),
                "incurred_cost": Decimal("280000.00"),
                "progress_pct": Decimal("20.0"),
                "completion_target_date": "2026-12-15",
                "delay_days": 0,
                "active_risks_count": 0,
                "assigned_lead": "Solutions Lead C",
            },
        ]

        items: List[ProjectPortfolioItem] = []
        total_val = Decimal("0.00")
        total_cost = Decimal("0.00")
        healthy = 0
        at_risk = 0
        critical = 0
        completed = 0

        for p in projects_data:
            val = Decimal(str(p["contract_value"]))
            cost = Decimal(str(p["incurred_cost"]))
            total_val += val
            total_cost += cost

            margin_pct = (
                ((val - cost) / val * Decimal("100.00")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
                if val > Decimal("0.00")
                else Decimal("0.00")
            )

            status = p["health_status"]
            if status == "HEALTHY":
                healthy += 1
            elif status == "AT_RISK":
                at_risk += 1
            elif status in ("CRITICAL", "BLOCKED"):
                critical += 1
            elif status == "COMPLETED":
                completed += 1

            item = ProjectPortfolioItem(
                project_id=p["project_id"],
                project_name=p["project_name"],
                client_name=p["client_name"],
                stage=p["stage"],
                health_status=status,
                contract_value=val,
                incurred_cost=cost,
                gross_margin_pct=margin_pct,
                progress_pct=Decimal(str(p["progress_pct"])),
                completion_target_date=p["completion_target_date"],
                delay_days=p.get("delay_days", 0),
                active_risks_count=p.get("active_risks_count", 0),
                assigned_lead=p.get("assigned_lead", ""),
            )
            items.append(item)

        avg_margin = (
            ((total_val - total_cost) / total_val * Decimal("100.00")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            if total_val > Decimal("0.00")
            else Decimal("0.00")
        )

        active_count = len(items) - completed
        on_time_pct = (
            (Decimal(healthy) / Decimal(active_count) * Decimal("100.00")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            if active_count > 0
            else Decimal("100.00")
        )

        return PortfolioSummary(
            total_projects=len(items),
            active_projects=active_count,
            healthy_projects=healthy,
            at_risk_projects=at_risk,
            critical_projects=critical,
            completed_projects=completed,
            on_time_delivery_rate_pct=on_time_pct,
            portfolio_average_margin_pct=avg_margin,
            total_portfolio_value=total_val,
            total_incurred_cost=total_cost,
            projects=items,
        )

    def evaluate_capacity(self, raw_members: Optional[List[Dict[str, Any]]] = None) -> CapacityPlanningSummary:
        members_data = raw_members or [
            {
                "member_id": "dev_1",
                "name": "Hamza Tariq",
                "role": "Lead Fullstack & AI Engineer",
                "primary_skills": ["Python", "FastAPI", "React", "LangChain", "PostgreSQL"],
                "capacity_weekly_hours": Decimal("40.0"),
                "assigned_weekly_hours": Decimal("44.0"),
                "active_projects_count": 2,
            },
            {
                "member_id": "dev_2",
                "name": "Sarah Ahmed",
                "role": "Senior Frontend & UX Architect",
                "primary_skills": ["Next.js", "TypeScript", "TailwindCSS", "State Management"],
                "capacity_weekly_hours": Decimal("40.0"),
                "assigned_weekly_hours": Decimal("36.0"),
                "active_projects_count": 2,
            },
            {
                "member_id": "dev_3",
                "name": "Zaid Malik",
                "role": "Backend & Cloud Infrastructure Engineer",
                "primary_skills": ["Docker", "Kubernetes", "Redis", "Celery", "PostgreSQL"],
                "capacity_weekly_hours": Decimal("40.0"),
                "assigned_weekly_hours": Decimal("32.0"),
                "active_projects_count": 1,
            },
            {
                "member_id": "dev_4",
                "name": "Ayesha Khan",
                "role": "AI Research & Evaluation Engineer",
                "primary_skills": ["PyTorch", "NLP", "Prompt Evaluation", "MLOps"],
                "capacity_weekly_hours": Decimal("40.0"),
                "assigned_weekly_hours": Decimal("46.0"),
                "active_projects_count": 2,
            },
        ]

        items: List[TeamCapacityItem] = []
        total_cap = Decimal("0.0")
        total_assigned = Decimal("0.0")
        overloaded = 0
        underutilized = 0

        for m in members_data:
            cap = Decimal(str(m["capacity_weekly_hours"]))
            assigned = Decimal(str(m["assigned_weekly_hours"]))
            total_cap += cap
            total_assigned += assigned

            util_pct = (
                (assigned / cap * Decimal("100.00")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
                if cap > Decimal("0.0")
                else Decimal("0.0")
            )

            if util_pct > Decimal("105.0"):
                workload_status = "OVERLOADED"
                overloaded += 1
            elif util_pct < Decimal("70.0"):
                workload_status = "UNDERUTILIZED"
                underutilized += 1
            else:
                workload_status = "OPTIMAL"

            item = TeamCapacityItem(
                member_id=m["member_id"],
                name=m["name"],
                role=m["role"],
                primary_skills=m.get("primary_skills", []),
                capacity_weekly_hours=cap,
                assigned_weekly_hours=assigned,
                utilization_pct=util_pct,
                workload_status=workload_status,
                active_projects_count=m.get("active_projects_count", 1),
            )
            items.append(item)

        agg_util = (
            (total_assigned / total_cap * Decimal("100.00")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            if total_cap > Decimal("0.0")
            else Decimal("0.0")
        )

        risk_level = "LOW"
        recs: List[str] = []
        if overloaded >= 2:
            risk_level = "HIGH"
            recs.append("Reallocate non-critical milestone tasks from overloaded engineers to maintain sprint velocity.")
            recs.append("Consider onboarding additional backend/AI capacity for upcoming Q4 pipeline commitments.")
        elif overloaded == 1:
            risk_level = "MEDIUM"
            recs.append("Shift secondary code-review duties from overloaded lead engineers.")

        return CapacityPlanningSummary(
            total_team_members=len(items),
            total_available_capacity_hours=total_cap,
            total_committed_hours=total_assigned,
            aggregate_utilization_pct=agg_util,
            overloaded_members_count=overloaded,
            underutilized_members_count=underutilized,
            capacity_risk_level=risk_level,
            recommendations=recs,
            team_members=items,
        )
