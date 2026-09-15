"""
Product/Service Concepts, Business Cases, Unit Economics, Prototypes, and PRD Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional


class ProductConceptBusinessCaseManager:
    """Manages product/service concepts, unit economics, business case modeling, prototypes, and PRDs."""

    def __init__(self):
        self._product_concepts: Dict[str, List[Dict[str, Any]]] = {}
        self._service_concepts: Dict[str, List[Dict[str, Any]]] = {}
        self._business_cases: Dict[str, List[Dict[str, Any]]] = {}
        self._economics: Dict[str, Dict[str, Any]] = {}
        self._prototypes: Dict[str, List[Dict[str, Any]]] = {}
        self._prds: Dict[str, List[Dict[str, Any]]] = {}

    # Product Concepts
    def create_product_concept(
        self,
        workspace_id: str,
        name: str,
        target_customer_persona: str,
        value_proposition: str,
        core_features: Optional[List[str]] = None,
        differentiators: Optional[List[str]] = None,
        business_model_type: str = "SUBSCRIPTION",
        technical_architecture_notes: Optional[str] = None,
        idea_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Synthesize promising idea into a concrete product concept."""
        cid = f"pcon_{uuid.uuid4().hex[:12]}"
        concept = {
            "id": cid,
            "workspace_id": workspace_id,
            "idea_id": idea_id,
            "name": name,
            "target_customer_persona": target_customer_persona,
            "value_proposition": value_proposition,
            "core_features": core_features or [],
            "differentiators": differentiators or [],
            "business_model_type": business_model_type,
            "technical_architecture_notes": technical_architecture_notes or "Cloud-native FastAPI + Next.js + Celery",
            "status": "DRAFT",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._product_concepts.setdefault(workspace_id, []).append(concept)
        return concept

    def list_product_concepts(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._product_concepts.get(workspace_id, [])

    # Service Concepts
    def create_service_concept(
        self,
        workspace_id: str,
        service_name: str,
        target_client_profile: str,
        service_deliverables: Optional[List[str]] = None,
        delivery_model: str = "HYBRID_AI_HUMAN",
        pricing_model: str = "MONTHLY_RETAINER",
        idea_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Synthesize promising idea into a governed service concept."""
        sid = f"scon_{uuid.uuid4().hex[:12]}"
        service = {
            "id": sid,
            "workspace_id": workspace_id,
            "idea_id": idea_id,
            "service_name": service_name,
            "target_client_profile": target_client_profile,
            "service_deliverables": service_deliverables or [],
            "delivery_model": delivery_model,
            "pricing_model": pricing_model,
            "status": "DRAFT",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._service_concepts.setdefault(workspace_id, []).append(service)
        return service

    def list_service_concepts(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._service_concepts.get(workspace_id, [])

    # Business Case & Unit Economics
    def create_business_case(
        self,
        workspace_id: str,
        concept_id: str,
        target_tam_usd: float = 1000000.0,
        projected_year1_revenue_usd: float = 250000.0,
        estimated_development_cost_usd: float = 50000.0,
        estimated_cac_usd: float = 1200.0,
        estimated_ltv_usd: float = 7200.0,
        break_even_customers_count: int = 25,
        gross_margin_percentage: float = 82.0,
        recommendation: str = "PROCEED_TO_MVP",
    ) -> Dict[str, Any]:
        """Compute financial business case with payback period and break-even."""
        annual_profit_per_cust = (estimated_ltv_usd / 3.0) * (gross_margin_percentage / 100.0)
        payback_months = round((estimated_cac_usd / (annual_profit_per_cust / 12.0)), 1) if annual_profit_per_cust > 0 else 12.0

        bc_id = f"bcase_{uuid.uuid4().hex[:12]}"
        bcase = {
            "id": bc_id,
            "workspace_id": workspace_id,
            "concept_id": concept_id,
            "target_tam_usd": target_tam_usd,
            "projected_year1_revenue_usd": projected_year1_revenue_usd,
            "estimated_development_cost_usd": estimated_development_cost_usd,
            "estimated_cac_usd": estimated_cac_usd,
            "estimated_ltv_usd": estimated_ltv_usd,
            "payback_months": payback_months,
            "break_even_customers_count": break_even_customers_count,
            "gross_margin_percentage": gross_margin_percentage,
            "recommendation": recommendation,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._business_cases.setdefault(workspace_id, []).append(bcase)
        return bcase

    def model_unit_economics(
        self,
        concept_id: str,
        price_per_unit_usd: float = 199.0,
        direct_labor_cost_usd: float = 20.0,
        ai_compute_cost_usd: float = 12.5,
        infrastructure_cost_usd: float = 8.0,
    ) -> Dict[str, Any]:
        """Model granular COGS, AI inference tokens, and unit margin."""
        cogs = direct_labor_cost_usd + ai_compute_cost_usd + infrastructure_cost_usd
        gross_profit = price_per_unit_usd - cogs
        margin_pct = round((gross_profit / price_per_unit_usd) * 100.0, 2) if price_per_unit_usd > 0 else 0.0

        econ = {
            "concept_id": concept_id,
            "price_per_unit_usd": price_per_unit_usd,
            "direct_labor_cost_usd": direct_labor_cost_usd,
            "ai_compute_cost_usd": ai_compute_cost_usd,
            "infrastructure_cost_usd": infrastructure_cost_usd,
            "gross_profit_per_unit_usd": round(gross_profit, 2),
            "gross_margin_percentage": margin_pct,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._economics[concept_id] = econ
        return econ

    # Prototypes & PRD
    def record_prototype(
        self,
        concept_id: str,
        prototype_name: str,
        version: str = "v0.1",
        usability_score: float = 8.5,
        user_feedback_summary: Optional[str] = None,
        prototype_url_or_repo: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Track prototype test iteration."""
        proto_id = f"proto_{uuid.uuid4().hex[:12]}"
        proto = {
            "id": proto_id,
            "concept_id": concept_id,
            "prototype_name": prototype_name,
            "version": version,
            "prototype_url_or_repo": prototype_url_or_repo or "https://github.com/norths/prototype",
            "usability_score": usability_score,
            "user_feedback_summary": user_feedback_summary or "Positive feedback on core workflow.",
            "status": "ACTIVE",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._prototypes.setdefault(concept_id, []).append(proto)
        return proto

    def generate_prd(
        self,
        concept_id: str,
        title: str,
        problem_summary: str,
        target_personas: Optional[List[str]] = None,
        user_stories: Optional[List[str]] = None,
        functional_requirements: Optional[List[str]] = None,
        security_privacy_requirements: Optional[List[str]] = None,
        success_metrics: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate structured Product Requirements Document draft."""
        prd_id = f"prd_{uuid.uuid4().hex[:12]}"
        prd = {
            "id": prd_id,
            "concept_id": concept_id,
            "title": title,
            "problem_summary": problem_summary,
            "target_personas": target_personas or ["Enterprise Operations Lead"],
            "user_stories": user_stories or ["As an operator, I want automated lead qualification so that I save 5 hours weekly."],
            "functional_requirements": functional_requirements or ["Multi-channel ingestion", "Fact validation engine"],
            "security_privacy_requirements": security_privacy_requirements or ["SOC2 compliance", "Tenant isolation"],
            "success_metrics": success_metrics or ["Conversion rate > 20%", "System uptime 99.9%"],
            "human_approved": False,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._prds.setdefault(concept_id, []).append(prd)
        return prd
