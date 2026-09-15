"""Unified Observability Engine - Metrics, Logs, Traces & APM."""

from typing import List, Dict, Any
from datetime import datetime, timezone

class ItOpsObservabilityService:
    @staticmethod
    def get_apm_metrics(service_code: str = "SVC-PAYMENT-GATEWAY", tenant_id: str = "tenant-default") -> Dict[str, Any]:
        return {
            "service_code": service_code,
            "throughput_rps": 1420.0,
            "avg_latency_ms": 42.5,
            "p95_latency_ms": 88.0,
            "p99_latency_ms": 145.0,
            "error_rate_pct": 0.015,
            "apdex_score": 0.98,
            "cpu_utilization_pct": 38.5,
            "memory_utilization_pct": 62.0,
            "synthetic_tests": [
                {"test_name": "Check Payment Endpoint Health", "passed": True, "response_ms": 38.0},
                {"test_name": "Verify Auth Token Issue", "passed": True, "response_ms": 24.0}
            ]
        }

    @staticmethod
    def get_recent_traces(service_code: str = "SVC-PAYMENT-GATEWAY", tenant_id: str = "tenant-default") -> List[Dict[str, Any]]:
        return [
            {
                "trace_id": "TRC-892019401",
                "span_id": "SPN-001",
                "service": service_code,
                "operation": "POST /api/v1/payments/process",
                "duration_ms": 48.2,
                "status": "OK",
                "http_status": 200,
                "spans_count": 4
            },
            {
                "trace_id": "TRC-892019402",
                "span_id": "SPN-002",
                "service": service_code,
                "operation": "POST /api/v1/payments/process",
                "duration_ms": 280.5,
                "status": "ERROR",
                "http_status": 504,
                "error_message": "Upstream Gateway Timeout on Stripe Adapter",
                "spans_count": 6
            }
        ]
