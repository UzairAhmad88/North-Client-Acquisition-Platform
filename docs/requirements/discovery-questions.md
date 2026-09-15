# Discovery Question Generator & Conversational Intake

## 1. Non-Interrogation Principle

To prevent overwhelming clients with long lists of questions (30+ questions), the `DiscoveryQuestionGenerator`:
1. Identifies critical unanswered gaps (e.g. working hours for booking, payment gateway choice, budget, timeline).
2. Generates short, client-friendly, non-technical questions.
3. Limits output to top prioritized questions (maximum 3 to 4 active questions).
4. Recalculates new questions progressively as client answers are submitted.

---

## 2. Question Schema (`requirement_questions`)

- `id`: UUID Primary Key.
- `discovery_session_id`: Foreign key to `discovery_sessions.id`.
- `source_requirement_id`: Foreign key to `requirements.id`.
- `question`: Clear, non-technical question text.
- `category`: Category (`SCOPE`, `WORKFLOW`, `INTEGRATION`, `BUDGET`, `TIMELINE`).
- `priority`: Priority tier (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `OPTIONAL`).
- `reason`: Internal explanation of why the question matters.
- `status`: Question status (`PROPOSED`, `ASKED`, `ANSWERED`, `SKIPPED`, `CANCELLED`).
- `answer_text`: Submitted client/operator answer text.
- `answered_at`: Timestamp when answered.
