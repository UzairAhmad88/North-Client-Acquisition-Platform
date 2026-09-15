"""
Vendor Risk Management & Third-Party Dependency Mapping Engine (Section 35-37).
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from backend.app.governance.base import (
    VendorCriticality,
)


class VendorProfile(BaseModel):
    vendor_code: str
    name: str
    service_provided: str
    criticality: VendorCriticality = VendorCriticality.MEDIUM
    data_access_level: str = "INTERNAL"
    security_risk: str = "LOW"
    privacy_risk: str = "LOW"
    owner_id: str
    status: str = "ACTIVE"
    dependent_services: List[str] = Field(default_factory=list)


class VendorRiskAssessment(BaseModel):
    assessment_id: str
    vendor_code: str
    assessor_id: str
    score: float = 85.0
    findings: List[str] = Field(default_factory=list)
    recommendation: str = "APPROVE"  # APPROVE, CONDITIONALLY_APPROVE, REJECT
    assessed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    next_review_due: datetime


class VendorRiskManager:
    """Manages third-party vendor risk profiles, compliance reviews, and service blast-radius mapping."""

    def __init__(self):
        self._vendors: Dict[str, VendorProfile] = {}
        self._assessments: List[VendorRiskAssessment] = []
        self._seed_default_vendors()

    def _seed_default_vendors(self) -> None:
        """Seeds critical platform third-party dependencies."""
        self.register_vendor(VendorProfile(
            vendor_code="VND_ANTHROPIC",
            name="Anthropic PBC",
            service_provided="Claude LLM Inference APIs",
            criticality=VendorCriticality.CRITICAL,
            data_access_level="RESTRICTED",
            security_risk="LOW",
            privacy_risk="MEDIUM",
            owner_id="ai_lead",
            dependent_services=["PersonalizationAgent", "ResearchAgent", "SolutionAgent"]
        ))

        self.register_vendor(VendorProfile(
            vendor_code="VND_SENDGRID",
            name="Twilio SendGrid",
            service_provided="Transactional Email & Inbound Processing",
            criticality=VendorCriticality.HIGH,
            data_access_level="CONFIDENTIAL",
            security_risk="LOW",
            privacy_risk="LOW",
            owner_id="comms_lead",
            dependent_services=["OutreachGateway", "NotificationService"]
        ))

        self.register_vendor(VendorProfile(
            vendor_code="VND_STRIPE",
            name="Stripe Payments UK",
            service_provided="Payment Gateway & Invoicing Processing",
            criticality=VendorCriticality.CRITICAL,
            data_access_level="RESTRICTED",
            security_risk="LOW",
            privacy_risk="LOW",
            owner_id="finance_lead",
            dependent_services=["BillingService", "CheckoutWorkflow"]
        ))

    def register_vendor(self, vendor: VendorProfile) -> None:
        if not vendor.owner_id:
            raise ValueError("All third-party vendors must have an internal owner assigned.")
        self._vendors[vendor.vendor_code] = vendor

    def get_vendor(self, vendor_code: str) -> Optional[VendorProfile]:
        return self._vendors.get(vendor_code)

    def list_vendors(self, criticality: Optional[VendorCriticality] = None) -> List[VendorProfile]:
        vendors = list(self._vendors.values())
        if criticality:
            vendors = [v for v in vendors if v.criticality == criticality]
        return vendors

    def record_assessment(
        self,
        assessment_id: str,
        vendor_code: str,
        assessor_id: str,
        score: float,
        findings: List[str],
        recommendation: str = "APPROVE"
    ) -> VendorRiskAssessment:
        """Records a periodic security and privacy assessment for a vendor."""
        if vendor_code not in self._vendors:
            raise KeyError(f"Vendor '{vendor_code}' not found.")

        now = datetime.now(timezone.utc)
        assessment = VendorRiskAssessment(
            assessment_id=assessment_id,
            vendor_code=vendor_code,
            assessor_id=assessor_id,
            score=score,
            findings=findings,
            recommendation=recommendation,
            assessed_at=now,
            next_review_due=now + timedelta(days=365)
        )
        self._assessments.append(assessment)
        return assessment

    def get_dependent_blast_radius(self, vendor_code: str) -> List[str]:
        """Calculates service and workflow blast radius in the event of vendor outage or compromise."""
        vendor = self.get_vendor(vendor_code)
        if not vendor:
            return []
        return vendor.dependent_services
