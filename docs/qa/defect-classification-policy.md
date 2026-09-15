# Defect Classification & Severity Triage Policy

## 1. Defect vs. Scope Change Policy

A strict boundary separates software defects from scope changes:

| Parameter | Defect (`DEFECT`) | Scope Change (`SCOPE_CHANGE`) |
| :--- | :--- | :--- |
| **Definition** | Non-compliance, error, or failure against the locked contract baseline specification. | Request for new functionality, modified workflow, or out-of-scope enhancement. |
| **Commercial Impact** | Resolved at no additional cost to client under engagement agreement. | Requires Phase 28 Change Request, PERT re-estimation, and client approval. |
| **Release Block** | Critical/High defects block release readiness gate. | Does not block release unless formally converted to an approved change. |

---

## 2. Severity Matrix

- **`CRITICAL`**: Complete system outage, data corruption, severe security vulnerability, or fatal crash in core user flow. **Strictly blocks release deployment.**
- **`HIGH`**: Major functional feature failure without workaround. **Blocks release deployment.**
- **`MEDIUM`**: Functional issue with accessible workaround or non-critical flow degradation.
- **`LOW`**: Cosmetic UI alignment, minor typo, or subtle visual flaw.
