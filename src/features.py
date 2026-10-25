from .risk_model import WearableFeatures

def activity_index(x: WearableFeatures) -> float:
    step_component = min(x.steps_per_day / 10000, 1.5)
    exercise_component = min(x.exercise_minutes / 150, 1.5)
    return round((step_component + exercise_component) / 2, 3)

def recovery_index(x: WearableFeatures) -> float:
    sleep_component = min(x.sleep_hours / 8, 1.2)
    hrv_component = min(x.hrv_ms / 60, 1.5)
    return round((sleep_component + hrv_component) / 2, 3)
