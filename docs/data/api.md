# API Reference
All ADKOS endpoints are mounted under `/api/v1/data-knowledge-os`:
- `GET /health`: Health and telemetry summary.
- `GET/POST /sources`: Data source registration and listing.
- `GET/POST /pipelines`: Pipeline execution and scheduling.
- `GET/POST /products`: Governed data products and contracts.
- `GET/POST /quality/rules`: Data quality rules and scorecards.
- `GET /lineage/{asset_id}`: End-to-end lineage graph.
- `POST /knowledge/query`: Multi-hop knowledge graph queries.
- `POST /search`: Hybrid enterprise search across documents and graph.
- `POST /query/natural-language`: Governed text-to-data studio.
- `POST /loop/run`: Autonomous data lifecycle loop orchestration.
