# Scoped API Keys & Service Account Infrastructure

## 1. Machine-to-Machine Integration Secrets

External pipelines, CI/CD systems, and third-party integrations authenticate using scoped API keys:

- **Key Format**: `uz_<prefix>_<secret>` (e.g. `uz_9a1f_aB8x9K2...`)
- **Storage Security**: Only the SHA-256 hash (`key_hash`) and key prefix (`key_prefix`) are stored in the database. The raw secret is displayed **exactly once** upon generation.
- **Granular Scopes**: API keys are restricted to explicit scope arrays (`["leads.read", "projects.read"]`). Wildcard root access is prohibited.

---

## 2. Infrastructure Service Accounts

Background workers (e.g. Celery workers, ETL schedulers) execute under dedicated `ServiceAccount` principals (`service_accounts`), receiving the minimum set of permissions required for their specific tasks.
