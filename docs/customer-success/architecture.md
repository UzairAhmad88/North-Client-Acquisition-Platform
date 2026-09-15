# Unified Customer Success Architecture

## System Diagram

```mermaid
graph TD
    ClientProfile[ClientProfileModel] --> ClientRelationship[Stakeholder Relationships]
    ClientProfile --> ClientHealth[HealthScoringEngine]
    ClientProfile --> ClientTimeline[ClientTimelineAggregator]
    ClientProfile --> ClientRisks[ClientRiskDetector]
    ClientProfile --> ClientOpps[ExpansionOpportunityFinder]
    ClientProfile --> ClientRenewals[Renewal Management]

    ClientHealth --> Client360[Client360Synthesizer]
    ClientTimeline --> Client360
    ClientRisks --> Client360
    ClientOpps --> Client360
    ClientRenewals --> Client360

    Client360 --> InternalAPI["/api/v1/customer-success (Full CSM Access)"]
    Client360 --> AuthMasking[CustomerSuccessAuthorizationManager]
    AuthMasking --> PortalAPI["/api/v1/portal/success (Client Safe View)"]
```

## Data Isolation & Multi-Tenancy

Every customer success entity is explicitly partitioned by `tenant_id` and indexed on `client_profile_id` (or `client_account_id`). Foreign key constraints ensure cascading consistency while enforcing strict organization isolation.
