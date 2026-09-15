"""
Research Synthesis, Report Generator, and Research Gap Analysis.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional


class SynthesisReportManager:
    """Synthesizes validated findings into structured reports with verifiable citations and gap tracking."""

    def __init__(self):
        self._syntheses: Dict[str, Dict[str, Any]] = {}
        self._reports: Dict[str, List[Dict[str, Any]]] = {}
        self._gaps: Dict[str, List[Dict[str, Any]]] = {}

    def generate_synthesis(
        self,
        workspace_id: str,
        executive_summary: str,
        key_findings: Optional[List[str]] = None,
        strategic_implications: Optional[List[str]] = None,
        recommended_actions: Optional[List[str]] = None,
        uncertainties_and_limitations: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Synthesize facts, claims, and verified findings into actionable conclusions."""
        synth = {
            "id": f"syn_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "executive_summary": executive_summary,
            "key_findings": key_findings or [],
            "strategic_implications": strategic_implications or [],
            "recommended_actions": recommended_actions or [],
            "uncertainties_and_limitations": uncertainties_and_limitations or [],
            "synthesized_at": datetime.utcnow().isoformat(),
        }
        self._syntheses[workspace_id] = synth
        return synth

    def get_synthesis(self, workspace_id: str) -> Optional[Dict[str, Any]]:
        return self._syntheses.get(workspace_id)

    def generate_report(
        self,
        workspace_id: str,
        title: str,
        report_markdown: str,
        citations: Optional[List[str]] = None,
        confidence_rating: str = "HIGH",
    ) -> Dict[str, Any]:
        """Generate structured markdown report with citations."""
        report = {
            "id": f"rep_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "title": title,
            "report_markdown": report_markdown,
            "citations": citations or [],
            "confidence_rating": confidence_rating,
            "generated_at": datetime.utcnow().isoformat(),
        }
        self._reports.setdefault(workspace_id, []).append(report)
        return report

    def list_reports(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._reports.get(workspace_id, [])

    def record_research_gap(
        self,
        workspace_id: str,
        gap_description: str,
        importance: str = "MEDIUM",
        recommended_investigation: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Identify unanswered question or missing source data."""
        gap = {
            "id": f"gap_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "gap_description": gap_description,
            "importance": importance,
            "recommended_investigation": recommended_investigation or "Schedule primary customer interview or field testing.",
        }
        self._gaps.setdefault(workspace_id, []).append(gap)
        return gap

    def list_gaps(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._gaps.get(workspace_id, [])
