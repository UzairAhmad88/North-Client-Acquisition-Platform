# Cybersecurity & Zero-Trust API Reference

## 1. API Surface
Prefix: `/api/v1/cybersecurity-zero-trust`

Endpoints:
- `GET /health`: Platform command center summary.
- `POST /assets`: Register enterprise asset.
- `POST /zero-trust/evaluate`: Execute continuous trust evaluation.
- `POST /privileged-access/request`: Request JIT PAM elevation.
- `POST /secrets`: Create encrypted secret in vault.
- `POST /secrets/{secret_id}/rotate`: Execute automated rotation.
- `POST /events/ingest`: Ingest and normalize security event.
- `POST /detections/rules`: Register Sigma/correlation rule.
- `POST /threats/indicators`: Ingest threat intelligence IoC.
- `POST /sbom/scan`: Scan CycloneDX/SPDX SBOM manifest.
- `POST /incidents`: Create security incident.
- `POST /ai/prompt-security/check`: Check prompt for injection and jailbreak.
- `POST /ai/agent-tool/validate`: Validate agent tool call permissions.
- `POST /graph/query`: Query security graph blast radius.
- `POST /defense-loop/run`: Trigger continuous 7-stage defense cycle.
