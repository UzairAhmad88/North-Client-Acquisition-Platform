# Platform Reliability & Resilience Architecture

## 1. Reliability Philosophy
A production system is not reliable because failures are rare; it is reliable because failures are **expected, detected, contained, recovered, and audited**.

```
FAILURE
   ↓
DETECTION
   ↓
CLASSIFICATION
   ↓
CONTAINMENT
   ↓
RECOVERY
   ↓
VERIFICATION
   ↓
RESTORATION
   ↓
ROOT-CAUSE ANALYSIS
   ↓
IMPROVEMENT
```

## 2. Core Resilience Mechanisms

### A. Health Diagnostics
1. **Liveness Probe (`/health/live`)**: Ultra-lightweight endpoint returning `200 OK` if the process loop is responsive.
2. **Readiness Probe (`/health/ready`)**: Verifies primary database and cache connectivity for traffic routing.
3. **Deep Administrative Health (`/health/deep`)**: Probes internal subsystems (PostgreSQL, Redis, Celery Workers, Object Storage, AI Providers, Search, Workflow Engine) with latency measurements, without exposing sensitive credentials.

### B. Circuit Breaker State Machine
External integrations (AI models, payment gateways, email dispatchers) are guarded by circuit breakers:
- `CLOSED`: Normal operation.
- `OPEN`: Failures exceed threshold (e.g. 5 consecutive failures). Traffic fails fast to fallback.
- `HALF_OPEN`: Recovery window expires. Single probe request allowed to verify recovery.

### C. Bounded Retries & Jitter
- Retries use exponential backoff with full randomized jitter:
  $$\text{delay} = \text{random}(0, \min(\text{max\_delay}, \text{base} \cdot 2^{\text{attempt}}))$$
- Bounded to maximum attempts (default 3); infinite retries are strictly prohibited.
- Unsafe operations (payments, external sends) require idempotency keys before retrying.

### D. Idempotency Guard
- State-changing operations carry a unique `Idempotency-Key` or hash token.
- Locks protect against concurrent double-execution. Completed operations return cached deterministic results.
