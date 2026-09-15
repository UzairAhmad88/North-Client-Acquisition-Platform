"""Phase 60: Background Worker Tasks for Unified Product Management & Product Intelligence OS."""

import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.product_os.service import ProductOperatingSystemService
except ImportError:
    from app.services.product_os.service import ProductOperatingSystemService

logger = logging.getLogger(__name__)


def run_feedback_theme_clustering_task(
    tenant_id: str = "default_tenant",
    product_id: str = "prod_default",
) -> List[Dict[str, Any]]:
    """Background task to cluster unstructured feedback into validated problem themes."""
    service = ProductOperatingSystemService()
    themes = service.problems_feedback_service.cluster_feedback_themes(tenant_id, product_id)
    logger.info(f"Clustered {len(themes)} feedback themes for product {product_id}")
    return [dict(t) for t in themes]


def run_opportunity_scoring_task(
    tenant_id: str,
    product_id: str,
    title: str,
    problem_id: str,
    customer_value_score: float = 9.0,
    business_value_score: float = 8.5,
    confidence_score: float = 9.0,
    effort_score: float = 4.0,
    strategic_fit_score: float = 9.0,
    revenue_potential_usd: float = 500000.0,
) -> Dict[str, Any]:
    """Background task to score product opportunities and update opportunity tree."""
    service = ProductOperatingSystemService()
    opp = service.problems_feedback_service.create_opportunity(
        tenant_id=tenant_id,
        product_id=product_id,
        title=title,
        problem_id=problem_id,
        customer_value_score=customer_value_score,
        business_value_score=business_value_score,
        confidence_score=confidence_score,
        effort_score=effort_score,
        strategic_fit_score=strategic_fit_score,
        revenue_potential_usd=revenue_potential_usd,
    )
    logger.info(f"Calculated opportunity score for {opp.opportunity_id}: {opp.score}")
    return dict(opp)


def run_product_health_evaluation_task(
    tenant_id: str,
    product_id: str,
    product_name: str,
    adoption_score: float = 85.0,
    retention_score: float = 80.0,
    reliability_score: float = 99.0,
    feedback_sentiment_score: float = 82.0,
    support_efficiency_score: float = 80.0,
    quality_defect_score: float = 90.0,
    gross_margin_score: float = 85.0,
) -> Dict[str, Any]:
    """Background task to evaluate 7-factor composite product health scorecard."""
    service = ProductOperatingSystemService()
    scorecard = service.analytics_service.calculate_product_health(
        tenant_id=tenant_id,
        product_id=product_id,
        product_name=product_name,
        adoption_score=adoption_score,
        retention_score=retention_score,
        reliability_score=reliability_score,
        feedback_sentiment_score=feedback_sentiment_score,
        support_efficiency_score=support_efficiency_score,
        quality_defect_score=quality_defect_score,
        gross_margin_score=gross_margin_score,
    )
    logger.info(f"Product health calculated for {product_name}: {scorecard.health_state} ({scorecard.composite_score})")
    return dict(scorecard)


def run_requirements_traceability_audit_task(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Background task to audit requirement completeness and detect orphaned initiatives."""
    service = ProductOperatingSystemService()
    audit = service.requirements_service.validate_requirements_completeness(tenant_id)
    logger.info(f"Requirements audit completed: {audit.get('requirements_health_score')}% health")
    return audit
