# Testing Strategy

Automated tests cover model ordering/validation plus database initialisation, reading persistence, assessment persistence and rejection of unknown participants.

Run:
```bash
python -m unittest discover -s tests -v
```

## Validation still required for real research
Representative datasets, missingness analysis, calibration, confidence intervals, subgroup analysis, temporal validation, device-specific bias checks and clinician-reviewed outcome definitions.
