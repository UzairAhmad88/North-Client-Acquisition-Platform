# Recommendation Priority & Confidence Matrix

## Priority Algorithm Matrix

Recommendation Priority balances **Relevance Score** against **Confidence**:

| Relevance Score | Confidence | Calculated Priority |
|---|---|---|
| 80 – 100 (`STRONG`) | `HIGH` / `MEDIUM` | `HIGH` |
| 80 – 100 (`STRONG`) | `LOW` | `MEDIUM` |
| 60 – 79 (`GOOD`) | `HIGH` / `MEDIUM` | `MEDIUM` |
| 60 – 79 (`GOOD`) | `LOW` | `LOW` |
| 0 – 59 (`POSSIBLE`/`WEAK`) | Any | `LOW` |

---

## Confidence Level Definitions

- **`HIGH`**: Supported by multiple high-trust evidence sources (e.g. completed technical audit AND validated public research).
- **`MEDIUM`**: Supported by at least one explicit evidence source (e.g. audit finding or business category alignment).
- **`LOW`**: Minimal or missing evidence data; recommendations based purely on general defaults.
