# Phase 62 — Unified Enterprise Data Operating System

## 1. Overview & Architectural Loop

The **Unified Enterprise Data Operating System** serves as the central data backbone connecting operational systems, engineering platforms, financial systems, AI agents, semantic analytics, and executive intelligence for **Uzaii Develop By North's**.

```
DATA SOURCES (PostgreSQL, MySQL, Kafka, APIs, S3)
       ↓
INGESTION & CDC (Batch, Micro-batch, Streaming, CDC Debezium)
       ↓
DATA LAKEHOUSE (Bronze: Raw Immutable → Silver: Validated & Cleaned → Gold: Business Data Products)
       ↓
DATA CONTRACTS & SCHEMA REGISTRY (Backward, Forward, Full Compatibility Gates)
       ↓
DATA QUALITY & OBSERVABILITY (Completeness, Accuracy, Consistency, Validity, Uniqueness, Freshness)
       ↓
ENTERPRISE DATA CATALOG & BUSINESS GLOSSARY (Natural Language Discovery, Lineage & Impact Analysis)
       ↓
CENTRALIZED METRIC STORE & SEMANTIC LAYER (ARR, MRR, CAC, LTV, Single Source of Truth)
       ↓
ANALYTICS, ML FEATURE STORE & RAG PIPELINE (Sandboxed SQL Engine, Point-in-Time Features, Vector RAG)
       ↓
AI WORKFORCE & GROUNDED DATA COPILOT (RBAC/ABAC/CLS/RLS Enforced, Fact/Inference/Hypothesis Separation)
       ↓
DECISION INTELLIGENCE & EXECUTIVE COMMAND CENTER (Traceable Metrics to Source Lineage)
```

---

## 2. Core Architectural Pillars

### A. Data Domain Architecture
- **Domains**: Customer, Product, Sales, Marketing, Finance, Operations, Engineering, Infrastructure, Security, AI/ML, HR, Support, Knowledge, Risk, Governance.
- **Domain Ownership**: Every domain owns its data products, registered data sources, schema contracts, and SLO definitions.

### B. Ingestion, CDC & Secret Isolation
- **Supported Modes**: Batch, Micro-Batch, Streaming, and Change Data Capture (CDC: INSERT, UPDATE, DELETE).
- **Security Rule**: Zero raw credentials stored in source records. All connections reference cryptographically secured Vault paths (`auth_type="VAULT_SECRET_REF"`).

### C. Lakehouse Medallion Architecture
- **Bronze Tier**: Raw, immutable, append-only ingested payloads with source watermark.
- **Silver Tier**: Schema-validated, standardized, deduplicated records with quality checks.
- **Gold Tier**: Aggregated, dimension-modeled, curated business-ready data products.

### D. Schema Registry & Data Contracts
- **Compatibility Modes**: `BACKWARD`, `FORWARD`, `FULL`, `NONE`.
- **Breaking Change Gate**: Schema modifications that drop columns or change data types are rejected unless an explicit contract evolution is negotiated between producer and consumer.

### E. 6-Dimension Data Quality Scorecard
Never exposes an opaque single number. Evaluates and reports evidence on:
1. **Completeness**: Null-value ratio against allowable thresholds.
2. **Accuracy**: Referential integrity and range constraint satisfaction.
3. **Consistency**: Cross-table and cross-domain entity matching.
4. **Validity**: Regex pattern matching (email, UUID, ISO timestamps).
5. **Uniqueness**: Duplicate primary and business key detection.
6. **Freshness**: Maximum ingestion-to-processing SLA latency.

### F. End-to-End Lineage & Blast Radius Impact Analysis
- Tracks full DAG: $\text{Source} \rightarrow \text{Dataset} \rightarrow \text{Pipeline} \rightarrow \text{Table} \rightarrow \text{Metric} \rightarrow \text{Dashboard} \rightarrow \text{AI Model} \rightarrow \text{Decision}$.
- When any upstream dataset or schema changes, the blast radius calculation outputs affected tables, downstream metrics, BI dashboards, and AI agents.

### G. Centralized Metric Store & Semantic Layer
- Standard definitions for critical KPIs (e.g. ARR, MRR, CAC, LTV, NRR, Gross Margin).
- Prevents metric fragmentation across dashboards, executive reports, and AI query prompts.

### H. Feature Store, ML Data & RAG Pipeline
- Offline / Online feature stores with point-in-time correctness.
- ML dataset versioning and deterministic train/val/test splits preventing target leakage.
- Governed RAG document ingestion pipeline with chunking, embedding, vector indexing, and source provenance.

### I. Data FinOps & Cost Management
- Granular cost tracking across storage, compute, query runs, and pipeline executions.
- Unit economics: Cost per pipeline run, cost per dataset GB, and budget variance alerts.

---

## 3. Data Governance & Security Boundaries

### Non-Negotiable Semantic Boundaries
1. $\text{RAW INGESTED DATA} \neq \text{VALIDATED SILVER} \neq \text{CURATED GOLD DATA PRODUCT} \neq \text{EXECUTIVE DECISION INPUT}$.
2. $\text{DATA AVAILABILITY} \neq \text{DATA PERMISSION} \neq \text{AI TRAINING AUTHORIZATION}$.

### Strict Prohibited Actions
- `AUTONOMOUS_DROP_DATASET`: AI and automated pipelines cannot drop production tables or delete data lake partitions.
- `AUTONOMOUS_EXPOSE_PII`: PII masking (redaction, hashing, tokenization) is enforced across non-production environments.
- `AUTONOMOUS_GRANT_DATA_ACCESS`: Access grants require designated Data Steward human approval.
- `AUTONOMOUS_DELETE_DATA_CONTRACT`: Active producer-consumer contracts require mutual agreement.
- `BYPASS_ROW_LEVEL_SECURITY` / `BYPASS_COLUMN_LEVEL_SECURITY`: Queries always execute within tenant and user authorization context.
- `FABRICATE_DATA_METRICS`: AI Copilot responses must expose underlying sources, SQL logic, and confidence scores.

---

## 4. AI Workforce Agents

| Agent Name | ID | Permissions | Core Responsibility |
|---|---|---|---|
| **Data Architect Agent** | `data_architect_agent` | `READ_ENTERPRISE_DATA_OS`, `MANAGE_DATA_SOURCES`, `MANAGE_SEMANTIC_LAYER` | Designs domain boundaries, medallion tiers, and storage layouts |
| **Ingestion Pipeline Agent** | `ingestion_pipeline_agent` | `READ_ENTERPRISE_DATA_OS`, `MANAGE_DATA_SOURCES`, `MANAGE_DATA_PIPELINES` | Configures CDC streams, orchestrates DAG workflows, monitors watermarks |
| **Data Quality Agent** | `data_quality_agent` | `READ_ENTERPRISE_DATA_OS`, `MANAGE_DATA_QUALITY` | Runs 6-dimension quality scorecards, detects schema and data drift |
| **Data Contract Agent** | `data_contract_agent` | `READ_ENTERPRISE_DATA_OS`, `MANAGE_DATA_CONTRACTS` | Evaluates schema compatibility (backward/forward), enforces SLAs |
| **Semantic Layer Agent** | `semantic_layer_agent` | `READ_ENTERPRISE_DATA_OS`, `MANAGE_SEMANTIC_LAYER`, `MANAGE_DATA_CATALOG` | Manages metric formulas (ARR, CAC, LTV) and business glossary terms |
| **Data Lineage Agent** | `data_lineage_agent` | `READ_ENTERPRISE_DATA_OS`, `MANAGE_DATA_CATALOG` | Builds end-to-end lineage graphs and calculates change blast radius |
| **Data Governance Agent** | `data_governance_agent` | `READ_ENTERPRISE_DATA_OS`, `MANAGE_DATA_GOVERNANCE` | Enforces RBAC/ABAC/CLS/RLS access grants and data retention policies |
| **Feature Store Agent** | `feature_store_agent` | `READ_ENTERPRISE_DATA_OS`, `MANAGE_FEATURE_STORE` | Manages ML entity features, point-in-time joins, and RAG pipelines |
| **Data FinOps Agent** | `data_finops_agent` | `READ_ENTERPRISE_DATA_OS`, `ANALYZE_DATA_FINOPS` | Allocates storage/compute costs, computes unit economics, monitors budgets |
| **Data Copilot Agent** | `data_copilot_agent` | `READ_ENTERPRISE_DATA_OS` | Grounded NL-to-Data conversational assistant with strict evidence boundaries |

---

## 5. API Endpoints Reference (`/api/v1/data-os`)

- `GET /api/v1/data-os/overview`: Summary metrics, counts, platform health.
- `GET /api/v1/data-os/domains`: List data domains.
- `POST /api/v1/data-os/sources`: Register new data source (credentials via Vault).
- `GET /api/v1/data-os/pipelines`: List pipelines and DAG status.
- `POST /api/v1/data-os/datasets`: Register lakehouse dataset (Bronze/Silver/Gold).
- `POST /api/v1/data-os/schemas/evaluate`: Schema evolution compatibility check.
- `POST /api/v1/data-os/contracts`: Register and enforce producer-consumer contract.
- `GET /api/v1/data-os/products`: List curated gold data products.
- `GET /api/v1/data-os/catalog/search`: Natural language catalog search.
- `GET /api/v1/data-os/glossary`: Business terms list and standardized definitions.
- `GET /api/v1/data-os/metrics`: Semantic layer metric formulas and dimensions.
- `POST /api/v1/data-os/quality/run`: Run 6-dimension data quality rules.
- `POST /api/v1/data-os/lineage/edge`: Register lineage edge in the enterprise graph.
- `GET /api/v1/data-os/impact-analysis`: Calculate blast radius of a dataset change.
- `POST /api/v1/data-os/access/grants`: Issue fine-grained RBAC/ABAC access grant.
- `POST /api/v1/data-os/features`: Register feature in the Feature Store.
- `POST /api/v1/data-os/rag/index`: Index document in the governed RAG data pipeline.
- `POST /api/v1/data-os/sql/query`: Execute read-only sandboxed analytical SQL query.
- `GET /api/v1/data-os/finops/costs`: Data platform cost allocations and unit economics.
- `POST /api/v1/data-os/copilot/query`: Ask Data Copilot with grounded reasoning.

---

## 6. Frontend Command Center (`/data-os`)

- **Interactive Tab Navigation**:
  - `Overview`: High-level metrics, domain distribution, quality index, FinOps budget.
  - `Sources & Pipelines`: Source catalog, connection status, ingestion jobs, pipeline DAGs.
  - `Lakehouse & Products`: Bronze/Silver/Gold medallion tiers, curated data products.
  - `Contracts & Quality`: Schema registry, contract SLAs, 6-dimension quality radar.
  - `Semantic & Metrics`: Business glossary, metric formulas (ARR, CAC, LTV), dimensions.
  - `Lineage & Governance`: Lineage graph, impact analysis blast radius, access grants.
  - `Data Copilot`: Natural language assistant with evidence grounding tabs (Facts, Inferences, Hypotheses, Recommendations).

---

## 7. Verification & Testing

Phase 62 includes a comprehensive test suite in [test_unified_enterprise_data_os_platform.py](file:///d:/Agents%20Doc%20Dov/Agen%20Dev/uzaii-develop-by-norths/tests/unit/backend/test_unified_enterprise_data_os_platform.py):
- **21 Unit Tests** validating all services, agents, prohibited safety actions, SQL sandboxing, schema compatibility, and FinOps calculations.
- **100% Pass Rate** with zero regressions across all previous platforms.
