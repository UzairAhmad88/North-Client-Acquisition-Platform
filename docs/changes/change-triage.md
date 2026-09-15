# Change Triage & Classification Protocol

This document outlines the classification engine rules used to categorize incoming change requests.

---

## 1. Classification Categories

| Classification | Meaning | Action Route |
| :--- | :--- | :--- |
| **`IN_SCOPE`** | Request aligns with committed baseline deliverables | Route to existing project tasks (No commercial change) |
| **`OUT_OF_SCOPE`** | New major feature or capability not in baseline | Proceed to formal Impact Analysis & Commercial Re-estimation |
| **`DEFECT`** | Software bug or unexpected behavior flaw | Route to defect remediation task (No fee adjustment) |
| **`CLARIFICATION`** | Requirement detail clarification | Update requirement specification |

---

## 2. Triage Policy Rules

1. **Defect Protection**:
   - Defect reports from clients must **never** be converted into commercial scope changes merely because the client reported them.
2. **In-Scope Protection**:
   - Items already promised in the contract baseline (e.g. mobile responsiveness) remain `IN_SCOPE`.
