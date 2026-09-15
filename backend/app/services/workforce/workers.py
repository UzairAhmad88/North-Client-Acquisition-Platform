"""
AI Worker Registry & Lifecycle Subsystem for Phase 52.
Manages the registration, templates, capability assignment, and lifecycle states of AI Knowledge Workers.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.workforce.base import AIWorker, SupervisionLevel, WorkerCapability, WorkerStatus
except ImportError:
    from app.services.workforce.base import AIWorker, SupervisionLevel, WorkerCapability, WorkerStatus

logger = logging.getLogger(__name__)


class WorkerRegistry:
    """
    Registry and lifecycle controller for specialized AI Knowledge Workers.
    Maintains 20 standard enterprise specializations.
    """

    INITIAL_WORKER_TEMPLATES = [
        {"role": "Research Specialist", "specialization": "RESEARCH", "supervision": SupervisionLevel.READ_ONLY_1},
        {"role": "Lead Qualification Specialist", "specialization": "LEAD_QUALIFICATION", "supervision": SupervisionLevel.DRAFT_GEN_2},
        {"role": "Sales Intelligence Specialist", "specialization": "SALES_INTELLIGENCE", "supervision": SupervisionLevel.READ_ONLY_1},
        {"role": "Outreach Drafting Specialist", "specialization": "OUTREACH_DRAFTING", "supervision": SupervisionLevel.DRAFT_GEN_2},
        {"role": "Client Success Specialist", "specialization": "CLIENT_SUCCESS", "supervision": SupervisionLevel.DRAFT_GEN_2},
        {"role": "Requirements Analyst", "specialization": "REQUIREMENTS", "supervision": SupervisionLevel.DRAFT_GEN_2},
        {"role": "Solution Architect", "specialization": "SOLUTION_ARCHITECT", "supervision": SupervisionLevel.DRAFT_GEN_2},
        {"role": "Estimation Specialist", "specialization": "ESTIMATION", "supervision": SupervisionLevel.DRAFT_GEN_2},
        {"role": "Project Management Specialist", "specialization": "PROJECT_MANAGEMENT", "supervision": SupervisionLevel.BOUNDED_ACTION_3},
        {"role": "Quality Assurance Specialist", "specialization": "QA", "supervision": SupervisionLevel.BOUNDED_ACTION_3},
        {"role": "Documentation Specialist", "specialization": "DOCUMENTATION", "supervision": SupervisionLevel.DRAFT_GEN_2},
        {"role": "Finance Analyst", "specialization": "FINANCE", "supervision": SupervisionLevel.READ_ONLY_1},
        {"role": "Operations Specialist", "specialization": "OPERATIONS", "supervision": SupervisionLevel.BOUNDED_ACTION_3},
        {"role": "Security Analyst", "specialization": "SECURITY", "supervision": SupervisionLevel.READ_ONLY_1},
        {"role": "Compliance Analyst", "specialization": "COMPLIANCE", "supervision": SupervisionLevel.READ_ONLY_1},
        {"role": "Knowledge Curator", "specialization": "KNOWLEDGE", "supervision": SupervisionLevel.BOUNDED_ACTION_3},
        {"role": "Data Analyst", "specialization": "DATA", "supervision": SupervisionLevel.READ_ONLY_1},
        {"role": "Strategy Analyst", "specialization": "STRATEGY", "supervision": SupervisionLevel.READ_ONLY_1},
        {"role": "Process Optimization Specialist", "specialization": "PROCESS_OPTIMIZATION", "supervision": SupervisionLevel.DRAFT_GEN_2},
        {"role": "Executive Intelligence Specialist", "specialization": "EXECUTIVE_INTELLIGENCE", "supervision": SupervisionLevel.READ_ONLY_1},
    ]

    def __init__(self):
        self._workers: Dict[str, AIWorker] = {}
        self._initialize_default_workers()

    def _initialize_default_workers(self):
        """Initializes default pre-configured workers."""
        for tmpl in self.INITIAL_WORKER_TEMPLATES:
            w_code = f"WRK-{tmpl['specialization']}-01"
            self._workers[w_code] = AIWorker(
                worker_code=w_code,
                name=f"Autonomous {tmpl['role']}",
                description=f"Governed AI specialist dedicated to {tmpl['specialization'].replace('_', ' ').lower()} tasks.",
                role=tmpl["role"],
                specialization=tmpl["specialization"],
                supervision_level=tmpl["supervision"],
                status=WorkerStatus.ACTIVE,
                capabilities=[
                    WorkerCapability.READ.value,
                    WorkerCapability.ANALYZE.value,
                    WorkerCapability.GENERATE_DRAFT.value,
                    WorkerCapability.SEARCH.value,
                    WorkerCapability.RETRIEVE_KNOWLEDGE.value,
                ],
                tool_policy={"max_calls_per_task": 10, "allowed_tools": ["search_web", "retrieve_knowledge", "calculate_metrics"]},
                budget_policy={"daily_cost_limit_usd": 15.0, "max_runtime_sec": 120.0},
                grounding_score=0.95,
            )

    def register_worker(
        self,
        name: str,
        role: str,
        specialization: str,
        description: Optional[str] = None,
        supervision_level: SupervisionLevel = SupervisionLevel.DRAFT_GEN_2,
        capabilities: Optional[List[str]] = None,
        owner: str = "system_admin",
        model_name: str = "gemini-1.5-pro",
    ) -> AIWorker:
        """Registers a new AI worker identity under governance rules."""
        worker = AIWorker(
            name=name,
            description=description,
            role=role,
            specialization=specialization,
            supervision_level=supervision_level,
            capabilities=capabilities or [WorkerCapability.READ.value, WorkerCapability.ANALYZE.value],
            owner=owner,
            model_name=model_name,
            status=WorkerStatus.APPROVED,
        )
        self._workers[worker.worker_code] = worker
        return worker

    def get_worker(self, worker_code: str) -> Optional[AIWorker]:
        return self._workers.get(worker_code)

    def list_workers(
        self,
        specialization: Optional[str] = None,
        status: Optional[WorkerStatus] = None,
    ) -> List[AIWorker]:
        res = list(self._workers.values())
        if specialization:
            res = [w for w in res if w.specialization == specialization]
        if status:
            res = [w for w in res if w.status == status]
        return res

    def transition_worker_status(
        self,
        worker_code: str,
        new_status: WorkerStatus,
        reason: Optional[str] = None,
    ) -> AIWorker:
        """Transitions a worker's lifecycle status."""
        worker = self._workers.get(worker_code)
        if not worker:
            raise ValueError(f"Worker {worker_code} not found in registry.")
        
        old_status = worker.status
        worker.status = new_status
        worker.version += 1
        logger.info(f"Worker {worker_code} transitioned from {old_status} to {new_status}. Reason: {reason}")
        return worker
