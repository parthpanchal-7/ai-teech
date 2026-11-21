# Product Requirements Document

## Problem and outcome

Typical answer-oriented tools cannot distinguish retrieval of a memorized result from a student's ability to explain, generalize and retain the idea. Ai-Teech uses an evidence-based learner model and gives teachers classroom interventions.

## Users and jobs

- **Student:** locate weak concepts, receive understandable help, prove comprehension through explanation and application, see what to revise.
- **Teacher:** identify the largest actionable gaps, investigate misconceptions, assign targeted activities, follow progress without manual spreadsheet work.
- **School admin (phase 2):** control rosters, consent, retention and reporting.

## MVP journey

1. Student joins an authorized class or demo account.
2. Takes short concept-tagged diagnostic (7-12 questions).
3. Receives a mastery map with unassessed states distinct from weak states.
4. Answers adaptive question plus optional confidence and mandatory short reasoning.
5. Receives supported misconception feedback and a "scenario flip" transfer question.
6. Mastery evidence updates after each response and next retrieval gets scheduled.
7. Teacher dashboard aggregates authorized class evidence and recommends intervention.

## Requirements and acceptance

| ID | Requirement | Testable acceptance |
|---|---|---|
| FR-01 | Diagnostic | Creates concept-specific records and provenance |
| FR-02 | Concept graph | Valid prerequisites alter next selection |
| FR-03 | Learner mastery | Every answer persists attempt, evidence and bounded score |
| FR-04 | Adaptation | Low/high mastery profiles get appropriately distinct difficulty |
| FR-05 | Misconceptions | AI/rule engine uses *reasoning*, not only final option; supports uncertainty |
| FR-06 | Spacing | Due/overdue/upcoming reviews persist across sessions |
| FR-07 | Teacher analytics | Real authorized learner records drive class-level aggregates |
| FR-08 | Transfer check | Same concept tested via changed context or representation |
| NFR-01 | Quality | Human-rated correctness and misconception evaluation meet release gates in QA doc |
| NFR-02 | Speed | API and UI performance budgets defined and instrumented |
| NFR-03 | Safety | Row-level authorization, privacy controls, audit and graceful AI fallback |

## Non-goals for MVP

No universal curricula, auto-grading long essays, live voice chat, parent app, ML fine-tuning, heavy multi-agent orchestration, competitive leaderboard or unmoderated user-upload knowledge base.

## Definition of done

One end-to-end Ohm's Law scenario demonstrates all seven mandatory features; AI outage is survivable; teacher drill-down is source-backed; tests pass; staging URL is usable and secrets not exposed.
