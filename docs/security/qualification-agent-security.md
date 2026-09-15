# Qualification Agent Security & Boundaries

## Security Model

The Qualification Agent is designed with zero-trust boundaries to ensure safe execution when evaluating raw external web research and CRM data.

---

## Key Security Controls

1. **Untrusted Data Isolation**:
   - Web research excerpts, HTML titles, and raw notes are wrapped in `<UNTRUSTED_EXTERNAL_DATA>` prompt tags during agent prompt formatting.
   - Prevents prompt injection attacks embedded inside scraped web pages or contact forms.

2. **Zero Communication Capabilities**:
   - Granted permissions: Read-only sandbox tools + `CREATE_QUALIFICATION_RESULT`.
   - Prohibited permissions: `SEND_EMAIL`, `SEND_MESSAGE`, `SEND_WHATSAPP`, `MAKE_PAYMENT`, `MODIFY_EXTERNAL_RESOURCE`.

3. **Immutable Scoring Integration**:
   - Reads deterministic Opportunity Scores and Service Recommendations without modifying or recalibrating them.

4. **Auditability & Traceability**:
   - Every qualification attempt records `agent_run_id`, tool execution steps, and factor evidence lists.
   - Human overrides maintain a full audit record including timestamp and user ID.
