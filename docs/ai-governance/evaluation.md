# AI Evaluation Framework & Quality Grading

## Evaluation Dimensions

The `AIEvaluationEngine` provides a composite scoring mechanism across four core pillars:

```text
               ┌───────────────────────────────┐
               │    Composite Score (0-100)    │
               └──────────────┬────────────────┘
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌───────────────────┐ ┌───────────────┐ ┌───────────────────┐
│Structural Quality │ │Policy Compl.  │ │Factual Grounding  │
│(Schema & Format)  │ │(Risk & Rules) │ │(Context Overlap)  │
└───────────────────┘ └───────────────┘ └───────────────────┘
```

### 1. Structural Quality (Weight: 25%)
- Non-empty output validation
- JSON parseability and type conformity
- Required key presence and schema validation

### 2. Policy Compliance (Weight: 25%)
- Detection of prohibited guarantees ("100% guaranteed delivery", "absolute zero downtime")
- Detection of unauthorized commitments
- Tone and safety compliance

### 3. Factual Grounding (Weight: 35%)
- Reference source token overlap & n-gram containment
- Prevention of hallucinations and ungrounded facts
- Citation validation against provided source context

### 4. Toxicity & Safety Defense (Weight: 15%)
- Pattern matching against adversarial prompts
- Scrubbing of sensitive customer identifiers
- Refusal behavior checks on unsafe instructions

## Human-in-the-Loop Evaluation

In addition to automated evaluators, human reviewers submit `HumanEvaluation` records scoring:
- Correctness (1-5)
- Completeness (1-5)
- Evidence & Citations (1-5)
- Safety (1-5)
- Business Usefulness (1-5)
- Edit distance & revision magnitude (`HumanRevisionRecord`)
