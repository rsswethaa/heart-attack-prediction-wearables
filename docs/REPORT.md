# Technical Project Report — Wearable Cardiovascular Risk Prototype

## Executive summary
This project demonstrates an end-to-end software pipeline for validating wearable-style signals, creating interpretable features, producing an educational cardiovascular-risk score and recording an auditable assessment history.

## 1. Problem
Wearables produce continuous physiological/activity data, but raw measurements need validation, feature engineering and context before analysis.

## 2. Objective
Build a reproducible educational pipeline with transparent scoring, synthetic data, durable storage, model-version tracking and strong clinical-safety boundaries.

## 3. System design
Feature/model code lives under `src/`; SQL assets live under `database/`; synthetic input examples live under `data/`; automated tests validate both computation and persistence.

## 4. Data model
Pseudonymous participants produce wearable readings. Each stored assessment is linked to a specific reading and model version, supporting reproducibility and auditability.

## 5. Method
The reference implementation uses an explainable weighted baseline over age, resting HR, HRV, sleep and activity. The goal is software architecture demonstration—not medical prediction performance.

## 6. Testing
Tests verify input validation, sensible score ordering and complete SQLite persistence. CI compiles and executes the test suite on repository changes.

## 7. Privacy and safety
No real patient data is included. A real deployment would need explicit consent, encryption, access control, retention policies, medical oversight and regulatory assessment.

## 8. Limitations
No diagnostic accuracy, sensitivity, specificity, calibration, prospective validation or clinical utility is claimed. Device error, confounding factors and omitted medical history materially limit interpretation.

## 9. Future work
Longitudinal time-series models, missing-data handling, device adapters, calibration curves, subgroup analysis, clinician-reviewed labels and prospective validation.

## Conclusion
The repository is a complete educational software artifact with model code, data, persistence, database assets, diagrams, tests, CI, deployment/security documentation, a model card and formal report.
