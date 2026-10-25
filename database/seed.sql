INSERT OR IGNORE INTO participants(participant_ref, age) VALUES
('SYNTH-001', 32), ('SYNTH-002', 67);

INSERT OR IGNORE INTO model_versions(version, description) VALUES
('baseline-v1','Transparent educational weighted baseline; not clinically validated.');

INSERT INTO wearable_readings(participant_id, resting_hr, hrv_ms, sleep_hours, steps)
SELECT id, 62, 58, 7.4, 9200 FROM participants WHERE participant_ref='SYNTH-001'
AND NOT EXISTS (SELECT 1 FROM wearable_readings wr JOIN participants p ON p.id=wr.participant_id WHERE p.participant_ref='SYNTH-001');

INSERT INTO wearable_readings(participant_id, resting_hr, hrv_ms, sleep_hours, steps)
SELECT id, 92, 18, 4.8, 2200 FROM participants WHERE participant_ref='SYNTH-002'
AND NOT EXISTS (SELECT 1 FROM wearable_readings wr JOIN participants p ON p.id=wr.participant_id WHERE p.participant_ref='SYNTH-002');
