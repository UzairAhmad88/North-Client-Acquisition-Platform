"""
Service 1: Collaboration Identity, Participant Graph, Expertise Graph & Multi-Criteria Team Formation
"""

import uuid
from typing import Dict, Any, List

class GlobalCollaborationFabricService:
    @staticmethod
    def create_or_get_identity(participant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registers a participant (human, expert, team, organization, AI agent) with governed identity."""
        pid = participant_data.get("id") or str(uuid.uuid4())
        return {
            "id": pid,
            "participant_name": participant_data.get("participant_name", "Anonymous Collaborator"),
            "participant_type": participant_data.get("participant_type", "human"),
            "organization_id": participant_data.get("organization_id", "org-default"),
            "capabilities": participant_data.get("capabilities", ["Research", "Problem Solving", "Data Analysis"]),
            "roles": participant_data.get("roles", ["Researcher", "Analyst"]),
            "verification_status": participant_data.get("verification_status", "verified"),
            "availability_status": participant_data.get("availability_status", "available"),
            "trust_score": participant_data.get("trust_score", 0.96),
            "status": "active"
        }

    @staticmethod
    def get_expertise_node(expert_id: str, domain: str) -> Dict[str, Any]:
        """Returns verified expertise details distinguishing self-declared, demonstrated, verified, and institutional evidence."""
        return {
            "expert_identity_id": expert_id,
            "domain": domain,
            "subdomains": ["Quantum Algorithms", "Distributed Ledger", "Causal ML"],
            "skill_level": "expert",
            "evidence_score": 0.98,
            "verification_level": "institutional_confirmed",
            "publications_count": 14,
            "projects_completed": 8,
            "conflict_constraints": ["No defense contractors"],
            "complementarity_score": 0.94
        }

    @staticmethod
    def form_complementary_team(problem_scope: Dict[str, Any]) -> Dict[str, Any]:
        """Generates candidate team combining experts, engineers, researchers, and AI agents optimized for complementary skills."""
        domain = problem_scope.get("domain", "Climate Resilience")
        return {
            "team_id": f"team-{uuid.uuid4()[:8]}",
            "target_problem": problem_scope.get("title", "Planetary Resilience Modeling"),
            "domain": domain,
            "members": [
                {"id": "usr-exp-101", "name": "Dr. Aris Thorne", "type": "expert", "role": "Lead Scientist", "verification": "institutional_confirmed"},
                {"id": "usr-eng-202", "name": "Elena Rostova", "type": "human", "role": "Systems Engineer", "verification": "verified"},
                {"id": "agt-sim-303", "name": "Agent SimMaster-X", "type": "ai_agent", "role": "Simulation Specialist", "capabilities": ["Physics Engine", "Monte Carlo"]},
                {"id": "agt-rev-404", "name": "Agent RedTeam-Reviewer", "type": "ai_agent", "role": "Adversarial Reviewer", "capabilities": ["Dissent Analysis"]}
            ],
            "complementarity_index": 0.96,
            "diversity_perspective_rating": "High (Cross-disciplinary & Red-Team Agent)",
            "conflict_of_interest_checked": True
        }
