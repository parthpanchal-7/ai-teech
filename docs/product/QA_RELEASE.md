# Quality Assurance and Release Plan

## Automated tests

- Unit: bounded mastery update, missing-signal normalization, concept graph cycles, review scheduler date arithmetic.
- API: diagnostic initialization, answer idempotency, transaction rollback, question ownership, schema validation.
- Security: forbidden teacher-to-other-class access, student-to-other-student access, injection strings, accidental secret logging.
- AI: golden reasoning examples, valid JSON, low confidence handling, timeouts, malformed output, fallback correctness.
- Frontend: diagnostic -> practice -> explanation -> transfer -> review, accessibility keyboard and mobile viewport.
- Analytics: sample size, missing records, stale data, demo flag, deduped misconceptions, teacher correction audit.

## End-to-end demo gate

Create 2 student profiles with different evidence. Run a misconception example; verify stored attempt, mastery evolution, next difficulty, next review; open teacher dashboard and confirm aggregate changes. Restart API to verify persistence. Disable AI key and repeat a fallback example.

## Performance test commands (suggested)

Use browser Lighthouse on representative hardware and network; run a 50-concurrent-user API load scenario with k6 or Locust after defining seed data and the endpoints. Observe p50/p95, request failures, DB query count, provider timeouts and cost per answer. Do not claim the speed targets were achieved before instrumented evidence.

## Release checklist

- [ ] Reviewed OpenAPI, environment example and migrations
- [ ] Test database separated from real student data
- [ ] Authentication and authorization tests pass
- [ ] No `.env` secrets in repository or frontend build
- [ ] CORS origins restricted to real frontend domains
- [ ] AI and network failures do not lose answers
- [ ] Syllabus content and generated questions validated
- [ ] Health, logs, error IDs and provider cost monitoring live
- [ ] Persistent database backups and restore check completed
- [ ] Domain, TLS, production URLs and rollback documented
- [ ] Pilot consent/privacy approval completed before minors onboard
