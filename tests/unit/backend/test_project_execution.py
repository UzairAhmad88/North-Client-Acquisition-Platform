"""Unit tests for Phase 26 — Project Initiation, Delivery Planning & Execution Management."""

import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from app.models.project import (
    Project,
    ProjectTask,
    ProjectMilestone,
    ProjectDeliverable,
    ProjectRisk,
    ProjectBlocker,
    ClientDependency,
    ProjectHealthSnapshot,
    TaskDependency,
    EffortEntry,
)
from agents.project.agent import ProjectAgent
from agents.project.planner import ProjectPlannerEngine
from agents.project.summarizer import ProjectSummarizerEngine
from agents.project.risk_analyzer import ProjectRiskAnalyzer
from agents.project.blocker_analyzer import ProjectBlockerAnalyzer
from agents.project.progress_analyzer import ProjectProgressAnalyzer
from agents.project.scope_monitor import ProjectScopeMonitor
from agents.core.context import AgentContext
from agents.core.permissions import PROHIBITED_PERMISSIONS


def test_project_agent_permissions_guardrails():
    """Verify ProjectAgent permissions deny all autonomous communication or baseline modification side effects."""
    agent = ProjectAgent()
    perms = {p.value for p in agent.get_required_permissions()}

    assert "READ_PROJECT" in perms
    assert "CREATE_PLAN_DRAFT" in perms
    assert "CREATE_STATUS_SUMMARY" in perms

    for prohibited in (
        "SEND_EMAIL",
        "SEND_MESSAGE",
        "MODIFY_BASELINE",
        "CHANGE_CONTRACT",
        "CHANGE_PRICE",
        "APPROVE_SCOPE",
        "APPROVE_CHANGE",
        "SEND_EXTERNAL_MESSAGE",
        "PROMISE_DEADLINE",
    ):
        assert prohibited not in perms
        assert prohibited in PROHIBITED_PERMISSIONS


def test_planner_engine_wbs_generation():
    """Test PERT WBS and milestone generation from baseline deliverables and estimates."""
    planner = ProjectPlannerEngine()

    deliverables = [{"name": "Auth Portal", "description": "JWT authentication system"}]
    estimates = [
        {"name": "Database Schema Setup", "expected_hours": 12.0, "category": "BACKEND"},
        {"name": "Frontend Dashboard UI", "expected_hours": 24.0, "category": "FRONTEND"},
    ]

    plan = planner.generate_draft_plan(
        project_name="Custom CRM Delivery",
        deliverables=deliverables,
        estimate_items=estimates,
    )

    assert plan.project_name == "Custom CRM Delivery"
    assert len(plan.suggested_wbs) == 2
    assert plan.suggested_wbs[0].name == "Database Schema Setup"
    assert plan.suggested_wbs[0].estimated_hours == 12.0
    assert len(plan.suggested_milestones) == 4
    assert plan.confidence_score >= 0.8


def test_progress_analyzer_calculations():
    """Test deterministic task progress and effort variance calculations."""
    analyzer = ProjectProgressAnalyzer()

    tasks = [
        {"status": "COMPLETED", "progress_percent": 100.0, "estimated_hours": 10.0, "actual_hours": 12.0},
        {"status": "IN_PROGRESS", "progress_percent": 50.0, "estimated_hours": 20.0, "actual_hours": 10.0},
        {"status": "TODO", "progress_percent": 0.0, "estimated_hours": 10.0, "actual_hours": 0.0},
    ]

    res = analyzer.calculate_progress(tasks)
    # Total estimated = 40.0, Total actual = 22.0
    # Weighted progress = 10 + 10 + 0 = 20.0 out of 40.0 -> 50.0%
    assert res["overall_progress_percent"] == 50.0
    assert res["completed_count"] == 1
    assert res["total_count"] == 3
    assert res["effort_variance_hours"] == -18.0


def test_risk_analyzer_detection():
    """Test delivery risk detection for overdue tasks and unfulfilled client dependencies."""
    risk_analyzer = ProjectRiskAnalyzer()

    tasks = [
        {"name": "Task 1", "status": "IN_PROGRESS", "is_overdue": True},
        {"name": "Task 2", "status": "TODO", "is_overdue": True},
        {"name": "Task 3", "status": "IN_PROGRESS", "is_overdue": True},
    ]
    milestones = [{"name": "M1", "status": "MISSED"}]
    client_deps = [{"title": "API Keys", "status": "OVERDUE"}]

    risks = risk_analyzer.analyze_risks(tasks, milestones, client_deps)
    assert len(risks) == 3
    titles = [r["title"] for r in risks]
    assert "Multiple Overdue Tasks Threatening Schedule" in titles
    assert "Unfulfilled Client Dependencies" in titles
    assert "Missed Milestone Target" in titles


def test_scope_monitor_signal_detection():
    """Test detection of scope expansion signals against baseline items."""
    monitor = ProjectScopeMonitor()

    baseline_items = [{"name": "Core Dashboard"}]
    tasks = [
        {"name": "Build Native iOS App", "description": "Swift application", "deliverable_id": None}
    ]
    messages = [{"content": "Can we also include a mobile app for iOS?"}]

    signals = monitor.evaluate_scope_signals(baseline_items, tasks, messages)
    assert len(signals) >= 1
    signal_types = [s.signal_type for s in signals]
    assert "NEW_SCOPE_REQUEST" in signal_types or "FEATURE_ADDED" in signal_types


def test_summarizer_engine_output():
    """Test executive project status summary generation."""
    summarizer = ProjectSummarizerEngine()

    project_data = {"id": "prj-123", "name": "E-Commerce System", "status": "IN_PROGRESS", "health": "HEALTHY", "progress_percent": 65.0}
    tasks = [{"status": "COMPLETED"}, {"status": "IN_PROGRESS"}]
    milestones = [{"status": "COMPLETED"}]
    blockers = [{"title": "Payment Gateway Sandbox Issue", "status": "OPEN"}]
    risks = [{"title": "Third party API delay", "status": "IDENTIFIED"}]
    client_deps = [{"title": "Brand Assets", "status": "REQUESTED"}]

    summary = summarizer.summarize_project(project_data, tasks, milestones, blockers, risks, client_deps)
    assert summary.project_id == "prj-123"
    assert summary.health == "HEALTHY"
    assert summary.progress_percent == 65.0
    assert len(summary.active_blockers) == 1
    assert "Payment Gateway Sandbox Issue" in summary.active_blockers[0]


@pytest.mark.asyncio
async def test_project_agent_full_execution():
    """Test full execution of Project AI Agent context."""
    agent = ProjectAgent()
    context = AgentContext(
        workflow_id="wf-test",
        task_id="t-test",
        agent_run_id="run-test",
        metadata={
            "action": "PLAN_WBS",
            "project_name": "Portal Build",
            "deliverables": [{"name": "Auth API"}],
            "estimate_items": [{"name": "Setup DB", "expected_hours": 10.0}],
        },
    )

    result = await agent.execute(context)
    assert "suggested_wbs" in result
    assert result["project_name"] == "Portal Build"
    assert len(result["suggested_wbs"]) == 1

