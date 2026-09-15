# Privileged Access Management (PAM) & JIT Access

## 1. Privileged Roles
- Enterprise Administrator
- Security Administrator
- Database Administrator
- Cloud & Infrastructure Administrator
- Root Service Account

## 2. Just-In-Time (JIT) Workflow
1. **Request**: Subject requests temporary elevation specifying duration and justification.
2. **Risk Check**: Automated evaluation of current threat posture and entity risk score.
3. **Approval Gate**: Multi-party or manager approval required for critical tiers.
4. **Time-Limited Access**: Session credentials issued with strict TTL (e.g., 60 minutes).
5. **Session Monitoring & Automatic Revocation**: All commands recorded to audit trail; credentials auto-expire.
