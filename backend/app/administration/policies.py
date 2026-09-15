"""Centralized Policy Registry and Precedence Evaluation Engine."""

import copy
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.administration.base import (
    PolicyDomain,
    PolicyEvaluationResult,
    PolicyItem,
    PolicyRule,
    PolicyScope,
    PolicyStatus,
)


class PolicyConflictError(Exception):
    pass


class PolicyEngine:
    """Evaluates multi-tier policy precedence, detects conflicts, and guards mandatory security rules."""

    def __init__(self):
        self._policies: Dict[str, PolicyItem] = {}
        self._policy_history: Dict[str, List[PolicyItem]] = {}
        self._seed_default_policies()

    def _seed_default_policies(self):
        """Seed authoritative platform governance policies."""
        policies = [
            PolicyItem(
                policy_id="POL-SEC-GLOBAL-01",
                name="Mandatory Global Security & Tenant Isolation",
                domain=PolicyDomain.SECURITY,
                description="Prohibits any cross-tenant data access, unauthorized credential transfers, or bypass of MFA.",
                scope=PolicyScope.GLOBAL,
                priority=1000,
                status=PolicyStatus.ACTIVE,
                rules=[
                    PolicyRule(
                        rule_id="RULE-SEC-01",
                        name="Strict Tenant Isolation",
                        condition="context.cross_tenant_access == True",
                        action=PolicyEvaluationResult.BLOCK,
                        reason="Cross-tenant access is strictly prohibited by global security policy.",
                        is_mandatory_security=True,
                    ),
                    PolicyRule(
                        rule_id="RULE-SEC-02",
                        name="Step-Up Auth for Recovery & Secrets",
                        condition="action in ['secret.read', 'recovery.execute', 'system_control.kill'] and not context.is_mfa_verified",
                        action=PolicyEvaluationResult.BLOCK,
                        reason="Step-up MFA verification is mandatory for privileged administrative operations.",
                        is_mandatory_security=True,
                    ),
                ],
            ),
            PolicyItem(
                policy_id="POL-COMM-GLOBAL-01",
                name="Communication Guard & Human-in-the-Loop",
                domain=PolicyDomain.COMMUNICATION,
                description="Mandates human approval for all external communications dispatched to prospects or clients.",
                scope=PolicyScope.GLOBAL,
                priority=900,
                status=PolicyStatus.ACTIVE,
                rules=[
                    PolicyRule(
                        rule_id="RULE-COMM-01",
                        name="Outbound Message Human Approval",
                        condition="action == 'send_external_message' and not context.has_human_approval",
                        action=PolicyEvaluationResult.REVIEW,
                        reason="All external customer and prospect communications require human authorization.",
                        is_mandatory_security=True,
                    ),
                ],
            ),
            PolicyItem(
                policy_id="POL-AI-GLOBAL-01",
                name="AI Autonomous Action Prohibitions",
                domain=PolicyDomain.AI,
                description="Restricts AI agents to proposing drafts; prohibits autonomous financial or contract actions.",
                scope=PolicyScope.GLOBAL,
                priority=950,
                status=PolicyStatus.ACTIVE,
                rules=[
                    PolicyRule(
                        rule_id="RULE-AI-01",
                        name="AI Financial Mutation Prohibition",
                        condition="actor_type == 'ai_agent' and action in ['payment.execute', 'refund.issue', 'contract.sign', 'security.modify']",
                        action=PolicyEvaluationResult.BLOCK,
                        reason="AI agents are strictly forbidden from autonomous financial or security mutations.",
                        is_mandatory_security=True,
                    ),
                ],
            ),
            PolicyItem(
                policy_id="POL-FIN-GLOBAL-01",
                name="Financial Controls & Dual Authorization",
                domain=PolicyDomain.FINANCE,
                description="Enforces approval thresholds on refunds, discounts, and invoice write-offs.",
                scope=PolicyScope.GLOBAL,
                priority=850,
                status=PolicyStatus.ACTIVE,
                rules=[
                    PolicyRule(
                        rule_id="RULE-FIN-01",
                        name="High-Value Refund Dual Approval",
                        condition="action == 'refund.issue' and float(amount or 0) > 1000.0 and not context.dual_approved",
                        action=PolicyEvaluationResult.REVIEW,
                        reason="Refunds exceeding $1,000 require dual managerial sign-off.",
                        is_mandatory_security=False,
                    ),
                ],
            ),
        ]
        for p in policies:
            self._policies[p.policy_id] = p
            self._policy_history[p.policy_id] = [copy.deepcopy(p)]

    def register_policy(self, policy: PolicyItem) -> PolicyItem:
        """Register a new policy with conflict and security validation."""
        self._check_for_security_weakening(policy)
        self._policies[policy.policy_id] = policy
        if policy.policy_id not in self._policy_history:
            self._policy_history[policy.policy_id] = [copy.deepcopy(policy)]
        return policy

    def _check_for_security_weakening(self, new_policy: PolicyItem):
        """Prevent any lower-level policy from weakening mandatory global security rules."""
        if new_policy.scope != PolicyScope.GLOBAL:
            for rule in new_policy.rules:
                if rule.action == PolicyEvaluationResult.ALLOW and rule.is_mandatory_security:
                    raise PolicyConflictError(
                        f"Policy '{new_policy.name}' cannot grant ALLOW for mandatory security constraint '{rule.name}'"
                    )

    def list_policies(self, domain: Optional[PolicyDomain] = None) -> List[PolicyItem]:
        """List all registered policies, optionally filtered by domain."""
        if domain:
            return [p for p in self._policies.values() if p.domain == domain]
        return list(self._policies.values())

    def get_policy(self, policy_id: str) -> Optional[PolicyItem]:
        """Retrieve policy by ID."""
        return self._policies.get(policy_id)

    def evaluate_action(
        self,
        domain: PolicyDomain,
        action: str,
        actor_type: str = "user",
        context: Optional[Dict[str, Any]] = None,
        amount: Optional[float] = None,
    ) -> Tuple[PolicyEvaluationResult, str]:
        """Evaluate action across matching policies ordered by priority (highest priority first)."""
        context = context or {}
        matching_policies = [p for p in self._policies.values() if p.domain == domain and p.status == PolicyStatus.ACTIVE]
        # Sort descending by priority
        matching_policies.sort(key=lambda p: p.priority, reverse=True)

        for policy in matching_policies:
            for rule in policy.rules:
                # Evaluate rule conditions
                triggered = False
                if "cross_tenant_access" in rule.condition and context.get("cross_tenant_access"):
                    triggered = True
                elif "actor_type == 'ai_agent'" in rule.condition and actor_type == "ai_agent":
                    if any(act in action for act in ["payment", "refund", "contract.sign", "security"]):
                        triggered = True
                elif "send_external_message" in rule.condition and action == "send_external_message":
                    if not context.get("has_human_approval"):
                        triggered = True
                elif "refund.issue" in rule.condition and action == "refund.issue":
                    if float(amount or 0) > 1000.0 and not context.get("dual_approved"):
                        triggered = True
                elif "is_mfa_verified" in rule.condition and not context.get("is_mfa_verified"):
                    if any(act in action for act in ["secret.read", "recovery.execute", "system_control.kill"]):
                        triggered = True

                if triggered:
                    return rule.action, f"Policy '{policy.name}' Rule '{rule.name}': {rule.reason}"

        return PolicyEvaluationResult.ALLOW, "Action permitted by standard governance baseline."

    def detect_conflicts(self, proposed_rule: PolicyRule, scope: PolicyScope) -> List[str]:
        """Detect potential policy conflicts before activating a new policy rule."""
        conflicts = []
        if scope != PolicyScope.GLOBAL and proposed_rule.is_mandatory_security and proposed_rule.action == PolicyEvaluationResult.ALLOW:
            conflicts.append(f"Rule '{proposed_rule.name}' attempts to permit a prohibited security condition at scope {scope}.")
        return conflicts
