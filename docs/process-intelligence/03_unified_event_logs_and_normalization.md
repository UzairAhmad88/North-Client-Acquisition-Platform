# Unified Event Logs and Normalization

## Ingestion Architecture
Processes run across heterogeneous enterprise software (SAP, Salesforce, Workday, ServiceNow, Jira, Kafka, Agent Mesh). The Normalization Engine transforms raw audit logs, CDC events, and API traces into standard Process Case Events.

## Schema
- `case_id`: Correlating business transaction ID (e.g., Order #, PO #, Ticket #)
- `event_id`: Monotonically increasing unique event UUID
- `activity`: Standardized activity name
- `timestamp`: UTC ISO-8601 timestamp with sub-millisecond precision
- `actor`: User, Agent, or Service identity
- `system`: Originating source system
- `status`: Scheduled, Started, In-Progress, Suspended, Completed, Failed
- `metadata`: Custom key-value payloads (amounts, SKUs, error codes)\n