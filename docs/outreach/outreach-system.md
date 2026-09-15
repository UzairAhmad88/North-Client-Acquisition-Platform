# Outreach System Architecture

## Overview
The Outreach System provides controlled execution and lifecycle management for human-approved communications sent to prospects and leads. It sits between AI agent drafting (Phase 18) and outbound external communication providers (Phase 19).

## Key Components

1. **ApprovalEngine**: Hashes outreach content using SHA-256 (`sub:<subject>|body:<body>|recip:<email>`). Enforces human review signatures. Any modification to content invalidates previous approval.
2. **CommunicationGuard**: A 15-step validation pipeline executed synchronously at send time before any payload touches an external provider.
3. **EmailProviderService**: Provider abstraction supporting mock dispatch (`REAL_SEND=false`) and live SMTP/SendGrid dispatch (`REAL_SEND=true`).
4. **IdempotencyManager**: Distributed Redis/DB locking keying on `outreach:{id}:send:{version}` to prevent concurrent or duplicate execution.
5. **DncService**: Checks Global, Domain, and Business-level Do Not Contact registries.
6. **FrequencyController**: Enforces per-business daily message limits and cooldown periods.

## System Flow

```
[Phase 18 Draft] ---> [Approval Engine] ---> (Human Approves SHA-256 Hash)
                                                        |
                                                        v
                                             [CommunicationGuard Check]
                                                        |
                                          +-------------+-------------+
                                          | PASS                      | FAIL
                                          v                           v
                               [EmailProviderService]       [Outreach Event Logged: FAILED]
                                          |
                                          v
                               [Outreach Event Logged: SENT]
```
