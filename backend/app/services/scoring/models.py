from typing import Any, Dict, List, Optional

from app.models.audit import BusinessAudit
from app.models.business import Business
from app.models.lead import Lead
from app.models.research import ResearchRecord
from app.models.service import Service


class ComponentScoreResult:
    def __init__(
        self,
        component: str,
        score: float,  # 0 to 100
        weight: float,  # e.g., 0.25
        reasons: List[str],
        evidence: List[str],
        status: str = "SCORED",  # "SCORED", "UNKNOWN", "NOT_APPLICABLE"
    ):
        self.component = component
        self.score = round(max(0.0, min(100.0, score)), 1)
        self.weight = weight
        self.weighted_contribution = round(self.score * self.weight, 2)
        self.reasons = reasons
        self.evidence = evidence
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "score": self.score,
            "weight": self.weight,
            "weighted_contribution": self.weighted_contribution,
            "reasons": self.reasons,
            "evidence": self.evidence,
            "status": self.status,
        }


class ScoringContext:
    def __init__(
        self,
        business: Business,
        lead: Optional[Lead] = None,
        audit: Optional[BusinessAudit] = None,
        research_records: Optional[List[ResearchRecord]] = None,
        available_services: Optional[List[Service]] = None,
    ):
        self.business = business
        self.lead = lead
        self.audit = audit
        self.research_records = research_records or []
        self.available_services = available_services or []


class LeadScoreResult:
    def __init__(
        self,
        score_version: str,
        total_score: float,  # 0 to 100
        band: str,  # "HIGH", "MEDIUM", "LOW", "VERY_LOW"
        component_scores: Dict[str, ComponentScoreResult],
        explanation: str,
        evidence: Dict[str, Any],
        confidence: str,  # "HIGH", "MEDIUM", "LOW"
    ):
        self.score_version = score_version
        self.total_score = round(max(0.0, min(100.0, total_score)), 1)
        self.band = band
        self.component_scores = component_scores
        self.explanation = explanation
        self.evidence = evidence
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score_version": self.score_version,
            "total_score": self.total_score,
            "band": self.band,
            "component_scores": {
                k: v.to_dict() for k, v in self.component_scores.items()
            },
            "explanation": self.explanation,
            "evidence": self.evidence,
            "confidence": self.confidence,
        }
