# Machine-to-Machine (M2M) Service Identity

## 1. Principle
Never share a universal service credential. Every microservice and pipeline receives an isolated cryptographic identity:
- `frontend-service`
- `api-service`
- `billing-service`
- `ai-orchestrator`
- `data-agent`
- `security-agent`

## 2. Workload Attestation
Workloads authenticate via SPIFFE/mTLS certificates with short-lived tokens.
