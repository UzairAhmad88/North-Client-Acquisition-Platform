# Contract Impact & Amendment Signal Detection

This document outlines contract amendment detection rules for Change Requests in **Uzaii Develop By North's Phase 28**.

---

## 1. Amendment Triggers

A change request triggers a `CONTRACT_AMENDMENT_REQUIRED` signal if:
1. The request classification is `OUT_OF_SCOPE`.
2. The change introduces a new project deliverable.
3. The commercial value delta is greater than zero ($> 0.00$).

---

## 2. Immutable Contract Preservation

The original signed contract and baseline remain untouched. Approved changes create linked `ChangeBaselineLink` records pointing to revised `ContractBaseline` versions.
