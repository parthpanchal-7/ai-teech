# Ai-Teech Hackathon Judge Demo

Duration: 3-5 minutes. Run with `docker compose up --build -d` or two local dev terminals. All learner records are synthetic demo data.

## Story: a student can choose the right option without understanding why

1. **Problem (20s):** Generic chat tutors answer questions; Ai-Teech records *evidence of comprehension* and makes it visible to teachers.
2. **Diagnostic (45s):** Select Parth demo profile, open Diagnostic Test and complete or show the 7 concept-tagged questions. Every answer requests short reasoning.
3. **Adaptive practice (60s):** Open Practice Lab and choose Ohm's Law from Concept Map. If asked "At constant voltage, if resistance doubles...", answer "Double" and reason "More resistance pushes more current through the wire." Feedback reveals the resistance-current misconception and a lower mastery score.
4. **Remediation (35s):** Show correction and follow-up question. Explain that the concept graph and recent evidence influence selection; AI analysis uses Gemini when configured and a safe offline rubric when not.
5. **Revision (25s):** Open My Revision and show persisted next-review date.
6. **Teacher analytics (45s):** Open Teacher Insights, click "Load sample class data", show concept chart, misconception radar and class gaps; clarify counts are synthetic.
7. **Close (20s):** "Ai-Teech does not just answer; it asks students to explain, practice in a changed situation and revisit later. Teachers see actionable learning gaps."

## Judge questions / honest answers

- **Is the mastery score clinically or scientifically calibrated?** No. The current explainable bounded update is a hackathon heuristic; classroom pilot validation is planned.
- **Does it use AI?** Optional Gemini structured reasoning analysis with model provenance. Without key it uses deterministic rule-based fallback and explicitly labels the analysis mode.
- **How can judges verify real Gemini?** Configure backend/.env, run `python -m app.ai_check`, then submit a practice answer and inspect `analysis_mode=gemini-structured`. The real call requires a valid key and network.
- **Is it safe for real school data?** Not yet. This demo uses selectable sample profiles; production requires real auth, class permissions, consent, privacy review and rate limiting.
- **Can it run without external APIs?** Yes. Core full-stack workflow works offline after dependencies are installed.

## Pre-demo verification

```bash
cd backend && python -m pytest -q
cd ../frontend && npm run build
```

For a fresh isolated demo database, use a new `DATABASE_PATH` (or a new Docker volume); avoid deleting real user data. Confirm service is healthy at `/health` before presenting.
