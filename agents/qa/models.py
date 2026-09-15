"""Pydantic schemas for Quality Assurance, UAT and Handover AI Subsystem."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TestCaseItem(BaseModel):
    """Structured test case definition."""

    code: str
    title: str
    description: Optional[str] = None
    category: str = "FUNCTIONAL"  # FUNCTIONAL, INTEGRATION, PERFORMANCE, SECURITY, REGRESSION, UAT
    priority: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW
    execution_type: str = "MANUAL"  # AUTOMATED, MANUAL, HYBRID
    preconditions: Optional[str] = None
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    expected_results: str
    is_regression: bool = True
    requirement_id: Optional[str] = None
    deliverable_id: Optional[str] = None


class TestCaseDraftResult(BaseModel):
    """Output for AI test case generation."""

    test_plan_id: str
    generated_test_cases: List[TestCaseItem] = Field(default_factory=list)
    total_count: int = 0
    confidence: float = 0.95


class DefectClassificationResult(BaseModel):
    """Output for defect classification & triage."""

    defect_id: Optional[str] = None
    title: str
    severity: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW
    priority: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW
    classification: str = "DEFECT"  # DEFECT, SCOPE_CHANGE, ENHANCEMENT, INVALID
    confidence: float = 0.90
    reasoning: str
    is_blocking_release: bool = False


class RegressionSelectionResult(BaseModel):
    """Selected regression test suite."""

    project_id: str
    selected_test_case_ids: List[str] = Field(default_factory=list)
    selection_reason: str
    total_selected: int = 0


class ReleaseReadinessEvaluationResult(BaseModel):
    """Evaluation output for release readiness gate."""

    project_id: str
    version_tag: str
    readiness_score: float = Field(ge=0.0, le=100.0)
    is_ready_for_release: bool = False
    failing_test_count: int = 0
    open_critical_defects: int = 0
    open_high_defects: int = 0
    uat_approved: bool = False
    blocking_conditions: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class HandoverChecklistDraftResult(BaseModel):
    """Draft checklist items for project handover."""

    project_id: str
    code_repository_transferred: bool = False
    documentation_delivered: bool = False
    credentials_transferred: bool = False
    training_completed: bool = False
    deployment_verified: bool = False
    verification_notes: List[str] = Field(default_factory=list)


class QASummaryResult(BaseModel):
    """Executive QA summary report."""

    project_id: str
    total_test_cases: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    pass_rate: float = 0.0
    open_defects_by_severity: Dict[str, int] = Field(default_factory=dict)
    release_recommendation: str = "HOLD"
