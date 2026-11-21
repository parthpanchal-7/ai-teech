# Architecture and Data Contracts

## Baseline stack

- React/Vite/TypeScript + Tailwind; Recharts for teacher aggregates; optional React Flow for prerequisite graph.
- Python FastAPI + Pydantic + SQLAlchemy (Alembic migrations).
- Local SQLite only for prototype; managed PostgreSQL with pool and backups for production.
- Server-side LLM adapter for structured reasoning evaluation and question drafting; teacher-verified fallback question bank.

## Data flow

Frontend -> authenticated FastAPI -> validation/authorization -> deterministic learner engine -> database transaction -> optional model adapter -> schema validation -> persistence -> response. For slow AI operations return stable loading/progress states; avoid blocking teacher analytics on provider latency.

## Core entities

`users`, `classes`, `enrollments`, `concepts`, `concept_edges`, `questions`, `attempts`, `mastery_snapshots`, `misconception_events`, `review_schedules`, `assignments`, `audit_events`, `model_evaluations`.

Important invariants: one student-concept latest mastery row; append-only attempts; question version and rubric version on every attempt; study event timestamps UTC; tenant/class authorization on analytics; atomic writing of attempt, mastery and review schedule; AI provenance and confidence on inference.

## Performance strategy (targets, not measurements)

| Surface | Proposed target | Approach |
|---|---|---|
| SPA loading | LCP <=2.5s p75 on representative midrange device and network | Route splitting, font preload, compress assets |
| Non-AI API | p95 <=300ms under defined demo traffic | Indexed queries, bounded payloads, pooled DB |
| AI feedback | p95 <=6s on chosen provider under demo load | Structured short outputs, timeouts, fallback |
| Teacher dashboard | p95 <=1.5s on cached class summary | Preaggregate on writes or periodic recompute |
| Reliability | >=99% successful core demo journey in staging runs | Retries only idempotent operations, offline fallback |

Define staging test load explicitly: 50 concurrent users, 5-minute repeated sessions, synthetic data 500 learners/class. Adjust goals after measurement and hosting assessment. Never label these as achieved benchmarks until tested.

## Caching and quality

Use deterministic cached approved questions per concept/difficulty to avoid unnecessary generation. Never cache student-specific private feedback across learners. Request idempotency keys for answer submission to prevent double-scoring. Preload summary analytics asynchronously. Keep prompts concise and rubric-grounded. Quality gate must outrank speculative speed optimizations.

## Security architecture

Session/JWT auth with short expiration and refresh controls; teacher-student membership checks; parameterized DB queries; structured audit logs; secret manager for production; retention policy and deletion/export path; encrypted transit; backup recovery drill. Minors require applicable guardian/school consent review prior to real production onboarding.
