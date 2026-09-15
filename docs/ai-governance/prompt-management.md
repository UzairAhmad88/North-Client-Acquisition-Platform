# Prompt Management & Version Registry

## Architecture

The Prompt Registry provides centralized version control, SHA-256 cryptographic integrity verification, template parameter sanitization, and regression test linkage for all prompt templates.

## Prompt Lifecycle

1. **Draft (`DRAFT`)**: Authoring prompt templates with typed parameters (`{{lead_name}}`, `{{industry}}`).
2. **Testing (`TESTING`)**: Sandbox testing and offline benchmark runs.
3. **Approved (`APPROVED`)**: Validated by evaluation benchmarks and reviewed by human operators.
4. **Production (`PRODUCTION`)**: Active prompt version serving production workflows.
5. **Deprecated / Archived (`DEPRECATED`, `ARCHIVED`)**: Superseded or retired templates.

## Cryptographic Hash Integrity

Every prompt version computes a SHA-256 hash over its raw content:
```python
sha256 = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()
```
If a runtime payload's hash diverges from the registered `content_hash`, execution is rejected to prevent tampering.

## Template Parameter Injection Defense

Templates are scanned for:
- System prompt delimiter overrides (`[SYSTEM]`, `<|im_start|>`, `### Instruction`)
- Unsanitized dangerous parameter injections
- Jailbreak patterns attempting to override previous instructions
