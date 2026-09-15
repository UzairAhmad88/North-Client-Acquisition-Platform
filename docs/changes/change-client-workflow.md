# Client Portal Change Request Workflow

This document describes the client portal interface for reviewing and approving change requests in **Uzaii Develop By North's Phase 28**.

---

## 1. Client Review Interface

Clients access change proposals via `/client-portal/projects/[id]/changes`.
Exposed information:
- Change Title & Description
- Affected Deliverables & Features
- Estimated Schedule Shift (in working days)
- Commercial Adjustment Total (`change_value`)
- Important Assumptions

---

## 2. Protected Internal Data

The client view strictly filters out:
- Internal labor costs
- Hourly developer margins & multipliers
- Raw AI agent reasoning prompts
- Internal engineering risk ratings
