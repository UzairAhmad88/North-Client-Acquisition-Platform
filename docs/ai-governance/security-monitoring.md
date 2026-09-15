# AI Security, Safety & Threat Monitoring

## Threat Vectors & Mitigation

The AI Security subsystem monitors incoming prompts, agent tool executions, and generated completions against malicious or unsafe behavior patterns.

```mermaid
graph TD
    Prompt[User / Workflow Input] --> PromptScan[Prompt Injection & Delimiter Scanner]
    PromptScan --> ToolAuth[Tool Permission Whitelist Validator]
    ToolAuth --> SandboxedExec[Sandboxed Tool Execution]
    SandboxedExec --> ModelInfer[Model Completion Generation]
    ModelInfer --> LeakageScan[Data Leakage & PII Redactor]
    LeakageScan --> VerifiedOutput[Safe Emitted Output]
```

### 1. Prompt Injection Defense
- Scans inputs for instruction override phrases (`ignore all previous instructions`, `reveal your system prompt`, `you are now DAN`).
- Delimiter sandboxing: Encapsulates user inputs within structured XML/JSON contexts to avoid delimiter hijacking.

### 2. Unauthorized Tool Invocation
- Agents are explicitly restricted to tools specified in `AgentVersion.allowed_tools`.
- Attempts to call unregistered tools trigger an `AISecurityEvent` with action `BLOCKED` and audit notifications.

### 3. Data Exfiltration & PII Protection
- Inspects outputs for unredacted credit cards, authentication tokens, API secrets, and sensitive personal data.
- Redacts or aborts completions matching confidential data patterns.
