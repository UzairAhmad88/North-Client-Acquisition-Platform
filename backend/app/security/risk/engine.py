"""
Security Risk Engine and Multi-Dimensional Risk Heatmap (Section 16 & 35).
Computes versioned deterministic risk assessments and domain breakdowns.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

try:
    from app.security.base import (
        SecurityAlert,
        SecurityEvent,
        RiskAssessment,
        SecuritySeverity,
    )
except ImportError:
    from backend.app.security.base import (
        SecurityAlert,
        SecurityEvent,
        RiskAssessment,
        SecuritySeverity,
    )


class SecurityRiskEngine:
    """
    Evaluates enterprise security risk across 6 critical operational domains:
    Identity, AI/Agents, Data Access, Configuration, Integrations, and Finance.
    Implements versioned formula:
    Risk = min(100, Likelihood * Impact * EvidenceStrength * BlastRadiusFactor)
    """

    POLICY_VERSION = "1.0"

    @classmethod
    def calculate_detection_risk(
        cls,
        likelihood: float,  # 0.0 to 1.0
        impact: float,      # 0.0 to 1.0
        evidence_strength: float = 0.8,  # 0.0 to 1.0
        blast_radius_factor: float = 1.0  # 1.0 to 2.0
    ) -> float:
        """Calculates a deterministic risk score between 0.0 and 100.0."""
        raw_score = (likelihood * impact * evidence_strength * blast_radius_factor) * 100.0
        return round(min(100.0, max(0.0, raw_score)), 2)

    @classmethod
    def score_to_severity(cls, score: float) -> SecuritySeverity:
        if score >= 85.0:
            return SecuritySeverity.CRITICAL
        elif score >= 70.0:
            return SecuritySeverity.HIGH
        elif score >= 40.0:
            return SecuritySeverity.MEDIUM
        elif score >= 20.0:
            return SecuritySeverity.LOW
        return SecuritySeverity.INFO

    @classmethod
    def assess_tenant_posture(
        cls,
        tenant_id: str,
        alerts: List[SecurityAlert],
        events: Optional[List[SecurityEvent]] = None
    ) -> RiskAssessment:
        """
        Synthesizes active security alerts into a holistic multi-domain risk assessment and heatmap.
        """
        domain_risks = {
            "identity": 0.0,
            "ai": 0.0,
            "data": 0.0,
            "config": 0.0,
            "integration": 0.0,
            "financial": 0.0
        }

        # Weighting factors for domain severity
        for alert in alerts:
            score = alert.risk_score
            atype = alert.anomaly_type.value if hasattr(alert.anomaly_type, "value") else str(alert.anomaly_type)

            if atype in ("brute_force", "credential_stuffing", "impossible_travel", "token_leak"):
                domain_risks["identity"] = max(domain_risks["identity"], score)
            elif atype in ("agent_prompt_injection", "agent_tool_hijack", "agent_runaway_spend"):
                domain_risks["ai"] = max(domain_risks["ai"], score)
            elif atype in ("data_exfiltration", "unauthorized_resource_access", "cross_tenant_violation"):
                domain_risks["data"] = max(domain_risks["data"], score)
            elif atype in ("privilege_escalation", "sensitive_config_tampering"):
                domain_risks["config"] = max(domain_risks["config"], score)
            elif "api" in atype:
                domain_risks["integration"] = max(domain_risks["integration"], score)
            elif "finan" in atype:
                domain_risks["financial"] = max(domain_risks["financial"], score)

        # Calculate composite risk: Weighted average with highest domain penalty
        weights = {
            "identity": 0.25,
            "ai": 0.20,
            "data": 0.25,
            "config": 0.15,
            "integration": 0.10,
            "financial": 0.05
        }
        weighted_sum = sum(domain_risks[k] * weights[k] for k in weights)
        max_domain = max(domain_risks.values()) if domain_risks else 0.0
        composite = min(100.0, (weighted_sum * 0.6) + (max_domain * 0.4))

        return RiskAssessment(
            assessment_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            composite_risk_score=round(composite, 2),
            overall_severity=cls.score_to_severity(composite),
            identity_risk=round(domain_risks["identity"], 2),
            ai_risk=round(domain_risks["ai"], 2),
            data_risk=round(domain_risks["data"], 2),
            config_risk=round(domain_risks["config"], 2),
            integration_risk=round(domain_risks["integration"], 2),
            financial_risk=round(domain_risks["financial"], 2),
            policy_version=cls.POLICY_VERSION,
            assessed_at=datetime.now(timezone.utc)
        )

    @classmethod
    def generate_risk_heatmap(cls, assessment: RiskAssessment) -> List[Dict[str, Any]]:
        """Produces heatmap matrix for frontend visualization (Section 35)."""
        domains = [
            {"domain": "Identity", "score": assessment.identity_risk, "category": "Authentication & Credentials"},
            {"domain": "AI & Agents", "score": assessment.ai_risk, "category": "Prompt Injection & Tool Security"},
            {"domain": "Data Access", "score": assessment.data_risk, "category": "Exfiltration & Cross-Tenant"},
            {"domain": "Configuration", "score": assessment.config_risk, "category": "Privilege & Policy Drift"},
            {"domain": "Integrations", "score": assessment.integration_risk, "category": "API Keys & Provider Abuse"},
            {"domain": "Financial", "score": assessment.financial_risk, "category": "Payments & Transaction Fraud"},
        ]

        heatmap = []
        for d in domains:
            score = d["score"]
            sev = cls.score_to_severity(score)
            prob = "High" if score >= 70 else ("Medium" if score >= 40 else "Low")
            heatmap.append({
                "domain": d["domain"],
                "category": d["category"],
                "risk_score": score,
                "severity": sev.value,
                "probability": prob,
                "exposure": "Critical" if score >= 80 else ("High" if score >= 60 else "Normal"),
                "control_strength": "Robust" if score < 40 else ("Adequate" if score < 75 else "Degraded")
            })
        return heatmap
