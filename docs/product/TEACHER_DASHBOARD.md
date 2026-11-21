# Teacher Analytics Dashboard Specification

## Principal question

"Which concept should I reteach, which students need help, and did my intervention work?"

## Layout

1. Header: class/section selector, syllabus range, timeframe, data freshness and learner coverage.
2. KPI cards: active learners, assessments completed, coverage-weighted mastery, number needing attention; always show denominator.
3. Concept gap heatmap: concepts x students/groups, with `unassessed` separate from `low mastery`.
4. Misconception patterns: tag frequency, supporting anonymized excerpts, confidence, attempt counts and trend.
5. Intervention queue: student, weak prerequisite, evidence recency, overdue review, suggested practice action.
6. Growth: within-student concept trajectory, time since last revision, transfer/retention comparison.
7. Assignment actions: send a short practice set and check post-assignment outcome.

## Metric definitions

`coverage = assessed_students / eligible_students`; `class_mastery = mean(latest_mastery of assessed student-concept pairs)` with n and missingness disclosed. `recurring_misconception_rate = unique_assessed_students_with_tag / assessed_students_in_concept`, not raw model tag count alone. `review_overdue = due_at < now AND not completed`. Never compare cohorts without coverage and recentness caveats.

## Drill-down example

Teacher selects "Ohm's Law" with estimated class mastery 41%, based on 29/42 assessed learners (illustrative only). Dashboard shows 11 distinct students with resistance-current misconception labels. Teacher assigns a 5-minute mini-lesson and 3 scenario-flip items, then checks change in reasoning and transfer success 48h later. Avoid automatically stating the intervention *caused* any increase.

## Design, roles and safeguards

Teacher can only query enrolled students in classes assigned to them. Avoid publicly visible individual leaderboards. Show "AI-suggested" badges and allow corrections. Report uncertainty and low sample size. Limit PII and raw student text exports, with audit logging for drill-down views.

## API data needs

`GET /api/teacher/classes/{class_id}/overview?from=&to=` returns counts, coverage, timestamps and metrics. `GET /api/teacher/classes/{class_id}/concepts` returns class concept summary and prerequisite gaps. `GET /api/teacher/classes/{class_id}/misconceptions` returns aggregated tagged evidence. `GET /api/teacher/classes/{class_id}/interventions` returns eligible recommendations. Auth must derive teacher identity from session, not client-supplied teacher_id.
