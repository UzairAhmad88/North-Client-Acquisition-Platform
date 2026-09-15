"""Solution Architecture Builder producing proportional technical recommendations."""

from typing import List
from agents.solution.models import SolutionArchitectureSchema, SolutionFeatureSchema, SolutionIntegrationSchema


class ArchitectureBuilder:
    """Generates proportional, clean technical architecture recommendations."""

    @classmethod
    def build(
        cls, features: List[SolutionFeatureSchema]
    ) -> SolutionArchitectureSchema:
        categories = {f.category for f in features}

        frontend = "Modern Responsive Web Portal (React / Next.js)"
        backend = "FastAPI / Python Modular Application Service"
        database = "PostgreSQL Relational Database"
        authentication = "JWT / PBKDF2 Password Hashing & Role-Based Access Control"
        deployment = "Containerized Cloud Application Platform"
        summary = "Client Browser -> Next.js Frontend -> FastAPI REST API -> PostgreSQL Database"

        if "AI_FEATURE" in categories:
            backend += " with AI Provider Routing Layer"
            summary += " -> AI Provider API"

        if "PAYMENT" in categories:
            summary += " & Webhook Listener (Stripe)"

        return SolutionArchitectureSchema(
            frontend=frontend,
            backend=backend,
            database=database,
            authentication=authentication,
            deployment=deployment,
            diagram_summary=summary,
        )

    @classmethod
    def extract_integrations(
        cls, features: List[SolutionFeatureSchema]
    ) -> List[SolutionIntegrationSchema]:
        integrations: List[SolutionIntegrationSchema] = []
        categories = {f.category for f in features}

        if "PAYMENT" in categories:
            integrations.append(
                SolutionIntegrationSchema(
                    purpose="Online Payment Processing",
                    provider="Stripe / PayPal API",
                    data_flow="Client Checkout -> Payment Provider -> Webhook Callback -> Order Confirmation",
                    status="PROPOSED",
                )
            )

        if "NOTIFICATION" in categories or "BOOKING" in categories:
            integrations.append(
                SolutionIntegrationSchema(
                    purpose="Automated Email / SMS Reminders",
                    provider="SendGrid / Twilio API",
                    data_flow="System Event -> Worker Task -> Notification Provider -> Client Inbox",
                    status="PROPOSED",
                )
            )

        return integrations
