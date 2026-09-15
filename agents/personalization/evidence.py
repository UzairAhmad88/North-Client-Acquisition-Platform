"""Evidence collector linking personalization claims to verified evidence records."""

from typing import Any, Dict, List


class PersonalizationEvidenceCollector:
    """Collects and formats evidence items for traceability."""

    @staticmethod
    def collect_evidence(
        research_data: Dict[str, Any],
        audit_data: Dict[str, Any],
        score_data: Dict[str, Any],
        recommendations_data: List[Dict[str, Any]],
        qualification_data: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        evidence: List[Dict[str, Any]] = []

        # Audit Evidence
        findings = audit_data.get("findings", [])
        for f in findings:
            if isinstance(f, dict):
                evidence.append({
                    "id": str(f.get("id")) if f.get("id") else f"audit-{f.get('code', 'finding')}",
                    "type": "AUDIT_FINDING",
                    "title": f.get("title") or f.get("code", "Audit Finding"),
                    "description": f.get("description") or f.get("assessment", ""),
                    "severity": f.get("severity", "MEDIUM"),
                    "source": "Website Audit Engine",
                })

        # Research Evidence
        records = research_data.get("records", [])
        for r in records:
            if isinstance(r, dict):
                evidence.append({
                    "id": str(r.get("id")) if r.get("id") else f"research-{r.get('field_name', 'record')}",
                    "type": "RESEARCH_RECORD",
                    "title": r.get("field_name") or "Research Fact",
                    "description": str(r.get("fact_summary") or r.get("value", "")),
                    "confidence": r.get("confidence", "HIGH"),
                    "source": r.get("source_type", "Web Research"),
                })

        # Score Evidence
        total_score = score_data.get("total_score") or score_data.get("score")
        if total_score is not None:
            evidence.append({
                "id": "score-evidence",
                "type": "LEAD_SCORE",
                "title": "Lead Opportunity Score",
                "description": f"Deterministic score {total_score} ({score_data.get('band', 'HIGH')})",
                "source": "Deterministic Lead Scoring System",
            })

        # Qualification Evidence
        if qualification_data.get("decision"):
            evidence.append({
                "id": "qualification-evidence",
                "type": "QUALIFICATION_RESULT",
                "title": "Lead Qualification Assessment",
                "description": f"Qualification decision: {qualification_data.get('decision')}",
                "source": "Qualification Agent",
            })

        return evidence
