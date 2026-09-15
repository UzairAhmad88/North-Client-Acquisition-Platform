"""
Global Problem-Solving Engine & Open Marketplace Service (Phase 96)
Handles problem taxonomy, solution graphs, implementation readiness, open problem publishing, safe-to-fail experiments, and failure database indexing.
"""

from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime


class ProblemSolvingMarketplaceService:
    def __init__(self):
        self.published_problems: Dict[str, Dict[str, Any]] = {}
        self.failure_database: List[Dict[str, Any]] = []

    def publish_civilization_problem(
        self,
        title: str,
        category: str,  # Climate, Energy, Health, Food, Water, Education, Governance, etc.
        problem_description: str,
        subproblems: List[str],
        publishing_institution: str,
    ) -> Dict[str, Any]:
        prob_id = f"prb-{uuid.uuid4().hex[:8]}"
        problem = {
            "problem_id": prob_id,
            "title": title,
            "category": category,
            "description": problem_description,
            "subproblems": subproblems,
            "publishing_institution": publishing_institution,
            "submitted_solutions": [],
            "status": "Open_For_Submissions",
            "created_at": datetime.utcnow().isoformat(),
        }
        self.published_problems[prob_id] = problem
        return problem

    def submit_solution_proposal(
        self,
        problem_id: str,
        solution_title: str,
        proposer: str,
        readiness_stage: str,  # Research, Prototype, Pilot, Deployable, Scaled, Mature
        solution_graph: Dict[str, Any],
        is_safe_to_fail: bool = True,
    ) -> Dict[str, Any]:
        prob = self.published_problems.get(problem_id)
        if not prob:
            return {"status": "error", "message": f"Problem {problem_id} not found"}
        
        sol_id = f"sol-{uuid.uuid4().hex[:8]}"
        proposal = {
            "solution_id": sol_id,
            "problem_id": problem_id,
            "solution_title": solution_title,
            "proposer": proposer,
            "readiness_stage": readiness_stage,
            "solution_graph": solution_graph,
            "is_safe_to_fail": is_safe_to_fail,
            "review_status": "Peer_Review_In_Progress",
            "submitted_at": datetime.utcnow().isoformat(),
        }
        prob["submitted_solutions"].append(proposal)
        return proposal

    def log_failed_experiment_to_database(
        self,
        project_title: str,
        category: str,
        failure_type: str,
        root_cause_analysis: str,
        lessons_learned: str,
    ) -> Dict[str, Any]:
        record_id = f"fail-{uuid.uuid4().hex[:8]}"
        record = {
            "record_id": record_id,
            "project_title": project_title,
            "category": category,
            "failure_type": failure_type,
            "root_cause_analysis": root_cause_analysis,
            "lessons_learned": lessons_learned,
            "converted_to_knowledge_asset": True,
            "logged_at": datetime.utcnow().isoformat(),
        }
        self.failure_database.append(record)
        return record
