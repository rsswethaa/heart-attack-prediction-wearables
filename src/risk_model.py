from dataclasses import dataclass

@dataclass
class WearableFeatures:
    age: int
    resting_hr: float
    hrv_ms: float
    sleep_hours: float
    steps_per_day: int
    exercise_minutes: int


def validate_features(x: WearableFeatures) -> None:
    if not 18 <= x.age <= 100:
        raise ValueError("age out of supported demo range")
    if not 30 <= x.resting_hr <= 180:
        raise ValueError("resting heart rate out of range")
    if not 1 <= x.hrv_ms <= 250:
        raise ValueError("HRV out of range")
    if not 0 <= x.sleep_hours <= 16:
        raise ValueError("sleep hours out of range")
    if x.steps_per_day < 0 or x.exercise_minutes < 0:
        raise ValueError("activity values cannot be negative")


def risk_score(x: WearableFeatures) -> dict:
    validate_features(x)
    score = 0.0
    score += max(0, x.age - 40) * 0.8
    score += max(0, x.resting_hr - 70) * 0.7
    score += max(0, 50 - x.hrv_ms) * 0.5
    score += max(0, 7 - x.sleep_hours) * 4
    score += max(0, 7000 - x.steps_per_day) / 700
    score += max(0, 150 - x.exercise_minutes) / 30
    score = min(100.0, round(score, 1))
    band = "LOW" if score < 25 else "MODERATE" if score < 50 else "ELEVATED"
    return {"score": score, "band": band}
