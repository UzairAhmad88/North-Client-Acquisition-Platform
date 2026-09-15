# Event Bus & Domain Event Registry

## Central Event Registry

The platform maintains a formal registry (`global_event_registry`) defining all cataloged domain events with schema contracts, producers, consumers, sensitivity tiers, and retention rules.

| Event Type | Aggregate | Producer | Sensitivity | Default Retention |
| :--- | :--- | :--- | :--- | :--- |
| `business.discovered` | `business` | `discovery_service` | `INTERNAL` | 90 Days |
| `lead.created` | `lead` | `lead_service` | `INTERNAL` | 90 Days |
| `research.completed` | `business` | `research_service` | `INTERNAL` | 90 Days |
| `audit.completed` | `business` | `audit_service` | `INTERNAL` | 90 Days |
| `lead.qualified` | `lead` | `qualification_service` | `INTERNAL` | 90 Days |
| `service.recommended` | `lead` | `recommendation_service` | `INTERNAL` | 90 Days |
| `outreach.draft.created`| `lead` | `personalization_service`| `INTERNAL` | 90 Days |
| `outreach.approved` | `lead` | `outreach_service` | `RESTRICTED` | Permanent |
| `outreach.sent` | `lead` | `communication_guard` | `RESTRICTED` | Permanent |
| `conversation.message_received` | `conversation` | `response_intelligence` | `CONFIDENTIAL` | 180 Days |
| `requirements.confirmed`| `lead` | `requirements_service` | `INTERNAL` | Permanent |
| `solution.approved` | `lead` | `solution_service` | `INTERNAL` | Permanent |
| `estimate.approved` | `lead` | `estimation_service` | `CONFIDENTIAL` | Permanent |
| `proposal.accepted` | `lead` | `proposal_service` | `CONFIDENTIAL` | Permanent |
| `contract.signed` | `contract` | `contract_service` | `RESTRICTED` | Permanent |
| `project.created` | `project` | `project_service` | `INTERNAL` | Permanent |
| `change.approved` | `change_request`| `change_service` | `CONFIDENTIAL` | Permanent |
| `uat.accepted` | `project` | `qa_service` | `INTERNAL` | Permanent |
| `delivery.accepted` | `project` | `delivery_service` | `RESTRICTED` | Permanent |
| `support.request.created`| `support_request`| `support_service` | `INTERNAL` | 90 Days |
| `ai.incident.detected` | `ai_incident` | `ai_governance` | `RESTRICTED` | Permanent |
| `agent.evaluation.completed`| `agent_evaluation`| `ai_governance` | `INTERNAL` | 90 Days |

## Event Bus Provider Abstraction

The `EventBus` interface abstracts publish/subscribe mechanics from concrete messaging engines:
- **`InMemoryEventBus`**: Ultra-reliable in-memory broker with wildcard matching for self-hosted/laptop execution.
- **Provider Pluggability**: Seamless bridge to Redis Streams, RabbitMQ, or Apache Kafka.
