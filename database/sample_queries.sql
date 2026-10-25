-- Latest wearable readings
SELECT p.participant_ref, p.age, w.resting_hr, w.hrv_ms, w.sleep_hours, w.steps, w.recorded_at
FROM wearable_readings w JOIN participants p ON p.id=w.participant_id
ORDER BY w.recorded_at DESC;

-- Assessment audit trail
SELECT p.participant_ref, w.recorded_at, a.risk_score, a.risk_band, m.version
FROM risk_assessments a
JOIN wearable_readings w ON w.id=a.reading_id
JOIN participants p ON p.id=w.participant_id
JOIN model_versions m ON m.id=a.model_version_id
ORDER BY a.id DESC;

-- Count by educational risk band
SELECT risk_band, COUNT(*) AS assessments FROM risk_assessments GROUP BY risk_band;
