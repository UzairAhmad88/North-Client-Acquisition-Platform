"""Defect Classifier Engine for severity, priority and defect vs scope-change classification."""

from typing import Optional
from agents.qa.models import DefectClassificationResult


class DefectClassifierEngine:
    """Classifies reported issues, determines severity/priority, and detects if issue is a true defect or scope change."""

    def classify_defect(
        self,
        defect_id: Optional[str],
        title: str,
        description: str,
        is_against_baseline_spec: bool = True,
    ) -> DefectClassificationResult:
        """Analyze defect description and classify its severity, priority, and type."""
        title_lower = title.lower()
        desc_lower = description.lower()

        # Check if issue requests new functionality (Scope Change vs Defect)
        if not is_against_baseline_spec or any(kw in desc_lower for kw in ["new feature", "add support for", "change requirement", "out of scope", "also need"]):
            return DefectClassificationResult(
                defect_id=defect_id,
                title=title,
                severity="LOW",
                priority="LOW",
                classification="SCOPE_CHANGE",
                confidence=0.92,
                reasoning="The reported item describes a new or modified feature request outside the approved contract baseline specification. Classified as SCOPE_CHANGE.",
                is_blocking_release=False,
            )

        # Determine severity & blocking condition
        if any(kw in title_lower or kw in desc_lower for kw in ["crash", "data loss", "security vulnerability", "down", "unusable", "fatal"]):
            severity = "CRITICAL"
            priority = "CRITICAL"
            is_blocking = True
            reasoning = "Critical security vulnerability or severe system failure identified. Blocks release readiness."
        elif any(kw in title_lower or kw in desc_lower for kw in ["error", "failure", "broken", "incorrect calculation", "fails", "cannot"]):
            severity = "HIGH"
            priority = "HIGH"
            is_blocking = True
            reasoning = "High severity functional defect causing feature failure in main flow."
        elif any(kw in title_lower or kw in desc_lower for kw in ["slow", "alignment", "typo", "minor", "ui"]):
            severity = "LOW"
            priority = "LOW"
            is_blocking = False
            reasoning = "Cosmetic UI or minor performance degradation."
        else:
            severity = "MEDIUM"
            priority = "MEDIUM"
            is_blocking = False
            reasoning = "Standard functional defect affecting non-critical workflow."

        return DefectClassificationResult(
            defect_id=defect_id,
            title=title,
            severity=severity,
            priority=priority,
            classification="DEFECT",
            confidence=0.88,
            reasoning=reasoning,
            is_blocking_release=is_blocking,
        )
