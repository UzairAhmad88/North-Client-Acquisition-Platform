# Agent Core Runtime & Orchestration Architecture

## Overview

The **North's Agent Runtime** is a controlled, secure, and auditable framework for agentic AI execution in **Uzaii Develop By North's**.

---

## Core Pipeline

```
                               +-----------------------------+
                               |     Agent Execution Request  |
                               +--------------+--------------+
                                              |
                                     +--------v--------+
                                     |  Agent Registry |
                                     +--------+--------+
                                              | (Verify Enabled, Metadata, Permissions)
                                     +--------v--------+
                                     |   Agent Context | (Least-Privilege Tenant Context)
                                     +--------+--------+
                                              |
                                     +--------v--------+
                                     |   AI Router     | (Model Policy & Token Budget)
                                     +--------+--------+
                                              |
                        +---------------------+---------------------+
                        |                                           |
               +--------v--------+                         +--------v--------+
               |  Tool Sandbox   |                         |  Agent Engine   |
               | (Perm Guard,    |                         | (State Machine, |
               |  Budget & Auth) |                         |  Confidence)    |
               +--------+--------+                         +--------+--------+
                        |                                           |
                        +---------------------+---------------------+
                                              |
                                     +--------v--------+
                                     | Structured Result|
                                     +--------+--------+
                                              |
                                     +--------v--------+
                                     |  Orchestrator   | (Graph Nodes & Transitions)
                                     +--------+--------+
                                              |
                          +-------------------+-------------------+
                          |                                       |
                 +--------v--------+                     +--------v--------+
                 |  Human Approval |                     | Workflow Complete|
                 | (Paused State)  |                     | (Persisted State)|
                 +-----------------+                     +------------------+
```

---

## Architectural Guarantees

1. **Side-Effect Isolation**: Agents prepare work but have zero permission to issue autonomous external communications (`SEND_EMAIL`, `SEND_MESSAGE`, `SEND_WHATSAPP`, `MAKE_PAYMENT`).
2. **Deny-By-Default Permissions**: Tool execution requires explicit permission grants.
3. **Prompt Injection Isolation**: External web/search content is sanitized and wrapped as untrusted data blocks.
4. **State Machine Integrity**: State transitions follow an explicit allowed graph (`CREATED` -> `RUNNING` -> `WAITING_FOR_APPROVAL` / `PAUSED` / `COMPLETED` / `FAILED` / `CANCELLED`).
5. **Full Observability**: Persistent `agent_runs`, `agent_events`, and `ai_usage` tables record every step, tool call, token cost, and latency.
