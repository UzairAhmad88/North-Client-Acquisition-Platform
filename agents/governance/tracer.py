"""Structured AI Distributed Tracer & Observability Engine."""

from typing import Any, Dict, List, Optional
import time
from agents.governance.models import SpanRecord, TracePayload


class AITracerEngine:
    """Collects distributed execution spans, latency, token consumption, and safety checks without recording private CoT."""

    PROHIBITED_COT_KEYS = {
        "thought",
        "thoughts",
        "reasoning",
        "chain_of_thought",
        "internal_monologue",
        "hidden_scratchpad",
        "raw_cot",
    }

    def sanitize_event_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Strip raw private reasoning/CoT keys from trace payload metadata."""
        if not isinstance(data, dict):
            return {"value": str(data)[:200]}

        sanitized: Dict[str, Any] = {}
        for k, v in data.items():
            if k.lower() in self.PROHIBITED_COT_KEYS:
                continue
            if isinstance(v, dict):
                sanitized[k] = self.sanitize_event_summary(v)
            elif isinstance(v, list):
                sanitized[k] = [
                    self.sanitize_event_summary(item) if isinstance(item, dict) else str(item)[:150]
                    for item in v[:10]
                ]
            else:
                # String truncation for safety and size bounding
                val_str = str(v)
                sanitized[k] = v if len(val_str) <= 500 else val_str[:500] + "...[TRUNCATED]"
        return sanitized

    def create_span(
        self,
        span_type: str,
        name: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        tokens_consumed: int = 0,
        duration_ms: float = 0.0,
        status: str = "SUCCESS",
        error_message: Optional[str] = None,
    ) -> SpanRecord:
        """Create a sanitized span record for an execution step."""
        clean_in = self.sanitize_event_summary(input_data)
        clean_out = self.sanitize_event_summary(output_data)

        return SpanRecord(
            span_type=span_type,
            name=name,
            input_summary=clean_in,
            output_summary=clean_out,
            tokens_consumed=tokens_consumed,
            duration_ms=duration_ms,
            status=status,
            error_message=error_message,
        )

    def calculate_trace_summary(self, spans: List[SpanRecord]) -> Dict[str, Any]:
        """Aggregate total latency, token count, and estimated cost across all spans in a trace."""
        total_tokens = sum(s.tokens_consumed for s in spans)
        total_duration = sum(s.duration_ms for s in spans)
        has_failure = any(s.status != "SUCCESS" for s in spans)

        # Baseline cost estimate: $0.002 per 1k tokens
        estimated_cost = round((total_tokens / 1000.0) * 0.002, 4)

        return {
            "total_tokens": total_tokens,
            "total_duration_ms": total_duration,
            "estimated_cost": estimated_cost,
            "status": "FAILED" if has_failure else "COMPLETED",
            "span_count": len(spans),
        }
