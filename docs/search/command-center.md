# Global Command Center & Action Palette

## 1. Overview & Purpose

The Global Command Center provides a keyboard-driven (`Ctrl+K` / `Cmd+K`) interface for swift navigation, entity inspection, creation workflows, and sensitive state operations across **Uzaii Develop By North's**.

```text
[User / Keyboard Shortcut]
       │
       ▼
[Command Palette UI] ── (Ctrl+K / Cmd+K)
       │
       ▼
[Command Parser & Registry] ──► Tokenize input & match registered command definition
       │
       ▼
[Command Authorizer] ──► Default-deny authorization check against caller's role
       │
       ▼
[Risk & Approval Evaluator]
       ├── LOW / MEDIUM: Execute directly or prompt for basic confirmation
       └── HIGH / CRITICAL: Gate behind explicit Human Approval & Audit Log
       │
       ▼
[Command Executor] ──► Executes target action, emits audit event & returns result
```

---

## 2. Command Categories & Risk Matrix

Commands are strictly classified into 5 categories with explicit risk ratings:

| Category | Typical Actions | Risk Level | Requires Confirmation | Requires Approval Gate |
| :--- | :--- | :--- | :--- | :--- |
| **`NAVIGATION`** | Open dashboard, view proposals, jump to project | `LOW` | No | No |
| **`QUERY`** | Show revenue analytics, list open support tickets | `LOW` | No | No |
| **`CREATE`** | Create new lead, draft requirement, open defect | `MEDIUM` | Yes | No |
| **`UPDATE`** | Update project milestone, change task status | `MEDIUM` | Yes | No |
| **`ACTION`** | Send proposal to client, approve contract, trigger workflow | `HIGH` / `CRITICAL` | Yes | **Yes (Human Gate)** |

---

## 3. Human Approval Gates for Sensitive Actions

The Command Center strictly enforces the platform governance principle: **Autonomous agents and CLI scripts cannot bypass human oversight for sensitive operations.**

1. **High-Risk Operations**:
   - `action.send_proposal`: Dispatching legal or commercial proposals to external clients.
   - `action.approve_contract`: Legally committing tenant contracts or terms.
   - `action.reassign_project_lead`: Reallocating team leadership and delivery responsibility.
   - `action.trigger_workflow`: Initiating heavy asynchronous automation pipelines.
2. **Approval Flow**:
   - The executor inspects `requires_approval` and `has_approval`.
   - If `has_approval=False`, execution is halted with status `PENDING_APPROVAL`, generating a confirmation token and reason.
   - Only upon explicit user confirmation is the command completed.
   - All executions (approved, rejected, or executed) are recorded in `command_audit_events`.

---

## 4. API Endpoints

- `GET /api/v1/command/registry` — Retrieve all available command definitions
- `POST /api/v1/command/parse` — Parse natural command string or shortcut into structured parameters
- `POST /api/v1/command/validate` — Validate command parameters against JSON schema
- `POST /api/v1/command/execute` — Execute command with confirmation and approval flags
