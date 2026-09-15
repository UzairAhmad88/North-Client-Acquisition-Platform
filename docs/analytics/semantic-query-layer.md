# Semantic Query Layer for Natural Language Analytics

## 1. Architectural Guardrails

The Semantic Query Layer allows users and agents to query portfolio metrics using natural language without exposing the database to arbitrary SQL execution risks.

```text
User Question: "Why are project estimates inaccurate?"
                      ↓
Semantic Layer Intent Resolution (`SemanticLayerEngine`)
                      ↓
Approved Metric Model Mapping (`ESTIMATION_ACCURACY`)
                      ↓
Parameterized Query Execution & Aggregation
                      ↓
Factually Grounded Response with Caveats & Evidence Notes
```

---

## 2. Prohibited AI Capabilities

- `EXECUTE_ARBITRARY_SQL`: Strictly prohibited in agent permissions.
- Direct LLM table querying: Disallowed.
- Fabricating statistical metrics: Disallowed. Responses cite real sample sizes and dataset freshness.
