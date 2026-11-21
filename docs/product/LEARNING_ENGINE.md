# Learning Engine and Proof of Learning Loop

## Principle

"Understanding" is not directly observable. Build a transparent estimate from multiple evidence types: correctness, student explanation, near-transfer task and later independent recall. Avoid using self-reported confidence as proof.

## Sequence

`diagnostic -> ask -> explain -> evaluate -> flip scenario -> update -> schedule recall -> teacher signal`

Each concept has stable ID, prerequisites, syllabus reference and teacher-reviewed questions with rubric. Question selection first checks weak prerequisites and concept coverage, then chooses target difficulty. The transfer question changes representation/context and must not reproduce the same answer pattern.

## Scoring version 0 (heuristic to validate)

- Signals in `[0, 1]`: `correctness`, `reasoning_rubric`, `transfer`, `delayed_recall`. Weighted proportions proposed: 0.45/0.25/0.20/0.10.
- Only available signals contribute to normalized evidence score (never treat "not assessed" as failure).
- A deterministic updater moves mastery toward evidence at a capped rate (e.g., <=12 points per event). Track uncertainty and distinct assessment occasions.
- Strong promotion eligibility: at least 3 independent checks on at least 2 occasions, including a transfer check. These numbers are product hypotheses, not scientifically calibrated thresholds.
- Distinguish `unassessed`, `developing`, `provisional`, and `supported mastery` UI states; show evidence and last review date.

## Misconception analysis

Required structured output: `concept_id`, `answer_correct`, `reasoning_quality` (0..1), `misconception_tag|null`, `evidence_span`, `confidence`, `recommended_intervention`, `next_difficulty`. Reject unrecognized concept IDs/tags and malformed JSON. Model classification is a hypothesis; teacher can inspect, relabel or reject it.

Examples: confusion between resistance and current; misinterpreting series vs parallel circuit; adding currents incorrectly in series; conflating electrical power with energy.

If LLM unavailable, grade a validated question bank and run deterministic misconception rules for known examples. Mark complex explanations "unclassified" rather than invent diagnoses.

## Spaced repetition

Start with an explainable heuristic: misconception/incorrect -> next day (or short same-day retry); shaky correct -> 1 day; confident correct -> 3 days; repeated transfer/recall success -> 7+ days. Persist `review_count`, `interval_days`, `due_at`, `last_seen_at`; use a deterministic clock in tests.

## Example end-to-end acceptance

At fixed voltage student says "current rises as resistance rises because more resistance pushes more electricity." The model highlights this exact phrase as evidence, tags resistance-current confusion with qualified confidence, selects a simple contrasting circuit explanation, issues a new transfer scenario, updates mastery, schedules follow-up, and teacher sees the *aggregate* misconception trend.

## Experimental validation

Construct teacher-labeled corpus; compare AI classification against labels; measure delayed recall after 1/7/14 days in small pilot; audit Hindi/English explanation differences. Never treat initial heuristic weights as proven educational measurement.
