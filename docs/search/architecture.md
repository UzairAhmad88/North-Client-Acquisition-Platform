# Phase 38 — Search, Command Palette & Assistant Architecture

## 1. Subsystem Architecture

Phase 38 integrates search discovery, safe command execution, and a natural-language platform assistant into a single unified interaction interface.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        USER / FRONTEND INTERACTION                     │
│    ├── Global Search (/search)                                         │
│    ├── Command Palette (Ctrl + K)                                      │
│    └── Natural-Language Assistant (/assistant)                         │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   PARSING, PLANNING & VALIDATION                       │
│  - QueryParser (Search type, entity targets, priority/status filters)  │
│  - QueryPlanner (Parameterized plans without raw SQL)                  │
│  - CommandParser & Validator (Schema and entity state checks)          │
│  - AssistantPlanner (Grounded query planning & question breakdown)    │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 SECURITY, IDENTITY & AUTHORIZATION                     │
│  - Strict Tenant Isolation enforcement                                 │
│  - Role / Permission / ABAC access checks                              │
│  - Client visibility boundaries (Hides internal notes & margins)       │
│  - Secure snippet generation (Zero leakage of private text)           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  RETRIEVAL & EXECUTION ENGINES                         │
│  ├── SearchIndexManager (Local & event-driven search indexing)         │
│  ├── SearchRanker (Multi-factor ranking: lexical, exact, recency, etc.)│
│  ├── CommandExecutor (Approval gates for sensitive actions)            │
│  └── PlatformAssistantService (Context sanitization & citations)       │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   PERSISTENCE, TELEMETRY & AUDIT                       │
│  - SearchQueryAuditRecord & latency tracking                           │
│  - CommandAuditEventRecord (Full parameter and result hashing)         │
│  - AI Trace Logging (Integrated with Phase 33 Governance)              │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Entities

1. **`SearchIndexRecord`**: Index representation with entity type, tenant, title, search text, and metadata.
2. **`SearchSavedQueryRecord`**: User-saved query definitions and filter criteria.
3. **`SearchPinRecord`**: Pinned entity shortcuts displayed in command center.
4. **`CommandDefinitionRecord`**: Registered commands with category, risk rating, and required permissions.
5. **`CommandAuditEventRecord`**: Full audit log of command validations and execution outcomes.
6. **`AssistantSessionRecord` & `AssistantMessageRecord`**: Conversational assistant session history and source citations.
