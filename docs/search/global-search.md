# Unified Global Search Engine

## 1. Overview & Architecture

The Unified Global Search engine provides cross-entity discovery across all authorized business domains in **Uzaii Develop By North's**, including Businesses, Leads, Opportunities, Conversations, Requirements, Solutions, Proposals, Contracts, Projects, Tasks, Changes, QA/UAT Defects, Support Tickets, Incidents, Workflows, and AI Traces.

```text
User Query: "find high priority tickets for Acme Corp"
  │
  ▼
[Query Parser] ──► Extracts entity filters, tokens, priority tags, status tags
  │
  ▼
[Query Planner] ──► Compiles structured, parameterized query plan (No raw SQL)
  │
  ▼
[Authorizer] ──► Enforces tenant boundary, user RBAC & client-safe visibility filters
  │
  ▼
[Search Index / DB] ──► Retrieves matching records with exact, prefix & fuzzy matching
  │
  ▼
[Ranking Engine] ──► Multi-factor score = Lexical + Exact + Semantic + Recency + Weight
  │
  ▼
[Snippet Generator] ──► Produces contextual snippets with <mark> highlighting
  │
  ▼
[Search Audit & History] ──► Records query telemetry, latency, and result counts
```

---

## 2. Query Parsing & Structured Planning

The search subsystem operates on strict structured query planning to completely prevent SQL injection or arbitrary query execution:

- **Entity Detection**: Automatically identifies prefixes or keyword hints (`lead:`, `project:`, `defect:`, `client:`, etc.).
- **Status & Priority Extraction**: Maps phrases such as `"high priority"`, `"critical"`, `"open"`, `"resolved"` to typed query filters.
- **Exact Phrase Matching**: Retains quoted terms (`"Acme Corporation"`) for high-weight boost scoring.
- **Parametric Query Plan**: The query planner emits a typed `StructuredQueryPlan` containing only parameterized filter expressions.

---

## 3. Multi-Factor Relevance Ranking

The ranking engine calculates a weighted relevance score ($S \in [0.0, 1.0]$) for each candidate record:

$$S = 0.35 \cdot S_{\text{lexical}} + 0.25 \cdot S_{\text{exact}} + 0.15 \cdot S_{\text{semantic}} + 0.10 \cdot S_{\text{recency}} + 0.10 \cdot W_{\text{entity}} + 0.05 \cdot S_{\text{user}}$$

Where:
- $S_{\text{lexical}}$: Token overlap between parsed query tokens and searchable title/content fields.
- $S_{\text{exact}}$: Exact substring match bonus in titles and entity identifiers.
- $S_{\text{semantic}}$: Vector cosine similarity or conceptual tag match.
- $S_{\text{recency}}$: Exponential decay based on `updated_at` timestamp.
- $W_{\text{entity}}$: Static importance weight for core entities (e.g., Contracts, Proposals, Projects > raw event logs).
- $S_{\text{user}}$: Personalization boost for records assigned to, authored by, or pinned by the requesting user.

---

## 4. Snippet Generation & Private Data Masking

- **Context Window**: Extracts relevant sentences surrounding matching query terms.
- **Query Term Highlighting**: Wraps matched terms in `<mark>` tags for frontend rendering.
- **Data Protection**: Fields categorized as internal notes, margins, financial cost breakdowns, or restricted audit traces are automatically stripped or masked when evaluated for non-admin and client roles.

---

## 5. API Endpoints

- `GET /api/v1/search?q={query}&entity_type={type}&status={status}&priority={priority}&limit=20&offset=0`
- `GET /api/v1/search/suggestions?q={query}`
- `GET /api/v1/search/saved` — List saved search queries
- `POST /api/v1/search/saved` — Save a search query with filters
- `DELETE /api/v1/search/saved/{id}` — Delete a saved search
- `GET /api/v1/search/pins` — List pinned search items
- `POST /api/v1/search/pins` — Pin a specific entity
- `DELETE /api/v1/search/pins/{id}` — Unpin an entity
