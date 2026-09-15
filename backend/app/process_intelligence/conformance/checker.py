"""
Process Conformance Checker for Phase 49: Detects deviations between expected process rules and observed event traces.
"""

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.process_intelligence.base import ConformanceViolation, ViolationType
    from backend.app.process_intelligence.event_log.store import ProcessEventLogStore
except ImportError:
    from app.process_intelligence.base import ConformanceViolation, ViolationType
    from app.process_intelligence.event_log.store import ProcessEventLogStore


class ProcessConformanceChecker:
    """Evaluates case event logs against conformance rules (mandatory steps, ordering, approvals, loops)."""

    def __init__(self, event_store: ProcessEventLogStore):
        self.event_store = event_store
        self._rules: Dict[str, Dict[str, Any]] = {}

    def register_rule(
        self,
        rule_id: str,
        process_id: str,
        rule_code: str,
        rule_type: str,
        source_activity: Optional[str] = None,
        target_activity: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        severity: str = "HIGH",
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        """Registers a conformance rule for a process definition."""
        rule = {
            "id": rule_id,
            "process_id": process_id,
            "rule_code": rule_code,
            "rule_type": rule_type,  # MANDATORY_STEP, STRICT_ORDER, REQUIRED_APPROVAL, MAX_REPETITIONS
            "source_activity": source_activity,
            "target_activity": target_activity,
            "parameters": parameters or {},
            "severity": severity,
            "tenant_id": tenant_id,
        }
        self._rules[rule_id] = rule
        return rule

    def check_case_conformance(
        self,
        process_id: str,
        case_id: str,
        tenant_id: str = "default_tenant",
    ) -> List[ConformanceViolation]:
        """Checks a single case for conformance violations against all active rules."""
        events = self.event_store.get_events_for_case(case_id, tenant_id)
        if not events:
            return []

        activities = [e.activity for e in events]
        violations: List[ConformanceViolation] = []

        # Get relevant rules for this process
        rules = [r for r in self._rules.values() if r["process_id"] == process_id and r["tenant_id"] == tenant_id]

        for rule in rules:
            rule_type = rule["rule_type"]
            src = rule.get("source_activity")
            tgt = rule.get("target_activity")
            severity = rule.get("severity", "HIGH")
            rule_id = rule["id"]

            # 1. MANDATORY_STEP check
            if rule_type == "MANDATORY_STEP" and src:
                if src not in activities:
                    violations.append(
                        ConformanceViolation(
                            id=str(uuid.uuid4()),
                            tenant_id=tenant_id,
                            process_id=process_id,
                            case_id=case_id,
                            rule_id=rule_id,
                            violation_code=f"VIOL-SKIPPED-{uuid.uuid4().hex[:6].upper()}",
                            violation_type=ViolationType.SKIPPED_STEP,
                            detected_at=datetime.now(timezone.utc),
                            activity_involved=src,
                            severity=severity,
                            description=f"Mandatory activity '{src}' was skipped in case execution.",
                            evidence_payload={"observed_sequence": activities, "missing_step": src},
                        )
                    )

            # 2. REQUIRED_APPROVAL check (e.g. Proposal -> Approval -> Send)
            elif rule_type == "REQUIRED_APPROVAL" and src and tgt:
                # If tgt occurred, src MUST have occurred strictly before tgt
                if tgt in activities:
                    if src not in activities:
                        violations.append(
                            ConformanceViolation(
                                id=str(uuid.uuid4()),
                                tenant_id=tenant_id,
                                process_id=process_id,
                                case_id=case_id,
                                rule_id=rule_id,
                                violation_code=f"VIOL-APPR-BYPASS-{uuid.uuid4().hex[:6].upper()}",
                                violation_type=ViolationType.MISSING_APPROVAL,
                                detected_at=datetime.now(timezone.utc),
                                activity_involved=tgt,
                                severity="CRITICAL",
                                description=f"Required approval '{src}' was bypassed before executing '{tgt}'.",
                                evidence_payload={"bypassed_approval": src, "triggered_activity": tgt},
                            )
                        )
                    else:
                        src_idx = activities.index(src)
                        tgt_idx = activities.index(tgt)
                        if src_idx > tgt_idx:
                            violations.append(
                                ConformanceViolation(
                                    id=str(uuid.uuid4()),
                                    tenant_id=tenant_id,
                                    process_id=process_id,
                                    case_id=case_id,
                                    rule_id=rule_id,
                                    violation_code=f"VIOL-ORDER-{uuid.uuid4().hex[:6].upper()}",
                                    violation_type=ViolationType.OUT_OF_ORDER,
                                    detected_at=datetime.now(timezone.utc),
                                    activity_involved=tgt,
                                    severity=severity,
                                    description=f"Required step '{src}' occurred after '{tgt}' instead of preceding it.",
                                    evidence_payload={"source_step": src, "target_step": tgt},
                                )
                            )

            # 3. MAX_REPETITIONS (loop constraint)
            elif rule_type == "MAX_REPETITIONS" and src:
                max_allowed = rule.get("parameters", {}).get("max_repetitions", 1)
                count = activities.count(src)
                if count > max_allowed:
                    violations.append(
                        ConformanceViolation(
                            id=str(uuid.uuid4()),
                            tenant_id=tenant_id,
                            process_id=process_id,
                            case_id=case_id,
                            rule_id=rule_id,
                            violation_code=f"VIOL-LOOP-{uuid.uuid4().hex[:6].upper()}",
                            violation_type=ViolationType.UNEXPECTED_LOOP,
                            detected_at=datetime.now(timezone.utc),
                            activity_involved=src,
                            severity=severity,
                            description=f"Activity '{src}' repeated {count} times, exceeding max threshold of {max_allowed}.",
                            evidence_payload={"activity": src, "occurrences": count, "max_allowed": max_allowed},
                        )
                    )

        return violations

    def check_process_conformance(
        self,
        process_id: str,
        tenant_id: str = "default_tenant",
    ) -> List[ConformanceViolation]:
        """Runs conformance checking over all cases in a process."""
        cases = self.event_store.get_cases_for_process(process_id, tenant_id)
        all_violations: List[ConformanceViolation] = []
        for case in cases:
            if case.id:
                violations = self.check_case_conformance(process_id, case.id, tenant_id)
                all_violations.extend(violations)
        return all_violations
