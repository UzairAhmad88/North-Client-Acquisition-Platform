"""Pydantic Models for Learning and BI Agent Subsystem."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class InsightDraft(BaseModel):
    title: str = Field(..., description="Clear title summarizing the discovered empirical pattern")
    description: str = Field(..., description="Detailed explanation of the pattern, context, and cause")
    category: str = Field(..., description="Category: SALES, ESTIMATION, DELIVERY, QUALITY, SUPPORT, AI, OPERATIONS, FINANCE")
    confidence: str = Field(default="MEDIUM", description="Confidence level: HIGH, MEDIUM, LOW, INSUFFICIENT_DATA")
    sample_size: int = Field(default=0, description="Total entities analyzed")
    time_window: str = Field(default="30d", description="Analyzed period")
    affected_entities: Dict[str, Any] = Field(default_factory=dict, description="Affected services, industries, or components")
    recommended_action: Optional[str] = Field(None, description="Actionable recommendation for human consideration")
    evidence_items: List[Dict[str, Any]] = Field(default_factory=list, description="Audit-proof supporting evidence records")


class RecommendationDraft(BaseModel):
    title: str = Field(..., description="Recommendation headline")
    recommendation: str = Field(..., description="Specific proposed process, discovery, or operational adjustment")
    reason: str = Field(..., description="Empirical rationale based on insight evidence")
    expected_benefit: str = Field(..., description="Anticipated business/operational improvement")
    potential_downside: str = Field(..., description="Risks, costs, or tradeoffs of adopting the recommendation")
    confidence: str = Field(default="MEDIUM", description="Confidence: HIGH, MEDIUM, LOW, INSUFFICIENT_DATA")
    affected_workflow: str = Field(..., description="Target workflow (ESTIMATION, REQUIREMENTS, OUTREACH, SUPPORT, QA)")


class ExperimentDraft(BaseModel):
    title: str = Field(..., description="Experiment title")
    hypothesis: str = Field(..., description="Formal If-Then experimental hypothesis")
    target_workflow: str = Field(..., description="Workflow being experimented on")
    target_metric: str = Field(..., description="Target metric key")
    baseline_value: float = Field(default=0.0, description="Current baseline performance metric")
    target_value: float = Field(default=0.0, description="Desired metric target")
    sample_target: int = Field(default=10, description="Target number of projects/leads to test before concluding")


class SemanticQueryRequest(BaseModel):
    natural_language_query: str = Field(..., description="User's natural language question")
    context_filters: Dict[str, Any] = Field(default_factory=dict, description="Optional tenant or date range filters")


class SemanticQueryResult(BaseModel):
    query_key: str = Field(..., description="Approved metric/query identifier executed")
    intent: str = Field(..., description="Interpreted user intent")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Validated parameters passed to query engine")
    data: Any = Field(default=None, description="Aggregated factual query results")
    summary: str = Field(..., description="Factually grounded summary answering the user query")
    evidence_notes: List[str] = Field(default_factory=list, description="Caveats, sample size, or data freshness notes")
