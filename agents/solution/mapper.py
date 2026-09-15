"""Requirement-to-Feature Mapping Engine creating traceable solution specs."""

from typing import Any, Dict, List, Tuple
from agents.solution.models import SolutionFeatureSchema


class RequirementMapper:
    """Maps confirmed client requirements to solution features and modules."""

    FEATURE_MAPPINGS = {
        "BOOKING": {
            "title": "Online Appointment Booking System",
            "description": "Interactive appointment scheduling calendar allowing client booking and staff slot management.",
            "status": "REQUIRED",
            "priority": "HIGH",
        },
        "PAYMENT": {
            "title": "Online Payment Gateway Integration",
            "description": "Secure credit card and digital payment processing via Stripe/PayPal integration.",
            "status": "RECOMMENDED",
            "priority": "HIGH",
        },
        "WEBSITE": {
            "title": "Responsive Business Web Application",
            "description": "Custom branded web interface optimized for desktop and mobile performance.",
            "status": "REQUIRED",
            "priority": "HIGH",
        },
        "AUTOMATION": {
            "title": "Automated Business Workflow Engine",
            "description": "Background notification and status sync engine eliminating manual operational tasks.",
            "status": "RECOMMENDED",
            "priority": "MEDIUM",
        },
        "AI_FEATURE": {
            "title": "AI Conversational Assistant",
            "description": "Smart customer service AI bot capable of answering inquiries and capturing leads.",
            "status": "OPTIONAL",
            "priority": "MEDIUM",
        },
        "CRM": {
            "title": "Centralized Customer Lead Management",
            "description": "Customer relationship database tracking lead stages, contacts, and communication history.",
            "status": "RECOMMENDED",
            "priority": "MEDIUM",
        },
        "DASHBOARD": {
            "title": "Executive Operational Dashboard",
            "description": "Analytics and administrative command center displaying daily metrics, bookings, and revenue.",
            "status": "RECOMMENDED",
            "priority": "MEDIUM",
        },
        "AUTHENTICATION": {
            "title": "Secure User Authentication & Access Control",
            "description": "Role-based authentication system supporting Customer, Staff, and Admin credentials.",
            "status": "REQUIRED",
            "priority": "HIGH",
        },
    }

    @classmethod
    def map_requirements(
        cls, requirements: List[Dict[str, Any]]
    ) -> List[SolutionFeatureSchema]:
        features: List[SolutionFeatureSchema] = []
        mapped_categories = set()

        for req in requirements:
            cat = req.get("category", "").upper()
            req_title = req.get("title", "")

            if cat in cls.FEATURE_MAPPINGS and cat not in mapped_categories:
                mapped_categories.add(cat)
                spec = cls.FEATURE_MAPPINGS[cat]
                features.append(
                    SolutionFeatureSchema(
                        title=spec["title"],
                        description=spec["description"],
                        category=cat,
                        status=spec["status"] if req.get("explicit") else "RECOMMENDED",
                        priority=spec["priority"],
                        supporting_requirement_titles=[req_title],
                    )
                )

        # Fallback if no specific categories match
        if not features:
            features.append(
                SolutionFeatureSchema(
                    title="Core Business Digital Interface",
                    description="Standard web presence and intake portal.",
                    category="WEBSITE",
                    status="REQUIRED",
                    priority="HIGH",
                    supporting_requirement_titles=["General Digital Need"],
                )
            )

        return features
