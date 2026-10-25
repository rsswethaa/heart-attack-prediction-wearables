# Interface Contracts

The project exposes Python interfaces rather than a public medical API.

## Feature/model layer
See `src/features.py` and `src/risk_model.py` for validation, feature preparation and educational risk scoring.

## Persistence layer
- `init_db(path, seed=False)`
- `add_reading(path, participant_ref, resting_hr, hrv_ms, sleep_hours, steps)`
- `save_assessment(path, reading_id, score, band, explanation, model_version)`

A real clinical/research service would place authenticated, consent-aware APIs in front of these operations and enforce provenance, validation and authorisation.
