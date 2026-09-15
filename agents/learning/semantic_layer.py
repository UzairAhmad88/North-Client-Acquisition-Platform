"""Semantic Query Layer for Secure Natural Language Analytics."""

from typing import Any, Dict, List, Optional
import re
from agents.learning.models import SemanticQueryResult


class SemanticLayerEngine:
    """Translates user natural language questions into validated, parameterized queries.

    CRITICAL SECURITY RULE:
    Direct raw SQL generation or execution by AI is strictly prohibited. All requests map to
    pre-approved metric queries and repository aggregations.
    """

    APPROVED_METRIC_QUERIES = {
        "SALES_CONVERSION": {
            "name": "Sales Funnel & Conversion Rates",
            "keywords": ["convert", "conversion", "sales", "funnel", "win rate", "close rate", "lead"],
            "description": "Calculates lead funnel stages and conversion percentages by service/industry.",
        },
        "ESTIMATION_ACCURACY": {
            "name": "Estimation Variance & Accuracy",
            "keywords": ["estimate", "accuracy", "variance", "hours", "effort", "overrun", "inaccurate", "pert"],
            "description": "Measures planned effort vs actual delivery hours and variance percentage.",
        },
        "SCOPE_CHANGE_IMPACT": {
            "name": "Requirements Scope Changes",
            "keywords": ["scope", "change", "change request", "creep", "requirements", "unresolved"],
            "description": "Measures frequency and root causes of scope changes across projects.",
        },
        "QUALITY_DEFECT_LEAKAGE": {
            "name": "QA Quality & Defect Leakage",
            "keywords": ["quality", "defect", "bug", "escaped", "leakage", "qa", "uat"],
            "description": "Tracks QA pass rates, post-release defects, and test coverage.",
        },
        "AI_USAGE_COSTS": {
            "name": "AI Usage, Tokens & Financial Costs",
            "keywords": ["ai cost", "tokens", "cost", "ai usage", "model cost", "agent cost", "expensive"],
            "description": "Audits token consumption and estimated AI operational costs by agent/workflow.",
        },
        "SUPPORT_DEMAND": {
            "name": "Support Ticket Volume & SLA Performance",
            "keywords": ["support", "ticket", "sla", "warranty", "incident", "maintenance", "helpdesk"],
            "description": "Measures support volume, resolution times, and SLA adherence.",
        },
        "SERVICE_PERFORMANCE": {
            "name": "Service Portfolio Economics & Demand",
            "keywords": ["service", "portfolio", "best service", "custom software", "website", "automation", "crm"],
            "description": "Compares project volumes, duration, and demand across services.",
        },
    }

    def resolve_query_intent(self, question: str) -> Dict[str, Any]:
        """Classify user question to an approved query template."""
        question_clean = question.lower().strip()

        best_match = "SALES_CONVERSION"
        highest_score = 0

        for key, meta in self.APPROVED_METRIC_QUERIES.items():
            matches = sum(1 for kw in meta["keywords"] if kw in question_clean)
            if matches > highest_score:
                highest_score = matches
                best_match = key

        # Extract time window hint if specified
        time_window = "30d"
        if "quarter" in question_clean or "90 days" in question_clean or "3 months" in question_clean:
            time_window = "90d"
        elif "year" in question_clean or "365 days" in question_clean or "annual" in question_clean:
            time_window = "365d"
        elif "week" in question_clean or "7 days" in question_clean:
            time_window = "7d"

        return {
            "query_key": best_match,
            "query_name": self.APPROVED_METRIC_QUERIES[best_match]["name"],
            "confidence": "HIGH" if highest_score >= 2 else ("MEDIUM" if highest_score == 1 else "LOW"),
            "extracted_parameters": {
                "time_window": time_window,
            },
        }

    def format_semantic_response(
        self,
        query_meta: Dict[str, Any],
        raw_data: Any,
        summary_override: Optional[str] = None,
    ) -> SemanticQueryResult:
        """Create a factually grounded semantic query answer."""
        query_key = query_meta.get("query_key", "SALES_CONVERSION")
        query_name = query_meta.get("query_name", "Analytical Query")
        params = query_meta.get("extracted_parameters", {})

        if summary_override:
            summary = summary_override
        else:
            summary = f"Aggregated {query_name} across the specified window ({params.get('time_window', '30d')})."

        evidence_notes = [
            f"Query mapped to approved metric model: {query_key}",
            "Direct SQL execution is disabled by security policy",
            "Data derived from authoritative transactional facts",
        ]

        return SemanticQueryResult(
            query_key=query_key,
            intent=query_name,
            parameters=params,
            data=raw_data,
            summary=summary,
            evidence_notes=evidence_notes,
        )
