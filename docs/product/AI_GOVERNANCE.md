# AI Model Card, Privacy and Safety

## Intended use

Provide syllabus-bounded explanations, classify observed reasoning patterns, propose practice difficulty and assist with question drafting. The system augments teachers; it does not diagnose learner ability, disability or psychological condition.

## Model strategy

Start with hosted model via server adapter and fixed prompt templates. Require JSON schema with allowed misconception taxonomy, evidence span, reasoning quality, AI confidence and intervention. Reject unsupported concept IDs, low-confidence unfounded claims, toxic output and fabricated citations. Graceful fallback to vetted question bank and rule-based tags.

## Prompt versioning

Record `provider`, `model`, `prompt_version`, `rubric_version`, `question_version`, latency, token estimate and user-safe trace ID. Never log secrets. Raw student rationale retention must be separately justified and limited.

## Evaluation plan

Teacher-review a balanced 100-example seed set spanning correct reasoning, lucky guesses, misconceptions and multilingual explanations. Avoid label leakage between prompt tuning and held-out test. Proposed *gates*: >=95% factual correctness on teacher-approved sample, >=85% misconception precision, >=80% recall, >=99% schema validity, <1% severe unsafe/hallucinated advice; these are launch hypotheses and may require adjustment after test design. Conduct teacher adjudication on ambiguous cases and compare baseline rules vs LLM.

## Risk register

| Risk | Mitigation |
|---|---|
| Confidently wrong explanation | Rubric/checker, bounded chapter, human review, fallback |
| Misreads English ability as physics gap | Language-aware rubrics, audit by language, teacher correction |
| Student uses prompt injection | Student text treated only as data; no tool invocation from it |
| Sensitive student data leakage | RBAC, least privilege, redaction, retention, access logs |
| Undue dependence | Ask first, prompt for reasoning and transfer rather than provide full solution immediately |
| Bias in adaptive difficulty | Calibrate on observed performance, allow student/teacher override |

## Data governance

Publish privacy notice, retention schedule, deletion request flow, incident ownership and model vendor data-processing terms before processing real student accounts. For minors, conduct jurisdiction-specific legal review and consent workflow; no blanket compliance claims in this blueprint.

## Fine-tuning decision

Do not fine-tune in the MVP. Trigger evaluation only after sufficient licensed, consented, anonymized and teacher-labeled examples exist. Then: freeze evaluation set -> establish prompting baseline -> verify license + data use -> build clean train/validation/test splits by learner -> choose permitted checkpoint -> run small parameter-efficient fine-tuning -> compare pedagogy, safety, latency and cost -> version and rollback. Never train on identifiable student records by default.
