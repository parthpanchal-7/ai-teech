"""Run a safe, opt-in real provider check: python -m app.ai_check.

Makes one billable Gemini request if the key is set; no student data is sent.
"""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv
from .ai import analyze_with_model
from .content import QUESTION_BY_ID


def main() -> int:
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)
    if not os.getenv("GEMINI_API_KEY", "").strip():
        print("NOT CONFIGURED: Set GEMINI_API_KEY in backend/.env or environment first.")
        return 2
    sample = "At constant voltage, resistance is in the denominator, so current becomes half."
    result = analyze_with_model(QUESTION_BY_ID["q4"], 1, sample)
    if not result or result["analysis_mode"] != "gemini-structured":
        print("FAILED: Gemini did not return valid structured feedback. Check key, model, quota and network.")
        return 1
    print("SUCCESS: Gemini returned structured reasoning feedback. No student data was used.")
    print("Mode:", result["analysis_mode"])
    print("Reasoning quality:", result["reasoning_quality"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
