# Ai-Teech

> Learn it. Prove it. Own it.

Ai-Teech is an adaptive exam-preparation **demo MVP** for Class 10 Physics (Electricity). It helps learners practice, explain why they chose an answer, track concept mastery and schedule reviews; a teacher analytics screen summarizes class-wide gaps.

![Status](https://img.shields.io/badge/status-demo%20MVP-BD47F2)

## What works

- Seven-node prerequisite concept graph
- Concept-tagged diagnostic question set and practice questions
- Learner mastery updates persisted to SQLite
- Difficulty-aware, weak-concept question selection
- Optional Gemini structured reasoning analysis with an offline heuristic fallback
- Guided seven-question diagnostic flow and scenario-based follow-up
- Spaced-review dates and revision list
- Teacher concept analytics and misconception trends across demo students
- Responsive playful React interface

**Important limits:** Demo identities are selectable from the UI; this app has no production authorization, secure teacher-scoped access, guardian-consent flow or real student accounts. With a configured Gemini key the reasoning evaluator uses a hosted model; otherwise it transparently falls back to an offline rubric. Do **not** deploy it with real student personal data or publicly expose it as a school production service. Independent educational validation remains follow-up work.

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

### Live Gemini setup

1. Open [Google AI Studio](https://aistudio.google.com/apikey), create an API key, and keep it private.
2. Copy `backend/.env.example` to `backend/.env`.
3. Edit **only** the backend `.env` file:

```dotenv
GEMINI_API_KEY=replace_with_your_real_api_key
GEMINI_MODEL=gemini-2.5-flash
```

The backend loads `backend/.env` automatically at startup. Restart Uvicorn after changing the file. If you prefer environment variables instead, for PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_KEY_HERE"
$env:GEMINI_MODEL="gemini-2.5-flash"
```

`uvicorn` then reads the process environment. No key is required for the fallback demo. **Never** add this key to a frontend `VITE_` variable or commit `.env`. See Google's [structured output documentation](https://ai.google.dev/gemini-api/docs/structured-output).

4. In the activated backend virtual environment, verify the **real provider** with one synthetic test request:

```bash
cd backend
python -m app.ai_check
```

Expected success: `SUCCESS: Gemini returned structured reasoning feedback.` This checks network, authentication and schema using a sample Physics question without sending real student data. It consumes one model request. `GET /api/ai/status` reports whether the key is configured (it is not a live health check). The UI shows **Gemini configured** once the server sees a key; after you submit an answer, feedback labels the actual analysis mode as `gemini-structured` or `offline-rubric`. On invalid key, quota issue or timeout, offline fallback keeps the app usable.

### One-command Docker demo

```bash
docker compose up --build -d
```

Open http://localhost:8080. The frontend proxies API calls internally, and the SQLite database is mounted on a persistent Docker named volume. Set `GEMINI_API_KEY` in the shell or a private root `.env` before starting if you want model feedback. This command has not been verified on a Docker host in this session.

## Test

```bash
cd backend
pytest -q
cd ../frontend
npm run build
```

## Demo journey

1. Select `Parth (demo)` and open Practice Lab.
2. Use Diagnostic Test for all 7 concept checks, then select Ohm's Law in Concept Map.
3. Answer the Ohm's Law question incorrectly (e.g., choose "Double") and explain "more resistance pushes more current".
4. Observe misconception label, mastery change and targeted follow-up question.
5. Open the revision page.
6. Open Teacher Insights and click **Load sample class data** to inspect synthetic class-level gap/misconception aggregation.

## Architecture

```
frontend/  React + Vite + TypeScript + Recharts
backend/   FastAPI + SQLite + deterministic learner engine
docs/      product, brand, developer and safety handoff documentation
```

See `docs/` for the product requirements, design decisions, API contract, AI governance, QA, [hackathon demo script](docs/HACKATHON_DEMO.md), and Antigravity setup. Only demo endpoints are implemented; the full spec describes future production work.

## Security and deployment

Only ship this build in a private/demo environment. Production requires proper authentication/authorization, managed database, migrations, monitoring, model evaluation and privacy/legal review for minors. Use a persistent database volume or PostgreSQL; ephemeral SQLite on serverless hosting will lose state. Keep all provider secrets server-side.
