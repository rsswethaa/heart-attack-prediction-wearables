from src.features import activity_index, recovery_index
from src.risk_model import WearableFeatures, risk_score

sample = WearableFeatures(age=52, resting_hr=82, hrv_ms=32, sleep_hours=5.8, steps_per_day=4200, exercise_minutes=45)
print("Risk:", risk_score(sample))
print("Activity index:", activity_index(sample))
print("Recovery index:", recovery_index(sample))
