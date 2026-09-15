# Outreach Provider Architecture

## Architecture

The system decouples message orchestration from external transport providers using an abstract provider interface.

```
                 +------------------------+
                 |  BaseEmailProvider     |
                 +------------------------+
                             ^
                             |
         +-------------------+-------------------+
         |                                       |
+-------------------+                 +-------------------+
| MockEmailProvider |                 | LiveEmailProvider |
+-------------------+                 +-------------------+
```

## Security & Default Safety

- `REAL_SEND=false` by default in environment configuration.
- Under `REAL_SEND=false`, all messages are handled by `MockEmailProvider` which simulates network latency, random or explicit bounce responses, and generates synthetic message IDs without sending real emails.
- AI agents are completely isolated from provider interfaces; only `CommunicationService` can invoke provider dispatch after passing through `CommunicationGuard`.
