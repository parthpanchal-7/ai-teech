"""Focused regression checks for the seven-feature MVP backend."""
import importlib
import os

os.environ["DATABASE_PATH"] = "/tmp/ai_teech_test_learning.db"

from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)

def test_syllabus_and_health():
    assert client.get("/health").json()["status"] == "ok"
    concepts = client.get("/api/concepts").json()
    assert len(concepts) == 7
    assert all("prerequisites" in c for c in concepts)

def test_diagnostic_and_mastery_update():
    diagnostic = client.post("/api/diagnostic/start?student_id=demo-parth")
    assert diagnostic.status_code == 200
    assert len(diagnostic.json()["questions"]) == 7
    question = next(q for q in diagnostic.json()["questions"] if q["concept_id"] == "ohms_law")
    assert "answer" not in question
    before = client.get("/api/students/demo-parth/profile").json()
    score = next(m["score"] for m in before["mastery"] if m["concept_id"] == "ohms_law")
    response = client.post("/api/answers", json={
        "student_id":"demo-parth", "question_id":question["id"], "answer":0,
        "reasoning":"More resistance pushes more current through the wire."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["correct"] is False
    assert data["misconception"] is not None
    assert data["mastery_after"] < score
    assert data["next_question"]["concept_id"] == "ohms_law"
    assert client.get("/api/students/demo-parth/revision").json()["items"]

def test_class_analytics_and_validation():
    analytics=client.get("/api/teacher/analytics").json()
    assert analytics["demo_data"] is True
    assert len(analytics["concepts"]) == 7
    assert any(m["label"] for m in analytics["misconceptions"])
    assert client.post("/api/answers",json={"student_id":"demo-parth","question_id":"bad","answer":0,"reasoning":"Some reasoning"}).status_code == 404
    assert client.post("/api/answers",json={"student_id":"demo-parth","question_id":"q1","answer":7,"reasoning":"Some reasoning"}).status_code == 422
