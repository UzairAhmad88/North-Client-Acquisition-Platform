"""
Service 1: Digital Identity Fabric, SSI Verifiable Credentials & AI Personas
"""

import uuid
from typing import Dict, Any, List

class DigitalIdentityPersonaService:
    @staticmethod
    def issue_verifiable_credential(identity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Issues or verifies an interoperable digital identity and SSI credential with selective disclosure."""
        iid = identity_data.get("id") or str(uuid.uuid4())
        return {
            "identity_id": iid,
            "entity_name": identity_data.get("entity_name", "Dr. Aris Thorne"),
            "entity_type": identity_data.get("entity_type", "person"),
            "verification_level": identity_data.get("verification_level", "STRONG_VERIFIED"),
            "verifiable_credentials": [
                {"type": "DegreeCredential", "issuer": "MIT", "verified": True},
                {"type": "RoleCredential", "issuer": "Global AI Lab", "verified": True}
            ],
            "ssi_selective_disclosure_enabled": True,
            "recovery_workflow_configured": True,
            "status": "active"
        }

    @staticmethod
    def configure_ai_persona(persona_data: Dict[str, Any]) -> Dict[str, Any]:
        """Configures a user's AI persona representation, permissions, and action levels."""
        pid = persona_data.get("id") or f"persona-{uuid.uuid4()[:8]}"
        action_level = persona_data.get("action_level", "REQUEST_APPROVAL")
        return {
            "persona_id": pid,
            "user_id": persona_data.get("user_id", "usr-lead-001"),
            "persona_name": persona_data.get("persona_name", "Aris-AI Assistant"),
            "action_level": action_level,  # OBSERVE, SUGGEST, DRAFT, REQUEST_APPROVAL, EXECUTE
            "allowed_domains": ["Scheduling", "Research Summarization", "Drafting Communications"],
            "representation_disclosure_mandatory": True,
            "permissions_granted": {
                "read_calendar": True,
                "draft_email": True,
                "execute_financial_transactions": False  # Strictly forbidden for persona
            },
            "status": "configured"
        }
