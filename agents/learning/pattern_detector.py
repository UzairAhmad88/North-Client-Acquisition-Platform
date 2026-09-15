"""Pattern Detection Engine for Analyzing Historical Operational Lifecycles."""

from typing import Any, Dict, List, Optional
import math


class PatternDetectorEngine:
    """Empirical pattern detector operating across sales, estimation, delivery, QA, and support."""

    MIN_SAMPLE_SIZE = 5

    def analyze_lead_score_calibration(self, leads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate lead score precision, bands, and outcome discrepancies."""
        sample_size = len(leads_data)
        if sample_size < self.MIN_SAMPLE_SIZE:
            return {
                "status": "INSUFFICIENT_DATA",
                "sample_size": sample_size,
                "message": f"Sample size of {sample_size} is below the required threshold ({self.MIN_SAMPLE_SIZE}) for reliable inference.",
            }

        bands = {
            "80-100": {"total": 0, "won": 0, "lost": 0},
            "60-79": {"total": 0, "won": 0, "lost": 0},
            "40-59": {"total": 0, "won": 0, "lost": 0},
            "0-39": {"total": 0, "won": 0, "lost": 0},
        }

        false_positives = 0  # High score (>=80) but lost
        false_negatives = 0  # Low score (<50) but won

        for lead in leads_data:
            score = float(lead.get("score") or lead.get("lead_score") or 0.0)
            status = str(lead.get("status") or "").upper()
            won = status in ("WON", "CLOSED_WON", "ACCEPTED", "CONVERTED")

            if score >= 80:
                band_key = "80-100"
                if not won:
                    false_positives += 1
            elif score >= 60:
                band_key = "60-79"
            elif score >= 40:
                band_key = "40-59"
            else:
                band_key = "0-39"

            if score < 50 and won:
                false_negatives += 1

            bands[band_key]["total"] += 1
            if won:
                bands[band_key]["won"] += 1
            else:
                bands[band_key]["lost"] += 1

        band_conversions = {}
        for b_name, b_data in bands.items():
            tot = b_data["total"]
            rate = round((b_data["won"] / tot) * 100, 2) if tot > 0 else 0.0
            band_conversions[b_name] = {
                "total": tot,
                "won": b_data["won"],
                "conversion_rate_pct": rate,
            }

        return {
            "status": "VALID",
            "sample_size": sample_size,
            "band_conversions": band_conversions,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "high_score_precision_pct": band_conversions["80-100"]["conversion_rate_pct"],
        }

    def analyze_estimation_variance(self, projects_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compute estimation variance (Actual - Estimated) / Estimated across projects and services."""
        sample_size = len(projects_data)
        if sample_size < self.MIN_SAMPLE_SIZE:
            return {
                "status": "INSUFFICIENT_DATA",
                "sample_size": sample_size,
                "message": f"Sample size ({sample_size}) insufficient for estimation pattern detection.",
            }

        variances = []
        underestimated_count = 0
        overestimated_count = 0
        service_variances: Dict[str, List[float]] = {}

        total_estimated = 0.0
        total_actual = 0.0

        for p in projects_data:
            est = float(p.get("estimated_hours") or p.get("planned_effort") or 0.0)
            act = float(p.get("actual_hours") or p.get("actual_effort") or 0.0)
            service = str(p.get("service_type") or p.get("service") or "general")

            if est <= 0:
                continue

            total_estimated += est
            total_actual += act
            var_pct = ((act - est) / est) * 100.0
            variances.append(var_pct)

            if service not in service_variances:
                service_variances[service] = []
            service_variances[service].append(var_pct)

            if act > est * 1.1:
                underestimated_count += 1
            elif act < est * 0.9:
                overestimated_count += 1

        if not variances:
            return {"status": "INSUFFICIENT_DATA", "sample_size": 0}

        avg_variance_pct = sum(variances) / len(variances)
        abs_variances = [abs(v) for v in variances]
        mean_abs_error_pct = sum(abs_variances) / len(abs_variances)

        service_breakdown = {}
        for s_name, s_vars in service_variances.items():
            service_breakdown[s_name] = {
                "count": len(s_vars),
                "avg_variance_pct": round(sum(s_vars) / len(s_vars), 2),
            }

        return {
            "status": "VALID",
            "sample_size": len(variances),
            "total_estimated_hours": total_estimated,
            "total_actual_hours": total_actual,
            "average_variance_pct": round(avg_variance_pct, 2),
            "mean_abs_error_pct": round(mean_abs_error_pct, 2),
            "underestimated_projects": underestimated_count,
            "overestimated_projects": overestimated_count,
            "service_breakdown": service_breakdown,
        }

    def analyze_requirements_scope_creep(self, projects_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect correlation between unresolved initial requirements and subsequent scope changes."""
        sample_size = len(projects_data)
        if sample_size < self.MIN_SAMPLE_SIZE:
            return {"status": "INSUFFICIENT_DATA", "sample_size": sample_size}

        incomplete_req_projects = 0
        incomplete_with_multiple_changes = 0
        complete_req_projects = 0
        complete_with_multiple_changes = 0

        for p in projects_data:
            has_incomplete = bool(p.get("has_unresolved_requirements") or p.get("late_requirements_count", 0) > 0)
            change_count = int(p.get("change_requests_count") or 0)

            if has_incomplete:
                incomplete_req_projects += 1
                if change_count >= 2:
                    incomplete_with_multiple_changes += 1
            else:
                complete_req_projects += 1
                if change_count >= 2:
                    complete_with_multiple_changes += 1

        rate_incomplete = (
            round((incomplete_with_multiple_changes / incomplete_req_projects) * 100, 2)
            if incomplete_req_projects > 0
            else 0.0
        )
        rate_complete = (
            round((complete_with_multiple_changes / complete_req_projects) * 100, 2)
            if complete_req_projects > 0
            else 0.0
        )

        return {
            "status": "VALID",
            "sample_size": sample_size,
            "incomplete_req_projects": incomplete_req_projects,
            "incomplete_change_risk_pct": rate_incomplete,
            "complete_req_projects": complete_req_projects,
            "complete_change_risk_pct": rate_complete,
            "relative_risk_ratio": round(rate_incomplete / rate_complete, 2) if rate_complete > 0 else None,
        }

    def analyze_escaped_defects(self, qa_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze defects discovered in UAT/Delivery/Support after QA completion."""
        sample_size = len(qa_data)
        if sample_size < self.MIN_SAMPLE_SIZE:
            return {"status": "INSUFFICIENT_DATA", "sample_size": sample_size}

        total_defects = 0
        escaped_defects = 0
        critical_escaped = 0

        for item in qa_data:
            defects = int(item.get("total_defects") or 0)
            escaped = int(item.get("escaped_defects") or item.get("post_qa_defects") or 0)
            severity = str(item.get("severity") or "").upper()

            total_defects += defects
            escaped_defects += escaped
            if escaped > 0 and severity in ("CRITICAL", "HIGH"):
                critical_escaped += 1

        leakage_rate_pct = round((escaped_defects / total_defects) * 100, 2) if total_defects > 0 else 0.0

        return {
            "status": "VALID",
            "sample_size": sample_size,
            "total_defects": total_defects,
            "escaped_defects": escaped_defects,
            "leakage_rate_pct": leakage_rate_pct,
            "critical_escaped_count": critical_escaped,
        }
