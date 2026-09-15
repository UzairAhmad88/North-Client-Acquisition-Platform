"""Production Project Estimation, Effort & Commercial Intelligence Agent."""

import hashlib
import json
import uuid
from typing import Any, Dict, List
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.estimation.complexity import ComplexityEvaluator
from agents.estimation.costing import CostEngine
from agents.estimation.effort import RoleEffortDistributor
from agents.estimation.estimator import PERTEstimator
from agents.estimation.models import EstimateWorkItemSchema, EstimationResult
from agents.estimation.pricing import PricingRecommendationEngine
from agents.estimation.scenarios import ScenarioGenerator
from agents.estimation.validator import EstimationValidator


class EstimationAgent(BaseAgent):
    """
    Production Project Estimation, Effort & Commercial Intelligence Agent.
    Breaks solution designs into work items, computes PERT three-point effort ranges,
    distributes role allocations, calculates internal labor & external operating costs,
    applies risk buffers, and generates recommended internal commercial ranges for human decision-making.
    """

    agent_id = "estimation_agent"
    name = "Estimation Agent"
    version = "1.0"
    description = "Calculates internal engineering effort, PERT ranges, role allocations, labor/external costs, and recommended commercial ranges."
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_RESEARCH",
        "READ_AUDIT",
        "READ_SCORE",
        "READ_SERVICES",
        "READ_REQUIREMENTS",
        "READ_SOLUTION",
        "READ_PRICING_POLICY",
        "READ_COST_MODEL",
        "CREATE_ESTIMATE_DRAFT",
    }

    def get_permissions(self) -> list[AgentPermission]:
        return [AgentPermission(p) for p in self.permissions if p in AgentPermission.__members__]

    async def run(self, context: AgentContext) -> AgentResult:
        solution_data = context.metadata.get("solution_data", {})
        features = solution_data.get("features", [])

        # 1. Generate Work Breakdown Items (WBS)
        work_items: List[EstimateWorkItemSchema] = []
        for feat in features:
            f_title = feat.get("title", "Feature Module")
            f_category = feat.get("category", "BACKEND")
            complexity, opt, most, pess = ComplexityEvaluator.evaluate_feature_complexity(f_category)
            exp = PERTEstimator.calculate_expected_hours(opt, most, pess)

            work_items.append(
                EstimateWorkItemSchema(
                    name=f_title,
                    category=f_category,
                    description=feat.get("description", f"Implementation of {f_title}."),
                    complexity=complexity,
                    optimistic_hours=opt,
                    most_likely_hours=most,
                    pessimistic_hours=pess,
                    expected_hours=exp,
                    confidence="HIGH" if feat.get("status") == "REQUIRED" else "MEDIUM",
                    supporting_feature_title=f_title,
                )
            )

        # Baseline Testing & Deployment Item
        opt_t, most_t, pess_t = 6.0, 10.0, 16.0
        exp_t = PERTEstimator.calculate_expected_hours(opt_t, most_t, pess_t)
        work_items.append(
            EstimateWorkItemSchema(
                name="Testing, QA & Cloud Deployment",
                category="TESTING",
                description="Quality assurance testing, staging setup, domain configuration, and production launch.",
                complexity="MEDIUM",
                optimistic_hours=opt_t,
                most_likely_hours=most_t,
                pessimistic_hours=pess_t,
                expected_hours=exp_t,
                confidence="HIGH",
            )
        )

        # 2. Total PERT Effort Calculation
        min_h, exp_h, max_h = PERTEstimator.calculate_totals(work_items)
        overall_complexity = ComplexityEvaluator.evaluate_overall_complexity(exp_h, len(features))

        # 3. Role Effort Allocation
        role_breakdown = RoleEffortDistributor.distribute_hours(work_items)

        # 4. Labor Cost & External Costs Calculation
        internal_cost = CostEngine.calculate_internal_labor_cost(exp_h)
        external_costs = CostEngine.extract_external_costs(work_items)
        total_external_cost = sum(c.amount for c in external_costs)

        # 5. Commercial Recommendation Range
        risk_buffer_pct = 20.0
        _, rec_min, rec_max = PricingRecommendationEngine.calculate_commercial_range(
            internal_cost, total_external_cost, risk_buffer_percent=risk_buffer_pct
        )

        # 6. Scenarios Generation
        scenarios = ScenarioGenerator.generate_scenarios(work_items, total_external_cost)

        # 7. Safety Validation
        warnings = EstimationValidator.validate_estimate_safety(work_items, solution_data)

        # Content Hash
        content_dump = json.dumps([w.model_dump() for w in work_items], sort_keys=True)
        content_hash = hashlib.sha256(content_dump.encode("utf-8")).hexdigest()

        result_payload = EstimationResult(
            summary=f"Project estimate calculated: {exp_h} expected hours ({min_h}-{max_h} range) across {len(work_items)} work items.",
            complexity=overall_complexity,
            confidence="HIGH" if len(work_items) >= 2 else "MEDIUM",
            estimated_hours=exp_h,
            minimum_hours=min_h,
            maximum_hours=max_h,
            risk_buffer_percent=risk_buffer_pct,
            internal_cost=internal_cost,
            external_cost=total_external_cost,
            recommended_min=rec_min,
            recommended_max=rec_max,
            work_items=work_items,
            costs=external_costs,
            scenarios=scenarios,
            role_breakdown=role_breakdown,
            content_hash=content_hash,
        )

        return AgentResult(
            status="COMPLETED",
            result=result_payload.model_dump(),
            confidence="HIGH",
            evidence=[{"source": "SOLUTION_DESIGN", "features_count": len(features)}],
            warnings=warnings,
            errors=[],
            next_action={"action": "HUMAN_COMMERCIAL_REVIEW", "reason": "Review project effort, internal costs, and approve commercial recommendation range."},
            metadata={"run_id": context.agent_run_id, "agent_id": self.name},
        )


estimation_agent = EstimationAgent()
