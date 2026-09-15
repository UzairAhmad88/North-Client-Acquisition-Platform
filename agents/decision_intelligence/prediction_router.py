"""Predictive Inference Router & Baseline Predictive Models."""

from typing import Any, Dict, List, Optional
import math
from agents.decision_intelligence.models import PredictionDraft


class PredictionRouter:
    """Dispatches predictive inference requests across production baseline models."""

    # Model Version Constants
    LEAD_CONV_VERSION = "v1.0-baseline"
    PROJECT_DELAY_VERSION = "v1.0-baseline"
    ESTIMATION_RISK_VERSION = "v1.0-baseline"
    SCOPE_CHANGE_VERSION = "v1.0-baseline"
    SUPPORT_DEMAND_VERSION = "v1.0-baseline"
    CLIENT_RETENTION_VERSION = "v1.0-baseline"

    def predict_lead_conversion(self, lead_id: str, features: Dict[str, Any]) -> PredictionDraft:
        """Estimate lead conversion probability using calibrated multi-factor baseline."""
        lead_score = float(features.get("lead_score") or features.get("score") or 50.0)
        has_response = bool(features.get("has_response") or features.get("responded"))
        service_fit_score = float(features.get("service_fit_score") or 60.0)
        interaction_count = int(features.get("interaction_count") or 0)

        # Baseline probability function
        base_p = (lead_score / 100.0) * 0.5 + (service_fit_score / 100.0) * 0.3
        if has_response:
            base_p += 0.15
        if interaction_count >= 2:
            base_p += 0.05

        prob = min(0.95, max(0.05, round(base_p, 2)))
        half_width = 0.08
        conf_int = {"lower": max(0.0, round(prob - half_width, 2)), "upper": min(1.0, round(prob + half_width, 2))}

        risk_band = "HIGH" if prob >= 0.70 else ("MEDIUM" if prob >= 0.40 else "LOW")

        drivers = [
            {"feature": "lead_score", "value": lead_score, "impact": f"+{(lead_score/100)*0.5:.2f}"},
            {"feature": "service_fit_score", "value": service_fit_score, "impact": f"+{(service_fit_score/100)*0.3:.2f}"},
            {"feature": "client_responded", "value": has_response, "impact": "+0.15" if has_response else "0.00"},
        ]

        summary = (
            f"Historical model estimates a {int(prob * 100)}% probability of conversion (interval: {int(conf_int['lower']*100)}%–{int(conf_int['upper']*100)}%). "
            f"Primary positive signals: lead quality score ({lead_score}) and service alignment."
        )

        return PredictionDraft(
            prediction_type="LEAD_CONVERSION",
            entity_id=lead_id,
            probability=prob,
            risk_band=risk_band,
            confidence_interval=conf_int,
            model_version=self.LEAD_CONV_VERSION,
            key_drivers=drivers,
            summary_text=summary,
            safety_notes=["Probabilistic baseline estimate. Never guarantees deal closing."],
        )

    def predict_project_delay(self, project_id: str, features: Dict[str, Any]) -> PredictionDraft:
        """Estimate project schedule overrun risk from task dependencies, blockers, and scope changes."""
        blocked_tasks = int(features.get("blocked_tasks_count") or 0)
        unresolved_reqs = int(features.get("unresolved_requirements_count") or 0)
        scope_changes = int(features.get("active_scope_changes_count") or 0)
        past_variance_pct = float(features.get("historical_service_variance_pct") or 10.0)

        # Base risk calculation
        risk_score = 0.15
        if blocked_tasks > 0:
            risk_score += min(0.35, blocked_tasks * 0.10)
        if unresolved_reqs > 0:
            risk_score += min(0.25, unresolved_reqs * 0.08)
        if scope_changes > 0:
            risk_score += min(0.20, scope_changes * 0.07)
        if past_variance_pct > 15.0:
            risk_score += 0.10

        prob = min(0.95, max(0.05, round(risk_score, 2)))
        conf_int = {"lower": max(0.0, round(prob - 0.07, 2)), "upper": min(1.0, round(prob + 0.07, 2))}

        if prob >= 0.75:
            risk_band = "CRITICAL" if blocked_tasks >= 3 else "HIGH"
        elif prob >= 0.45:
            risk_band = "MEDIUM"
        else:
            risk_band = "LOW"

        drivers = [
            {"feature": "blocked_tasks_count", "value": blocked_tasks, "impact": f"+{min(0.35, blocked_tasks * 0.10):.2f}"},
            {"feature": "unresolved_requirements", "value": unresolved_reqs, "impact": f"+{min(0.25, unresolved_reqs * 0.08):.2f}"},
            {"feature": "active_scope_changes", "value": scope_changes, "impact": f"+{min(0.20, scope_changes * 0.07):.2f}"},
        ]

        summary = (
            f"Historical delay risk model estimates a {int(prob * 100)}% likelihood of schedule delay ({risk_band} Risk). "
            f"Key contributing factors: {blocked_tasks} blocked tasks and {unresolved_reqs} unresolved requirements."
        )

        return PredictionDraft(
            prediction_type="PROJECT_DELAY",
            entity_id=project_id,
            probability=prob,
            risk_band=risk_band,
            confidence_interval=conf_int,
            model_version=self.PROJECT_DELAY_VERSION,
            key_drivers=drivers,
            summary_text=summary,
            safety_notes=["Internal decision support only. Never automatically alter client milestone commitments."],
        )

    def predict_estimation_risk(self, estimate_id: str, features: Dict[str, Any]) -> PredictionDraft:
        """Estimate likelihood of material effort underestimation (>15% overrun)."""
        integration_count = int(features.get("integrations_count") or 0)
        has_ai_components = bool(features.get("has_ai_components") or False)
        unclear_req_pct = float(features.get("unclear_requirements_pct") or 0.0)
        complexity = str(features.get("complexity") or "MEDIUM").upper()

        risk_p = 0.10
        if complexity == "HIGH":
            risk_p += 0.25
        elif complexity == "VERY_HIGH":
            risk_p += 0.40

        if integration_count >= 3:
            risk_p += 0.20
        if has_ai_components:
            risk_p += 0.15
        if unclear_req_pct > 20.0:
            risk_p += 0.15

        prob = min(0.95, max(0.05, round(risk_p, 2)))
        risk_band = "HIGH" if prob >= 0.65 else ("MEDIUM" if prob >= 0.35 else "LOW")

        drivers = [
            {"feature": "complexity", "value": complexity, "impact": "+0.25" if complexity in ("HIGH", "VERY_HIGH") else "0.00"},
            {"feature": "third_party_integrations", "value": integration_count, "impact": "+0.20" if integration_count >= 3 else "0.00"},
            {"feature": "has_ai_components", "value": has_ai_components, "impact": "+0.15" if has_ai_components else "0.00"},
        ]

        summary = (
            f"Estimation risk baseline estimates a {int(prob * 100)}% probability of &gt;15% effort underestimation. "
            f"Associated with high complexity integrations and custom AI components."
        )

        return PredictionDraft(
            prediction_type="PROJECT_EFFORT_VARIANCE",
            entity_id=estimate_id,
            probability=prob,
            risk_band=risk_band,
            confidence_interval={"lower": max(0.0, round(prob - 0.06, 2)), "upper": min(1.0, round(prob + 0.06, 2))},
            model_version=self.ESTIMATION_RISK_VERSION,
            key_drivers=drivers,
            summary_text=summary,
            safety_notes=["Informative risk estimate. Original approved estimate is never automatically changed."],
        )

    def predict_client_retention_risk(self, client_account_id: str, features: Dict[str, Any]) -> PredictionDraft:
        """Estimate client churn / inactivity risk using cautious operational signals."""
        support_reopen_count = int(features.get("support_reopens_count") or 0)
        active_incidents = int(features.get("unresolved_incidents_count") or 0)
        days_since_contact = int(features.get("days_since_last_activity") or 0)
        has_active_maintenance = bool(features.get("has_active_maintenance") or False)

        risk_p = 0.10
        if support_reopen_count >= 2:
            risk_p += 0.25
        if active_incidents > 0:
            risk_p += 0.30
        if days_since_contact > 60:
            risk_p += 0.20
        if not has_active_maintenance:
            risk_p += 0.10

        prob = min(0.95, max(0.05, round(risk_p, 2)))
        risk_band = "HIGH" if prob >= 0.65 else ("MEDIUM" if prob >= 0.35 else "LOW")

        drivers = [
            {"feature": "unresolved_incidents", "value": active_incidents, "impact": "+0.30" if active_incidents > 0 else "0.00"},
            {"feature": "support_reopens", "value": support_reopen_count, "impact": "+0.25" if support_reopen_count >= 2 else "0.00"},
            {"feature": "days_since_contact", "value": days_since_contact, "impact": "+0.20" if days_since_contact > 60 else "0.00"},
        ]

        summary = (
            f"Internal retention risk baseline estimates a {int(prob * 100)}% risk index ({risk_band} Level). "
            f"Signals indicate operational follow-up is recommended."
        )

        return PredictionDraft(
            prediction_type="CLIENT_RETENTION",
            entity_id=client_account_id,
            probability=prob,
            risk_band=risk_band,
            confidence_interval={"lower": max(0.0, round(prob - 0.08, 2)), "upper": min(1.0, round(prob + 0.08, 2))},
            model_version=self.CLIENT_RETENTION_VERSION,
            key_drivers=drivers,
            summary_text=summary,
            safety_notes=["Internal decision support only. Strictly prohibited from sharing with client."],
        )
