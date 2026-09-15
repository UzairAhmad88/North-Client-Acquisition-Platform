# Lead Scoring System Architecture

## Overview

The Lead Scoring System in **Uzaii Develop By North's** is a deterministic, explainable, and auditable opportunity evaluation engine.

It calculates an **Opportunity Score** (0–100) representing how promising a business opportunity is for North's web development, software, AI systems, and business automation services.

```text
BUSINESS / LEAD
   ↓
RESEARCH RECORDS (Phase 10)
   ↓
WEBSITE AUDIT FINDINGS (Phase 11)
   ↓
SERVICE CATALOG (Phase 07)
   ↓
SCORING ENGINE (`app/services/scoring/engine.py`)
   ↓
7 WEIGHTED COMPONENT CALCULATORS
   ↓
REASON CODES & EVIDENCE ATTACHMENT
   ↓
SCORE SNAPSHOT PERSISTENCE (`lead_scores`)
   ↓
LEAD PRIORITY BAND (`HIGH`, `MEDIUM`, `LOW`, `VERY_LOW`)
```

## Ethical Boundary

The scoring engine evaluates **business and opportunity characteristics only** ("Score opportunities, not people").
Sensitive personal attributes (race, ethnicity, religion, political affiliation, health data, sexual orientation, etc.) are strictly excluded and never inferred.
