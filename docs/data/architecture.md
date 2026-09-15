# Architecture & System Design

## Architecture Topology
ADKOS is designed as a multi-tier, decoupled, event-driven data and knowledge fabric:

```
[ Data Producers ] (Postgres, APIs, Kafka, S3, ERP, GitHub, IoT)
       │
       ▼
[ Connector Engine ] (connect, discover_schema, extract, validate, load)
       │
       ▼
[ Orchestration & Pipelines ] (Batch, Micro-batch, Streaming, AI-Triggered)
       │
       ▼
[ Storage Lakehouse ] (Raw / Bronze → Silver Cleaned → Gold Modeled)
       │
       ▼
[ Semantic & Knowledge Layer ] (Metric Store, Canonical Entities, Graph Engine)
       │
       ▼
[ Retrieval & AI Copilot ] (Hybrid Search, Memory Store, Query Engine)
       │
       ▼
[ Autonomous Agent Workforce ] (15 Specialized Agents)
```

## Security & Isolation
- Multi-tenancy strictly enforced at database and API levels (`tenant_id`).
- Zero plaintext credential storage: Vault-backed reference keys.
- Read-only AST validation for all LLM-generated SQL queries.
