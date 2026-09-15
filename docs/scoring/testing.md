# Lead Scoring Test Suite & Verification Policy

## Automated Test Coverage

- `tests/unit/backend/test_scoring.py`: Covers 7 component scoring rules, exact weighted formula calculation, boundary testing (`0`, `39`, `40`, `59`, `60`, `79`, `80`, `100`), missing data handling, confidence score, score change explanations, API routes, security IDOR protection, and read-only non-side-effect enforcement.
- `tests/unit/services/test_scoring_service.py`: Verifies service availability and imports.

## Validation Commands

```bash
python -m pytest tests/unit/backend/test_scoring.py
python -m pytest
python -m ruff check .
python -m mypy app
npm run build (in frontend/)
```
