# Agent Permission System & Deny-by-Default Policy

## Allowed Granular Permissions

| Permission Name | Description |
|---|---|
| `READ_BUSINESS` | Read business profile attributes |
| `READ_LEAD` | Read lead opportunity details |
| `READ_RESEARCH` | Read public research records |
| `READ_AUDIT` | Read technical website audit findings |
| `READ_SCORE` | Read lead opportunity score breakdown |
| `READ_SERVICES` | Read service catalog entries |
| `SEARCH_WEB` | Perform web search queries |
| `FETCH_WEB` | Fetch public web page content |
| `CREATE_DRAFT` | Prepare internal draft recommendations/outreach |
| `READ_CONVERSATION` | Read historical conversation context |

---

## Strictly Prohibited Communication Permissions

By architectural design, the following permissions are **denied by default** and cannot be granted to any agent:

- `SEND_EMAIL`
- `SEND_MESSAGE`
- `SEND_WHATSAPP`
- `MAKE_PAYMENT`
- `DELETE_DATA`
- `MODIFY_EXTERNAL_RESOURCE`

Any attempt to register an agent or execute a tool with these permissions raises `AgentPermissionDeniedError`.
