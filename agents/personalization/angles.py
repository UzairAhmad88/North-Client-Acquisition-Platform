"""Angle selector choosing primary and supporting evidence-backed communication angles."""

from typing import List, Tuple
from agents.personalization.schemas import BusinessNeedMapping, CommunicationAngle, VerifiedSignal


class AngleSelector:
    """Selects 1 primary communication angle and 0–2 supporting angles grounded in verified evidence."""

    @staticmethod
    def select_angles(
        signals: List[VerifiedSignal],
        needs: List[BusinessNeedMapping],
    ) -> Tuple[CommunicationAngle, List[CommunicationAngle]]:
        # Map needs to candidate angles
        candidate_angles: List[CommunicationAngle] = []

        for need in needs:
            slug = need.relevant_service_slug or ""
            if "booking" in slug or "BOOKING" in need.observed_gap.upper():
                candidate_angles.append(
                    CommunicationAngle(
                        angle_type="BOOKING",
                        title="Online Booking & Scheduling Flow",
                        problem_statement=need.observed_gap,
                        value_proposition="Make it effortless for visitors to book services or appointments directly.",
                        evidence_ids=need.evidence_ids,
                        confidence="HIGH",
                    )
                )
            elif "website" in slug or "WEBSITE" in need.observed_gap.upper():
                candidate_angles.append(
                    CommunicationAngle(
                        angle_type="WEBSITE_IMPROVEMENT",
                        title="Modern High-Converting Website",
                        problem_statement=need.observed_gap,
                        value_proposition="Establish a fast, professional digital presence tailored for customer conversion.",
                        evidence_ids=need.evidence_ids,
                        confidence="HIGH",
                    )
                )
            elif "lead" in slug or "CAPTURE" in need.observed_gap.upper():
                candidate_angles.append(
                    CommunicationAngle(
                        angle_type="LEAD_CAPTURE",
                        title="Automated Lead Capture",
                        problem_statement=need.observed_gap,
                        value_proposition="Capture every visitor inquiry automatically so no customer request is missed.",
                        evidence_ids=need.evidence_ids,
                        confidence="HIGH",
                    )
                )

        if not candidate_angles:
            candidate_angles.append(
                CommunicationAngle(
                    angle_type="DIGITAL_PRESENCE",
                    title="Digital Growth & Customer Conversion",
                    problem_statement="Digital presence opportunity identified from public business evaluation.",
                    value_proposition="Enhance online visibility and simplify customer acquisition.",
                    evidence_ids=[],
                    confidence="HIGH",
                )
            )

        primary_angle = candidate_angles[0]
        supporting_angles = candidate_angles[1:3]

        return primary_angle, supporting_angles
