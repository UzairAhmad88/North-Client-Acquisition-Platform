# Risk Policy Specification

## Server-Controlled Policy Model
Risk policies are versioned, server-controlled objects (`RiskPolicy`). AI agents or browser clients can never modify or override risk policy parameters.

## Configurable Policy Settings

- `policy_version`: Current active policy version (default `v1`).
- `engine_version`: Active engine version (default `1.0.0`).
- `max_allowed_risk_level`: Maximum acceptable risk level for `PASS` (`LOW` or `MEDIUM`).
- `min_evidence_coverage`: Minimum required evidence coverage ratio (default `0.50`).
- `min_quality_score`: Minimum required quality score threshold (default `50.0`).
- `ai_semantic_review_enabled`: Enable/disable AI semantic evaluator.
- `fail_safe_behavior`: Default fallback decision when AI provider times out or fails (`REVIEW` or `BLOCK`).
