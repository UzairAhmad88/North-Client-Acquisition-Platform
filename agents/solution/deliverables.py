"""Deliverable Builder producing concrete outcome deliverables."""

from typing import List
from agents.solution.models import SolutionDeliverableSchema, SolutionFeatureSchema


class DeliverableBuilder:
    """Builds concrete deliverable items from solution features."""

    @classmethod
    def build_deliverables(
        cls, features: List[SolutionFeatureSchema]
    ) -> List[SolutionDeliverableSchema]:
        deliverables: List[SolutionDeliverableSchema] = []

        for feature in features:
            deliv_name = f"{feature.title} Package"
            deliv_desc = f"Complete implementation, testing, and deployment of {feature.title.lower()}."

            deliverables.append(
                SolutionDeliverableSchema(
                    name=deliv_name,
                    description=deliv_desc,
                    status="PROPOSED",
                    priority=feature.priority,
                    supporting_feature_titles=[feature.title],
                )
            )

        # Standard technical deliverable
        deliverables.append(
            SolutionDeliverableSchema(
                name="Deployment & User Documentation",
                description="Cloud deployment setup, domain configuration, and administrative user guide.",
                status="PROPOSED",
                priority="HIGH",
                supporting_feature_titles=[f.title for f in features],
            )
        )

        return deliverables
