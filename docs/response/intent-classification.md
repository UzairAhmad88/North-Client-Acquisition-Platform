# Intent Classification, Buying Signals & Requirements Extraction

## 1. Multi-Label Intent Classifier

The `IntentClassifier` evaluates inbound message bodies against deterministic keyword patterns and linguistic rules. It returns:
1. `primary_intent`: Top matching intent category.
2. `all_intents`: List of all matched intent categories.
3. `confidence`: Classification confidence score (`HIGH` >= 0.8, `MEDIUM` >= 0.5, `LOW` < 0.5).

### Supported Intent Categories

| Intent Code | Trigger Patterns / Examples | Default Next Action |
| :--- | :--- | :--- |
| `OPT_OUT` | `stop`, `unsubscribe`, `don't contact me` | `OPT_OUT` |
| `NOT_INTERESTED` | `not interested`, `no thanks`, `remove me` | `CLOSE_CONVERSATION` |
| `REQUEST_FOR_MEETING` | `schedule a call`, `book a meeting`, `available next week` | `SCHEDULE_MEETING` |
| `REQUEST_FOR_PRICE` | `how much`, `pricing`, `quote`, `rates` | `SEND_PROPOSAL` |
| `REQUEST_FOR_INFO` | `tell me more`, `what services`, `send details` | `ANSWER_QUESTIONS` |
| `TECHNICAL_INQUIRY` | `how does it integrate`, `tech stack`, `security` | `ANSWER_QUESTIONS` |
| `BUYING_SIGNAL` | `ready to start`, `send contract`, `where do I sign` | `SCHEDULE_MEETING` |
| `OBJECTION` | `too expensive`, `no budget`, `already using X` | `ADDRESS_OBJECTION` |
| `INTERESTED` | `sounds great`, `interested`, `let's discuss` | `SCHEDULE_MEETING` |
| `GENERAL_QUERY` | Any uncategorized inbound message | `ANSWER_QUESTIONS` |

---

## 2. Buying Signal & Objection Detectors

### Buying Signal Classification (`BuyingSignalDetector`)
- **HIGH**: Mentions contract, readiness to sign, budget allocated, immediate project launch.
- **MODERATE**: Requests pricing sheets, proposal documents, or detailed scope of work.
- **LOW**: Expresses general curiosity or polite interest.
- **NONE**: Neutral or negative message.

### Objection Classification (`ObjectionClassifier`)
- **PRICE**: "Too expensive", "exceeds budget", "high cost".
- **TIMING**: "Not now", "next quarter", "busy right now".
- **COMPETITOR**: "Using another vendor", "already built in-house".
- **AUTHORITY**: "Need approval from CTO", "decision maker away".

---

## 3. Requirement Extractor (`RequirementExtractor`)

Identifies explicit scope items and missing details required for proposals:
- **Categories Extracted**: `WEBSITE`, `SEO`, `AUTOMATION`, `AI_AGENTS`, `CRM_INTEGRATION`, `DESIGN`, `SECURITY`.
- **Missing Information Gaps**: Automatically flags missing `Budget Range`, `Target Timeline`, `Decision Maker Role`, or `Technical Prerequisites`.
