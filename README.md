# Ai-Teech

> Learn it. Prove it. Own it.

Ai-Teech is an adaptive exam-preparation **demo MVP** for Class 10 Physics (Electricity). It helps learners practice, explain why they chose an answer, track concept mastery and schedule reviews; a teacher analytics screen summarizes class-wide gaps.

![Status](https://img.shields.io/badge/status-demo%20MVP-BD47F2)

## What works

- Seven-node prerequisite concept graph
- Concept-tagged diagnostic question set and practice questions
- Learner mastery updates persisted to SQLite
- Difficulty-aware, weak-concept question selection
- Reasoning-based misconception heuristics and transparent feedback
- Spaced-review dates and revision list
- Teacher concept analytics and misconception trends across demo students
- Responsive playful React interface

**Important limits:** Demo identities are selectable from the UI; this app has no production authorization, secure teacher-scoped access, guardian-consent flow or real student accounts. The current evaluator is a transparent offline rubric (not a live LLM). Do **not** deploy it with real student personal data or publicly expose it as a school production service. AI provider integration and independent educational validation remain follow-up work.

## Run locally

Requires Python 3.11+ and Node.js 20+.

### Terminal 1 - API

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Terminal 2 - UI

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Vite proxies `/api` to port 8000. Set `VITE_API_BASE_URL` when frontend and backend are on different hosts. See `.env.example` in each package.

## Test

```bash
cd backend
pytest -q
cd ../frontend
npm run build
```

## Demo journey

1. Select `Parth (demo)` and open Practice Lab.
2. Answer the Ohm's Law question incorrectly (e.g., choose "Double") and explain "more resistance pushes more current".
3. Observe misconception label, mastery change and targeted follow-up question.
4. Open concept map and revision page.
5. Open Teacher Insights and inspect class-level gap/misconception aggregation.

## Architecture

```
frontend/  React + Vite + TypeScript + Recharts
backend/   FastAPI + SQLite + deterministic learner engine
docs/      product, brand, developer and safety handoff documentation
```

See `docs/` for the product requirements, design decisions, API contract, AI governance, QA and Antigravity setup. Only demo endpoints are implemented; the full spec describes future production work.

## Security and deployment

Only ship this build in a private/demo environment. Production requires proper authentication/authorization, managed database, migrations, monitoring, model evaluation and privacy/legal review for minors. Use a persistent database volume or PostgreSQL; ephemeral SQLite on serverless hosting will lose state. Keep all provider secrets server-side.
