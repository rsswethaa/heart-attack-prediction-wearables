# Research Evaluation Path

The interactive PulseLens dashboard is deliberately a **wellness-analytics prototype**, not a clinically validated predictor. The repository therefore separates product demonstration from research benchmarking.

## Optional model benchmark
`experiments/model_comparison.py` compares:

- Logistic Regression
- Random Forest
- XGBoost (when installed)

For each model it reports ROC AUC, Brier score, a confusion matrix, and calibration-bin data. This makes calibration visible instead of reporting accuracy alone.

## Required dataset contract
The benchmark expects a legally obtained labelled CSV containing the following features (or a documented transformation into them):

`resting_hr, hrv_ms, sleep_hours, steps, spo2, skin_temperature_c, target`

The target must be binary and must correspond to a clearly defined research outcome. Do not relabel an unrelated wellness dataset as “heart attack” data.

## Public-data guidance
Potential public research sources should be selected based on whether their sensing modality and outcome genuinely match the question. Many public cardiovascular datasets contain clinical measurements but **not smartwatch time-series data**, while many wearable datasets contain physiological signals but **not adjudicated cardiovascular-event labels**. That mismatch must be documented rather than hidden.

A defensible evaluation therefore requires:

1. dataset provenance and licence recorded;
2. exact target definition documented;
3. participant-level train/test separation where repeated observations exist;
4. missing-data handling recorded;
5. calibration and confusion matrices reported;
6. subgroup performance assessed where permitted and ethically appropriate;
7. no clinical-validity claim without appropriate medical validation.

## Run
```bash
pip install -r requirements-research.txt
python experiments/model_comparison.py path/to/labelled_dataset.csv
```

The repository intentionally does **not** include fabricated benchmark metrics.
