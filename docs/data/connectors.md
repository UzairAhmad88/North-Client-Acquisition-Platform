# Connector Framework
Standardized connectors in `backend/app/services/data/connectors/`:
- Database (PostgreSQL, MySQL, Snowflake)
- REST / GraphQL APIs
- File Stores (CSV, Parquet, JSON, Excel)
- Cloud Storage (S3, GCS, Azure Blob)
- Applications & CRM (Salesforce, HubSpot, Jira, GitHub)
- Messaging & Streams (Kafka, RabbitMQ, Webhooks)
- Documents & Enterprise Content

Each connector implements `connect()`, `discover_schema()`, `extract()`, `validate()`, `load()`, `health_check()`, `disconnect()`.
