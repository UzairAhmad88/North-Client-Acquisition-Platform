"""AI Governance & Observability Agent built on BaseAgent runtime."""

from typing import Any, Dict, List, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.governance.budget_monitor import AIBudgetMonitor
from agents.governance.evaluator import AIEvaluationEngine
from agents.governance.kill_switch import KillSwitchEngine
from agents.governance.prompt_registry import PromptRegistryEngine
from agents.governance.regression_engine import AIRegressionEngine
from agents.governance.tracer import AITracerEngine


class AIGovernanceAgent(BaseAgent):
    """Production AI Governance, Evaluation & Observability Agent.

    Observes agent workflows, tracks spans without private reasoning, enforces prompt versioning & budgets,
    runs offline evaluations, and provides emergency kill switch circuit-breaking.
    """

    agent_id = "ai_governance_agent"
    name = "AI Governance Agent"
    version = "1.0"
    description = (
        "Orchestrates AI system observability, prompt registry versioning, golden test dataset evaluations, "
        "regression gating, budget ceilings, and emergency kill-switch circuit-breaking."
    )

    def __init__(self):
        super().__init__()
        self.tracer = AITracerEngine()
        self.prompt_registry = PromptRegistryEngine()
        self.evaluator = AIEvaluationEngine()
        self.regression_engine = AIRegressionEngine()
        self.kill_switch = KillSwitchEngine()
        self.budget_monitor = AIBudgetMonitor()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_AI_TRACES,
            AgentPermission.READ_AI_METRICS,
            AgentPermission.READ_AI_EVALUATIONS,
            AgentPermission.READ_PROMPT_REGISTRY,
            AgentPermission.CREATE_PROMPT_DRAFT,
            AgentPermission.CREATE_EVALUATION_DRAFT,
            AgentPermission.CREATE_INCIDENT_DRAFT,
            AgentPermission.CREATE_IMPROVEMENT_DRAFT,
            AgentPermission.READ_ANALYTICS,
            AgentPermission.READ_METRICS,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Execute observability tracing, prompt validation, regression evaluation, or budget verification."""
        input_data = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        task_action = str(input_data.get("action") or "EVALUATE_OUTPUT")

        if task_action == "CHECK_KILL_SWITCH":
            agent_key = input_data.get("agent_key")
            model_key = input_data.get("model_key")
            tool_name = input_data.get("tool_name")
            res = self.kill_switch.check_execution_allowed(agent_key, model_key, tool_name)
            return {
                "action": "CHECK_KILL_SWITCH",
                "status": "SUCCESS",
                "check": res,
            }

        elif task_action == "VALIDATE_PROMPT":
            content = str(input_data.get("content") or "")
            validation = self.prompt_registry.validate_prompt_safety(content)
            return {
                "action": "VALIDATE_PROMPT",
                "status": "SUCCESS",
                "validation": validation,
            }

        elif task_action == "CHECK_BUDGET":
            current_cost = float(input_data.get("current_daily_cost") or 0.0)
            daily_limit = float(input_data.get("daily_limit") or 50.0)
            estimated_cost = float(input_data.get("estimated_call_cost") or 0.05)
            budget_res = self.budget_monitor.evaluate_budget_allowance(current_cost, daily_limit, estimated_cost)
            return {
                "action": "CHECK_BUDGET",
                "status": "SUCCESS",
                "budget_check": budget_res.model_dump(),
            }

        elif task_action == "RUN_REGRESSION_TEST":
            agent_key = str(input_data.get("agent_key") or "research_agent")
            agent_version = str(input_data.get("agent_version") or "v1.1")
            prompt_version = str(input_data.get("prompt_version") or "v1.1")
            model_version = str(input_data.get("model_version") or "v1.0")
            cases = input_data.get("cases") or []
            baseline_score = float(input_data.get("baseline_score") or 90.0)
            benchmark = self.regression_engine.execute_golden_suite_benchmark(
                agent_key=agent_key,
                agent_version=agent_version,
                prompt_version=prompt_version,
                model_version=model_version,
                cases=cases,
                baseline_score=baseline_score,
            )
            return {
                "action": "RUN_REGRESSION_TEST",
                "status": "SUCCESS",
                "benchmark": benchmark.model_dump(),
            }

        else:
            # Default EVALUATE_OUTPUT action
            output_data = input_data.get("output_data") or {}
            required_fields = input_data.get("required_fields") or ["status"]
            evidence_context = input_data.get("evidence_context") or {}
            eval_res = self.evaluator.run_comprehensive_evaluation(output_data, required_fields, evidence_context)

            return {
                "action": "EVALUATE_OUTPUT",
                "status": "SUCCESS",
                "evaluation": eval_res,
            }
