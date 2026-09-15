# Change Management AI Agent Architecture & Policy

This document details the architecture and policy guardrails of `ChangeAgent` v1.0 in **Uzaii Develop By North's Phase 28**.

---

## 1. Sub-Engine Capabilities

`ChangeAgent` v1.0 executes four core analysis engines:
1. `ChangeClassifier`: Triages requests into `IN_SCOPE`, `OUT_OF_SCOPE`, `DEFECT`, `CLARIFICATION`.
2. `ChangeImpactAnalyzer`: Evaluates 12 impact dimensions across project artifacts.
3. `ChangeEffortAnalyzer`: Computes PERT 3-point expected effort $(O + 4M + P)/6$.
4. `ChangeCommercialAnalyzer`: Proposes price adjustments based on pricing policies.

---

## 2. Strictly Prohibited Actions

`ChangeAgent` is forbidden from autonomous side-effect actions:
- ❌ `APPROVE_CHANGE`
- ❌ `APPROVE_SCOPE_CHANGE`
- ❌ `CHANGE_CONTRACT`
- ❌ `MODIFY_BASELINE`
- ❌ `CHANGE_PRICE`
- ❌ `PROMISE_DEADLINE`
- ❌ `SEND_EXTERNAL_MESSAGE`
