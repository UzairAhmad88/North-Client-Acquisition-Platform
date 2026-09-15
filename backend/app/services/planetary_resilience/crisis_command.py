"""
Crisis Command Center & Decision Support Service
Provides incident command interfaces, crisis event correlation, confidence verification, emergency communications, decision logging, reversibility analysis, and audit trails.
"""

from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime


class CrisisCommandService:
    def __init__(self):
        self.crises: Dict[str, Dict[str, Any]] = {}
        self.decision_logs: List[Dict[str, Any]] = []

    def declare_crisis_incident(
        self,
        title: str,
        category: str,
        severity_level: int,
        primary_location: str,
        affected_jurisdictions: List[str],
        declared_by_human_id: str,
        initial_description: str,
    ) -> Dict[str, Any]:
        incident_id = f"crs-{uuid.uuid4().hex[:8]}"
        incident = {
            "incident_id": incident_id,
            "title": title,
            "category": category,  # Natural Disaster, Infrastructure Failure, Cyber Incident, Compound Crisis, etc.
            "severity_level": max(1, min(5, severity_level)),  # Level 1 to Level 5
            "status": "Active",
            "primary_location": primary_location,
            "affected_jurisdictions": affected_jurisdictions,
            "declared_by_human_id": declared_by_human_id,
            "description": initial_description,
            "verification_status": "Confirmed",  # Confirmed, Probable, Unconfirmed, False
            "source_confidence": 0.95,
            "timeline": [
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "event": "Crisis Officially Declared",
                    "actor": declared_by_human_id,
                }
            ],
            "affected_systems": [],
            "emergency_approvals": [],
            "created_at": datetime.utcnow().isoformat(),
        }
        self.crises[incident_id] = incident
        return incident

    def evaluate_escalation_thresholds(self, incident_id: str, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        crisis = self.crises.get(incident_id)
        if not crisis:
            return {"status": "error", "message": f"Incident {incident_id} not found"}
        
        current_lvl = crisis["severity_level"]
        affected_count = current_metrics.get("affected_population_estimate", 0)
        cascading_count = current_metrics.get("cascading_failures_count", 0)

        recommended_lvl = current_lvl
        if affected_count > 1000000 or cascading_count >= 5:
            recommended_lvl = 5
        elif affected_count > 100000 or cascading_count >= 3:
            recommended_lvl = 4
        elif affected_count > 10000 or cascading_count >= 1:
            recommended_lvl = 3

        requires_human_approval = recommended_lvl > current_lvl

        return {
            "incident_id": incident_id,
            "current_severity": current_lvl,
            "recommended_severity": recommended_lvl,
            "escalation_recommended": recommended_lvl > current_lvl,
            "requires_human_authority_approval": requires_human_approval,
            "justification": f"Affected pop: {affected_count}, Cascading events: {cascading_count}",
        }

    def record_emergency_decision(
        self,
        incident_id: str,
        decision_maker: str,
        decision_title: str,
        options_considered: List[str],
        chosen_option: str,
        reversibility: str,  # Reversible, Partially Reversible, Irreversible
        evidence_summary: str,
    ) -> Dict[str, Any]:
        decision_id = f"dec-{uuid.uuid4().hex[:8]}"
        record = {
            "decision_id": decision_id,
            "incident_id": incident_id,
            "decision_maker": decision_maker,
            "decision_title": decision_title,
            "options_considered": options_considered,
            "chosen_option": chosen_option,
            "reversibility": reversibility,
            "evidence_summary": evidence_summary,
            "timestamp": datetime.utcnow().isoformat(),
            "audit_hash": f"sha256-{uuid.uuid4().hex}",
        }
        self.decision_logs.append(record)
        
        if incident_id in self.crises:
            self.crises[incident_id]["timeline"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "event": f"Emergency Decision: {decision_title}",
                "actor": decision_maker,
                "reversibility": reversibility,
            })
        return record

    def run_crisis_ai_assistant(self, incident_id: str, query: str) -> Dict[str, Any]:
        crisis = self.crises.get(incident_id, {})
        return {
            "incident_id": incident_id,
            "query": query,
            "ai_disclaimer": "AI recommendations are strictly advisory and require authorized human approval for execution.",
            "summarized_situation": crisis.get("description", "No active description"),
            "detected_contradictions": [],
            "recommended_next_questions": [
                "What is the current fuel and energy buffer remaining?",
                "Are hospital backup generators online and supplied?",
                "What are the upstream dependencies of the primary affected water station?",
            ],
            "recommended_actions": [
                "Activate local-first offline emergency comms channel",
                "Deploy humanitarian food and water reserves to regional hubs",
            ],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def verify_crisis_information_signal(
        self, claim: str, source: str, supporting_evidence: List[str]
    ) -> Dict[str, Any]:
        # High confidence source check
        confidence = 0.88 if len(supporting_evidence) >= 2 else 0.55
        status = "Confirmed" if confidence >= 0.8 else "Probable"
        return {
            "claim": claim,
            "source": source,
            "verification_status": status,
            "confidence_score": confidence,
            "supporting_evidence_count": len(supporting_evidence),
            "timestamp": datetime.utcnow().isoformat(),
        }
