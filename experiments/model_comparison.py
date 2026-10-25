"""Research-only model benchmark for an externally supplied labelled dataset.

Expected CSV columns by default:
resting_hr, hrv_ms, sleep_hours, steps, spo2, skin_temperature_c, target

This script intentionally does not ship or download a clinical dataset and does not
claim medical validity. Use only a legally obtained, appropriately labelled research
dataset whose target actually matches the research question.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score, brier_score_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

FEATURES = ['resting_hr','hrv_ms','sleep_hours','steps','spo2','skin_temperature_c']


def models():
    result = {
        'logistic_regression': Pipeline([
            ('impute', SimpleImputer(strategy='median')),
            ('scale', StandardScaler()),
            ('model', LogisticRegression(max_iter=1000, class_weight='balanced')),
        ]),
        'random_forest': Pipeline([
            ('impute', SimpleImputer(strategy='median')),
            ('model', RandomForestClassifier(n_estimators=250, random_state=42, class_weight='balanced')),
        ]),
    }
    try:
        from xgboost import XGBClassifier
        result['xgboost'] = Pipeline([
            ('impute', SimpleImputer(strategy='median')),
            ('model', XGBClassifier(n_estimators=250, max_depth=4, learning_rate=.05, subsample=.9, colsample_bytree=.9, random_state=42, eval_metric='logloss')),
        ])
    except ImportError:
        pass
    return result


def evaluate_csv(path: str, target='target'):
    frame = pd.read_csv(path)
    missing = [c for c in FEATURES + [target] if c not in frame.columns]
    if missing:
        raise ValueError(f'missing columns: {missing}')
    X = frame[FEATURES]
    y = frame[target].astype(int)
    if y.nunique() != 2:
        raise ValueError('target must contain exactly two classes for this benchmark')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, stratify=y, random_state=42)
    output = {}
    for name, model in models().items():
        model.fit(X_train, y_train)
        probabilities = model.predict_proba(X_test)[:,1]
        predictions = (probabilities >= .5).astype(int)
        prob_true, prob_pred = calibration_curve(y_test, probabilities, n_bins=min(8, max(2, len(y_test)//10)), strategy='quantile')
        output[name] = {
            'roc_auc': round(float(roc_auc_score(y_test, probabilities)), 4),
            'brier_score': round(float(brier_score_loss(y_test, probabilities)), 4),
            'confusion_matrix': confusion_matrix(y_test, predictions).tolist(),
            'calibration': {'mean_predicted_probability': prob_pred.round(4).tolist(), 'observed_fraction_positive': prob_true.round(4).tolist()},
            'n_train': int(len(y_train)),
            'n_test': int(len(y_test)),
        }
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv')
    parser.add_argument('--target', default='target')
    args = parser.parse_args()
    import json
    print(json.dumps(evaluate_csv(args.csv, args.target), indent=2))


if __name__ == '__main__':
    main()
