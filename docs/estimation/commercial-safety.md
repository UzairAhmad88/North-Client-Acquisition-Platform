# Commercial Safety & Human Control Architecture

## 1. Core Principles

The **Project Estimation, Effort & Commercial Intelligence Engine** enforces strict boundaries separating estimation from pricing and commercial commitment:

```text
ESTIMATION (Internal Effort x Cost)
    ≠
PRICING (Cost + Configured Margin)
    ≠
COMMERCIAL COMMITMENT (Human Operator Approved Price)
```

---

## 2. Guardrails & Restrictions

1. **Zero AI Autonomous Pricing**:
   - `EstimationAgent` recommends commercial ranges based on authoritative server configurations, but **NEVER** commits to a final binding price, discount, or delivery date.
   - Prohibited permissions: `APPROVE_ESTIMATE`, `MODIFY_PRICING_POLICY`, `SEND_EMAIL`, `SEND_MESSAGE`, `SIGN_CONTRACT`, `MAKE_PAYMENT`.

2. **Internal Data Protection**:
   - Internal hourly rates, cost bases, target profit margins, and risk multipliers are tagged `INTERNAL_ONLY`.
   - Internal financial details are never rendered in client proposals or exposed to external AI prompts unnecessarily.

3. **Staleness Tracking**:
   - Any modifications to requirements, solution features, or pricing policy invalidates existing estimate approvals, setting status to `STALE`.

4. **Proposal Mismatch Detection**:
   - If a client proposal attempts to offer a price or timeline conflicting with an approved estimate, the system flags `REVIEW_REQUIRED`.
