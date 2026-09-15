"""GTM Strategy, Segmentation, ICP Engine, Target Account Scoring, Market Coverage, and Territory Intelligence."""
from typing import Any, Dict, List, Optional
from backend.app.services.revenue_growth.base import (
    AttrDict,
    SalesMotion,
    generate_rev_id,
    current_utc_time,
)


class GtmTargetingService:
    """Manages GTM strategies, segments, ICP criteria, target account scoring, coverage, and territories."""

    def __init__(self, db_session=None):
        self.db = db_session
        self._in_memory_strategies: List[Dict[str, Any]] = []
        self._in_memory_segments: List[Dict[str, Any]] = []
        self._in_memory_icps: List[Dict[str, Any]] = []
        self._in_memory_accounts: List[Dict[str, Any]] = []
        self._in_memory_scores: List[Dict[str, Any]] = []
        self._in_memory_coverage: List[Dict[str, Any]] = []
        self._in_memory_territories: List[Dict[str, Any]] = []

    def create_gtm_strategy(
        self,
        name: str,
        target_market: str,
        sales_motion: str = SalesMotion.CONSULTATIVE.value,
        positioning: Optional[str] = None,
        value_proposition: Optional[str] = None,
        channels: Optional[List[str]] = None,
        metrics_targets: Optional[Dict[str, Any]] = None,
    ) -> AttrDict:
        s_id = generate_rev_id("gtm")
        now = current_utc_time().isoformat()
        strategy = AttrDict({
            "id": s_id,
            "name": name,
            "target_market": target_market,
            "sales_motion": sales_motion.lower(),
            "positioning": positioning or "Deterministic AI Workforce for Enterprise Operations",
            "value_proposition": value_proposition or "Reduces operational cycle time by 60% with zero hallucination guarantee",
            "status": "active",
            "channels": channels or ["direct_sales", "partners", "inbound_web"],
            "metrics_targets": metrics_targets or {"arr_target_usd": 5000000.0, "win_rate_target": 0.35},
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_strategies.append(strategy)
        return strategy

    def list_gtm_strategies(self) -> List[AttrDict]:
        return list(self._in_memory_strategies)

    def create_segment(
        self,
        name: str,
        industry: str,
        company_size_tier: str = "enterprise",
        estimated_tam_usd: float = 120000000.0,
        estimated_sam_usd: float = 35000000.0,
        priority_tier: str = "tier_1",
        description: Optional[str] = None,
        strategy_id: Optional[str] = None,
    ) -> AttrDict:
        seg_id = generate_rev_id("seg")
        now = current_utc_time().isoformat()
        segment = AttrDict({
            "id": seg_id,
            "strategy_id": strategy_id,
            "name": name,
            "description": description or f"Target market segment for {name}",
            "industry": industry,
            "company_size_tier": company_size_tier.lower(),
            "estimated_tam_usd": estimated_tam_usd,
            "estimated_sam_usd": estimated_sam_usd,
            "priority_tier": priority_tier.lower(),
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_segments.append(segment)
        return segment

    def list_segments(self) -> List[AttrDict]:
        return list(self._in_memory_segments)

    def create_icp(
        self,
        name: str,
        target_industries: List[str],
        min_employee_count: int = 250,
        max_employee_count: int = 10000,
        min_arr_usd: float = 10000000.0,
        required_tech_profile: Optional[List[str]] = None,
        pain_points: Optional[List[str]] = None,
        buying_signals: Optional[List[str]] = None,
        exclusions: Optional[List[str]] = None,
        segment_id: Optional[str] = None,
    ) -> AttrDict:
        icp_id = generate_rev_id("icp")
        now = current_utc_time().isoformat()
        icp = AttrDict({
            "id": icp_id,
            "segment_id": segment_id,
            "name": name,
            "target_industries": target_industries,
            "min_employee_count": min_employee_count,
            "max_employee_count": max_employee_count,
            "min_arr_usd": min_arr_usd,
            "required_tech_profile": required_tech_profile or ["Cloud Native", "Kubernetes", "PostgreSQL"],
            "pain_points": pain_points or ["Manual governance overhead", "Slow release cycles", "Compliance audit friction"],
            "buying_signals": buying_signals or ["Hiring VP of Platform", "Public multi-cloud migration", "GRC audit initiative"],
            "exclusions": exclusions or ["Pre-revenue startups", "Non-digital service agencies"],
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_icps.append(icp)
        return icp

    def list_icps(self) -> List[AttrDict]:
        return list(self._in_memory_icps)

    def create_target_account(
        self,
        company_name: str,
        domain: Optional[str] = None,
        industry: Optional[str] = "FinTech",
        employee_count: int = 500,
        estimated_annual_revenue: float = 45000000.0,
        country: str = "US",
        priority_level: str = "high",
        assigned_rep: Optional[str] = "Sarah Chen",
    ) -> AttrDict:
        acc_id = generate_rev_id("acc")
        now = current_utc_time().isoformat()
        
        # Calculate ICP fit score
        fit_score = 0.85 if employee_count >= 250 and estimated_annual_revenue >= 10000000.0 else 0.65

        account = AttrDict({
            "id": acc_id,
            "company_name": company_name,
            "domain": domain or f"{company_name.lower().replace(' ', '')}.com",
            "industry": industry,
            "employee_count": employee_count,
            "estimated_annual_revenue": estimated_annual_revenue,
            "country": country,
            "icp_fit_score": fit_score,
            "priority_level": priority_level.lower(),
            "coverage_status": "researched",
            "assigned_rep": assigned_rep,
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_accounts.append(account)
        return account

    def list_target_accounts(self) -> List[AttrDict]:
        return list(self._in_memory_accounts)

    def score_target_account(
        self,
        account_id: str,
        icp_fit: float = 0.90,
        business_need: float = 0.85,
        digital_gap: float = 0.80,
        revenue_potential: float = 0.92,
        buying_signal: float = 0.88,
    ) -> AttrDict:
        """Computes multi-factor composite account prioritization score."""
        composite = round(
            (icp_fit * 0.25) +
            (business_need * 0.25) +
            (digital_gap * 0.15) +
            (revenue_potential * 0.20) +
            (buying_signal * 0.15),
            2
        )
        sc_id = generate_rev_id("sc")
        now = current_utc_time().isoformat()
        score = AttrDict({
            "id": sc_id,
            "account_id": account_id,
            "icp_fit": icp_fit,
            "business_need": business_need,
            "digital_gap": digital_gap,
            "revenue_potential": revenue_potential,
            "buying_signal": buying_signal,
            "composite_score": composite,
            "scored_at": now,
        })
        self._in_memory_scores.append(score)
        
        # update account
        for acc in self._in_memory_accounts:
            if acc["id"] == account_id:
                acc["icp_fit_score"] = composite
                acc["updated_at"] = now
                break

        return score

    def list_account_scores(self, account_id: Optional[str] = None) -> List[AttrDict]:
        if account_id:
            return [s for s in self._in_memory_scores if s.get("account_id") == account_id]
        return list(self._in_memory_scores)

    def get_market_coverage(self) -> List[AttrDict]:
        if not self._in_memory_coverage:
            now = current_utc_time().isoformat()
            self._in_memory_coverage = [
                AttrDict({
                    "id": generate_rev_id("cov"),
                    "segment": "Tier-1 Strategic FinTech",
                    "territory": "North America East",
                    "accounts_discovered": 140,
                    "accounts_researched": 98,
                    "qualified_accounts": 64,
                    "contacted_accounts": 42,
                    "active_opportunities": 18,
                    "won_accounts": 9,
                    "coverage_percentage": 0.68,
                    "recorded_at": now,
                }),
                AttrDict({
                    "id": generate_rev_id("cov"),
                    "segment": "Enterprise Logistics & 3PL",
                    "territory": "EMEA Central",
                    "accounts_discovered": 110,
                    "accounts_researched": 72,
                    "qualified_accounts": 45,
                    "contacted_accounts": 28,
                    "active_opportunities": 12,
                    "won_accounts": 5,
                    "coverage_percentage": 0.54,
                    "recorded_at": now,
                }),
            ]
        return list(self._in_memory_coverage)

    def list_territories(self) -> List[AttrDict]:
        if not self._in_memory_territories:
            now = current_utc_time().isoformat()
            self._in_memory_territories = [
                AttrDict({
                    "id": generate_rev_id("ter"),
                    "name": "North America Strategic Enterprise",
                    "geography": "US / Canada",
                    "industry_focus": ["FinTech", "SaaS", "Autonomous Systems"],
                    "account_tier": "tier_1",
                    "owner_name": "Sarah Chen",
                    "revenue_potential_usd": 12500000.0,
                    "created_at": now,
                    "updated_at": now,
                }),
                AttrDict({
                    "id": generate_rev_id("ter"),
                    "name": "EMEA Enterprise Growth",
                    "geography": "UK / DACH / Nordics",
                    "industry_focus": ["Supply Chain", "FinTech"],
                    "account_tier": "tier_1",
                    "owner_name": "Marcus Vance",
                    "revenue_potential_usd": 8500000.0,
                    "created_at": now,
                    "updated_at": now,
                }),
            ]
        return list(self._in_memory_territories)
