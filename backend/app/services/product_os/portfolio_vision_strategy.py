"""Phase 60: Product Portfolio Hierarchy, Product Vision, Strategy, and Objectives / OKRs."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.product_os.base import (
        AttrDict,
        ProductLifecycleState,
        generate_product_id,
    )
except ImportError:
    from app.services.product_os.base import (
        AttrDict,
        ProductLifecycleState,
        generate_product_id,
    )

logger = logging.getLogger(__name__)


class PortfolioVisionStrategyService:
    """Manages product portfolio items, lines, visions, strategy roadmaps, and OKRs."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._products: Dict[str, Dict[str, Any]] = {}
        self._product_lines: Dict[str, Dict[str, Any]] = {}
        self._visions: Dict[str, Dict[str, Any]] = {}
        self._strategies: Dict[str, Dict[str, Any]] = {}
        self._objectives: Dict[str, Dict[str, Any]] = {}
        self._key_results: Dict[str, Dict[str, Any]] = {}

    def create_product(
        self,
        tenant_id: str = "default_tenant",
        name: str = "New Product",
        product_line: str = "Enterprise Intelligence",
        code: Optional[str] = None,
        lifecycle_state: str = ProductLifecycleState.DISCOVERY.value,
        target_icp: str = "Enterprise Leaders",
        owner_email: str = "product-ops@uzaii.com",
        description: str = "",
        **kwargs,
    ) -> AttrDict:
        """Create and register a new product in the portfolio."""
        prod_id = generate_product_id("prd")
        now = datetime.now(timezone.utc).isoformat()
        code_val = code or f"UZAII-PRD-{hash(name) % 10000:04d}"

        record = {
            "product_id": prod_id,
            "id": prod_id,
            "tenant_id": tenant_id,
            "name": name,
            "product_line": product_line,
            "code": code_val,
            "lifecycle_state": lifecycle_state,
            "target_icp": target_icp,
            "owner_email": owner_email,
            "description": description,
            "created_at": now,
            "updated_at": now,
        }
        self._products[prod_id] = record
        return AttrDict(record)

    def create_product_line(
        self,
        tenant_id: str = "default_tenant",
        name: str = "Core AI Platform",
        description: str = "",
    ) -> AttrDict:
        line_id = generate_product_id("line")
        now = datetime.now(timezone.utc).isoformat()
        record = {
            "line_id": line_id,
            "id": line_id,
            "tenant_id": tenant_id,
            "name": name,
            "description": description,
            "created_at": now,
        }
        self._product_lines[line_id] = record
        return AttrDict(record)

    def create_product_vision(
        self,
        tenant_id: str = "default_tenant",
        product_id: str = "prod_001",
        target_users: Any = "Enterprise Leaders",
        core_problem: str = "",
        value_proposition: str = "",
        differentiation: str = "",
        strategic_fit: str = "",
        market_opportunity: str = "",
        **kwargs,
    ) -> AttrDict:
        """Create versioned strategic product vision document."""
        vision_id = generate_product_id("vis")
        now = datetime.now(timezone.utc).isoformat()
        record = {
            "vision_id": vision_id,
            "id": vision_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "target_users": target_users,
            "core_problem": core_problem,
            "value_proposition": value_proposition,
            "differentiation": differentiation,
            "strategic_fit": strategic_fit,
            "market_opportunity": market_opportunity,
            "version": 1,
            "created_at": now,
            "updated_at": now,
        }
        self._visions[product_id] = record
        return AttrDict(record)

    def create_product_strategy(
        self,
        tenant_id: str = "default_tenant",
        product_id: str = "prod_001",
        positioning: str = "",
        growth_strategy: str = "",
        product_bets: Optional[List[Any]] = None,
        core_metrics: Optional[Dict[str, Any]] = None,
        icp_definition: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> AttrDict:
        """Create cohesive product strategy mapping bets and growth mechanics."""
        strat_id = generate_product_id("str")
        now = datetime.now(timezone.utc).isoformat()
        record = {
            "strategy_id": strat_id,
            "id": strat_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "positioning": positioning,
            "growth_strategy": growth_strategy,
            "product_bets": product_bets or ["Deterministic Decision Governance", "Real-time Telemetry"],
            "core_metrics": core_metrics or {},
            "icp_definition": icp_definition or {},
            "created_at": now,
            "updated_at": now,
        }
        self._strategies[product_id] = record
        return AttrDict(record)

    def create_objective(
        self,
        tenant_id: str = "default_tenant",
        product_id: str = "prod_001",
        title: str = "Accelerate Adoption",
        timeframe: str = "2026-Q3",
        **kwargs,
    ) -> AttrDict:
        """Create OKR level strategic product objective."""
        obj_id = generate_product_id("obj")
        now = datetime.now(timezone.utc).isoformat()
        record = {
            "objective_id": obj_id,
            "id": obj_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "title": title,
            "timeframe": timeframe,
            "status": "IN_PROGRESS",
            "created_at": now,
        }
        self._objectives[obj_id] = record
        return AttrDict(record)

    def add_key_result(
        self,
        tenant_id: str = "default_tenant",
        objective_id: str = "obj_001",
        title: str = "Increase Retention",
        baseline_value: float = 50.0,
        target_value: float = 85.0,
        current_value: float = 65.0,
        unit: str = "%",
    ) -> AttrDict:
        """Attach measurable Key Result with progress calculations."""
        kr_id = generate_product_id("kr")
        now = datetime.now(timezone.utc).isoformat()

        denom = target_value - baseline_value
        if denom == 0:
            progress = 100.0
        else:
            progress = round(((current_value - baseline_value) / denom) * 100.0, 2)

        record = {
            "key_result_id": kr_id,
            "id": kr_id,
            "tenant_id": tenant_id,
            "objective_id": objective_id,
            "title": title,
            "baseline_value": baseline_value,
            "target_value": target_value,
            "current_value": current_value,
            "unit": unit,
            "progress_pct": max(0.0, progress),
            "created_at": now,
        }
        self._key_results[kr_id] = record
        return AttrDict(record)
