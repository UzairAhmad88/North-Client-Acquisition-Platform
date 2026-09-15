# Disaster Recovery Runbook: Primary Region Outage & Cross-Region Failover

## 1. Overview
* **Scenario**: Complete unavailability or degraded network partition in Primary AWS Region (`us-east-1`).
* **Target RPO**: 5 minutes (Financial & double-entry ledger), 15 minutes (CRM, Projects, Documents).
* **Target RTO**: $\le$ 30 minutes total platform restoration.
* **Secondary Region**: `us-west-2` (Warm standby replicas & cross-region S3 replication).

---

## 2. Trigger Criteria & Incident Declaration
* **SEV-1 Critical Outage** declared when:
  - Multi-AZ availability in primary region is 0% for $> 5$ consecutive minutes.
  - Heartbeat probes from external canary monitors fail continuously.
  - Failover authorization signed off by Lead SRE / Incident Commander.

---

## 3. Strict 14-Step Recovery Priority Sequence

1. **Step 1 — Identity & RBAC Access Control (`TIER_0`)**:
   - Promote secondary Auth0/Cognito identity gateway and JWT key caches in `us-west-2`.
2. **Step 2 — PostgreSQL Primary Database (`TIER_0`)**:
   - Promote read replica in `us-west-2` to primary read-write cluster via `pg_promote()` / AWS RDS failover.
   - Verify transaction log (WAL) sequence alignment.
3. **Step 3 — Core Backend API Gateway (`TIER_0`)**:
   - Switch DNS records (Cloudflare / Route53) via weighted health routing to `us-west-2` API load balancers.
4. **Step 4 — Object & Document Storage (`TIER_1`)**:
   - Enable primary routing to `s3-us-west-2` cross-region synchronized buckets.
5. **Step 5 — Event Bus & Transactional Outbox (`TIER_1`)**:
   - Spin up Kafka/SQS worker clusters in `us-west-2` and replay unprocessed outbox events.
6. **Step 6 — Workflow Orchestration Engine (`TIER_1`)**:
   - Acquire distributed locks in Redis `us-west-2` cluster and resume paused step functions.
7. **Step 7 — Communication & Notification Dispatcher (`TIER_1`)**:
   - Re-establish SMTP / SendGrid / Twilio webhook endpoints to secondary gateway.
8. **Step 8 — Finance & Double-Entry Ledger (`TIER_1`)**:
   - Execute ledger reconciliation checker to verify 0 unbalanced debit/credit journals.
9. **Step 9 — CRM, Leads & Opportunities (`TIER_2`)**:
   - Resume CRM customer read/write sync.
10. **Step 10 — Project Delivery & Tasks WBS (`TIER_2`)**:
    - Resume collaboration portals and project status pipelines.
11. **Step 11 — Customer Support & Incident Escalation (`TIER_2`)**:
    - Restore ticket routing and SLA escalation triggers.
12. **Step 12 — Analytics & Business Intelligence (`TIER_3`)**:
    - Resume ClickHouse / analytics pipeline ingestion.
13. **Step 13 — AI Model Router & Agent Subsystems (`TIER_3`)**:
    - Re-enable multi-model AI agent routing and background audit generation.
14. **Step 14 — Predictive Operations & Advanced Intelligence (`TIER_4`)**:
    - Re-enable background ML forecasting and autonomous discovery pipelines.

---

## 4. Verification & Health Sign-Off
* Run `/health/deep` on new primary region endpoint.
* Verify all 8 subsystem health probes return `HEALTHY`.
* Run test transaction through idempotency guard to ensure exactly-once semantics.
* Broadcast incident resolved notification to customer status page.
