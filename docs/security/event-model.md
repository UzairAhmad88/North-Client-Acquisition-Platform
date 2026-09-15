# Security Information & Event Model

## 1. Normalized Schema
All ingested events normalize into standard attributes:
- `timestamp`: UTC ISO-8601 timestamp.
- `actor`: Subject identifier.
- `action`: Specific operation performed.
- `resource`: Target URI or ARN.
- `source` / `destination`: IP address, port, and geo metadata.
- `device_id`: Originating hardware ID.
- `result`: SUCCESS, FAILURE, or DENIED.
- `risk_score`: Initial telemetry score.
