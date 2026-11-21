"""Focused regression checks for the seven-feature MVP backend."""
import importlib
import os
import uuid
import json
import pytest

os.environ["DATABASE_PATH"] = "/tmp/ai_teech_test_learning.db"

from fastapi.testclient import TestClient
from app import main
from app.ai import analyze_with_model
from app.content import QUESTION_BY_ID

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def isolated_test_db(tmp_path, monkeypatch):
    """Tests must not depend on prior runs or mutate a shared demo DB."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(main, "DB_PATH", str(tmp_path / "learning_test.db"))
    main.init_db()

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
    client.post("/api/demo/seed")
    analytics=client.get("/api/teacher/analytics").json()
    assert analytics["demo_data"] is True
    assert len(analytics["concepts"]) == 7
    assert any(m["label"] for m in analytics["misconceptions"])
    assert client.post("/api/answers",json={"student_id":"demo-parth","question_id":"bad","answer":0,"reasoning":"Some reasoning"}).status_code == 404
    assert client.post("/api/answers",json={"student_id":"demo-parth","question_id":"q1","answer":7,"reasoning":"Some reasoning"}).status_code == 422

def test_demo_seed_is_repeat_safe():
    first = client.post("/api/demo/seed")
    assert first.status_code == 200
    assert first.json()["inserted"] >= 0
    again = client.post("/api/demo/seed")
    assert again.status_code == 200
    assert again.json()["inserted"] == 0
    analytics = client.get("/api/teacher/analytics").json()
    assert any(c["assessed"] > 0 for c in analytics["concepts"])
    assert analytics["misconceptions"]

def test_idempotency_and_live_ai_fallback(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    key = f"test-answer-{uuid.uuid4()}"
    payload={"student_id":"demo-ananya","question_id":"q5","answer":1,
             "reasoning":"Current is voltage divided by resistance.","request_key":key}
    response=client.post("/api/answers",json=payload)
    assert response.status_code==200
    assert response.json()["analysis_mode"] == "offline-rubric"
    again=client.post("/api/answers",json=payload)
    assert again.status_code==409

def test_mocked_gemini_structured_response(monkeypatch):
    """Exercise the SDK integration path without a real API key/network call."""
    from google import genai

    class Response:
        text = json.dumps({"reasoning_quality":"strong","misconception":None,
                           "evidence":"resistance is in the denominator",
                           "coach_tip":"At constant voltage, doubling resistance halves current."})

    class Client:
        def __init__(self, **kwargs):
            assert kwargs["api_key"] == "test-only-key"
            self.models = self
        def generate_content(self, **kwargs):
            assert kwargs["contents"]
            assert kwargs["config"].response_mime_type == "application/json"
            return Response()

    monkeypatch.setenv("GEMINI_API_KEY", "test-only-key")
    monkeypatch.setattr(genai, "Client", Client)
    result = analyze_with_model(QUESTION_BY_ID["q4"], 1, "Resistance is in the denominator so current halves.")
    assert result is not None
    assert result["analysis_mode"] == "gemini-structured"
    assert "halves" in result["coach_tip"]

def test_ai_status_never_reveals_secret(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "private-test-secret")
    response = client.get("/api/ai/status")
    assert response.status_code == 200
    assert response.json()["configured"] is True
    assert "private-test-secret" not in response.text
