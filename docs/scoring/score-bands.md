# Score Bands & Boundary Specifications

## Priority Bands

| Score Range | Priority Band | Description |
| :--- | :--- | :--- |
| **80 – 100** | `HIGH` | High-priority opportunity with significant service gaps and strong contactability/fit. |
| **60 – 79** | `MEDIUM` | Moderate opportunity with clear gaps in digital presence or automation. |
| **40 – 59** | `LOW` | Low opportunity; business has functional systems or low initial fit. |
| **0 – 39** | `VERY_LOW` | Minimal opportunity or unqualified business signals. |

## Explicit Boundary Rules

```text
Score:  0 -> VERY_LOW
Score: 39 -> VERY_LOW
Score: 40 -> LOW
Score: 59 -> LOW
Score: 60 -> MEDIUM
Score: 79 -> MEDIUM
Score: 80 -> HIGH
Score:100 -> HIGH
```
