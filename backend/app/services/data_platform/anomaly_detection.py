"""Automated Anomaly Detection & Metric Change Point Explanation Service."""

from typing import List, Dict, Any
from datetime import datetime, timezone

class DataPlatformAnomalyService:
    @staticmethod
    def list_anomalies(tenant_id: str = "tenant-default") -> List[Dict[str, Any]]:
        return [
            {
                "anomaly_code": "ANOM-2026-081",
                "metric_code": "MTR-OPS-SLA",
                "metric_name": "Process SLA Compliance Rate",
                "detected_at": datetime.now(timezone.utc).isoformat(),
                "expected_value": 98.5,
                "actual_value": 92.1,
                "deviation_pct": -6.5,
                "detection_method": "TIME_SERIES_ISOLATION_FOREST",
                "severity": "HIGH",
                "affected_segment": "Region: EMEA / Process: Order-to-Cash",
                "potential_drivers": [
                    "Manual approval gate backlog in manager review queue",
                    "Third-party credit validation API latency spike (+4,200ms)"
                ],
                "confidence": 0.96
            },
            {
                "anomaly_code": "ANOM-2026-079",
                "metric_code": "MTR-AI-TOKEN-EFF",
                "metric_name": "AI Agent Token Efficiency",
                "detected_at": datetime.now(timezone.utc).isoformat(),
                "expected_value": 3400.0,
                "actual_value": 6850.0,
                "deviation_pct": +101.4,
                "detection_method": "STATISTICAL_ZSCORE",
                "severity": "MEDIUM",
                "affected_segment": "Model: Claude-3.5-Sonnet / Agent: ResearchAgent",
                "potential_drivers": [
                    "Infinite retry loop triggered on malformed HTML document retrieval",
                    "Prompt context overflow on unstructured 80-page PDF attachment"
                ],
                "confidence": 0.98
            }
        ]
