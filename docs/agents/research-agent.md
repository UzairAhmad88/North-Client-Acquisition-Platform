# Phase 15 — Research Agent Specification

## 1. Executive Summary
The **Research Agent** is the first production-oriented AI agent built on top of the **Phase 14 Agent Core Runtime**. It automates evidence-backed business intelligence gathering, validation, recency checking, and conflict identification without human intervention, while maintaining strict security boundaries and auditability.

---

## 2. Architecture & Design Principles

### 2.1 Runtime Integration
- **Agent Registry**: Registered under `research_agent` v1.0 in `AgentRegistry`.
- **Context Awareness**: Receives `AgentContext` containing `business_profile`, `research_data`, and `metadata`.
- **State Management**: Execution steps tracked via Phase 14 `AgentRunRepository` (`PENDING`, `RUNNING`, `COMPLETED`, `PARTIAL`, `FAILED`).

### 2.2 Permissions Scoping
The agent operates under least-privilege permissions:
- **Granted Permissions**:
  - `READ_BUSINESS`: Read public business profile.
  - `READ_LEAD`: Access associated lead context.
  - `READ_RESEARCH`: Inspect existing research records.
  - `SEARCH_WEB`: Execute targeted web search queries.
  - `FETCH_WEB`: Fetch web page contents.
  - `CREATE_RESEARCH_RECORD`: Persist verified research records.
- **Prohibited Permissions (Strictly Denied)**:
  - `SEND_EMAIL`, `SEND_MESSAGE`, `SEND_WHATSAPP`, `MAKE_PAYMENT` (Zero autonomous outbound communication).

---

## 3. Evidence-First Pipeline

```
1. Freshness Evaluation (Reuse research <= 30 days)
2. Targeted Web Research (Only for missing / stale sections)
3. Source Trust Classification (OFFICIAL > HIGH_TRUST > MEDIUM_TRUST > LOW_TRUST > UNKNOWN)
4. Fact Fabrication Defense (Unsupported model assertions downgraded or rejected)
5. Structured Output Validation (Pydantic schema validation & confidence scoring)
```

### 3.1 Trust Hierarchy Classifier
- `OFFICIAL`: Official business domain, official social pages, GMB listing.
- `HIGH_TRUST`: Government registries, reputable business directories.
- `MEDIUM_TRUST`: Industry blogs, news outlets.
- `LOW_TRUST`: User-generated forums, unverified web aggregators.
- `UNKNOWN`: Unclassified web sources.

### 3.2 Confidence Calculation
- **HIGH**: Official source, fresh (<= 30 days), no conflicts.
- **MEDIUM**: High-trust source or older official record without conflict.
- **LOW**: Low-trust source, stale record (> 30 days), or conflicting evidence.

---

## 4. Input & Output Schemas

### 4.1 Agent Input
```json
{
  "job_id": "uuid",
  "requested_sections": ["identity", "services", "digital_presence", "contact_information"],
  "max_age_days": 30
}
```

### 4.2 Agent Result Output
```json
{
  "business_summary": {
    "name": "Starlight Fitness & Wellness",
    "category": "gym",
    "website_url": "https://starlightfitness.com",
    "findings_count": 4
  },
  "findings": [...],
  "evidence": [...],
  "conflicts": [...],
  "missing_information": [],
  "limitations": [
    "Research is based on publicly available web pages and existing records.",
    "Internal financial details and private communications were not accessed."
  ]
}
```
