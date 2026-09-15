# Change Request, Scope Change & Commercial Change Management

The **Uzaii Develop By North's Change Management System** is a secure, audited, version-controlled governance engine that manages requests after a project enters execution, preventing uncontrolled scope creep while preserving baseline immutability.

---

## 1. System Architecture

```text
+-----------------------------------------------------------------------+
|                      Client / Internal Request                        |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                     Triage & Classification Engine                    |
|       (IN_SCOPE | OUT_OF_SCOPE | DEFECT | CLARIFICATION | UNKNOWN)     |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                 Multi-Dimensional Impact Analysis                     |
|    (Requirements, Features, Deliverables, Tasks, Schedule, Risk)      |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                 PERT 3-Point Effort Re-estimation                     |
|                     Expected = (O + 4M + P) / 6                       |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                   Commercial & Contract Delta Engine                  |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|             Internal Review & Phase 20 RiskEngine Check               |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|              Client Review & Cryptographic Sign-Off                   |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|          Immutable Baseline Revision (Baseline v1 -> Baseline v2)    |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|               Task Mapping & Project Execution Tasks                  |
+-----------------------------------------------------------------------+
```

---

## 2. Core Non-Negotiable Principles

1. **Request $\neq$ Scope Change**:
   - A request is not a scope change until it has passed the controlled change workflow.
2. **`IN_SCOPE` vs `OUT_OF_SCOPE`**:
   - Requests that align with the committed baseline remain `IN_SCOPE` and route directly to existing work without commercial changes.
3. **Defect Separation**:
   - Software bugs and defects are classified as `DEFECT` and routed to defect remediation tasks without charging additional fees.
4. **Approval Invalidation**:
   - Any modification to an active change proposal invalidates prior approvals, requiring re-issue and re-signing of the new content hash.
5. **AI Security Boundary**:
   - `ChangeAgent` v1.0 provides impact analysis and recommendations but possesses **ZERO** permissions to approve scope changes, alter contract baselines, modify pricing, promise deadlines, or send un-guarded external messages.
