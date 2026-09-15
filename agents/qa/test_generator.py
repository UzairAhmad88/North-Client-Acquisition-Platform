"""Test Case Generator Engine for drafting structured QA test cases."""

from typing import Any, Dict, List, Optional
from agents.qa.models import TestCaseDraftResult, TestCaseItem


class TestGeneratorEngine:
    """Drafts comprehensive test cases based on project requirements and deliverable specs."""

    def generate_test_cases(
        self,
        test_plan_id: str,
        requirements: Optional[List[Dict[str, Any]]] = None,
        deliverables: Optional[List[Dict[str, Any]]] = None,
    ) -> TestCaseDraftResult:
        """Draft automated and manual test cases for given requirements and deliverables."""
        requirements = requirements or []
        deliverables = deliverables or []

        cases: List[TestCaseItem] = []
        counter = 1

        for req in requirements:
            req_id = req.get("id")
            req_title = req.get("title", "Requirement")
            req_desc = req.get("description", "")

            # Happy path test case
            cases.append(
                TestCaseItem(
                    code=f"TC-REQ-{counter:03d}-01",
                    title=f"Verify {req_title} - Functional Baseline",
                    description=f"Validate that core functional requirements for '{req_title}' are fulfilled as described: {req_desc[:100]}",
                    category="FUNCTIONAL",
                    priority="HIGH" if req.get("priority") == "HIGH" else "MEDIUM",
                    execution_type="AUTOMATED",
                    preconditions="System environment initialized and target module deployed.",
                    steps=[
                        {"step_number": 1, "action": "Trigger requirement entrypoint", "expected": "Input parameters accepted without validation error"},
                        {"step_number": 2, "action": "Execute baseline scenario", "expected": "Output matches required specification"},
                    ],
                    expected_results=f"Successful execution meeting requirement criteria for '{req_title}'.",
                    is_regression=True,
                    requirement_id=req_id,
                )
            )

            # Negative / edge case test case
            cases.append(
                TestCaseItem(
                    code=f"TC-REQ-{counter:03d}-02",
                    title=f"Verify {req_title} - Invalid Input & Boundary Error Handling",
                    description=f"Validate system resilience and error handling for '{req_title}' when malformed inputs are submitted.",
                    category="SECURITY",
                    priority="MEDIUM",
                    execution_type="AUTOMATED",
                    preconditions="System active.",
                    steps=[
                        {"step_number": 1, "action": "Submit invalid payload", "expected": "HTTP 400 or explicit validation error returned"},
                        {"step_number": 2, "action": "Verify exception logging", "expected": "Error logged securely without sensitive leaks"},
                    ],
                    expected_results="Graceful error response with appropriate status code.",
                    is_regression=True,
                    requirement_id=req_id,
                )
            )
            counter += 1

        for deliv in deliverables:
            deliv_id = deliv.get("id")
            deliv_title = deliv.get("title", "Deliverable")

            cases.append(
                TestCaseItem(
                    code=f"TC-DELIV-{counter:03d}",
                    title=f"Deliverable Acceptance Verification - {deliv_title}",
                    description=f"Verify acceptance criteria for deliverable artifact '{deliv_title}'.",
                    category="UAT",
                    priority="HIGH",
                    execution_type="MANUAL",
                    preconditions="Deliverable package built and deployed to staging environment.",
                    steps=[
                        {"step_number": 1, "action": "Inspect deliverable package and documentation", "expected": "All assets present and checksums match"},
                        {"step_number": 2, "action": "Perform end-to-end acceptance review", "expected": "Meets approved scope criteria"},
                    ],
                    expected_results=f"Deliverable '{deliv_title}' verified against baseline criteria.",
                    is_regression=False,
                    deliverable_id=deliv_id,
                )
            )
            counter += 1

        if not cases:
            # Fallback default test case
            cases.append(
                TestCaseItem(
                    code="TC-GEN-001",
                    title="Sanity & Deployment Verification",
                    description="General application launch and health check test.",
                    category="FUNCTIONAL",
                    priority="CRITICAL",
                    execution_type="AUTOMATED",
                    preconditions="Server instance online.",
                    steps=[
                        {"step_number": 1, "action": "GET /health endpoint", "expected": "HTTP 200 OK with status UP"}
                    ],
                    expected_results="Health check returns HTTP 200 OK.",
                    is_regression=True,
                )
            )

        return TestCaseDraftResult(
            test_plan_id=test_plan_id,
            generated_test_cases=cases,
            total_count=len(cases),
            confidence=0.95,
        )
