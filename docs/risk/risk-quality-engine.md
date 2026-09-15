# Risk & Quality Engine Architecture

## Overview
The **Risk & Quality Engine** is the centralized evaluation layer responsible for evaluating whether AI-generated or system-generated artifacts (such as outreach drafts, messages, or documents) are safe, supported by evidence, consistent with business data, compliant with communication policies, and suitable for human review or workflow progression.

## Architecture Pipeline

```text
AI GENERATES
      │
      ▼
RISK & QUALITY ENGINE
  ├── Deterministic Rules Engine (Claims, Evidence, PII, Channels, Recipients, Injection)
  ├── Quality Scorer (Subject, Body Length, CTA, Tone)
  ├── Optional AI Semantic Reviewer
  └── Risk Reconciler (PASS / REVIEW / BLOCK)
      │
      ▼
HUMAN REVIEW & APPROVAL
      │
      ▼
COMMUNICATION GUARD (Send-Time Validation)
      │
      ▼
TRANSPORT PROVIDER (Mock / Live)
```

## Key Architectural Principles

1. **Evaluator Role Only**: The Risk Engine never performs external communication, calls transport providers, or sends messages directly (`SEND_EMAIL`, `SEND_MESSAGE` forbidden).
2. **Deterministic Precedence**: Deterministic rules always override AI semantic evaluations. An AI semantic review can flag an artifact for `REVIEW` or `BLOCK`, but can **never** override a deterministic `BLOCK`.
3. **Complementary to Communication Guard**: The Risk Engine evaluates artifact safety prior to human approval; the server-side `CommunicationGuard` remains authoritative for send-time policy enforcement.
4. **Staleness Tracking**: Modifications to an artifact invalidate prior assessments, marking them `is_stale=True` and requiring re-evaluation.
