"""
Pydantic Schemas for Phase 54 — Unified Autonomous Research, Intelligence & Continuous Discovery Engine.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ResearchWorkspaceCreateRequest(BaseModel):
    title: str = Field(..., description="Research workspace title")
    research_question: str = Field(..., description="Core business research question")
    owner_id: str = Field(default="lead_analyst")
    research_type: str = Field(default="MARKET", description="MARKET, COMPETITIVE, TECHNOLOGY, AI, SECURITY, REGULATORY")
    objective: Optional[str] = None
    scope: Optional[Dict[str, Any]] = None


class DecomposeQuestionRequest(BaseModel):
    subquestions: Optional[List[str]] = None


class RegisterSourceRequest(BaseModel):
    url_or_reference: str = Field(...)
    source_type: str = Field(default="SECONDARY")
    publisher: Optional[str] = None
    author: Optional[str] = None
    authority_score: float = Field(default=0.75, ge=0.0, le=1.0)
    freshness: str = Field(default="CURRENT")


class ExtractFactRequest(BaseModel):
    claim: str = Field(...)
    source_id: Optional[str] = None
    value_extracted: Optional[str] = None
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    provenance: Optional[str] = None


class VerifyClaimRequest(BaseModel):
    claim_text: str = Field(...)
    supporting_sources: Optional[List[str]] = None
    contradicting_sources: Optional[List[str]] = None


class SurfaceConflictRequest(BaseModel):
    topic: str = Field(...)
    source_a_id: str = Field(...)
    claim_a: str = Field(...)
    source_b_id: str = Field(...)
    claim_b: str = Field(...)
    possible_explanation: Optional[str] = None


class UpsertCompetitorRequest(BaseModel):
    company_name: str = Field(...)
    market_position: str = Field(default="CHALLENGER")
    products_offered: Optional[List[str]] = None
    pricing_signals: Optional[Dict[str, Any]] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    recent_changes: Optional[List[str]] = None


class CreateMonitoringRuleRequest(BaseModel):
    target_entity: str = Field(...)
    watch_frequency: str = Field(default="DAILY")
    topics_monitored: Optional[List[str]] = None
    alert_significance_threshold: str = Field(default="MEDIUM")


class GenerateSynthesisRequest(BaseModel):
    executive_summary: str = Field(...)
    key_findings: Optional[List[str]] = None
    strategic_implications: Optional[List[str]] = None
    recommended_actions: Optional[List[str]] = None
    uncertainties_and_limitations: Optional[List[str]] = None


class GenerateReportRequest(BaseModel):
    title: str = Field(...)
    report_markdown: str = Field(...)
    citations: Optional[List[str]] = None
    confidence_rating: str = Field(default="HIGH")


class CopilotQueryRequest(BaseModel):
    workspace_id: str = Field(...)
    query: str = Field(...)
