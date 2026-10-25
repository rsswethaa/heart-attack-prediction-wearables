PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS participants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  participant_ref TEXT NOT NULL UNIQUE,
  age INTEGER NOT NULL CHECK(age BETWEEN 18 AND 120),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wearable_readings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  participant_id INTEGER NOT NULL,
  resting_hr REAL NOT NULL CHECK(resting_hr BETWEEN 20 AND 250),
  hrv_ms REAL NOT NULL CHECK(hrv_ms >= 0),
  sleep_hours REAL NOT NULL CHECK(sleep_hours BETWEEN 0 AND 24),
  steps INTEGER NOT NULL CHECK(steps >= 0),
  recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(participant_id) REFERENCES participants(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS model_versions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  version TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS risk_assessments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  reading_id INTEGER NOT NULL,
  model_version_id INTEGER NOT NULL,
  risk_score REAL NOT NULL CHECK(risk_score BETWEEN 0 AND 100),
  risk_band TEXT NOT NULL CHECK(risk_band IN ('LOW','MODERATE','ELEVATED')),
  explanation TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(reading_id) REFERENCES wearable_readings(id) ON DELETE CASCADE,
  FOREIGN KEY(model_version_id) REFERENCES model_versions(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_readings_participant ON wearable_readings(participant_id);
CREATE INDEX IF NOT EXISTS idx_assessments_reading ON risk_assessments(reading_id);
