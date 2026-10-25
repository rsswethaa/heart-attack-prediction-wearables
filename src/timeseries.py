from __future__ import annotations

from dataclasses import asdict
from datetime import date
from statistics import mean, median

from .risk_model import WearableFeatures, risk_score

REQUIRED = ("resting_hr", "hrv_ms", "sleep_hours", "steps")


def _number(row, key, default=None):
    value = row.get(key, default)
    if value is None:
        raise ValueError(f"missing {key}")
    return float(value)


def normalise_reading(row: dict) -> dict:
    reading = {
        "date": str(row.get("date") or date.today().isoformat()),
        "resting_hr": _number(row, "resting_hr"),
        "hrv_ms": _number(row, "hrv_ms"),
        "sleep_hours": _number(row, "sleep_hours"),
        "steps": int(_number(row, "steps")),
        "exercise_minutes": int(float(row.get("exercise_minutes", 20))),
        "spo2": float(row.get("spo2", 98.0)),
    }
    if not 70 <= reading["spo2"] <= 100:
        raise ValueError("SpO2 out of supported demo range")
    return reading


def _slope(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    xbar = (len(values) - 1) / 2
    ybar = mean(values)
    denom = sum((i - xbar) ** 2 for i in range(len(values))) or 1.0
    return sum((i - xbar) * (v - ybar) for i, v in enumerate(values)) / denom


def _robust_flags(values: list[float], threshold: float = 3.5) -> list[bool]:
    if len(values) < 4:
        return [False] * len(values)
    centre = median(values)
    deviations = [abs(v - centre) for v in values]
    mad = median(deviations)
    if mad == 0:
        return [False] * len(values)
    return [0.6745 * abs(v - centre) / mad > threshold for v in values]


def feature_contributions(age: int, reading: dict) -> dict:
    x = WearableFeatures(
        age=age,
        resting_hr=reading["resting_hr"],
        hrv_ms=reading["hrv_ms"],
        sleep_hours=reading["sleep_hours"],
        steps_per_day=reading["steps"],
        exercise_minutes=reading["exercise_minutes"],
    )
    raw = {
        "Age": max(0, x.age - 40) * 0.8,
        "Resting HR": max(0, x.resting_hr - 70) * 0.7,
        "HRV": max(0, 50 - x.hrv_ms) * 0.5,
        "Sleep": max(0, 7 - x.sleep_hours) * 4,
        "Steps": max(0, 7000 - x.steps_per_day) / 700,
        "Exercise": max(0, 150 - x.exercise_minutes) / 30,
    }
    total = sum(raw.values()) or 1.0
    return {k: round(v / total * 100, 1) for k, v in raw.items()}


def analyse_history(age: int, rows: list[dict]) -> dict:
    if not 18 <= int(age) <= 100:
        raise ValueError("age out of supported demo range")
    if len(rows) < 3:
        raise ValueError("at least three daily readings are required")

    readings = [normalise_reading(r) for r in rows]
    latest = readings[-1]
    baseline = risk_score(WearableFeatures(
        age=int(age),
        resting_hr=latest["resting_hr"],
        hrv_ms=latest["hrv_ms"],
        sleep_hours=latest["sleep_hours"],
        steps_per_day=latest["steps"],
        exercise_minutes=latest["exercise_minutes"],
    ))

    hr_slope = _slope([r["resting_hr"] for r in readings])
    hrv_slope = _slope([r["hrv_ms"] for r in readings])
    sleep_slope = _slope([r["sleep_hours"] for r in readings])
    trend_adjustment = max(0.0, hr_slope * 1.5) + max(0.0, -hrv_slope * 0.7) + max(0.0, -sleep_slope * 2.0)
    trend_score = min(100.0, round(baseline["score"] + trend_adjustment, 1))
    trend_band = "LOW" if trend_score < 25 else "MODERATE" if trend_score < 50 else "ELEVATED"

    hr_flags = _robust_flags([r["resting_hr"] for r in readings])
    hrv_flags = _robust_flags([r["hrv_ms"] for r in readings])
    spo2_flags = _robust_flags([r["spo2"] for r in readings])
    anomalies = []
    for i, r in enumerate(readings):
        reasons = []
        if hr_flags[i]: reasons.append("resting HR deviation")
        if hrv_flags[i]: reasons.append("HRV deviation")
        if spo2_flags[i] or r["spo2"] < 94: reasons.append("SpO2 deviation")
        if reasons:
            anomalies.append({"date": r["date"], "reasons": reasons})

    return {
        "latest": latest,
        "baseline": baseline,
        "trend_aware": {"score": trend_score, "band": trend_band},
        "model_comparison": [
            {"name": "Point-in-time baseline", "score": baseline["score"], "purpose": "single-day interpretable reference"},
            {"name": "Trend-aware prototype", "score": trend_score, "purpose": "adds recent directional change"},
            {"name": "Conservative view", "score": max(baseline["score"], trend_score), "purpose": "shows the higher prototype signal"},
        ],
        "trends": {
            "resting_hr_per_day": round(hr_slope, 2),
            "hrv_ms_per_day": round(hrv_slope, 2),
            "sleep_hours_per_day": round(sleep_slope, 2),
        },
        "averages": {
            "resting_hr": round(mean(r["resting_hr"] for r in readings), 1),
            "hrv_ms": round(mean(r["hrv_ms"] for r in readings), 1),
            "sleep_hours": round(mean(r["sleep_hours"] for r in readings), 1),
            "steps": round(mean(r["steps"] for r in readings)),
            "spo2": round(mean(r["spo2"] for r in readings), 1),
        },
        "contributions": feature_contributions(int(age), latest),
        "anomalies": anomalies,
        "series": readings,
        "notice": "Educational wellness analytics only. This does not diagnose, predict, or rule out a heart attack or other medical condition.",
    }
