# Disaster Recovery Runbook: Database Corruption Recovery

## 1. Overview
* **Scenario**: Logical data corruption, accidental table drop, unmitigated bad migration, or storage bit rot.
* **Target RPO**: $\le 5$ minutes Point-in-Time Recovery (PITR) via continuous Write-Ahead Log (WAL) archiving.
* **Target RTO**: $\le 45$ minutes to complete isolated verification and switch over.

---

## 2. Recovery Workflow

1. **Quarantine & Traffic Freezing**:
   - Immediately switch API gateway to read-only degradation mode (`FeatureFlag: deep_data_reconciliation = strict`).
   - Stop background worker processing queues to prevent writing corrupted child records.
2. **Determine Point of Corruption ($T_{\text{corrupt}}$)**:
   - Inspect database audit logs / event store to identify the exact transaction timestamp $T_{\text{corrupt}}$.
   - Set recovery target time $T_{\text{recovery}} = T_{\text{corrupt}} - 1\text{ second}$.
3. **Launch Isolated Sandbox Instance**:
   - Spin up isolated scratch PostgreSQL instance.
   - Restore latest base full backup snapshot taken prior to $T_{\text{corrupt}}$.
4. **Replay WAL Archive up to $T_{\text{recovery}}$**:
   - Apply continuous WAL archives from S3 repository with `recovery_target_time = $T_{\text{recovery}}`.
5. **Run Automated Integrity Validation**:
   - Execute `DataIntegrityChecker.scan_all_domains()`.
   - Verify SHA-256 checksums and double-entry ledger balance.
6. **Swap Clean Database into Active Production**:
   - Update connection pool routing to point to verified recovered database.
   - Re-enable background workers and lift read-only mode.
   - Publish incident postmortem with 5-whys root cause analysis.
