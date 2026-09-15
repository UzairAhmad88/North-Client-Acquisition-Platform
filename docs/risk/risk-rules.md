# Risk Rules Specifications

## Rule Taxonomy

Each deterministic rule in the Risk & Quality Engine evaluates a specific safety, legal, privacy, or content quality constraint.

| Rule ID | Category | Severity | Description |
|---------|----------|----------|-------------|
| `R-CLAIM-GUARANTEE` | `CLAIM_ACCURACY` | `CRITICAL` | Flags false guarantees (e.g. "300% growth", "guaranteed revenue"). |
| `R-CLAIM-SOCIAL-PROOF` | `DECEPTION` | `CRITICAL` | Flags unverified social proof (e.g. "worked with hundreds of clients"). |
| `R-CLAIM-FALSE-URGENCY` | `DECEPTION` | `HIGH` | Flags artificial urgency tactics (e.g. "only 2 slots left"). |
| `R-CLAIM-DECEPTIVE-IDENTITY` | `DECEPTION` | `CRITICAL` | Flags misleading subject lines or impersonation patterns. |
| `R-EVIDENCE-UNSUPPORTED-CLAIM` | `EVIDENCE` | `MEDIUM` | Flags factual claims not linked to audit findings or research records. |
| `R-EVIDENCE-COVERAGE-LOW` | `EVIDENCE` | `HIGH` | Flags drafts where evidence coverage falls below policy threshold (< 50%). |
| `R-PRIVACY-SENSITIVE-DATA` | `PII` | `CRITICAL` | Detects exposed API keys, passwords, bearer tokens, or DB connection URIs. |
| `R-PRIVACY-INTERNAL-INFO` | `PRIVACY` | `HIGH` | Detects leaked stack traces, SQL strings, or system prompt tags. |
| `R-RECIPIENT-MISMATCH` | `RECIPIENT` | `CRITICAL` | Detects cross-business recipient mismatches. |
| `R-CHANNEL-FORMAT-MISMATCH` | `CHANNEL` | `CRITICAL` | Enforces format compatibility (EMAIL requiring email syntax, SMS requiring phone). |
| `R-SECURITY-PROMPT-INJECTION` | `PROMPT_INJECTION` | `CRITICAL` | Detects prompt injection or instruction override commands in external text. |
| `R-CONTENT-QUALITY-EVALUATION` | `CONTENT` | `MEDIUM` | Evaluates subject, body length, CTA clarity, and tone score. |
