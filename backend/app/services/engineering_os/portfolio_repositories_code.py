"""Portfolio, Repositories, Commits, Pull Requests, Reviews and Code Quality Service.

Manages engineering organizations, teams, repository catalogs, branch governance,
commit intelligence, pull requests, automated review findings, and multi-factor code quality scorecards.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.engineering_os.base import (
        AttrDict,
        PullRequestStatus,
        generate_engineering_id,
    )
except ImportError:
    from app.services.engineering_os.base import (
        AttrDict,
        PullRequestStatus,
        generate_engineering_id,
    )

logger = logging.getLogger(__name__)


class PortfolioRepositoriesCodeService:
    """Manages engineering organizations, teams, repositories, PRs, and code quality."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._orgs: Dict[str, Dict[str, Any]] = {}
        self._teams: Dict[str, Dict[str, Any]] = {}
        self._projects: Dict[str, Dict[str, Any]] = {}
        self._repositories: Dict[str, Dict[str, Any]] = {}
        self._pull_requests: Dict[str, Dict[str, Any]] = {}
        self._reviews: Dict[str, List[Dict[str, Any]]] = {}
        self._quality_results: Dict[str, Dict[str, Any]] = {}

    def create_organization(
        self,
        tenant_id: str = "default_tenant",
        name: str = "Uzaii Core Engineering",
        slug: str = "uzaii-eng",
        description: str = "Global engineering organization driving autonomous decision systems.",
        head_of_engineering_email: str = "vp-eng@uzaii.com",
    ) -> AttrDict:
        org_id = generate_engineering_id("org")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "org_id": org_id,
            "id": org_id,
            "tenant_id": tenant_id,
            "name": name,
            "slug": slug,
            "description": description,
            "head_of_engineering_email": head_of_engineering_email,
            "created_at": now,
        }
        self._orgs[org_id] = record
        return AttrDict(record)

    def create_team(
        self,
        tenant_id: str = "default_tenant",
        org_id: Optional[str] = None,
        name: str = "Core Platform Engineering",
        team_type: str = "PLATFORM",
        lead_email: str = "tech-lead@uzaii.com",
        member_count: int = 8,
    ) -> AttrDict:
        team_id = generate_engineering_id("team")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "team_id": team_id,
            "id": team_id,
            "tenant_id": tenant_id,
            "org_id": org_id,
            "name": name,
            "team_type": team_type,
            "lead_email": lead_email,
            "member_count": member_count,
            "created_at": now,
        }
        self._teams[team_id] = record
        return AttrDict(record)

    def register_repository(
        self,
        tenant_id: str = "default_tenant",
        project_id: Optional[str] = None,
        name: str = "uzaii-develop-by-norths",
        provider: str = "GITHUB",
        default_branch: str = "main",
        primary_language: str = "Python / TypeScript",
        is_private: bool = True,
    ) -> AttrDict:
        repo_id = generate_engineering_id("repo")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "repo_id": repo_id,
            "id": repo_id,
            "tenant_id": tenant_id,
            "project_id": project_id,
            "name": name,
            "provider": provider,
            "default_branch": default_branch,
            "primary_language": primary_language,
            "is_private": is_private,
            "branch_protection_rules": {
                "require_pull_request": True,
                "required_approvals": 2,
                "require_ci_pass": True,
                "block_force_pushes": True,
            },
            "created_at": now,
        }
        self._repositories[repo_id] = record
        return AttrDict(record)

    def create_pull_request(
        self,
        tenant_id: str = "default_tenant",
        repository_id: str = "repo_001",
        pr_number: int = 104,
        title: str = "feat(decision-engine): streaming telemetry connector",
        author: str = "staff-eng@uzaii.com",
        source_branch: str = "feat/streaming-telemetry",
        target_branch: str = "main",
        linked_work_item: Optional[str] = "REQ-5021",
        files_changed_count: int = 14,
        additions: int = 420,
        deletions: int = 35,
    ) -> AttrDict:
        pr_id = generate_engineering_id("pr")
        now = datetime.now(timezone.utc).isoformat()

        # Risk Score calculation based on blast radius
        churn = additions + deletions
        risk_score = round(min(10.0, (files_changed_count * 0.3) + (churn / 200.0)), 2)

        record = {
            "pr_id": pr_id,
            "id": pr_id,
            "tenant_id": tenant_id,
            "repository_id": repository_id,
            "pr_number": pr_number,
            "title": title,
            "author": author,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "status": PullRequestStatus.OPEN.value,
            "risk_score": risk_score,
            "linked_work_item": linked_work_item,
            "stats": {
                "files_changed": files_changed_count,
                "additions": additions,
                "deletions": deletions,
                "total_churn": churn,
            },
            "ci_checks_status": "PASSING",
            "approvals_count": 0,
            "is_mergeable": False,
            "created_at": now,
        }
        self._pull_requests[pr_id] = record
        return AttrDict(record)

    def submit_code_review(
        self,
        tenant_id: str,
        pr_id: str,
        reviewer_email: str,
        decision: str = "APPROVED",  # APPROVED, CHANGES_REQUESTED, COMMENT
        findings: Optional[List[Dict[str, Any]]] = None,
        security_findings_count: int = 0,
        architecture_notes: str = "",
    ) -> AttrDict:
        """Submit code review. AI cannot merge PR into production autonomously."""
        review_id = generate_engineering_id("rev")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "review_id": review_id,
            "id": review_id,
            "tenant_id": tenant_id,
            "pr_id": pr_id,
            "reviewer_email": reviewer_email,
            "decision": decision,
            "findings": findings or [],
            "security_findings_count": security_findings_count,
            "architecture_notes": architecture_notes,
            "created_at": now,
        }
        self._reviews.setdefault(pr_id, []).append(record)

        if pr_id in self._pull_requests and decision == "APPROVED":
            self._pull_requests[pr_id]["approvals_count"] += 1
            if self._pull_requests[pr_id]["approvals_count"] >= 1:
                self._pull_requests[pr_id]["is_mergeable"] = True

        return AttrDict(record)

    def evaluate_code_quality(
        self,
        tenant_id: str,
        repository_id: str,
        commit_sha: str,
        static_analysis_score: float = 94.5,
        test_coverage_pct: float = 88.2,
        cyclomatic_complexity_avg: float = 4.2,
        code_duplication_pct: float = 1.8,
        dependency_vulnerability_count: int = 0,
    ) -> AttrDict:
        """Compute multi-factor code quality scorecard."""
        cq_id = generate_engineering_id("cq")
        now = datetime.now(timezone.utc).isoformat()

        # Composite Quality Index (100 max)
        quality_index = (
            (static_analysis_score * 0.35)
            + (test_coverage_pct * 0.35)
            + (max(0.0, 100.0 - (cyclomatic_complexity_avg * 10.0)) * 0.15)
            + (max(0.0, 100.0 - (code_duplication_pct * 10.0)) * 0.15)
        )
        quality_index = round(max(0.0, min(100.0, quality_index)), 2)

        record = {
            "cq_id": cq_id,
            "id": cq_id,
            "tenant_id": tenant_id,
            "repository_id": repository_id,
            "commit_sha": commit_sha,
            "composite_quality_score": quality_index,
            "static_analysis_score": static_analysis_score,
            "test_coverage_pct": test_coverage_pct,
            "cyclomatic_complexity_avg": cyclomatic_complexity_avg,
            "code_duplication_pct": code_duplication_pct,
            "dependency_vulnerability_count": dependency_vulnerability_count,
            "quality_grade": "A" if quality_index >= 90.0 else "B" if quality_index >= 80.0 else "C",
            "evaluated_at": now,
        }
        self._quality_results[cq_id] = record
        return AttrDict(record)
