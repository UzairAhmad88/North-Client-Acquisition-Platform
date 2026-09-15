"""Validation & Fact Fabrication Defender for Research Agent."""

from typing import Any, Dict, List, Tuple
from agents.core.errors import AgentOutputInvalidError


class ResearchOutputValidator:
    """Validates structured research findings and prevents unsupported claim fabrication."""

    @staticmethod
    def validate_research_output(output: Dict[str, Any]) -> Dict[str, Any]:
        """Verify output schema and convert unsupported assertions to UNKNOWN or CONFLICT."""
        if not isinstance(output, dict):
            raise AgentOutputInvalidError("Research agent output must be a dictionary.")

        if "findings" not in output or not isinstance(output["findings"], list):
            output["findings"] = []

        if "conflicts" not in output or not isinstance(output["conflicts"], list):
            output["conflicts"] = []

        validated_findings: List[Dict[str, Any]] = []
        for finding in output["findings"]:
            if not isinstance(finding, dict):
                continue

            # Fact fabrication guard: if value present without evidence, mark confidence LOW or UNKNOWN
            val = finding.get("value")
            ev = finding.get("evidence", "")
            if val is not None and not ev:
                finding["confidence"] = "LOW"
                finding["evidence"] = "Unverified claim extracted from LLM without direct source text citation."

            validated_findings.append(finding)

        output["findings"] = validated_findings
        return output
