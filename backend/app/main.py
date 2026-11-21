"""Ai-Teech demo API: deterministic learning state + optional structured AI analysis."""
from __future__ import annotations

import json
import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .content import CONCEPTS, CONCEPT_BY_ID, QUESTIONS, QUESTION_BY_ID, public_question
from .ai import analyze_with_model

# Load backend/.env on developer machines while keeping host-provided values authoritative.
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)
DB_PATH = os.getenv("DATABASE_PATH", str(Path(__file__).resolve().parent.parent / "ai_teech.db"))
app = FastAPI(title="Ai-Teech Learning API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if x.strip()],
    allow_methods=["GET", "POST"], allow_headers=["Content-Type"],
)

@contextmanager
def database():
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with database() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS mastery (
            student_id TEXT NOT NULL, concept_id TEXT NOT NULL, score INTEGER NOT NULL DEFAULT 35,
            attempts INTEGER NOT NULL DEFAULT 0, correct_count INTEGER NOT NULL DEFAULT 0,
            next_review_at TEXT, updated_at TEXT,
            PRIMARY KEY (student_id, concept_id), FOREIGN KEY(student_id) REFERENCES students(id));
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL, concept_id TEXT NOT NULL,
            question_id TEXT NOT NULL, answer INTEGER NOT NULL, correct INTEGER NOT NULL,
            reasoning TEXT NOT NULL, misconception TEXT, difficulty TEXT NOT NULL,
            created_at TEXT NOT NULL, request_key TEXT UNIQUE,
            FOREIGN KEY(student_id) REFERENCES students(id));
        """)
        # In-place, idempotent migration for the first demo database version.
        cols = {row[1] for row in db.execute("PRAGMA table_info(attempts)")}
        if "request_key" not in cols:
            db.execute("ALTER TABLE attempts ADD COLUMN request_key TEXT")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_attempt_request_key ON attempts(request_key)")
        db.executemany("INSERT OR IGNORE INTO students(id,name) VALUES (?,?)", [
            ("demo-parth", "Parth (demo)"), ("demo-ananya", "Ananya (demo)"), ("demo-rahul", "Rahul (demo)"),
        ])

init_db()

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def ensure_student(db, student_id: str):
    student = db.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    if not student:
        raise HTTPException(404, "Unknown demo student")
    return student

def get_mastery(db, student_id: str):
    rows = {r["concept_id"]: dict(r) for r in db.execute("SELECT * FROM mastery WHERE student_id=?", (student_id,))}
    return [{"concept_id": c["id"], "score": rows.get(c["id"],{}).get("score",35),
             "attempts": rows.get(c["id"],{}).get("attempts",0),
             "correct_count": rows.get(c["id"],{}).get("correct_count",0),
             "next_review_at": rows.get(c["id"],{}).get("next_review_at"),
             "status": "unassessed" if rows.get(c["id"],{}).get("attempts",0)==0 else "assessed"}
            for c in CONCEPTS]

def choose_question(db, student_id: str, requested_concept: str | None = None):
    profile = get_mastery(db, student_id)
    by_id = {m["concept_id"]:m for m in profile}
    target = requested_concept
    if target and target not in CONCEPT_BY_ID:
        raise HTTPException(400, "Unknown concept")
    if not target:
        # Prefer least mastered/prerequisite-ready concepts; unassessed concepts get priority.
        target = min(profile, key=lambda m:(m["attempts"]>0, m["score"], m["attempts"]))["concept_id"]
    candidate_concepts = [target]
    candidate_concepts += [p for p in CONCEPT_BY_ID[target]["prerequisites"] if by_id[p]["score"] < 45 and by_id[p]["attempts"] > 0]
    target = candidate_concepts[-1]
    target_score = by_id[target]["score"]
    difficulty = "easy" if target_score < 50 else "medium" if target_score < 75 else "hard"
    candidates = [q for q in QUESTIONS if q["concept_id"] == target]
    history = {r["question_id"] for r in db.execute("SELECT question_id FROM attempts WHERE student_id=? ORDER BY id DESC LIMIT 8", (student_id,))}
    ranked = sorted(candidates, key=lambda q:(q["id"] in history, abs(["easy","medium","hard"].index(q["difficulty"])-["easy","medium","hard"].index(difficulty))))
    return public_question(ranked[0])

def evaluate_reasoning(question, selected_answer, reasoning):
    """Offline misconception detection reads explanatory text, not only option index."""
    raw = reasoning.lower().strip()
    correct = selected_answer == question["answer"]
    misleading_patterns = [
        (r"resistan\w*.*(push|increase|more current)|more resistan\w*.*more current", "Resistance-current confusion"),
        (r"series.*(same voltage|voltage same)|parallel.*(same current|current same)", "Series-parallel confusion"),
        (r"power.*(charge per|current per)|power is.*(resistance)", "Power-energy confusion"),
    ]
    tag = next((label for pattern,label in misleading_patterns if re.search(pattern,raw)),None)
    evidence = any(word in raw for word in question["keywords"])
    if not tag and not correct:
        tag = "Needs concept review" if evidence else "Unclear reasoning"
    if not tag and correct and not evidence:
        tag = "Reasoning needs evidence"
    quality = "strong" if correct and evidence and not tag else "partial" if correct else "needs_support"
    return {"misconception":tag,"reasoning_quality":quality,"analysis_mode":"offline-rubric","confidence":"heuristic","coach_tip":question["explanation"]}

class AnswerRequest(BaseModel):
    student_id: str
    question_id: str
    answer: int = Field(ge=0, le=3)
    reasoning: str = Field(min_length=8, max_length=1000)
    request_key: str | None = Field(default=None, min_length=8, max_length=100)

@app.get("/health")
def health():
    return {"status":"ok","mode":"demo"}

@app.get("/api/ai/status")
def ai_status():
    """Safe capability status; never returns an API key or private provider errors."""
    configured = bool(os.getenv("GEMINI_API_KEY", "").strip())
    return {"provider":"gemini", "configured":configured,
            "evaluation_mode":"gemini-with-fallback" if configured else "offline-rubric",
            "model":os.getenv("GEMINI_MODEL","gemini-2.5-flash") if configured else None}

@app.get("/api/concepts")
def concepts():
    return CONCEPTS

@app.get("/api/students")
def students():
    with database() as db:
        return [dict(r) for r in db.execute("SELECT * FROM students ORDER BY id")]

@app.get("/api/students/{student_id}/profile")
def profile(student_id: str):
    with database() as db:
        student = ensure_student(db,student_id)
        return {"student":dict(student),"mastery":get_mastery(db,student_id)}

@app.post("/api/diagnostic/start")
def diagnostic(student_id: str = "demo-parth"):
    with database() as db:
        ensure_student(db, student_id)
        # Fixed 7-concept diagnostic; each submitted answer still updates mastery.
        return {"questions":[public_question(next(q for q in QUESTIONS if q["concept_id"]==c["id"])) for c in CONCEPTS]}

@app.get("/api/questions/next")
def next_question(student_id: str = "demo-parth", concept_id: str | None = None):
    with database() as db:
        ensure_student(db,student_id)
        return choose_question(db,student_id,concept_id)

@app.post("/api/answers")
def answer(body: AnswerRequest):
    question = QUESTION_BY_ID.get(body.question_id)
    if not question: raise HTTPException(404,"Unknown question")
    with database() as db:
        ensure_student(db,body.student_id)
        if body.request_key and db.execute("SELECT 1 FROM attempts WHERE request_key=?",(body.request_key,)).fetchone():
            raise HTTPException(409,"Answer already submitted. Refresh the profile before continuing.")
        prior = next((m for m in get_mastery(db,body.student_id) if m["concept_id"]==question["concept_id"]),None)
        correct = body.answer==question["answer"]
        # Synthetic fixtures stay offline, instant and free even when a Gemini key exists.
        synthetic = bool(body.request_key and body.request_key.startswith("demo-seed-"))
        analysis = (None if synthetic else analyze_with_model(question,body.answer,body.reasoning)) or evaluate_reasoning(question,body.answer,body.reasoning)
        delta = 12 if correct and analysis["reasoning_quality"]=="strong" else 5 if correct else -10 if analysis["misconception"] else -6
        updated = max(0,min(100,prior["score"]+delta))
        attempts = prior["attempts"]+1
        consecutive_positive = correct and analysis["reasoning_quality"]=="strong"
        days = 7 if consecutive_positive and attempts>=3 else 3 if consecutive_positive and attempts>=2 else 1
        when = (datetime.now(timezone.utc)+timedelta(days=days)).isoformat()
        db.execute("""INSERT INTO mastery(student_id,concept_id,score,attempts,correct_count,next_review_at,updated_at)
            VALUES (?,?,?,?,?,?,?) ON CONFLICT(student_id,concept_id) DO UPDATE SET
            score=excluded.score,attempts=excluded.attempts,correct_count=excluded.correct_count,
            next_review_at=excluded.next_review_at,updated_at=excluded.updated_at""",
            (body.student_id,question["concept_id"],updated,attempts,prior["correct_count"]+int(correct),when,utc_now()))
        db.execute("""INSERT INTO attempts(student_id,concept_id,question_id,answer,correct,reasoning,misconception,difficulty,created_at,request_key)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",(body.student_id,question["concept_id"],body.question_id,body.answer,int(correct),body.reasoning,analysis["misconception"],question["difficulty"],utc_now(),body.request_key))
        # Deterministic next-step selection sees the new mastery within this transaction.
        followup=choose_question(db,body.student_id,question["concept_id"])
        return {"correct":correct,"correct_option":question["answer"],"explanation":question["explanation"],
            "mastery_before":prior["score"],"mastery_after":updated,"next_review_at":when,
            "next_question":followup,**analysis}

@app.get("/api/students/{student_id}/revision")
def revision(student_id: str):
    with database() as db:
        ensure_student(db,student_id)
        now=utc_now()
        items=[{**dict(r),"concept_title":CONCEPT_BY_ID[r["concept_id"]]["title"],"due":r["next_review_at"]<=now}
            for r in db.execute("SELECT concept_id,score,next_review_at FROM mastery WHERE student_id=? AND next_review_at IS NOT NULL ORDER BY next_review_at",(student_id,))]
        return {"items":items}

@app.get("/api/teacher/analytics")
def teacher_analytics():
    """Demo aggregate only; NO production authentication/teacher scopes implemented."""
    with database() as db:
        total=db.execute("SELECT COUNT(*) AS n FROM students").fetchone()["n"]
        scored={r["concept_id"]:dict(r) for r in db.execute("SELECT concept_id,ROUND(AVG(score),1) as avg_score, COUNT(*) as learners FROM mastery GROUP BY concept_id")}
        gaps=[{"concept_id":c["id"],"title":c["title"],"avg_mastery":scored.get(c["id"],{}).get("avg_score"),"assessed":scored.get(c["id"],{}).get("learners",0)} for c in CONCEPTS]
        misconceptions=[dict(r) for r in db.execute("SELECT misconception AS label,COUNT(*) AS count FROM attempts WHERE misconception IS NOT NULL GROUP BY misconception ORDER BY count DESC LIMIT 6")]
        learners=[dict(r) for r in db.execute("SELECT s.name,COUNT(m.concept_id) AS assessed,ROUND(AVG(m.score),1) AS avg_mastery FROM students s LEFT JOIN mastery m ON s.id=m.student_id GROUP BY s.id ORDER BY avg_mastery ASC")]
        return {"demo_data":True,"total_learners":total,"concepts":gaps,"misconceptions":misconceptions,"learners":learners}


@app.post("/api/demo/seed")
def seed_demo_classroom():
    """Idempotently populate synthetic learner attempts for the hackathon demo."""
    if os.getenv("DEMO_MODE", "true").lower() != "true":
        raise HTTPException(403, "Demo seeding disabled")
    examples = [
        ("demo-ananya", "q1", 0, "Current equals charge divided by time."),
        ("demo-ananya", "q4", 1, "With constant voltage, current halves when resistance doubles."),
        ("demo-ananya", "q7", 1, "Series elements share the same current along one path."),
        ("demo-ananya", "q9", 1, "Parallel branches have the same voltage."),
        ("demo-rahul", "q3", 0, "More resistance pushes more current through the wire."),
        ("demo-rahul", "q4", 0, "More resistance pushes more current, so it doubles."),
        ("demo-rahul", "q7", 0, "Series means same voltage across each resistor."),
        ("demo-rahul", "q11", 1, "Power is voltage multiplied by current."),
    ]
    inserted = 0
    for i, (student, qid, choice, reasoning) in enumerate(examples):
        request_key = f"demo-seed-{i:02d}"
        with database() as db:
            exists = db.execute("SELECT 1 FROM attempts WHERE request_key=?", (request_key,)).fetchone()
        if exists:
            continue
        answer(AnswerRequest(student_id=student,question_id=qid,answer=choice,reasoning=reasoning,request_key=request_key))
        inserted += 1
    return {"demo_data":True,"inserted":inserted,"message":"Synthetic demo class is ready"}
