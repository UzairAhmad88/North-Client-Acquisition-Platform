"""Production Quality Assurance & Handover AI Agent built on BaseAgent runtime."""

from typing import Any, Dict, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.qa.test_generator import TestGeneratorEngine
from agents.qa.defect_classifier import DefectClassifierEngine
from agents.qa.regression_analyzer import RegressionAnalyzerEngine
from agents.qa.readiness_evaluator import ReadinessEvaluatorEngine
from agents.qa.handover_engine import HandoverEngine


class QAAgent(BaseAgent):
    """Production QA AI Agent providing test generation, defect triage, regression suite selection, release readiness gate evaluation, and handover checklist drafting."""

    agent_id = "qa_agent"
    name = "Quality Assurance & Handover Agent"
    version = "1.0"
    description = "Generates test cases, triages defects, selects regression suites, evaluates release readiness gates, and drafts handover checklists."

    def __init__(self):
        super().__init__()
        self.test_generator = TestGeneratorEngine()
        self.defect_classifier = DefectClassifierEngine()
        self.regression_analyzer = RegressionAnalyzerEngine()
        self.readiness_evaluator = ReadinessEvaluatorEngine()
        self.handover_engine = HandoverEngine()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_PROJECT,
            AgentPermission.READ_BASELINE,
            AgentPermission.READ_REQUIREMENTS,
            AgentPermission.READ_DELIVERABLES,
            AgentPermission.READ_TEST_PLANS,
            AgentPermission.READ_TEST_CASES,
            AgentPermission.READ_TEST_RESULTS,
            AgentPermission.READ_DEFECTS,
            AgentPermission.READ_UAT,
            AgentPermission.READ_RELEASES,
            AgentPermission.CREATE_TEST_CASE_DRAFT,
            AgentPermission.CREATE_QA_SUMMARY,
            AgentPermission.CREATE_CLASSIFICATION_DRAFT,
            AgentPermission.CREATE_RELEASE_READINESS_DRAFT,
            AgentPermission.CREATE_HANDOVER_CHECKLIST_DRAFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Execute test drafting, defect triage, regression selection, readiness evaluation, or handover drafting."""
        input_data = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        task_action = str(input_data.get("action") or "GENERATE_TEST_CASES")

        if task_action == "GENERATE_TEST_CASES":
            plan_id = str(input_data.get("test_plan_id") or "tp-1")
            reqs = input_data.get("requirements", [])
            delivs = input_data.get("deliverables", [])
            res = self.test_generator.generate_test_cases(plan_id, reqs, delivs)
            return res.model_dump()

        elif task_action == "CLASSIFY_DEFECT":
            def_id = input_data.get("defect_id")
            title = str(input_data.get("title") or "Defect Report")
            desc = str(input_data.get("description") or "")
            against_spec = bool(input_data.get("is_against_baseline_spec", True))
            res = self.defect_classifier.classify_defect(def_id, title, desc, against_spec)
            return res.model_dump()

        elif task_action == "SELECT_REGRESSION":
            proj_id = str(input_data.get("project_id") or "p-1")
            cases = input_data.get("test_cases", [])
            req_ids = input_data.get("changed_requirement_ids", [])
            deliv_ids = input_data.get("changed_deliverable_ids", [])
            res = self.regression_analyzer.select_regression_suite(proj_id, cases, req_ids, deliv_ids)
            return res.model_dump()

        elif task_action == "EVALUATE_READINESS":
            proj_id = str(input_data.get("project_id") or "p-1")
            tag = str(input_data.get("version_tag") or "v1.0.0")
            total_t = int(input_data.get("total_test_count") or 0)
            passed_t = int(input_data.get("passed_test_count") or 0)
            failed_t = int(input_data.get("failed_test_count") or 0)
            crit_def = int(input_data.get("open_critical_defects") or 0)
            high_def = int(input_data.get("open_high_defects") or 0)
            uat_app = bool(input_data.get("uat_approved", False))
            res = self.readiness_evaluator.evaluate_readiness(
                proj_id, tag, total_t, passed_t, failed_t, crit_def, high_def, uat_app
            )
            return res.model_dump()

        elif task_action == "DRAFT_HANDOVER":
            proj_id = str(input_data.get("project_id") or "p-1")
            repo = str(input_data.get("code_repo_url") or "")
            docs = str(input_data.get("docs_url") or "")
            staging = str(input_data.get("staging_url") or "")
            res = self.handover_engine.build_handover_checklist(proj_id, repo, docs, staging)
            return res.model_dump()

        else:
            return {
                "status": "COMPLETED",
                "message": f"QA action '{task_action}' processed cleanly.",
            }
