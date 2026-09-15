# Score Versioning & Historical Snapshot Policy

## Score Versioning

All scores are stored with an explicit `score_version` (default `"1.0"`).
When formula weights or component rules change in future releases, historical scores in `lead_scores` remain unchanged, preserving full auditability.

## Invalidation & Staleness

- `is_stale = true`: Applied to previous score records when a new score calculation is executed.
- Previous score history remains readable via `GET /api/v1/scoring/leads/{lead_id}/history`.
