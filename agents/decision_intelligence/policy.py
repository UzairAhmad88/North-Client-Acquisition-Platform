"""Decision Policy Engine & Deterministic Rule Enforcement Layer."""

from typing import Any, Dict, Optional
from agents.decision_intelligence.models import DecisionSupportDraft, PredictionDraft


class DecisionPolicyEngine:
    """Enforces the 'Rules Before AI' paradigm and transforms predictions into human decision support."""

    def evaluate_deterministic_rules(
        self,
        prediction_type: str,
        entity_context: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Check for authoritative deterministic business rules that strictly supersede AI predictions."""
        # 1. QA Release Blocking Rule
        if prediction_type == "PROJECT_DELAY" or entity_context.get("action_context") == "RELEASE_APPROVAL":
            if int(entity_context.get("open_critical_defects_count") or 0) > 0:
                return {
                    "rule_key": "CRITICAL_DEFECT_RELEASE_BLOCK",
                    "action": "BLOCK_RELEASE",
                    "reason": "Deterministic rule: 1 or more open critical defects exist. Release is strictly blocked regardless of model predictions.",
                }

        # 2. Outreach Opt-Out Rule
        if prediction_type == "LEAD_CONVERSION" or entity_context.get("action_context") == "OUTREACH":
            if bool(entity_context.get("is_opted_out") or entity_context.get("dnc_registered")):
                return {
                    "rule_key": "DNC_REGISTRY_BLOCK",
                    "action": "BLOCK_COMMUNICATION",
                    "reason": "Deterministic rule: Contact is registered in Do-Not-Contact registry. All outreach is blocked.",
                }

        # 3. Contract Unsigned Execution Rule
        if entity_context.get("action_context") == "START_PROJECT":
            if not bool(entity_context.get("contract_signed")):
                return {
                    "rule_key": "UNSIGNED_CONTRACT_BLOCK",
                    "action": "BLOCK_INITIATION",
                    "reason": "Deterministic rule: Project baseline and contract signatures are missing.",
                }

        return None

    def formulate_decision_support(
        self,
        prediction: PredictionDraft,
        entity_context: Dict[str, Any],
    ) -> DecisionSupportDraft:
        """Combine prediction probability, evidence, and deterministic rules into a reviewable decision draft."""
        det_rule = self.evaluate_deterministic_rules(prediction.prediction_type, entity_context)

        if det_rule:
            return DecisionSupportDraft(
                prediction_type=prediction.prediction_type,
                entity_id=prediction.entity_id,
                title=f"Deterministic Rule Triggered: {det_rule['rule_key']}",
                recommended_action=f"Mandatory Action: {det_rule['action']} - {det_rule['reason']}",
                tradeoff_analysis="Deterministic policy rule overrides all statistical predictions.",
                urgency="CRITICAL",
                governing_policy="DETERMINISTIC_OVERRIDE_POLICY",
                deterministic_override_applied=True,
                deterministic_rule_notes=det_rule["reason"],
            )

        # Standard Probabilistic Decision Support
        p_type = prediction.prediction_type
        prob = prediction.probability
        risk_band = prediction.risk_band

        if p_type == "PROJECT_DELAY":
            if prob >= 0.65:
                action = "Schedule urgent project blocker triage and review task dependency critical path."
                tradeoff = "May require reallocating senior engineering effort from upcoming sprint planning."
                urgency = "HIGH"
            else:
                action = "Maintain standard sprint cadence; monitor dependency resolution."
                tradeoff = "Standard operational routine; low overhead."
                urgency = "LOW"

        elif p_type == "LEAD_CONVERSION":
            if prob >= 0.70:
                action = "Fast-track personalized discovery call booking with dedicated technical lead."
                tradeoff = "Prioritizes high-potential opportunity over lower-probability outreach queues."
                urgency = "HIGH"
            else:
                action = "Nurture lead via scheduled follow-up sequence."
                tradeoff = "Conserves direct sales engineering bandwidth."
                urgency = "LOW"

        elif p_type == "PROJECT_EFFORT_VARIANCE":
            if prob >= 0.60:
                action = "Conduct technical estimation buffer review before contract finalization."
                tradeoff = "Adds 24h to proposal timeline but mitigates delivery margin erosion."
                urgency = "MEDIUM"
            else:
                action = "Proceed with approved baseline estimation."
                tradeoff = "Maintains commercial momentum."
                urgency = "LOW"

        elif p_type == "CLIENT_RETENTION":
            if prob >= 0.60:
                action = "Assign Client Success Manager for proactive health review and incident postmortem."
                tradeoff = "Dedicates operational hours to relationship stabilization."
                urgency = "HIGH"
            else:
                action = "Continue standard quarterly check-in schedule."
                tradeoff = "Standard relationship maintenance."
                urgency = "LOW"

        else:
            action = f"Review {p_type.replace('_', ' ').lower()} indicators."
            tradeoff = "General operational review."
            urgency = risk_band

        return DecisionSupportDraft(
            prediction_type=p_type,
            entity_id=prediction.entity_id,
            title=f"Decision Support: {p_type.replace('_', ' ').title()} ({risk_band} Risk / {int(prob*100)}%)",
            recommended_action=action,
            tradeoff_analysis=tradeoff,
            urgency=urgency,
            governing_policy=f"{p_type}_POLICY_v1.0",
            deterministic_override_applied=False,
            deterministic_rule_notes=None,
        )
