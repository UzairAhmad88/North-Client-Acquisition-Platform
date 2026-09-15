"""State and classification schemas for Response Agent."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ExtractedRequirement(BaseModel):
    category: str
    item: str
    is_explicit: bool = True
    source_message_id: Optional[str] = None


class BuyingSignalDetail(BaseModel):
    level: str = Field(description="Signal level: STRONG, MODERATE, WEAK, NONE")
    signals: List[str] = Field(default_factory=list)


class DetectedObjection(BaseModel):
    type: str = Field(description="Type: PRICE, TIMING, TRUST, NEED, ALREADY_HAVE_PROVIDER, NO_BUDGET, AUTHORITY, TECHNICAL_CONCERN")
    confidence: str = Field(default="HIGH")
    detail: Optional[str] = None


class ResponseAnalysisResult(BaseModel):
    primary_intent: str
    all_intents: List[str] = Field(default_factory=list)
    intent_confidence: str = "HIGH"
    buying_signal: BuyingSignalDetail = Field(default_factory=BuyingSignalDetail)
    objection: Optional[DetectedObjection] = None
    extracted_requirements: List[ExtractedRequirement] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    conversation_stage: str = "NEW_RESPONSE"
    recommended_next_action: str = "REPLY_WITH_DETAILS"
    recommended_next_action_reason: str = "Client requested information"
    next_action_confidence: str = "HIGH"
    sentiment_signal: str = "NEUTRAL"
    priority: str = "NORMAL"
    draft_body: Optional[str] = None
    draft_subject: Optional[str] = None
