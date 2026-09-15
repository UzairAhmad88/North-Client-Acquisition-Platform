# Finding Model & Health Classification

## Finding Structure

```json
{
  "code": "MISSING_CONTACT_FORM",
  "category": "LEAD_CAPTURE",
  "severity": "MEDIUM",
  "confidence": "MEDIUM",
  "title": "No obvious contact form detected",
  "description": "No visible contact form was detected on the analyzed pages.",
  "evidence": {
    "pages": ["/", "/contact"]
  },
  "affected_page": "https://example.com/contact"
}
```

## Severity vs Confidence

- **Severity** (`INFO`, `LOW`, `MEDIUM`, `HIGH`): Business risk and impact level. (No `CRITICAL` severity used for standard web presence observations).
- **Confidence** (`HIGH`, `MEDIUM`, `LOW`): Certainty of measurement observation.

## Overall Health Score

Determined deterministically:
- `LIMITED_DATA`: Website unavailable, blocked, or `NO_WEBSITE` target.
- `NEEDS_ATTENTION`: At least 1 `HIGH` severity finding observed.
- `FAIR`: 0 `HIGH` findings, but > 2 `MEDIUM` severity findings.
- `HEALTHY`: 0 `HIGH` findings and <= 2 `MEDIUM` severity findings.
