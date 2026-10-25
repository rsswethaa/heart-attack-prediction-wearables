from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'database' / 'schema.sql'
SEED = ROOT / 'database' / 'seed.sql'


def connect(db_path):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def init_db(db_path, seed=False):
    with connect(db_path) as db:
        db.executescript(SCHEMA.read_text(encoding='utf-8'))
        if seed:
            db.executescript(SEED.read_text(encoding='utf-8'))
    return Path(db_path)


def add_reading(db_path, participant_ref, resting_hr, hrv_ms, sleep_hours, steps):
    with connect(db_path) as db:
        participant = db.execute('SELECT id FROM participants WHERE participant_ref=?', (participant_ref,)).fetchone()
        if not participant:
            raise ValueError('participant does not exist')
        cur = db.execute('''INSERT INTO wearable_readings(participant_id,resting_hr,hrv_ms,sleep_hours,steps)
                            VALUES (?,?,?,?,?)''',
                         (participant['id'], float(resting_hr), float(hrv_ms), float(sleep_hours), int(steps)))
        return cur.lastrowid


def save_assessment(db_path, reading_id, score, band, explanation='', model_version='baseline-v1'):
    with connect(db_path) as db:
        model = db.execute('SELECT id FROM model_versions WHERE version=?', (model_version,)).fetchone()
        if not model:
            raise ValueError('model version does not exist')
        db.execute('''INSERT INTO risk_assessments(reading_id,model_version_id,risk_score,risk_band,explanation)
                      VALUES (?,?,?,?,?)''', (reading_id, model['id'], float(score), band, explanation))
