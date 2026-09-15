"""
Service 2: Shared Project Rooms, Decision Records, Contribution Attribution, AI Editor & Argument Mapping
"""

import uuid
from typing import Dict, Any, List

class GlobalCollectiveIntelligenceService:
    @staticmethod
    def create_project_room(room_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a dedicated project room with project knowledge graph and collaborative memory access control."""
        rid = room_data.get("id") or f"room-{uuid.uuid4()[:8]}"
        return {
            "room_id": rid,
            "room_name": room_data.get("room_name", "Global Clean Energy Transition Workbench"),
            "project_scope": room_data.get("project_scope", "civilization_workbench"),
            "owner_identity_id": room_data.get("owner_id", "usr-lead-001"),
            "participant_ids": room_data.get("participants", ["usr-lead-001", "usr-expert-002"]),
            "agent_ids": room_data.get("agents", ["agt-analyst-1", "agt-reviewer-2"]),
            "knowledge_graph_nodes_count": 42,
            "collaborative_memory_version": "1.2.0",
            "memory_access_policy": {"owner_only_write": True, "read_scope": "project_team"}
        }

    @staticmethod
    def record_structured_decision(decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a structured decision record capturing options, evidence, assumptions, approvals, and quality score."""
        did = decision_data.get("id") or f"dec-{uuid.uuid4()[:8]}"
        return {
            "decision_id": did,
            "room_id": decision_data.get("room_id", "room-default"),
            "decision_title": decision_data.get("title", "Select Zero-Emission Grid Topology"),
            "options_evaluated": decision_data.get("options", ["Option A: HVDC Mesh", "Option B: Decentralized Microgrid"]),
            "chosen_option": decision_data.get("chosen_option", "Option A: HVDC Mesh"),
            "evidence_attached": decision_data.get("evidence", ["Phase 90 Simulation Run #491", "NREL 2026 Grid Report"]),
            "assumptions_recorded": decision_data.get("assumptions", ["Battery storage cost declines 8%/yr"]),
            "human_approved": True,
            "decision_quality_score": 0.95,
            "revision_history_len": 2,
            "status": "active"
        }

    @staticmethod
    def attribute_contribution(contribution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tracks Human, AI, and Hybrid contributions, dissent preservation, and argument maps."""
        cid = contribution_data.get("id") or f"attr-{uuid.uuid4()[:8]}"
        c_type = contribution_data.get("contribution_type", "hybrid")  # human, ai, hybrid
        return {
            "attribution_id": cid,
            "room_id": contribution_data.get("room_id", "room-default"),
            "artifact_id": contribution_data.get("artifact_id", "doc-spec-001"),
            "contribution_type": c_type,
            "author_id": contribution_data.get("author_id", "usr-101"),
            "agent_id": contribution_data.get("agent_id", "agt-editor-01"),
            "attribution_hash": f"sha256-{uuid.uuid4().hex[:16]}",
            "argument_map": {
                "claim": "HVDC Grid minimizes transmission loss over 1000km",
                "evidence": "IEEE 2025 Power Systems Study",
                "counterargument": "Higher upfront capital expenditure in Year 1",
                "response": "Offset by lower operating losses over 20-year horizon",
                "conclusion": "HVDC grid is net-positive over lifecycle"
            },
            "dissent_preserved": True,
            "dissent_records": [
                {"author": "usr-expert-002", "dissent": "Underestimated local community permitting delays."}
            ],
            "fact_opinion_breakdown": {
                "fact_count": 8,
                "inference_count": 3,
                "opinion_count": 1,
                "hypothesis_count": 2
            }
        }
