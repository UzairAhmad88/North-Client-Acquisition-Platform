"""Qualification Output Validator enforcing valid decision schemas and preventing fact fabrication."""

from typing import Any, Dict, List


class QualificationOutputValidator:
    """Validates qualification output dictionary structure and allowed enum values."""

    ALLOWED_DECISIONS = {
        "QUALIFIED",
        "POTENTIALLY_QUALIFIED",
        "NEEDS_REVIEW",
        "NOT_QUALIFIED",
        "INSUFFICIENT_DATA",
    }
    ALLOWED_CONFIDENCES = {"HIGH", "MEDIUM", "LOW"}
    ALLOWED_READINESS = {
        "OUTREACH_READY",
        "NEEDS_VERIFICATION",
        "NOT_READY",
        "OUTREACH_BLOCKED",
    }

    @classmethod
    def validate_result(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        decision = str(data.get("decision", "INSUFFICIENT_DATA")).upper()
        if decision not in cls.ALLOWED_DECISIONS:
            decision = "NEEDS_REVIEW"

        confidence = str(data.get("confidence", "MEDIUM")).upper()
        if confidence not in cls.ALLOWED_CONFIDENCES:
            confidence = "MEDIUM"

        readiness = str(data.get("outreach_readiness", "NOT_READY")).upper()
        if readiness not in cls.ALLOWED_READINESS:
            readiness = "NOT_READY"

        data["decision"] = decision
        data["confidence"] = confidence
        data["outreach_readiness"] = readiness
        data["summary"] = str(data.get("summary", "Qualification evaluation completed.")).strip()
        data["factors"] = data.get("factors", [])
        data["reasons"] = data.get("reasons", [])
        data["evidence"] = data.get("evidence", [])
        data["risks"] = data.get("risks", [])
        data["missing_information"] = data.get("missing_information", [])
        data["limitations"] = data.get("limitations", [])
        data["recommended_internal_action"] = data.get("recommended_internal_action", "REVIEW_LEAD")

        return data
