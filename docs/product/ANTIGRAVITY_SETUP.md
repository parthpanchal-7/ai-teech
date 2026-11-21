# Antigravity Implementation and Deployment Handoff

Antigravity is the intended command-runner/developer environment. The hosting provider, domains, credentials and MCP server choices are *not decided* in this documentation. Do not assert automatic deployment success. Ask for provider/authorization before issuing external mutations.

## Step 1 - Repository

```bash
mkdir ai-teech && cd ai-teech
mkdir backend frontend content docs
git init
```

Copy the documentation pack's `docs/` and `brand/` into the repository. Keep `README.md` as top-level project index.

## Step 2 - FastAPI local setup (Python 3.11+)

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install fastapi 'uvicorn[standard]' sqlalchemy alembic pydantic-settings httpx pytest
mkdir app
```

Create `app/__init__.py` and `app/main.py` with the starter below. Freeze dependencies to `requirements.txt` after smoke test.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ai-Teech API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "Idempotency-Key"],
)

@app.get("/health")
def health():
    return {"status": "ok"}
```

```bash
uvicorn app.main:app --reload --port 8000
```

## Step 3 - React frontend

```bash
# Open another terminal at repo root
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install react-router-dom recharts lucide-react
npm run dev
```

## Step 4 - Environment examples

Backend `.env` (private, never commit):

```dotenv
APP_ENV=development
DATABASE_URL=sqlite:///./ai_teech.db
GEMINI_API_KEY=your_server_only_key
AI_MODEL_NAME=choose_an_available_model
CORS_ALLOWED_ORIGINS=http://localhost:5173
JWT_SECRET=generate_a_long_random_secret
```

Frontend `.env` (all `VITE_` values become public):

```dotenv
VITE_API_BASE_URL=http://localhost:8000
```

Add `.env`, `.venv`, `node_modules`, `.pytest_cache`, `.db` and build outputs to `.gitignore`; commit `.env.example` without credentials. Backend config must actually load and validate env values before provider integration; example keys alone do not configure application logic.

## Step 5 - AI integration

Create `backend/app/services/ai_adapter.py`; define `analyze(reasoning, question, rubric) -> validated schema`. Use official provider SDK appropriate to the model that is truly available, retry with bounded timeout and fallback on failure. Never import SDK secrets into frontend. Do not fine-tune for first MVP.

## Step 6 - MCP instructions to Antigravity

1. Inspect existing MCP configuration and list only the servers currently installed.
2. Confirm necessary capabilities: repository/filesystem, Git provider (if authorized), chosen deployment provider, managed database, and optionally browser QA.
3. Ask for any missing service selection, auth or secret; never write credentials into tracked config.
4. Configure each server with provider-approved commands and environment variables; test tool discovery and least privilege.
5. Require explicit confirmation before a production deployment or database migration affecting real user data.

## Step 7 - Deploy safely

Deploy backend and database to a provider supporting persistent storage and environment secrets. Run migrations, verify `/health`, then deploy static frontend with the real HTTPS API URL. Set production CORS to exact frontend origin. Smoke-test a fresh diagnostic, record a practice answer, open teacher analytics, restart backend and confirm data persists. Prepare rollback plan.

## Suggested prompt to Antigravity

> Implement Ai-Teech from the attached docs. Start with the 7 MVP requirements and Class 10 Electricity. Read `BRAND_GUIDELINES.md`, `PRD.md`, `LEARNING_ENGINE.md`, `ARCHITECTURE.md` and `API_SPEC.md` before coding. Set up React/Vite TypeScript and FastAPI. Use deterministic learner model and approved question fallback, strict structured AI evaluation, role-based access, schema migrations and tests. Respect performance/quality release gates. Show commands, files and test results. Do not deploy or configure unapproved MCP credentials without asking me first.
