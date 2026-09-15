# Scope Creep & Baseline Monitoring Engine

## Overview
The Scope Monitor Engine continuously inspects active execution tasks and client communication logs against the locked `ContractBaseline` to detect uncommitted scope additions.

---

## Detection Signals

### 1. `FEATURE_ADDED`
Triggered when an execution task does not trace back to any deliverable or feature in the committed baseline.

### 2. `NEW_SCOPE_REQUEST`
Triggered when client communication messages contain scope expansion requests (*"can we also add"*, *"new feature"*, *"mobile app"*).

---

## Governance Workflow

```text
Scope Signal Detected
        ↓
Logged to project_scope_signals
        ↓
Alert displayed on Scope Monitor Panel
        ↓
Human Operator Review
        ↓
Option A: Reject & Keep Baseline Scope
Option B: Issue Formal Change Order & Re-Baseline
```
