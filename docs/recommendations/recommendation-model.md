# Service Recommendation Model

## Data Schema (`service_recommendations`)

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Unique recommendation identifier |
| `lead_id` | UUID | FK -> leads.id (CASCADE) | Associated lead |
| `business_id` | UUID | FK -> businesses.id (CASCADE) | Associated business |
| `service_id` | UUID | FK -> services.id (CASCADE) | Associated service catalog entry |
| `recommendation_version` | String(20) | Default "1.0" | Version of recommendation logic |
| `relevance_score` | Float | 0.0 - 100.0 | Weighted relevance score |
| `band` | String(20) | Indexed | `STRONG`, `GOOD`, `POSSIBLE`, `WEAK` |
| `priority` | String(20) | Indexed | `HIGH`, `MEDIUM`, `LOW` |
| `confidence` | String(20) | Indexed | `HIGH`, `MEDIUM`, `LOW` |
| `status` | String(20) | Indexed | `SUGGESTED`, `REVIEWED`, `ACCEPTED`, `REJECTED`, `STALE` |
| `reasons` | JSON | List of strings | Natural language justification |
| `evidence` | JSON | List of dicts | Traceable evidence source items |
| `limitations` | JSON | List of strings | Objective caveats & boundaries |
| `rejection_reason` | Text | Nullable | User reason when rejected |
| `rejected_by` | UUID | FK -> users.id | User who rejected recommendation |
| `rejected_at` | DateTime | Nullable | Timestamp of rejection |
| `accepted_by` | UUID | FK -> users.id | User who accepted recommendation |
| `accepted_at` | DateTime | Nullable | Timestamp of acceptance |
