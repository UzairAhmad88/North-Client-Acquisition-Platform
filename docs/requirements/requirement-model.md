# Requirement Model & Source Evidence Architecture

## 1. Explicit vs Inferred Distinction

A core design requirement of Phase 22 is preserving the boundary between what the client explicitly stated and what the system or AI inferred:

- `explicit = True`: Requirement explicitly requested in client messages (`source_type: CLIENT_MESSAGE`).
- `explicit = False`: Requirement inferred by AI (`source_type: AI_INFERENCE`).
- `status`:
  - `PROPOSED`: Newly extracted or inferred requirement awaiting human review.
  - `IN_REVIEW`: Currently under operator inspection.
  - `CONFIRMED`: Explicitly confirmed by a human operator (`confirmed_by_id`, `confirmed_at`).
  - `NEEDS_CLARIFICATION`: Subject to contradiction or missing critical details.
  - `REJECTED`: Rejected during human review.
  - `SUPERSEDED`: Replaced by a newer requirement version.

---

## 2. Requirement Entity Schema (`requirements`)

```python
class ClientRequirement(BaseModel):
    id: uuid.UUID
    discovery_session_id: uuid.UUID
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID]
    category: str  # BOOKING, PAYMENT, WEBSITE, AUTOMATION, AI_FEATURE, CRM, etc.
    title: str
    description: str
    source_type: str  # CLIENT_MESSAGE, CLIENT_DOCUMENT, CLIENT_CONFIRMATION, HUMAN_NOTE, RESEARCH, AUDIT, SYSTEM_INFERENCE, AI_INFERENCE
    source_reference: Optional[str]
    explicit: bool
    confidence: str  # HIGH, MEDIUM, LOW, UNKNOWN
    status: str  # PROPOSED, IN_REVIEW, NEEDS_CLARIFICATION, CONFIRMED, REJECTED, SUPERSEDED, UNKNOWN
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL
    version: int
    confirmed_by_id: Optional[uuid.UUID]
    confirmed_at: Optional[datetime]
```

---

## 3. Evidence Traceability (`requirement_evidence`)

Every requirement can link to one or more `RequirementEvidence` records containing the exact source text snippet, source type, and confidence score, making all AI inferences and extracted scope items 100% auditable.
