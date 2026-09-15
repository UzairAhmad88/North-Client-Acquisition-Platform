# Phase 10 — Research System Architecture

## Overview

The **Research System** in **Uzaii Develop By North's** is a structured, evidence-backed business intelligence engine that collects, normalizes, validates, and organizes public information for businesses while preserving strict source provenance.

---

## Core Architecture & Flow

```text
BUSINESS PROFILE
       ↓
RESEARCH JOB REQUEST (Sections: Identity, Contact, Services, Website, Social)
       ↓
PROVIDER SELECTION (MockResearchProvider / WebScraperResearchProvider)
       ↓
SSRF & SECURITY VALIDATION (IP resolution, forbidden CIDR check, redirect caps)
       ↓
FETCH & PARSE (Safe HTML parser, text sanitization, prompt-injection defense)
       ↓
FACT EXTRACTION & NORMALIZATION (Phone, Email, URLs, Services)
       ↓
CONFIDENCE & SOURCE TRUST EVALUATION (OFFICIAL, HIGH_TRUST, MEDIUM_TRUST, LOW_TRUST)
       ↓
CONFLICT DETECTION (Check competing values against historical observations)
       ↓
PERSISTENCE (research_jobs, research_records, research_conflicts)
       ↓
SAFE BUSINESS PROFILE ENRICHMENT (Fills missing fields without mutating verified data)
```

---

## Database Models

- **`ResearchJob`** (`research_jobs`): Tracks research job execution state (`PENDING`, `RUNNING`, `COMPLETED`, `PARTIAL`, `FAILED`, `CANCELLED`), target sections, record counts, and timestamps.
- **`ResearchRecord`** (`research_records`): Granular evidence facts containing `field_name`, `raw_value`, `normalized_value`, `source_url`, `source_trust`, `confidence` (`HIGH`, `MEDIUM`, `LOW`), `evidence_text`, `observed_at`, and `expires_at`.
- **`ResearchConflict`** (`research_conflicts`): Stores mismatched facts detected across sources for a business field (`status`: `CONFLICT`).

---

## Providers

1. **`MockResearchProvider`**: Deterministic synthetic provider for offline development and testing.
2. **`WebScraperResearchProvider`**: Live HTML parser using SSRF-safe HTTP fetching and clean text extraction.

---

## Verification & Test Suite

- Unit & Security tests: `tests/unit/backend/test_research.py` (5/5 passed).
- Backend suite: `tests/unit/backend/` (47/47 passed).
- Type checking: `mypy app` (0 errors across 126 source files).
- Linter: `ruff check .` (0 errors).
- Next.js build: Clean build output.
