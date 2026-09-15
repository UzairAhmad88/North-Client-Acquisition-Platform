"""Troubleshooting Engine providing grounded diagnostic recommendations."""

from typing import List, Optional
from agents.support.models import TroubleshootingSuggestionResult


class TroubleshooterEngine:
    """Generates structured troubleshooting steps while strictly separating observed facts from inferences."""

    def analyze_troubleshooting(
        self,
        request_id: Optional[str],
        title: str,
        description: str,
        category: str = "APPLICATION",
    ) -> TroubleshootingSuggestionResult:
        """Generate structured diagnostics distinguishing OBSERVED, INFERRED, POSSIBLE, and CONFIRMED."""
        observed: List[str] = [f"Reported Issue: {title}"]
        if "login" in description.lower() or "auth" in description.lower():
            observed.append("Authentication / Session workflow failure reported.")
            inferred = ["Possible token expiration or JWT secret mismatch.", "Database connection pool exhaustion on auth service."]
            possible = ["Verify JWT signing keys and expiry timestamps.", "Check database connectivity under auth endpoint /api/v1/auth/me.", "Review recent environment configuration deployment."]
            confirmed: List[str] = []
            steps = ["1. Inspect auth server logs for HTTP 401/500 errors.", "2. Test authentication endpoints using curl or Postman.", "3. Verify client browser cookies and session headers."]
        elif "payment" in description.lower() or "stripe" in description.lower():
            observed.append("Payment processing transaction failure.")
            inferred = ["Third-party gateway webhook timeout or invalid API key.", "Webhook signature validation failure on server."]
            possible = ["Check webhook endpoint /api/v1/webhooks/stripe status.", "Verify API test/live mode configuration."]
            confirmed = []
            steps = ["1. Verify gateway webhook delivery dashboard logs.", "2. Review application error logs for WebhookSignatureVerificationError.", "3. Retry failed transaction in test sandbox."]
        else:
            observed.append("General application functionality issue.")
            inferred = ["Unexpected runtime exception or invalid client input."]
            possible = ["Inspect application server logs.", "Check database read/write latency."]
            confirmed = []
            steps = ["1. Replicate issue with provided steps.", "2. Review application error logs for stack trace.", "3. Confirm staging vs production environment parity."]

        return TroubleshootingSuggestionResult(
            request_id=request_id,
            observed_symptoms=observed,
            inferred_causes=inferred,
            possible_solutions=possible,
            confirmed_findings=confirmed,
            recommended_next_steps=steps,
        )
