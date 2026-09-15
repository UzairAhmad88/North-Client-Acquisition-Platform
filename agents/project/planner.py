"""Project WBS and delivery planner engine."""

from typing import Any, Dict, List
from agents.project.models import DraftMilestoneSchema, DraftWBSItemSchema, ProjectPlanDraftResult


class ProjectPlannerEngine:
    """Generates suggested Work Breakdown Structure (WBS) and milestone plans from solution deliverables and estimates."""

    def generate_draft_plan(
        self,
        project_name: str,
        deliverables: List[Dict[str, Any]],
        estimate_items: List[Dict[str, Any]],
    ) -> ProjectPlanDraftResult:
        suggested_wbs: List[DraftWBSItemSchema] = []
        suggested_milestones: List[DraftMilestoneSchema] = []
        notes: List[str] = []

        # 1. Standard Milestones
        suggested_milestones.append(
            DraftMilestoneSchema(
                name="Project Kickoff & Environment Setup",
                description="Project initiation, repository setup, and access configuration",
                target_days_from_start=5,
            )
        )
        suggested_milestones.append(
            DraftMilestoneSchema(
                name="Core Deliverables Architecture",
                description="Completion of core backend and frontend foundation components",
                target_days_from_start=20,
            )
        )
        suggested_milestones.append(
            DraftMilestoneSchema(
                name="System Integration & QA Verification",
                description="End-to-end integration testing and client feedback incorporation",
                target_days_from_start=35,
            )
        )
        suggested_milestones.append(
            DraftMilestoneSchema(
                name="Final Handover & Deployment",
                description="Production deployment, documentation handover, and sign-off",
                target_days_from_start=45,
            )
        )

        # 2. Map Estimate Items or Deliverables to WBS
        if estimate_items:
            for idx, item in enumerate(estimate_items):
                hours = float(item.get("expected_hours") or item.get("most_likely_hours") or 10.0)
                category = str(item.get("category") or "ENGINEERING").upper()
                name = str(item.get("name") or f"Work Item #{idx + 1}")
                desc = str(item.get("description") or f"Implement {name}")
                priority = "HIGH" if hours >= 20 else "MEDIUM"
                predecessors = [idx - 1] if idx > 0 else []

                suggested_wbs.append(
                    DraftWBSItemSchema(
                        name=name,
                        description=desc,
                        category=category,
                        priority=priority,
                        estimated_hours=hours,
                        predecessor_temp_ids=predecessors,
                        milestone_name="Core Deliverables Architecture" if idx < len(estimate_items) // 2 else "System Integration & QA Verification",
                    )
                )
        elif deliverables:
            for idx, d in enumerate(deliverables):
                name = str(d.get("name") or f"Deliverable #{idx + 1}")
                desc = str(d.get("description") or f"Build deliverable {name}")
                suggested_wbs.append(
                    DraftWBSItemSchema(
                        name=f"Implement {name}",
                        description=desc,
                        category="DELIVERABLE",
                        priority="HIGH",
                        estimated_hours=16.0,
                        predecessor_temp_ids=[idx - 1] if idx > 0 else [],
                        deliverable_name=name,
                        milestone_name="Core Deliverables Architecture",
                    )
                )

        if not suggested_wbs:
            # Baseline fallback WBS
            suggested_wbs = [
                DraftWBSItemSchema(
                    name="Architecture & Foundation",
                    description="Setup baseline project scaffolding and data models",
                    category="FOUNDATION",
                    priority="HIGH",
                    estimated_hours=16.0,
                    predecessor_temp_ids=[],
                    milestone_name="Project Kickoff & Environment Setup",
                ),
                DraftWBSItemSchema(
                    name="Feature Implementation",
                    description="Implement requested business features and integrations",
                    category="ENGINEERING",
                    priority="HIGH",
                    estimated_hours=40.0,
                    predecessor_temp_ids=[0],
                    milestone_name="Core Deliverables Architecture",
                ),
                DraftWBSItemSchema(
                    name="Testing & QA Verification",
                    description="Execute unit, integration, and security verification suites",
                    category="QA",
                    priority="MEDIUM",
                    estimated_hours=16.0,
                    predecessor_temp_ids=[1],
                    milestone_name="System Integration & QA Verification",
                ),
            ]

        notes.append("Generated structured WBS from baseline deliverables and commercial estimates.")
        notes.append("All tasks require human Project Manager review before committing to execution schedule.")

        return ProjectPlanDraftResult(
            project_name=project_name,
            suggested_wbs=suggested_wbs,
            suggested_milestones=suggested_milestones,
            planning_notes=notes,
            confidence_score=0.92,
        )
