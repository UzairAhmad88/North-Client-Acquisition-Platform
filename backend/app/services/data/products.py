"""Data Products service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class ProductsService:
    """Manages curated, SLA-bound, governed Data Products (Customer 360, Sales Intel)."""

    def __init__(self):
        self._products: Dict[str, Dict[str, Any]] = {}
        self._seed_default_products()

    def _seed_default_products(self):
        default_items = [
            ("Customer 360", "Unified multi-channel customer identity, health, LTV, and risk profile.", "Customers", 99.4),
            ("Sales Intelligence", "Predictive win rates, deal velocity, and pipeline attribution.", "Sales", 98.9),
            ("Financial Intelligence", "Reconciled ledger, ARR/MRR cash flow, and cost forecasting.", "Finance", 99.8),
            ("Engineering Intelligence", "DORA metrics, code velocity, test flakiness, and tech debt.", "Engineering", 97.8),
            ("AI Training Gold Dataset", "Cleaned, deduplicated, PII-scrubbed LLM fine-tuning corpus.", "AI", 99.5),
        ]
        for name, desc, domain, q_score in default_items:
            pid = f"prod_{name.lower().replace(' ', '_')}"
            self._products[pid] = {
                "id": pid,
                "tenant_id": "default_tenant",
                "name": name,
                "description": desc,
                "domain": domain,
                "owner": "data-product-lead@uzaii.com",
                "source_datasets": [f"lake_{domain.lower()}_gold"],
                "contract_id": f"contract_{domain.lower()}",
                "schema_def": {"entities": 15, "dimensions": 8},
                "quality_score": q_score,
                "sla_freshness_minutes": 60,
                "security_classification": "INTERNAL",
                "monthly_cost_usd": 150.0,
                "version": "v1.0.0",
                "status": "ACTIVE",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

    def create_product(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        product_id = data.get("id") or f"prod_{uuid.uuid4().hex[:12]}"
        record = {
            "id": product_id,
            "tenant_id": tenant_id,
            "name": data.get("name", "Custom Data Product"),
            "description": data.get("description", ""),
            "domain": data.get("domain", "General"),
            "owner": data.get("owner", "data-product-lead@uzaii.com"),
            "source_datasets": data.get("source_datasets", []),
            "contract_id": data.get("contract_id"),
            "schema_def": data.get("schema_def", {}),
            "quality_score": data.get("quality_score", 98.5),
            "sla_freshness_minutes": data.get("sla_freshness_minutes", 60),
            "security_classification": data.get("security_classification", "INTERNAL"),
            "tier": data.get("tier", "GOLD"),
            "sla_tier": data.get("sla_tier", "TIER_1_ENTERPRISE"),
            "monthly_cost_usd": data.get("monthly_cost_usd", 100.0),
            "version": data.get("version", "v1.0.0"),
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._products[product_id] = record
        return record

    def list_products(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [p for p in self._products.values() if p.get("tenant_id") == tenant_id]

    def get_product(self, product_id: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        p = self._products.get(product_id)
        if p and p.get("tenant_id") == tenant_id:
            return p
        return None
