"""Requirement Dependency Analyzer building relationship graphs between scope items."""

from typing import List
from agents.requirements.models import ExtractedRequirementSchema, RequirementDependencySchema


class DependencyAnalyzer:
    """Analyzes requirements to construct dependency relationships."""

    DEPENDENCY_RULES = [
        ("BOOKING", "AUTHENTICATION", "REQUIRES"),
        ("PAYMENT", "BOOKING", "ENHANCES"),
        ("PAYMENT", "AUTHENTICATION", "REQUIRES"),
        ("DASHBOARD", "BOOKING", "ENHANCES"),
        ("DASHBOARD", "CRM", "ENHANCES"),
        ("NOTIFICATION", "BOOKING", "ENHANCES"),
    ]

    @classmethod
    def analyze(
        cls, requirements: List[ExtractedRequirementSchema]
    ) -> List[RequirementDependencySchema]:
        dependencies: List[RequirementDependencySchema] = []
        by_category = {req.category: req for req in requirements}

        for source_cat, target_cat, dep_type in cls.DEPENDENCY_RULES:
            if source_cat in by_category and target_cat in by_category:
                dependencies.append(
                    RequirementDependencySchema(
                        requirement_title=by_category[source_cat].title,
                        depends_on_title=by_category[target_cat].title,
                        dependency_type=dep_type,
                        confidence="HIGH",
                    )
                )

        return dependencies
