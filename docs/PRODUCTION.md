# Production hardening

PulseLens uses managed PostgreSQL through `DATABASE_URL` for platform accounts, audit events, experiments and model/version metadata, with SQLite fallback locally. Production controls include RBAC, API keys, rate limiting, structured logs, metrics, optional Sentry error tracking, admin CSV export, Docker and release automation.

The forecast endpoint projects recent signal direction with transparent linear trends and produces a descriptive readiness-style score. It is deliberately not a medical diagnosis, prognosis or heart-attack prediction. No clinical accuracy claim is made without an appropriate labelled dataset, calibration and medical validation.
