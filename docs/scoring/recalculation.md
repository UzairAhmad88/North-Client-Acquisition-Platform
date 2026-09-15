# Score Recalculation & Workflow Integration

## Recalculation Triggers

Score recalculation is triggered:
1. **On-demand via API**: `POST /api/v1/scoring/leads/{lead_id}/calculate`.
2. **On-demand via UI**: Clicking "Recalculate Score" on the Lead Detail page.
3. **Background Worker Task**: `workers/tasks/scoring.py` -> `execute_scoring_task(db, lead_id)`.
4. **Post-Audit Completion**: Automatically executed when a website audit completes for a business.
