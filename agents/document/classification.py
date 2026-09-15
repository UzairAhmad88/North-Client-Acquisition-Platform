"""Document AI classification and tagging engine."""

from typing import Any, Dict, List, Optional


class DocumentAIClassifier:
    """Classifies documents into canonical business categories."""

    def classify_document(self, filename: str, content: str) -> Dict[str, Any]:
        lower_content = (filename + " " + content).lower()

        if any(w in lower_content for w in ["proposal", "commercial offer", "pricing table", "scope of work"]):
            classification = "PROPOSAL"
            confidence = 0.94
        elif any(w in lower_content for w in ["contract", "agreement", "master services", "terms and conditions"]):
            classification = "CONTRACT"
            confidence = 0.96
        elif any(w in lower_content for w in ["requirement", "user story", "acceptance criteria", "specification"]):
            classification = "REQUIREMENTS"
            confidence = 0.91
        elif any(w in lower_content for w in ["test plan", "test run", "defect", "qa report", "uat"]):
            classification = "TEST_EVIDENCE"
            confidence = 0.93
        elif any(w in lower_content for w in ["incident", "ticket", "support", "troubleshoot", "error log"]):
            classification = "SUPPORT_ATTACHMENT"
            confidence = 0.89
        elif any(w in lower_content for w in ["policy", "standard", "manual", "guide", "handbook"]):
            classification = "KNOWLEDGE_SOURCE"
            confidence = 0.88
        else:
            classification = "GENERAL"
            confidence = 0.70

        return {
            "suggested_classification": classification,
            "confidence": confidence,
            "suggested_tags": [classification.lower(), "ai_classified"],
            "authority": "AI_INFERRED",
        }
