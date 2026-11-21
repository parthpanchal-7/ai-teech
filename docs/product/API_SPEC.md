# API Contract v1

This contract is illustrative and must be implemented with generated OpenAPI via FastAPI. All protected endpoints require an authenticated subject and server-enforced resource ownership.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Service health; no secrets |
| GET | `/api/concepts` | Syllabus nodes and prerequisites |
| POST | `/api/diagnostic/start` | Start tagged diagnostic session |
| POST | `/api/answers` | Grade and record attempt, update learning state |
| GET | `/api/students/me/profile` | Authenticated student mastery |
| GET | `/api/students/me/reviews` | Upcoming and overdue study items |
| GET | `/api/teacher/classes/{id}/overview` | Class analytics (membership verified) |
| GET | `/api/teacher/classes/{id}/misconceptions` | Aggregate misconception themes |
| POST | `/api/teacher/classes/{id}/assignments` | Assign concept practice |

## POST /api/answers

Request:

```json
{
  "question_id": "ohms-001",
  "session_id": "session-uuid",
  "answer": "Current decreases",
  "reasoning": "With constant voltage, increasing resistance reduces current.",
  "confidence": 0.8,
  "idempotency_key": "event-uuid"
}
```

Response:

```json
{
  "attempt_id": "attempt-uuid",
  "correct": true,
  "reasoning_quality": 0.93,
  "misconception": null,
  "mastery": {"before": 42, "after": 49, "state": "developing", "evidence_count": 3},
  "next_action": "scenario_flip",
  "next_question_id": "ohms-transfer-002",
  "review_due_at": "2026-11-22T13:00:00Z",
  "ai_evaluation": {"mode": "model", "confidence": 0.87}
}
```

Numbers and identifiers are example data, not an actual student evaluation. Correctness must use stored question rubric, never unrestricted free-text LLM verdict alone.

## Error contract

Use `application/problem+json` with `type`, `title`, `status`, `detail`, `request_id`. Codes: 400 schema/context error, 401 unauthorized, 403 forbidden, 404 unknown concept/question, 409 duplicate/conflicting attempt, 429 rate limit, 503 provider unavailable *only if fallback is impossible*. Do not expose prompts, keys, raw provider trace or student PII in errors.

## Data semantics

Every aggregate returns `sample_size`, `eligible_count`, `last_updated_at`, and `demo_data` flag. Use pagination on history; immutable `attempt_id`; server timestamps UTC; consistent concept IDs and schema versioning.
