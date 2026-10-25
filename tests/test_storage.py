import sqlite3
import tempfile
import unittest
from pathlib import Path

from src.storage import add_reading, init_db, save_assessment


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / 'wearable.db'
        init_db(self.db, seed=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_store_reading_and_assessment(self):
        reading_id = add_reading(self.db, 'SYNTH-001', 70, 44, 6.5, 7000)
        save_assessment(self.db, reading_id, 35.0, 'MODERATE', 'Synthetic educational assessment')
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM risk_assessments').fetchone()[0], 1)

    def test_unknown_participant_rejected(self):
        with self.assertRaises(ValueError):
            add_reading(self.db, 'MISSING', 70, 40, 7, 5000)


if __name__ == '__main__':
    unittest.main()
