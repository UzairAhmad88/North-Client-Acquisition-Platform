"""Declarative Workflow Definitions & Templates Catalog for Phase 34."""

from typing import Any, Dict, List, Optional
from app.models.orchestration import TaskType


class WorkflowStepDef:
    """Step specification inside a declarative workflow template."""

    def __init__(
        self,
        step_key: str,
        name: str,
        step_type: TaskType,
        config: Optional[Dict[str, Any]] = None,
        timeout_seconds: int = 3600,
    ):
        self.step_key = step_key
        self.name = name
        self.step_type = step_type
        self.config = config or {}
        self.timeout_seconds = timeout_seconds

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_key": self.step_key,
            "name": self.name,
            "step_type": self.step_type.value if hasattr(self.step_type, "value") else str(self.step_type),
            "config": self.config,
            "timeout_seconds": self.timeout_seconds,
        }


class WorkflowTransitionDef:
    """Transition edge between workflow steps."""

    def __init__(
        self,
        from_step_key: str,
        to_step_key: str,
        condition: Optional[str] = None,
        is_default: bool = True,
    ):
        self.from_step_key = from_step_key
        self.to_step_key = to_step_key
        self.condition = condition
        self.is_default = is_default

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_step_key": self.from_step_key,
            "to_step_key": self.to_step_key,
            "condition": self.condition,
            "is_default": self.is_default,
        }


class DeclarativeWorkflowTemplate:
    """Declarative workflow graph template specification."""

    def __init__(
        self,
        workflow_key: str,
        name: str,
        description: str,
        category: str,
        version: str,
        steps: List[WorkflowStepDef],
        transitions: List[WorkflowTransitionDef],
    ):
        self.workflow_key = workflow_key
        self.name = name
        self.description = description
        self.category = category
        self.version = version
        self.steps = steps
        self.transitions = transitions

    def get_step(self, step_key: str) -> Optional[WorkflowStepDef]:
        for s in self.steps:
            if s.step_key == step_key:
                return s
        return None

    def get_next_steps(self, current_step_key: str) -> List[str]:
        return [t.to_step_key for t in self.transitions if t.from_step_key == current_step_key]


class WorkflowRegistry:
    """Catalog of built-in declarative business workflows."""

    def __init__(self):
        self._templates: Dict[str, DeclarativeWorkflowTemplate] = {}
        self._register_built_in_workflows()

    def register(self, template: DeclarativeWorkflowTemplate) -> None:
        self._templates[template.workflow_key] = template

    def get(self, workflow_key: str) -> Optional[DeclarativeWorkflowTemplate]:
        return self._templates.get(workflow_key)

    def list_all(self) -> List[DeclarativeWorkflowTemplate]:
        return list(self._templates.values())

    def _register_built_in_workflows(self) -> None:
        """Register default cross-system business lifecycle templates."""
        # 1. Lead Acquisition Workflow
        self.register(
            DeclarativeWorkflowTemplate(
                workflow_key="lead_acquisition_workflow",
                name="Lead Acquisition & Outbound Pipeline",
                description="Automated discovery, research, audit, qualification, and personalized outreach draft with mandatory human approval.",
                category="CLIENT_ACQUISITION",
                version="v1.0",
                steps=[
                    WorkflowStepDef("discovery", "Business Discovery", TaskType.AGENT_TASK, {"agent": "discovery_agent"}),
                    WorkflowStepDef("research", "Digital Footprint Research", TaskType.AGENT_TASK, {"agent": "research_agent"}),
                    WorkflowStepDef("audit", "Website Performance Audit", TaskType.AGENT_TASK, {"agent": "audit_agent"}),
                    WorkflowStepDef("qualify", "Lead Fit Qualification", TaskType.AGENT_TASK, {"agent": "qualification_agent"}),
                    WorkflowStepDef("recommend", "Service Catalog Mapping", TaskType.WORKER_TASK, {"engine": "recommendation_engine"}),
                    WorkflowStepDef("personalize", "Synthesize Outreach Draft", TaskType.AGENT_TASK, {"agent": "personalization_agent"}),
                    WorkflowStepDef("risk_check", "Safety & Claim Verification", TaskType.SYSTEM_TASK, {"engine": "risk_engine"}),
                    WorkflowStepDef("human_approval", "Human Operator Approval", TaskType.HUMAN_TASK, {"task_type": "APPROVE_OUTREACH"}),
                    WorkflowStepDef("send_outreach", "Guarded Dispatch", TaskType.INTEGRATION_TASK, {"guard": "communication_guard"}),
                ],
                transitions=[
                    WorkflowTransitionDef("discovery", "research"),
                    WorkflowTransitionDef("research", "audit"),
                    WorkflowTransitionDef("audit", "qualify"),
                    WorkflowTransitionDef("qualify", "recommend"),
                    WorkflowTransitionDef("recommend", "personalize"),
                    WorkflowTransitionDef("personalize", "risk_check"),
                    WorkflowTransitionDef("risk_check", "human_approval"),
                    WorkflowTransitionDef("human_approval", "send_outreach"),
                ],
            )
        )

        # 2. Client Discovery to Contract Workflow
        self.register(
            DeclarativeWorkflowTemplate(
                workflow_key="client_conversion_workflow",
                name="Client Discovery & Contract Pipeline",
                description="Inbound response intelligence, requirements extraction, solution design, estimation, proposal, and contract generation.",
                category="COMMERCIAL",
                version="v1.0",
                steps=[
                    WorkflowStepDef("response_intel", "Response & Intent Classifier", TaskType.AGENT_TASK, {"agent": "response_agent"}),
                    WorkflowStepDef("requirements_extract", "Requirements Extraction", TaskType.AGENT_TASK, {"agent": "requirements_agent"}),
                    WorkflowStepDef("requirements_confirm", "Human Requirements Confirmation", TaskType.HUMAN_TASK, {"task_type": "CONFIRM_REQUIREMENTS"}),
                    WorkflowStepDef("solution_design", "Architecture & Solution Design", TaskType.AGENT_TASK, {"agent": "solution_agent"}),
                    WorkflowStepDef("estimation", "PERT Effort & Commercial Range", TaskType.AGENT_TASK, {"agent": "estimation_agent"}),
                    WorkflowStepDef("proposal_synthesis", "Proposal Synthesis", TaskType.AGENT_TASK, {"agent": "proposal_agent"}),
                    WorkflowStepDef("proposal_approval", "Commercial Review & Approval", TaskType.HUMAN_TASK, {"task_type": "APPROVE_PROPOSAL"}),
                    WorkflowStepDef("contract_generation", "Contract & Baseline Drafting", TaskType.AGENT_TASK, {"agent": "contract_agent"}),
                ],
                transitions=[
                    WorkflowTransitionDef("response_intel", "requirements_extract"),
                    WorkflowTransitionDef("requirements_extract", "requirements_confirm"),
                    WorkflowTransitionDef("requirements_confirm", "solution_design"),
                    WorkflowTransitionDef("solution_design", "estimation"),
                    WorkflowTransitionDef("estimation", "proposal_synthesis"),
                    WorkflowTransitionDef("proposal_synthesis", "proposal_approval"),
                    WorkflowTransitionDef("proposal_approval", "contract_generation"),
                ],
            )
        )

        # 3. Project Delivery & Handover Workflow
        self.register(
            DeclarativeWorkflowTemplate(
                workflow_key="project_delivery_workflow",
                name="Project Delivery, QA & Handover",
                description="Project initiation from contract baseline, delivery execution, test suite verification, client UAT, package delivery, and handover.",
                category="DELIVERY",
                version="v1.0",
                steps=[
                    WorkflowStepDef("project_init", "Initialize Project & WBS", TaskType.WORKER_TASK, {"engine": "project_planner"}),
                    WorkflowStepDef("qa_test_run", "Automated QA Verification", TaskType.AGENT_TASK, {"agent": "qa_agent"}),
                    WorkflowStepDef("uat_session", "Client UAT Acceptance", TaskType.HUMAN_TASK, {"task_type": "ACCEPT_UAT"}),
                    WorkflowStepDef("package_delivery", "Delivery Package Synthesis", TaskType.SYSTEM_TASK, {"engine": "handover_engine"}),
                    WorkflowStepDef("final_handover", "Client Handover Signoff", TaskType.HUMAN_TASK, {"task_type": "COMPLETE_HANDOVER"}),
                ],
                transitions=[
                    WorkflowTransitionDef("project_init", "qa_test_run"),
                    WorkflowTransitionDef("qa_test_run", "uat_session"),
                    WorkflowTransitionDef("uat_session", "package_delivery"),
                    WorkflowTransitionDef("package_delivery", "final_handover"),
                ],
            )
        )

        # 4. Change Request Governance Workflow
        self.register(
            DeclarativeWorkflowTemplate(
                workflow_key="change_management_workflow",
                name="Scope & Commercial Change Governance",
                description="Change request classification, impact analysis, re-estimation, internal review, client sign-off, and baseline versioning.",
                category="CHANGE_MANAGEMENT",
                version="v1.0",
                steps=[
                    WorkflowStepDef("change_classification", "Classify Request", TaskType.AGENT_TASK, {"agent": "change_agent"}),
                    WorkflowStepDef("impact_analysis", "Effort & Schedule Impact", TaskType.AGENT_TASK, {"agent": "change_agent"}),
                    WorkflowStepDef("internal_approval", "Internal Operator Review", TaskType.HUMAN_TASK, {"task_type": "APPROVE_CHANGE_INTERNAL"}),
                    WorkflowStepDef("client_approval", "Client Commercial Signoff", TaskType.HUMAN_TASK, {"task_type": "APPROVE_CHANGE_CLIENT"}),
                    WorkflowStepDef("baseline_update", "Update Contract Baseline", TaskType.SYSTEM_TASK, {"engine": "baseline_engine"}),
                ],
                transitions=[
                    WorkflowTransitionDef("change_classification", "impact_analysis"),
                    WorkflowTransitionDef("impact_analysis", "internal_approval"),
                    WorkflowTransitionDef("internal_approval", "client_approval"),
                    WorkflowTransitionDef("client_approval", "baseline_update"),
                ],
            )
        )

        # 5. AI Evaluation & Continuous Improvement Workflow
        self.register(
            DeclarativeWorkflowTemplate(
                workflow_key="ai_evaluation_workflow",
                name="AI Evaluation & Regression Gate",
                description="Golden dataset benchmark execution, regression comparison, threshold gating, and continuous improvement logging.",
                category="AI_GOVERNANCE",
                version="v1.0",
                steps=[
                    WorkflowStepDef("run_benchmark", "Execute Golden Benchmark", TaskType.AGENT_TASK, {"agent": "ai_governance_agent"}),
                    WorkflowStepDef("regression_gate", "Evaluate Regression Gate", TaskType.SYSTEM_TASK, {"engine": "regression_engine"}),
                    WorkflowStepDef("backlog_sync", "Sync Improvement Items", TaskType.SYSTEM_TASK, {"engine": "continuous_improvement"}),
                ],
                transitions=[
                    WorkflowTransitionDef("run_benchmark", "regression_gate"),
                    WorkflowTransitionDef("regression_gate", "backlog_sync"),
                ],
            )
        )


# Global singleton instance
global_workflow_registry = WorkflowRegistry()
