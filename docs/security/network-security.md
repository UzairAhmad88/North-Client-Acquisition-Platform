# Network Security & Microsegmentation

## 1. Logical Security Zones
- `PUBLIC`: External CDN and ingress endpoints.
- `DMZ`: Reverse proxies and API gateways.
- `APPLICATION`: Business microservices and application servers.
- `DATABASE`: Relational, document, and vector data stores.
- `MANAGEMENT`: Bastion hosts and administrative planes.
- `SECURITY`: SOC, SIEM, and vault infrastructure.
- `AI`: Model inference nodes and training infrastructure.
- `DATA`: Data lakehouse and ETL pipelines.
