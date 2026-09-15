# Customer Success AI Agent Safety & Guardrails

## 1. Advisory-Only Mandate

The `CustomerSuccessAgent` is an analytical decision-support copilot designed to assist human CSMs and leadership.

## 2. Hardcoded Prohibitions

The following permissions are strictly prohibited and will trigger an `AgentPermissionDeniedError`:

| Prohibited Action | Enforcement Mechanism |
|---|---|
| `SEND_CLIENT_MESSAGE` | Agent runtime permission guard |
| `SEND_EXTERNAL_EMAIL` | Agent runtime permission guard |
| `APPROVE_RENEWAL` | Agent runtime permission guard |
| `CHANGE_CLIENT_PRICING` | Agent runtime permission guard |
| `CHANGE_CONTRACT_BASELINE` | Agent runtime permission guard |
| `DELETE_CLIENT_RECORD` | Agent runtime permission guard |
| `EXECUTE_PAYMENT` | Agent runtime permission guard |
| `MODIFY_HEALTH_BASELINE` | Agent runtime permission guard |
