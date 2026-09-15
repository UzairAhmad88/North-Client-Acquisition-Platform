# PERT 3-Point Effort Re-Estimation Engine

This document outlines the effort re-estimation methodology for Change Requests in **Uzaii Develop By North's Phase 28**.

---

## 1. PERT 3-Point Formula

For any proposed change, three estimates are calculated:
- **Optimistic ($O$)**: Best-case scenario under ideal conditions.
- **Most Likely ($M$)**: Expected effort under normal velocity.
- **Pessimistic ($P$)**: Worst-case scenario with unexpected technical blockers.

The expected effort ($E$) is derived using the standard PERT formula:

$$E = \frac{O + 4M + P}{6}$$

---

## 2. Historical Baseline Protection

Original committed estimates in Phase 24 remain **100% immutable**. Change request effort is stored as a distinct `ChangeEstimate` record with variance tracking against historical actuals.
